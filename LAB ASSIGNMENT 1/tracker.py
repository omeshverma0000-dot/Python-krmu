''' 
STUDENT NAME= OMESH VERMA
DATE=30/10/2025
TITLE=COLORIE TRACKER

'''
print("WELCOME! Many students want a quick "
"and simple way to monitor their daily" \
" calorie intake. This mini project aims to" \
" help them build a Python-based CLI (Command Line Interface)" \
" tool where they can log their meals and keep track of total calories" \
" consumed, compare against a personal daily limit,"
" and save session logs for future tracking. ")
meal_name=[]
calorie_amount=[]
numb=int(input("how many meals do you want to enter:"))
for i in range(numb):
    a=(input(f"enter the meal name {i+1}: "))
    meal_name.append(a)


    b=float(input(f"enter the calorie amount {i+1}:"))
    calorie_amount.append(b)

Total_calorie=sum(calorie_amount)


avg_calorie=Total_calorie/len(calorie_amount)

user_calorie_limit=int(input("enter your daily calorie limit"))

if Total_calorie>user_calorie_limit:
    print(f"Warning! You have exceeded your daily calorie limit.\n"
          f"Your calorie intake: {Total_calorie}\n"
          f"Your calorie limit:  {user_calorie_limit}\n"
          f"Exceeded calories by: {Total_calorie - user_calorie_limit}")
    
else:
    print(f"your calorie intake is within calorie limit\n"
          f"your calorie intake:, {Total_calorie}\n"
          f"your calorie limit:, {user_calorie_limit}\n" )
    4
print("\n=========== SUMMARY REPORT ===========\n")
print("Meal Name\tCalories")
print("--------------------------------------")
for i in range(len(meal_name)):
    print(f"{meal_name[i]}\t\t{calorie_amount[i]}")
print("--------------------------------------")
print(f"Total:\t\t{Total_calorie}")
print(f"Average:\t{avg_calorie:.2f}")

save = input("\nDo you want to save this report? (yes/no): ").lower()
if save == "yes":
    from datetime import datetime
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("calorie_log.txt", "a") as f:
        f.write("Daily Calorie Tracker Log\n")
        f.write(f"Timestamp: {time}\n\n")
        f.write("Meal Name\tCalories\n")
        f.write("----------------------------------\n")
        for i in range(len(meal_name)):
            f.write(f"{meal_name[i]}\t\t{calorie_amount[i]}\n")
        f.write("----------------------------------\n")
        f.write(f"Total:\t\t{Total_calorie}\n")
        f.write(f"Average:\t{avg_calorie:.2f}\n")
        
    print("\n✅ Log saved to calorie_log.txt")

print("\nThank you for using the Calorie Tracker!")


