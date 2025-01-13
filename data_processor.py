import csv
from collections import defaultdict

# Process data from csv file
class DataProcessor:

    def __init__(self, file_path):
        """
        Initializes the DataProcessor with data loaded from a CSV file.

        :param file_path:path to the csv file we are working with
        """
        self.data = [] # store all data from the csv file
        self.load_data(file_path)


# Load the data from csv file
    def load_data(self, file_path):
        """
        Loads data from specified csv file.

        :param file_path: Path to the CSV file into data.
        :return: None
        """
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.data = list(reader) # store all rows in a list

# Counts the total amount of transactions
    def get_total_transactions(self):
        """
        Counts the total number of transactions.

        :return: total number of transactions
        """
        return len(self.data)


# Showing the list of possible locations and possible product categories
    def get_unique_locations_and_categories(self):
        """
        Retrieves unique store locations and product categories from the data.

        :return: two lists, one with unique locations, second one with unique product categories.
        """
        locations = set()
        categories = set()
        for transaction in self.data:
            locations.add(transaction['StoreLocation'])
            categories.add(transaction['ProductCategory'])
        return list(locations), list(categories)

# Retrieve details of a specific transaction using the TransactionID
    def get_transaction_details(self, transaction_id):
        """
        Show details of a specific transaction by ID

        :param transaction_id: the ID of transaction to show the information about
        :return: details about specified transaction, or None if not found
        """
        for transaction in self.data:
            if transaction['TransactionID'] == transaction_id:
                return transaction
        return None

# Retrieve all transactions for a specific store location
    def get_transactions_by_location(self, location):
        """Retrieves all transactions for a specific store location."""
        return [transaction for transaction in self.data if transaction.get('StoreLocation') == location]

    def get_transactions_by_category(self, category):
        """Retrieves all transactions for a specific product category."""
        result = [transaction for transaction in self.data if transaction.get('ProductCategory') == category]
        if not result:
            print(f"No transactions found for category: {category}")
        else:
            for transaction in result:
                print(transaction)
        return result

    def group_by_location(self):
        """
        Groups transactions by store location and calculates total revenue for each location.
        Stores the result as an instance attribute and returns it.

        :return: a dictionary with store locations as keys and total revenue as values.
        """
        self.revenue_by_location = defaultdict(float)

        # Iterate through each transaction in the dataset
        for transaction in self.data:
            # Check if both 'StoreLocation' and 'TotalPrice' are present in the transaction
            if 'StoreLocation' in transaction and 'TotalPrice' in transaction:
                store_location = transaction['StoreLocation']
                total_price_str = transaction['TotalPrice'].strip()
                # Convert total price to a float
                total_price = float(total_price_str.replace(',', '.')) if total_price_str.replace(',', '').replace('.',
                                                                                                                   '',
                                                                                                                   1).isdigit() else 0.0
                self.revenue_by_location[store_location] += total_price

        # Format the revenue values and store them as an attribute
        self.revenue_by_location = {location: round(revenue, 2) for location, revenue in
                                    self.revenue_by_location.items()}

        # Return the dictionary
        return self.revenue_by_location

#  Provide a summary of sales for a specific store location
    def sales_summary(self, location):
        """
        Generates a sales summary for a specific store location.
        :param location: consist of multiple calculations to fill all the requested information for sales summary
        :return: sales summary including total transactions, total revenue, average transaction value, total quantity sold, average customer satisfaction and payment method percentage
        """
        # Show transactions specific to the provided location
        location_data = self.get_transactions_by_location(location)
        # Check if there are any transactions for the given location
        if not location:
            print(f"No transactions found for location: {location}")
        return None

    # Calculate total number of transactions
    total_transactions = len(location_data)
    # Set total revenue to zero
    total_revenue = 0
    # Use for oop to go through each transaction to calculate total revenue
    for transaction in location_data:
        if 'TotalPrice' in transaction: # Ensure the 'TotalPrice' field exists
            # Remove currency symbols and format the price for calculation
            value = transaction['TotalPrice'].replace('£', '').replace(',', '').strip()
            if value.replace('.', '', 1).isdigit(): # Check if the value is numeric
                total_revenue += float(value)
    # Calculate average transaction value
    average_transaction_value = total_revenue / total_transactions if total_transactions > 0 else 0
    # Calculate total quantity sold by summing the 'Quantity' field
    total_quantity = sum(int(transaction['Quantity']) for transaction in location_data if
                         'Quantity' in transaction and transaction['Quantity'])
    # Calculate average customer satisfaction
    average_satisfaction = (
        sum(float(transaction['CustomerSatisfaction']) for transaction in location_data if
            'CustomerSatisfaction' in transaction and transaction['CustomerSatisfaction']) / total_transactions
        if total_transactions > 0 else 0
    )
    # Count payment methods
    payment_method_count = defaultdict(int)
    for transaction in location_data:
        payment_method_count[transaction['PaymentMethod']] += 1
    # Calculate the percentage of each payment method
    payment_method_percentage = [
        f"{method}: {(count / total_transactions) * 100:.2f}%"
        for method, count in payment_method_count.items()
    ]
    # Return the sales summary as a dictionary
    return {
        "Total Transactions": total_transactions,
        "Total Revenue": format(total_revenue, '.2f'),
        "Average Transaction Value": format(average_transaction_value, '.2f'),
        "Total Quantity Sold": total_quantity,
        "Average Customer Satisfaction": format(average_satisfaction,'.2f'),
        "Payment Method Percentage": ', '.join(payment_method_percentage)
    }