import pandas as pd
from prettytable import PrettyTable


cricketer_directory = []


try:
    cricketer_data = pd.read_csv("cricketer_data.csv")
    cricketer_directory = cricketer_data.to_dict("records")
except FileNotFoundError:
    pass


def calculate_strike_rate(player):
    if player["Role"] in ["Batsmen","Wk-batsmen"]:
        if player["Balls"] == 0:
            return 0
        return round(player["Runs"] / player["Balls"],3)
    elif player["Role"] == "Bowler":
        if player["Balls"] == 0:
            return 0
        return round(player["Wickets"] / player["Balls"],3)
    elif player["Role"] == "All-rounder":
        batting_strike_rate = calculate_strike_rate({"Runs": player["Runs"], "Balls": player["Balls"], "Role": "Batsmen"})
        bowling_strike_rate = calculate_strike_rate({"Wickets": player["Wickets"], "Balls": player["Balls"], "Role": "Bowler"})
        return round(max(batting_strike_rate, bowling_strike_rate),3) 
    elif player["Role"] in ["Wk-batsmen"]:
        if player["Balls"] == 0:
            return 0
        return round(player["Runs"] / player["Balls"],3)





def display_directory(directory):
    if not directory:
        print("The cricketer directory is empty.")
        return

    table = PrettyTable()
    table.field_names = ["First Name", "Last Name", "Age", "Nationality", "Role", "Runs", "Balls", "Wickets", "Strike Rate"]
    
    for player in directory:
        table.add_row([player["First Name"], player["Last Name"], player["Age"], player["Nationality"], player["Role"], player["Runs"], player["Balls"], player["Wickets"], player["Strike Rate"]])

    print(table)


def add_entry():
    print("Add a New Cricketer Entry:")
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    age = int(input("Enter Age: "))
    nationality = input("Enter Nationality: ")
    role = input("Enter Role (Batsmen/Bowler/All-rounder/Wk-Batsmen): ").capitalize()
    runs = int(input("Enter Runs: "))
    balls = int(input("Enter Balls: "))
    wickets = int(input("Enter Wickets: "))

    
    strike_rate = calculate_strike_rate({"Role": role, "Runs": runs, "Balls": balls, "Wickets": wickets})

    entry = {
        "First Name": first_name,
        "Last Name": last_name,
        "Age": age,
        "Nationality": nationality,
        "Role": role,
        "Runs": runs,
        "Balls": balls,
        "Wickets": wickets,
        "Strike Rate": strike_rate
    }

    cricketer_directory.append(entry)
    print("Cricketer entry added successfully.")


def remove_entry():
    display_directory(cricketer_directory)
    first_name = input("Enter the First Name of the cricketer to remove: ")
    last_name = input("Enter the Last Name of the cricketer to remove: ")
    
    entries_to_remove = [player for player in cricketer_directory if player["First Name"] == first_name and player["Last Name"] == last_name]

    if not entries_to_remove:
        print("Cricketer not found in the directory.")
    else:
        for entry in entries_to_remove:
            cricketer_directory.remove(entry)
        print("Cricketer entry removed successfully.")



def update_entry():
    display_directory(cricketer_directory)
    first_name = input("Enter the First Name of the cricketer to update: ")
    last_name = input("Enter the Last Name of the cricketer to update: ")
    for player in cricketer_directory:
        if player["Last Name"] == last_name and player["First Name"] == first_name:
            print("Update Cricketer Entry:")
            runs = int(input(f"Enter new Runs for {player['First Name']} {player['Last Name']}: "))
            balls = int(input(f"Enter new Balls for {player['First Name']} {player['Last Name']}: "))
            wickets = int(input(f"Enter new Wickets for {player['First Name']} {player['Last Name']}: "))
            player["Runs"] = runs
            player["Balls"] = balls
            player["Wickets"] = wickets
            player["Strike Rate"] = calculate_strike_rate(player)
            print("Cricketer entry updated successfully.")
            return
    print("Cricketer not found in the directory.")



criteria_mapping = {
    "1": "First Name",
    "2": "Last Name",
    "3": "Age",
    "4": "Nationality",
    "5": "Role",
}



def search_entries():
    print("Search Cricketer Entries:")
    print("1. First Name")
    print("2. Last Name")
    print("3. Age")
    print("4. Nationality")
    print("5. Role (Batsmen, Bowler, All-rounder, Wk-Batsmen)")
    
    choice = input("Enter the search criteria (1-5): ")
    search_term = input(f"Enter the {criteria_mapping[choice]} you want to search for: ").lower()
    
    search_results = []

    if choice == "1":
        search_results = [player for player in cricketer_directory if search_term in player["First Name"].lower()]
    elif choice == "2":
        search_results = [player for player in cricketer_directory if search_term in player["Last Name"].lower()]
    elif choice == "3":
        search_results = [player for player in cricketer_directory if search_term in str(player["Age"])]
    elif choice == "4":
        search_results = [player for player in cricketer_directory if search_term in player["Nationality"].lower()]
    elif choice == "5":
        search_results = [player for player in cricketer_directory if search_term in player["Role"].lower()]
    
    display_directory(search_results)




def save_to_csv():
    df = pd.DataFrame(cricketer_directory)
    df.to_csv("cricketer_data.csv", index=False)
    print("Data saved to cricketer_data.csv")


while True:
    print("\nCricketer Directory Menu:")
    print("1. Display Directory")
    print("2. Add New Entry")
    print("3. Remove Entry")
    print("4. Update Entry")
    print("5. Search Entries")
    print("6. Save to CSV")
    print("7. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        display_directory(cricketer_directory)
    elif choice == "2":
        add_entry()
    elif choice == "3":
        remove_entry()
    elif choice == "4":
        update_entry()
    elif choice == "5":
        search_entries()
    elif choice == "6":
        save_to_csv()
    elif choice == "7":
        break
    else:
        print("Invalid choice. Please select a valid option.")

print("Thank you for using the Cricketer Directory.")
