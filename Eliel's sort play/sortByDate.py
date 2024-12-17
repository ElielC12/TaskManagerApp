import json
from datetime import datetime

def sortByDate():
    try:
        # Attempt to open and load the JSON file
        with open("storage.json", "r") as file:
            data = file.read()  # Read the raw file content to see if it's loaded correctly
            print("Raw file content:", data)  # Debugging line to print the raw file content
            data = json.loads(data)  # Load it into a dictionary
        
        # Ensure the 'items' key exists and contains a list
        if "items" in data and isinstance(data["items"], list):
            # Sort the items by date
            data["items"].sort(key=lambda x: datetime.strptime(x["date"], "%m/%d/%YYYY"))
            
            # Print the sorted data
            print("Sorted items by date:")
            for item in data["items"]:
                print(item)
        else:
            print("Error: 'items' key is missing or not a list.")
    
    except FileNotFoundError:
        print("Error: 'storage.json' file not found. Make sure it's in the same directory.")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except KeyError as e:
        print(f"Error: Missing key in JSON. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    sortByDate()
