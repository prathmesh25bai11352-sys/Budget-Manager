## Page 1

# Personal Budget Tracker (CLI)

## Project Overview

This is a simple, command-line interface (CLI) application designed to help users track their income and expenses. It allows for the addition of new transactions and provides a detailed financial summary, including net balance and categorized expense breakdown.

The project is built around the core concepts of data persistence (using JSON), structured input validation, and modular data processing/reporting, fulfilling the requirements for a basic academic project structure.

## Features

*   **Transaction Input:** Add income (positive amount) or expense (negative amount) with a description, date, and category.
*   **Data Persistence:** Transactions are automatically saved to `budget_data.json`.
*   **Financial Reporting:** Displays total income, total expenses, net balance, and a transaction log.
*   **Expense Analytics:** Shows a breakdown of spending by category (e.g., Food, Utilities).
*   **Error Handling:** Includes validation for numerical inputs and file operations.

## Technologies/Tools Used

*   **Language:** Python 3.x
*   **Data Storage:** Standard JSON library for simple data persistence.
*   **Libraries:** `os`, `json`, `datetime` (all standard library modules).

## Steps to Install & Run the Project

1.  **Prerequisites:** Ensure you have Python 3 installed on your system.
2.  **Download:** Download the `budget_tracker.py` file to your local machine.
3.  **Run:** Open your terminal or command prompt, navigate to the directory where the file is saved, and execute the script:
    
    python budget_tracker.py
    
4.  **Interaction:** Follow the main menu prompts (1 for Add Transaction, 2 for View Report, 3 for Exit).


---


1. Input Test: Choose option [1] Add New Transaction.
    * Test case 1: Enter a positive amount (e.g., `1000`) for Income.
    * Test case 2: Enter a negative amount (e.g., `-50`) for Expense.
    * Test case 3: Enter invalid input for amount (e.g., `abc`) and verify the error message appears.

2. Reporting Test: Choose option [2] View Financial Report.
    * Verify that "Total Income" matches the sum of all positive transactions.
    * Verify that the "Net Balance" is calculated correctly (`Total Income + Total Expense`).
    * Verify the "Category Expense Breakdown" accurately totals expenses per category.

3. Persistence Test:
    * Add a few transactions.
    * Exit the application ([3] Exit).
    * Rerun the application (`python budget_tracker.py`) and select [2] View Financial Report.
    * The previously entered transactions should be loaded and displayed.


