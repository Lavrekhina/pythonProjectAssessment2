import pytest
from data_processor_my import DataProcessor

@pytest.fixture
def processor():
    # Create a temporary CSV file for testing
    test_data = """TransactionID,StoreLocation,ProductCategory,TotalPrice,Quantity,CustomerSatisfaction,PaymentMethod
1,Store A,Category 1,10.00,1,5,Card
2,Store B,Category 2,20.00,2,4,Cash
3,Store A,Category 1,15.00,1,3,Card
4,Store C,Category 3,25.00,1,4,Card
5,Store B,Category 2,30.00,3,5,Cash
"""
    # Create a temporary test_data.csv file
    with open('test_data.csv', 'w') as f:
        f.write(test_data)  # Write test data to the file

    return DataProcessor('test_data.csv')


def test_get_total_transactions(processor):
    # Verify that the total number of transactions is 5
    assert processor.get_total_transactions() == 5, "Error: Total transactions should be 5"


def test_get_unique_locations_and_categories(processor):
    # Get unique locations and categories
    locations, categories = processor.get_unique_locations_and_categories()
    # Verify that unique locations match the expected values
    assert set(locations) == {"Store A", "Store B", "Store C"}, "Error: Unique locations mismatch"
    # Verify that unique categories match the expected values
    assert set(categories) == {"Category 1", "Category 2", "Category 3"}, "Error: Unique categories mismatch"


def test_get_transaction_details(processor):
    # Get transaction details by ID
    transaction = processor.get_transaction_details('1')
    # Verify that the transaction location matches the expected value
    assert transaction['StoreLocation'] == 'Store A', "Error: Transaction details mismatch"


def test_get_transactions_by_location(processor):
    # Get transactions by location
    transactions = processor.get_transactions_by_location('Store A')
    # Verify that the number of transactions for Store A is 2
    assert len(transactions) == 2, "Error: Should return 2 transactions for Store A"


def test_get_transactions_by_category(processor):
    # Get transactions by category
    transactions = processor.get_transactions_by_category('Category 2')
    # Verify that the number of transactions for Category 2 is 2
    assert len(transactions) == 2, "Error: Should return 2 transactions for Category 2"


def test_group_by_location(processor):
    # Group revenue by location
    revenue = processor.group_by_location()
    # Verify that the revenue for Store A is 25.00
    assert revenue['Store A'] == 25.00, "Error: Revenue for Store A should be $25.00"
    # Verify that the revenue for Store B is 50.00
    assert revenue['Store B'] == 50.00, "Error: Revenue for Store B should be $50.00"


def test_sales_summary(processor):
    # Get sales summary for Store A
    summary = processor.sales_summary('Store A')
    # Verify that the total number of transactions for Store A is 2
    assert summary['Total Transactions'] == 2, "Error: Total transactions for Store A should be 2"
    # Verify that the total revenue for Store A is 25.00
    assert summary['Total Revenue'] == 25.00, "Error: Total revenue for Store A should be $25.00"
    # Verify that the average customer satisfaction for Store A is 4.0
    assert summary['Average Customer Satisfaction'] == 4.0, "Error: Average customer satisfaction should be 4.0"





