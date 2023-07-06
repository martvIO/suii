import os

from mysql import connector
from dotenv import load_dotenv

# Access environment variables
load_dotenv()
PASSWORD = os.getenv("PASSWORD")

"""PART 5: SELECTING DATA"""
# Select specific columns example
try: 
    # Connect to existing database
    with connector.connect(
        host = "localhost",
        user = "root",
        password = PASSWORD,
        database = "book_ratings"
    ) as existing_database:
        
        # Create cursor object
        select_specific_cols = "SELECT author, release_year FROM books"
        with existing_database.cursor() as cursor:
            cursor.execute(select_specific_cols)
            
            # Display returned data
            returned_data = cursor.fetchall()
            for result in returned_data:
                print(result)
        
except connector.Error as e: 
    print(e)

# Select all columns example
try:
    # Connect to existing database
    with connector.connect(
        host = "localhost",
        user = "root",
        password = PASSWORD,
        database = "book_ratings"
    ) as existing_database:
        
        # Create cursor object
        select_all_cols = "SELECT * FROM books"
        with existing_database.cursor() as cursor:
            cursor.execute(select_all_cols)
            
            # Display returned data
            returned_data = cursor.fetchall()
            for result in returned_data:
                print(result)
        
except connector.Error as e: 
    print(e)
