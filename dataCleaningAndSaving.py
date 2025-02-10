import pandas as pd
from cleaningModules import *
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def dataCleaningAndSaving(config):
    db_url = config['db_url']
    data_set_path = config['data_set_path']
    table_name = config['table_name']
    column_names = config['column_names']
    numeric_columns = config['numeric_columns']
    save_to_path = config['save_path'] 

    # Database connection details
    try:
        engine = connect_to_db(db_url)
    except Exception as e:
        logging.error(f"Error in connecting to database: {e}")
        return

    # Load the data
    logging.info(f"Loading data from {data_set_path}")
    original_data = pd.read_csv(data_set_path, delim_whitespace=True, header=None)

    # Add the column names to the data
    if original_data.shape[1] == len(column_names):
        original_data.columns = column_names
    else:
        logging.error("Column size mismatch")
        return

    if original_data.isnull().sum().any():
        original_data = null_data_removing(original_data)

    # Removing non-numeric data
    original_data = remove_non_numeric(original_data, numeric_columns)

    # Converting to proper data types and rounding off
    original_data = converting_dtype(original_data, 'weight', int)
    original_data = converting_dtype(original_data, 'horsepower', float)
    original_data = rounding_float(original_data, 'horsepower', 1)

    # Save the data to a new CSV file
    logging.info("Saving cleaned data to mpg_silver_new.csv")
    original_data.to_csv(save_to_path, index=False)

    # Load the data from the new CSV file
    new_data = pd.read_csv(save_to_path)

    # Update the database
    logging.info("Updating the database with cleaned data")
    result = update_database(new_data, engine, table_name)
    logging.info(result)

if __name__ == "__main__":
    # Load the configuration from the JSON file
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    dataCleaningAndSaving(config)