from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to remove rows with missing values
def null_data_removing(original_data):
    logging.info("Removing rows with missing values")
    # Drop rows with missing values
    original_data = original_data.dropna()
    return original_data

# Function to remove rows with non-numeric data in the numeric columns
def remove_non_numeric(original_data, numeric_columns):
    logging.info("Removing rows with non-numeric data in the numeric columns")
    # Remove rows with non-numeric data in the numeric columns
    for column in numeric_columns:
        original_data = original_data[pd.to_numeric(original_data[column], errors='coerce').notnull()]
    return original_data

# Function to convert the data type of a column
def converting_dtype(original_data, column, dtype):
    logging.info(f"Converting column {column} to {dtype}")
    # Convert the column to the specified dtype
    original_data[column] = original_data[column].astype(dtype)
    return original_data

# Function to round off the values in a column
def rounding_float(original_data, column, precision):
    logging.info(f"Rounding column {column} to {precision} decimal places")
    # Round the column to the specified precision
    original_data[column] = original_data[column].round(precision)
    return original_data

def connect_to_db(db_url):
    logging.info("Connecting to the database")
    # Create a SQLAlchemy engine
    engine = create_engine(db_url)
    return engine

def update_database(new_data, engine, table_name):
    logging.info(f"Updating database table {table_name}")
    # Define the table schema
    metadata = MetaData()
    auto_mpg_silver = Table(
        table_name, metadata,
        Column('mpg', Float),
        Column('cylinders', Integer),
        Column('displacement', Float),
        Column('horsepower', Float),
        Column('weight', Integer),
        Column('acceleration', Float),
        Column('model_year', Integer),
        Column('origin', Integer),
        Column('car_name', String, primary_key=True)  # Assuming car_name is unique
    )

    # Create the table if it doesn't exist
    metadata.create_all(engine)

    # Insert the data into PostgreSQL
    new_data.to_sql(table_name, engine, if_exists='append', index=False)
    return f"Data added to {table_name} table in the database"