from data_processor_my import DataProcessor
from visualizer import Visualizer
import json

# Ask user to input the path to the CSV file
def main():
    file_path = input("Enter the path to the CSV file: ")
    processor = DataProcessor(file_path)

    while True:
        # Display a menu of options to the user
        print("\nMenu:")
        print("1. Total Transactions")
        print("2. Unique Store Locations and Product Categories")
        print("3. Transaction Details by ID")
        print("4. Transactions by Store Location")
        print("5. Transactions by Product Category")
        print("6. Revenue by Store Location")
        print("7. Sales Summary by Store Location")
        print("8. Visualize Data")
        print("9. Interactive Dashboard")
        print("10. Export Sales Summary to JSON")
        print("11. Exit")

        # User should make the choice what information they want to receive
        choice = input("Select an option: ")

        # Display the total number of transactions
        if choice == '1':
            print("Total Transactions:", processor.get_total_transactions())
        # Display unique store locations and product categories
        elif choice == '2':
            locations, categories = processor.get_unique_locations_and_categories()
            print("Unique Locations:", locations)
            print("Unique Categories:", categories)
        # Display details of a specific transaction by ID
        elif choice == '3':
            transaction_id = input("Enter Transaction ID: ")
            details = processor.get_transaction_details(transaction_id)
            print(details if details else "Transaction not found.")
        # Display all transactions for a specific store location
        elif choice == '4':
            location = input("Enter Store Location: ")
            transactions = processor.get_transactions_by_location(location)
            for transaction in transactions:
                print(transaction)
        # Display all transactions for a specific product category
        elif choice == '5':
            category = input("Enter Product Category: ")
            transactions = processor.get_transactions_by_category(category)
            for transaction in transactions:
                print(transaction)
        # Display total revenue by store location
        elif choice == '6':
            revenue_data = processor.group_by_location()
            print(revenue_data)
        # Display a sales summary for a specific store location
        elif choice == '7':
            location = input("Enter Store Location for Summary: ")
            summary = processor.sales_summary(location)
            if summary:
                for key, value in summary.items():
                    print(f"{key}:{value}")
            else:
                print("No transactions found for this location.")
        # Visualize revenue by store location using a pie chart
        elif choice == '8':
            location_revenue = processor.group_by_location()
            Visualizer.pie_chart(location_revenue, "Revenue by Store Location")
        # Show interactive dashboard
        elif choice == '9':
            Visualizer.interactive_dashboard(processor)
        # Export a sales summary for a specific location to a JSON file
        elif choice == '10':
            location = input("Enter Store Location for JSON export: ")
            summary = processor.sales_summary(location)
            if summary:
                with open(f"{location}_sales_summary.json", "w") as json_file:
                    json.dump(summary, json_file, indent=4)
                print(f"Sales summary exported to {location}_sales_summary.json")
            else:
                print("No transactions found for this location.")
        # Exit the program
        elif choice == '11':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()


