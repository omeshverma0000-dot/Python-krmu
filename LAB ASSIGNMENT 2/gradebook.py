
"""GradeBook Analyzer
Author: OMESH VERMA
Enrollment Number: 251730331
Date: 2025-11-24
Course: Programming for Problem Solving using Python

Features:
- Manual input or CSV import of student marks
- Statistical analysis: mean, median, min, max
- Grade assignment (A-F)
- Pass/Fail lists using list comprehensions
- Formatted result table and menu loop
- Optional CSV export of final grade table
"""

import csv
import sys
from statistics import mean, median
from typing import Dict, Tuple, List

def read_csv(path: str) -> Dict[str, float]:
    data = {}
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if not row: 
                    continue
                name = row[0].strip()
                try:
                    score = float(row[1])
                except (IndexError, ValueError):
                    continue
                data[name] = score
    except FileNotFoundError:
        print(f"CSV file not found: {path}")
    except Exception as e:
        print("Error reading CSV:", e)
    return data

def manual_entry() -> Dict[str, float]:
    print("Enter student records. Type 'done' as name when finished.")
    data = {}
    while True:
        name = input("Student name: ").strip()
        if not name:
            print("Name cannot be empty. Try again.")
            continue
        if name.lower() == 'done':
            break
        score_raw = input("Score (0-100): ").strip()
        try:
            score = float(score_raw)
            if score < 0 or score > 100:
                print("Score must be between 0 and 100.")
                continue
        except ValueError:
            print("Invalid score. Enter a numeric value.")
            continue
        data[name] = score
    return data

# Task 3: Statistical functions
def calculate_average(marks: Dict[str, float]) -> float:
    if not marks: return 0.0
    return mean(marks.values())

def calculate_median(marks: Dict[str, float]) -> float:
    if not marks: return 0.0
    return median(marks.values())

def find_max_score(marks: Dict[str, float]) -> Tuple[str, float]:
    if not marks: return ("", 0.0)
    name = max(marks, key=marks.get)
    return (name, marks[name])

def find_min_score(marks: Dict[str, float]) -> Tuple[str, float]:
    if not marks: return ("", 0.0)
    name = min(marks, key=marks.get)
    return (name, marks[name])

# Task 4: Grade assignment
def assign_grade(score: float) -> str:
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def build_gradebook(marks: Dict[str, float]) -> Dict[str, str]:
    return {name: assign_grade(score) for name, score in marks.items()}

def grade_distribution(grades: Dict[str, str]) -> Dict[str, int]:
    dist = {g: 0 for g in ['A','B','C','D','F']}
    for g in grades.values():
        if g in dist:
            dist[g] += 1
    return dist

# Task 5: Pass/Fail filter
def pass_fail_lists(marks: Dict[str, float], pass_mark: float = 40.0) -> Tuple[List[str], List[str]]:
    passed = [name for name, s in marks.items() if s >= pass_mark]
    failed = [name for name, s in marks.items() if s < pass_mark]
    return passed, failed

# Task 6: Results table
def print_table(marks: Dict[str, float], grades: Dict[str, str]):
    print("\nName\t\tMarks\tGrade")
    print("----------------------------------------")
    for name, score in marks.items():
        print(f"{name:15}\t{score:6.1f}\t{grades[name]}")
    print("----------------------------------------")

def export_csv(path: str, marks: Dict[str, float], grades: Dict[str, str]):
    try:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Name","Marks","Grade"])
            for name, score in marks.items():
                writer.writerow([name, score, grades[name]])
        print(f"Exported grade table to {path}")
    except Exception as e:
        print("Failed to export CSV:", e)

def sample_demo():
    # A quick demo dataset with 5 students
    return {
        'Alice': 78,
        'Bob': 92,
        'Carol': 65,
        'Dave': 34,
        'Eve': 88
    }

def main():
    print("Welcome to GradeBook Analyzer!")
    while True:
        print("\nMenu:\n1) Manual entry\n2) Load CSV\n3) Demo sample data\n4) Exit")
        choice = input("Choose an option (1-4): ").strip()
        if choice == '4':
            print("Goodbye!")
            break
        if choice == '1':
            marks = manual_entry()
        elif choice == '2':
            path = input("Enter CSV file path: ").strip()
            marks = read_csv(path)
        elif choice == '3':
            marks = sample_demo()
        else:
            print("Invalid option.")
            continue

        if not marks:
            print("No student data available. Returning to menu.")
            continue

        avg = calculate_average(marks)
        med = calculate_median(marks)
        mx_name, mx_score = find_max_score(marks)
        mn_name, mn_score = find_min_score(marks)
        grades = build_gradebook(marks)
        dist = grade_distribution(grades)
        passed, failed = pass_fail_lists(marks)

        print_table(marks, grades)
        print(f"Average: {avg:.2f}")
        print(f"Median: {med:.2f}")
        print(f"Max: {mx_name} -> {mx_score:.1f}")
        print(f"Min: {mn_name} -> {mn_score:.1f}")
        print("\nGrade distribution:")
        for g in ['A','B','C','D','F']:
            print(f"{g}: {dist[g]}")
        print(f"\nPassed ({len(passed)}): {', '.join(passed) if passed else 'None'}")
        print(f"Failed ({len(failed)}): {', '.join(failed) if failed else 'None'}")

        # Export option
        exp = input("\nDo you want to export the grade table to CSV? (y/n): ").strip().lower()
        if exp == 'y':
            out = input("Enter output CSV path (default: grades_output.csv): ").strip() or 'grades_output.csv'
            export_csv(out, marks, grades)

        cont = input("\nDo you want to perform another analysis? (y/n): ").strip().lower()
        if cont != 'y':
            print("Exiting. Thank you!")
            break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
