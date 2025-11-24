import json
import os
from datetime import datetime

# The file where all the transaction records are stored
DATA_FILE = "budget_data.json" 

# --- Data Handling Functions (Saving/Loading) ---

def load_data():
    """Loads records from the JSON file. Starts empty if no file is found."""
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            # Added a basic check just in case the file gets messed up
            data = json.load(f)
            if not isinstance(data, list):
                print(f"\n[ERROR] Data file ({DATA_FILE}) seems corrupted. Starting fresh.")
                return []
            return data
    except json.JSONDecodeError:
        print(f"\n[ERROR] Failed to read JSON from {DATA_FILE}. Starting fresh.")
        return []
    except Exception as e:
        print(f"\n[ERROR] Unexpected error loading file: {e}. Starting fresh.")
        return []

def save_data(txns):
    """Writes the current list of transactions back to the file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(txns, f, indent=4)
    except Exception as e:
        # Crucial to print error if saving fails
        print(f"\n[FATAL ERROR] Could not save data to {DATA_FILE}: {e}")

def add_new_txn(txns):
    """
    Handles user input for a new transaction and adds it to the list.
    """
    print("\n--- Add New Transaction ---")
    
    # 1. Get description
    desc = input("Enter description (e.g., 'Groceries', 'Job Salary'): ").strip()
    if not desc:
        print("Description cannot be empty.")
        return

    # 2. Get and validate amount
    while True:
        try:
            amount_str = input("Enter amount (+ for Income, - for Expense): ")
            amt = float(amount_str)
            if amt == 0:
                print("Amount cannot be zero.")
                continue
            break
        except ValueError:
            # Simple error handling for non-numeric input
            print("Invalid input. Please enter a number.")

    # 3. Get and validate date
    while True:
        date_in = input("Enter date (YYYY-MM-DD, or Enter for today): ").strip()
        if not date_in:
            date_str = datetime.now().strftime("%Y-%m-%d")
            break
        try:
            datetime.strptime(date_in, "%Y-%m-%d")
            date_str = date_in
            break
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            
    # 4. Select category (simplified map)
    s_map = {'1': 'Income', '2': 'Food', '3': 'Utilities', '4': 'Fun/Hobby', '5': 'Other'}
    print("Select Category:")
    for key, val in s_map.items():
        print(f"  [{key}] {val}")
        
    cat_choice = input("Enter category number (1-5): ").strip()
    category = s_map.get(cat_choice, 'Other') # Default to 'Other'

    # Determine next ID based on current list length
    next_id = len(txns) + 1

    # Create the transaction dictionary
    new_txn = {
        'id': next_id,
        'date': date_str,
        'description': desc,
        'amount': amt,
        'category': category,
        'type': 'Income' if amt > 0 else 'Expense'
    }
    
    txns.append(new_txn)
    save_data(txns)
    print(f"\n[SUCCESS] Added transaction: {desc} ({new_txn['type']}) for ${amt:,.2f} on {date_str}.")

# --- Reporting and Calculation ---

def calculate_totals(txns):
    """Calculates income, expense, balance, and spending breakdown."""
    
    total_inc = 0.0
    total_exp = 0.0
    cat_spending = {}
    
    for t in txns:
        amt = t['amount']
        if amt > 0:
            total_inc += amt
        else:
            total_exp += amt # total_exp remains negative
            category = t['category']
            # Calculate absolute expense for the category breakdown
            cat_spending[category] = cat_spending.get(category, 0) + abs(amt)
            
    net_bal = total_inc + total_exp
            
    return total_inc, total_exp, net_bal, cat_spending

def show_report(txns):
    """Prints the full transaction history and the financial report."""
    if not txns:
        print("\n[INFO] Nothing recorded yet. Add a transaction first.")
        return

    print("\n" + "="*70)
    print(" " * 25 + "FINANCIAL SUMMARY")
    print("="*70)

    total_inc, total_exp, net_bal, cat_spending = calculate_totals(txns)

    # Basic Report Card (removed ANSI colors)
    print(f"Total Income:    ${total_inc:,.2f}")
    print(f"Total Expense:   ${abs(total_exp):,.2f}") # Display expense as positive
    print(f"---")
    print(f"NET BALANCE:     ${net_bal:,.2f}")
    print("-" * 70)
    
    # Transaction Details Table
    print("{:<5} {:<10} {:<20} {:<15} {:>15}".format(
        "ID", "DATE", "DESCRIPTION", "CATEGORY", "AMOUNT"
    ))
    print("-" * 70)
    
    for t in txns:
        # Display absolute amount for expenses, and the raw amount for income
        display_amt = abs(t['amount'])
        
        print("{:<5} {:<10} {:<20} {:<15} {:>15,.2f}".format(
            t['id'], 
            t['date'], 
            t['description'][:20],
            t['category'],
            t['amount']
        ))
        
    print("="*70)

    # Category Spending Breakdown
    print("\nEXPENSE BREAKDOWN:")
    if cat_spending:
        # Sort by largest amount for readability
        sorted_spending = sorted(cat_spending.items(), key=lambda item: item[1], reverse=True)
        for category, amount in sorted_spending:
            # Added a check to prevent division by zero if somehow total_exp is 0
            percentage = (amount / abs(total_exp) * 100) if total_exp != 0 else 0
            print(f"- {category:<15}: ${amount:,.2f} ({percentage:.1f}%)")
    else:
        print("No expenses recorded.")
    print("="*70)


# --- Main Logic ---

def main():
    """Starts the application and displays the menu."""
    
    # Load data at startup
    all_txns = load_data()
    
    while True:
        print("\n--- Simple Budget Tracker Menu ---")
        print("1: Add New Transaction")
        print("2: View Full Financial Report")
        print("3: Exit Application")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            add_new_txn(all_txns)
        elif choice == '2':
            show_report(all_txns)
        elif choice == '3':
            print("\nShutting down the Budget Tracker. Have a great day!")
            break
        else:
            # Simple error message
            print("[Error] Invalid option. Try again.")

# --- Entry Point ---
if __name__ == "__main__":
    main()