import json
from dataCleaningAndSaving import dataCleaningAndSaving

if __name__ == "__main__":
    # Load the configuration from the JSON file
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    dataCleaningAndSaving(config)