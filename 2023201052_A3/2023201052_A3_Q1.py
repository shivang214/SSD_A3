import csv
from prettytable import PrettyTable

people = {}
expenses = []

def add_participants():
    names = input("Enter participant names (comma-separated): ").split(',')
    for name in names:
        people[name.strip()] = 0

def add_expense():
    paid_by = input("Paid by: ")
    amount = float(input("Amount: "))
    participants_involved = input("Distributed amongst (comma-separated): ").split(',')
    participants_involved = [name.strip() for name in participants_involved]


    if paid_by not in people:
        print(f"{paid_by} is not a valid participant.")
        return

    if any(participant not in people for participant in participants_involved):
        print("One or more participants not found. Please add them first.")
        return

    amount_per_person = amount / len(participants_involved)

    for participant in participants_involved:
        people[participant] -= amount_per_person

    people[paid_by] += amount



    expenses.append((paid_by, amount, participants_involved))

def show_participants():
    print("Participants:")
    for participant in people:
        print(participant)

def show_expenses():
    table = PrettyTable()
    table.field_names = ["Participant's Name", "Amount", "Owes/Gets Back"]

    for participant in people:
        
        balance = people[participant]
        if balance < 0:
            status = "Owes"
        elif balance > 0:
            status = "Gets Back"
        else:
            status="Settled"


        table.add_row([participant, f"${balance:.2f}", status])

    table.align = "l"  
    print(table)


def save_to_csv():
    with open("expenses.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Participant's Name", "Amount", "Owes/Gets Back"])

        if len(people) == 0:
            print("Please enter the values")
            return

        for participant, balance in people.items():
            if balance < 0:
                status = "Owes"
            elif balance > 0:
                status = "Gets Back"
            else:
                status = "Settled"

            writer.writerow([participant, balance, status])


def main():
    while True:
        print("\nMenu:")
        print("1. Add participant(s)")
        print("2. Add expense")
        print("3. Show all participants")
        print("4. Show expenses")
        print("5. Exit/Export")

        choice = input("Enter your choice (1/2/3/4/5):")

        if choice == '1':
            add_participants()
        elif choice == '2':
            add_expense()
        elif choice == '3':
            show_participants()
        elif choice == '4':
            show_expenses()
        elif choice == '5':
            save_to_csv()
            print("Data saved ")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
