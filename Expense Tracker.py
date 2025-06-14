import csv
import os
from datetime import datetime

# Global filename for saving/loading expenses
EXPENSES_FILE = "expenses.csv"

def add_expense(expenses):
    """
    Prompts the user for expense details, validates the date and amount, and adds the expense as a dictionary to the expenses list.
    """
    # Get and validate the date input in YYYY-MM-DD format
    date_str = input("Enter the date of the expense (YYYY-MM-DD): ")
    try:
        # raise an exception if the format is incorrect
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter the date as YYYY-MM-DD.")
        return

    category = input("Enter the expense category (example:Education, Food, Travel, Leisure): ").strip()
    # Ensure category is not left blank
    if not category:
        print("Expense category cannot be empty.")
        return

    # Get and validate the expense amount
    amount_str = input("Enter the amount spent: ").strip()
    try:
        amount = float(amount_str)
    except ValueError:
        print("Invalid amount. Please enter a number (example: 22.50).")
        return

    description = input("Enter a brief description of the expense: ").strip()
    if not description:
        print("Expense description cannot be empty.")
        return

    # Create and add the expense dictionary to the list
    expense = {
        "date": date_str,
        "category": category,
        "amount": amount,
        "description": description
    }
    expenses.append(expense)
    print("Expense added successfully!")

def view_expenses(expenses):
    """
    Displays all saved expenses. For each expense, checks if all required keys are present. If not, notifies the user that the entry is incomplete.
    """
    if not expenses:
        print("No expenses to display.")
        return

    print("\n--- Expense List ---")
    for i, expense in enumerate(expenses, start=1):
        # Check for the required fields presence in the dictionary.
        if not all(key in expense and expense[key] != "" for key in ["date", "category", "amount", "description"]):
            print(f"Expense {i}: Incomplete entry, skipping...")
            continue

        print(f"Expense {i}:")
        print(f"  Date       : {expense['date']}")
        print(f"  Category   : {expense['category']}")
        print(f"  Amount     : {expense['amount']}")
        print(f"  Description: {expense['description']}")
    print("--------------------\n")

def track_budget(expenses, budget):
    """
    Calculates the total expense amount and compares it with the provided monthly budget. Displays a warning if expenses exceed the budget, otherwise shows the remaining balance.
    """
    total_expenses = sum(expense.get("amount", 0) for expense in expenses)
    print(f"\nTotal expenses so far: {total_expenses}")

    if total_expenses > budget:
        print("WARNING: You have exceeded your budget by {:.2f}!\n".format(total_expenses - budget))
    else:
        print("You have {:.2f} left for the month.\n".format(budget - total_expenses))

def save_expenses(expenses, filename):
    """
    Saves the list of expenses to a CSV file. Each row in the CSV file corresponds to one expense.
    """
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["date", "category", "amount", "description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for expense in expenses:
                writer.writerow(expense)
        print("Expenses saved successfully!")
    except Exception as e:
        print(f"An error occurred while saving expenses: {e}")

def load_expenses(filename):
    """
    Loads expenses from the CSV file and returns them as a list of dictionaries. If the file does not exist, returns an empty list.
    """
    expenses = []
    if not os.path.exists(filename):
        return expenses

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert the amount to float
                try:
                    row["amount"] = float(row["amount"])
                except ValueError:
                    row["amount"] = 0.0
                expenses.append(row)
        print("Loaded previous expenses successfully!")
    except Exception as e:
        print(f"An error occurred while loading expenses: {e}")
    return expenses

def show_menu():
    """
    Displays the main menu options.
    """
    print("==== Personal Expense Tracker Menu ====")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Track budget")
    print("4. Save expenses")
    print("5. Exit")
    print("=======================================\n")

def main():
    # Load previous expenses from file if available
    expenses = load_expenses(EXPENSES_FILE)

    # Budget is not set until the user inputs a value in option 3.
    monthly_budget = None

    while True:
        show_menu()
        try:
            choice = int(input("Enter your option (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.\n")
            continue

        if choice == 1:
            add_expense(expenses)
        elif choice == 2:
            view_expenses(expenses)
        elif choice == 3:
            if monthly_budget is None:
                try:
                    monthly_budget = float(input("Enter your monthly budget: "))
                except ValueError:
                    print("Invalid budget input. Please enter a numeric value.")
                    continue
            track_budget(expenses, monthly_budget)
        elif choice == 4:
            save_expenses(expenses, EXPENSES_FILE)
        elif choice == 5:
            # Save before exiting the program
            save_expenses(expenses, EXPENSES_FILE)
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Please choose a valid option from the menu.\n")

if __name__ == "__main__":
    main()
