import csv
import matplotlib.pyplot as plt


def read_expenses_data(filename):
    data = {}
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            participant = row["Participant's Name"]
            amount = float(row["Amount"].replace('$', '').replace(',', ''))
            data[participant] = amount
    return data

def calculate_net_balance(data):
    total_expenses = sum(data.values())
    equal_share = total_expenses / len(data)
    net_balance = {participant: amount - equal_share for participant, amount in data.items()}
    return net_balance

def create_pie_chart(data, chart_title, explode_participant):
    labels = data.keys()
    sizes = data.values()


    explode = [0.1 if explode_participant else 0] * len(sizes)

    
    sizes = [abs(size) for size in sizes]

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, explode=explode)
    plt.axis('equal')

    plt.title(chart_title)
    plt.legend(labels, loc='upper left', bbox_to_anchor=(1, 1))

def plot_expenses_data():
    expenses_data = read_expenses_data("expenses.csv")
    net_balance = calculate_net_balance(expenses_data)

    owes_data = {participant: balance for participant, balance in net_balance.items() if balance < 0}
    gets_back_data = {participant: -balance for participant, balance in net_balance.items() if balance > 0}

    create_pie_chart(owes_data, "Owes", True)  
    plt.show()

    create_pie_chart(gets_back_data, "Gets Back", True)  
    plt.show()


def read_cricket_data(filename):
    first_names = []
    last_names = []
    roles = []
    runs = []
    balls = []
    wickets = []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_names.append(row['First Name'])
            last_names.append(row['Last Name'])
            roles.append(row['Role'])
            runs.append(int(row['Runs']))
            balls.append(int(row['Balls']))
            wickets.append(int(row['Wickets']))

    return first_names, last_names, roles, runs, balls, wickets

def categorize_and_calculate_strike_rates(roles, runs, balls, wickets):
    batting_strike_rates = []
    bowling_strike_rates = []

    for role, run, ball, wicket in zip(roles, runs, balls, wickets):
        if role.lower() == 'batsmen':
            batting_strike_rates.append(run / ball if ball > 0 else 0)
            bowling_strike_rates.append(0)  # Set a default value for bowlers
        elif role.lower() == 'bowler':
            batting_strike_rates.append(0)  # Set a default value for batsmen
            bowling_strike_rates.append(wicket / ball if ball > 0 else 0)
        elif role.lower() == 'wk-batsmen':
            batting_strike_rates.append(run / ball if ball > 0 else 0)
            bowling_strike_rates.append(0)  
        else:  # All-rounder
            batting_strike_rates.append(run / ball if ball > 0 else 0)
            bowling_strike_rates.append(wicket / ball if ball > 0 else 0)

    return batting_strike_rates, bowling_strike_rates

def plot_cricket_data(first_names, last_names, batting_strike_rates, bowling_strike_rates):
    plt.figure(figsize=(10, 6))
    width = 0.35
    x = range(len(first_names))
    batting_bars = plt.bar(x, batting_strike_rates, width, label='Batting Strike Rate', color='b')
    bowling_bars = plt.bar(
        [i + width for i in x], bowling_strike_rates, width, label='Bowling Strike Rate', color='g'
    )
    x_labels = [f"{first_name} {last_name}" for first_name, last_name in zip(first_names, last_names)]
    plt.xticks([i + width/2 for i in x], x_labels, rotation=45)
    plt.xlabel('Players')
    plt.ylabel('Strike Rate')
    plt.title('Batting and Bowling Strike Rates for Players')
    plt.legend()
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    while True:
        print("Menu:")
        print("1. Expenses")
        print("2. Cricket Data")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            plot_expenses_data()
        elif choice == '2':
            first_names, last_names, roles, runs, balls, wickets = read_cricket_data('cricketer_data.csv')
            batting_strike_rates, bowling_strike_rates = categorize_and_calculate_strike_rates(roles, runs, balls, wickets)
            plot_cricket_data(first_names, last_names, batting_strike_rates, bowling_strike_rates)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select a valid option (1, 2, or 3).")
