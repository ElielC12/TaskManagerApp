import json
from datetime import datetime
import os


def createID():
    """
    Generates a new unique ID for a new item by finding the highest current ID 
    and adding 1 to it.
    """
    with open('storage.json', 'r+') as storage:
        storage = json.load(storage)  # Load the current JSON data from 'storage.json'
    
    ids = []  # List to store all the current IDs
    for item in storage["items"]:
        ids.append(item['id'])  # Collect all item IDs into the list
        ids.sort()  # Sort the list of IDs
    
    # Return the highest ID + 1 to create a new unique ID
    if len(storage["items"]) == 0:
        return 0
    return ids[-1] + 1


def addToJSON(id: int, name: str, date: str, category: str = ''):
    """
    Adds a new item to the JSON file 'storage.json' with a given ID, name, date, and category.
    """
    with open('storage.json', 'r+') as file:
        storage = json.load(file)  # Load existing data from the file

    items = storage["items"]  # Access the list of items in the JSON structure
    items.append({
        "name": name,
        "date": date,
        "category": category,
        "id": id
    })  # Append a new item to the list with provided details

    # Write the updated data back to 'storage.json'
    with open('storage.json', 'w') as newfile:
        json.dump(storage, newfile, indent=4)  # Write the JSON data with formatting


def removeFromJSON(id: int):
    """
    Removes an item with a specific ID from the 'storage.json' file.
    """
    with open('storage.json', 'r+') as file:
        storage = json.load(file)  # Load the current JSON data from the file

    items = storage["items"]  # Access the list of items in the JSON structure
    for index, obj in enumerate(items):
        if obj["id"] == id:  # Check if the item ID matches the one to remove
            items.pop(index)  # Remove the item from the list
    
    # Write the updated data back to 'storage.json'
    with open('storage.json', 'w') as newfile:
        json.dump(storage, newfile, indent=4)  # Write the JSON data with formatting


def editJSONItem(id: int, name: str, date: str, category: str = ''):
    """
    Edits an existing item in 'storage.json' by removing it and adding it with updated details.
    """
    removeFromJSON(id)  # First, remove the old item with the given ID
    addToJSON(id, name, date, category)  # Then, add the updated item


def resetJSON():
    """
    Resets the entire 'storage.json' file by clearing the list of items.
    """
    # Create an empty structure with just an "items" key holding an empty list
    empty_data = {
        "items": []
    }
    
    # Open the file in write mode, which will overwrite it with the empty data
    with open('storage.json', 'w') as file:
        json.dump(empty_data, file, indent=4)  # Write the empty data to the file
    
    print("JSON file has been reset to an empty state.")


def sortByDate(): 
    """
    Sorts the items in 'storage.json' by the 'date' field, from earliest to latest.
    """
    try:
        # Check if the file exists
        if not os.path.exists("storage.json"):
            print("Error: 'storage.json' file does not exist. Make sure it's in the same directory.")
            return
        
        # Load the data from 'storage.json' file
        with open("storage.json", "r") as file:
            data = file.read()
            print(f"Raw file content: {data}")  # Debugging line to print the raw file content
            data = json.loads(data)  # Parse the data from JSON into a Python dictionary
        
        # Check if 'items' key exists and is a list
        if "items" in data and isinstance(data["items"], list):
            # Sort items by the 'date' field (format: month/day/year)
            data["items"].sort(key=lambda x: datetime.strptime(x["date"], "%m/%d/%Y"))
            
            # Print the sorted items by date
            print("Sorted items by date:")
            for item in data["items"]:
                print(item)
        else:
            print("Error: 'items' key is missing or not a list.")
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def sortByCategoryAndDate():
    """
    Sorts the items in 'storage.json' first by 'category' and then by 'date' (from earliest to latest).
    """
    try:
        # Check if the file exists
        if not os.path.exists("storage.json"):
            print("Error: 'storage.json' file does not exist. Make sure it's in the same directory.")
            return
        
        # Load the data from 'storage.json' file
        with open("storage.json", "r") as file:
            data = file.read()
            print(f"Raw file content: {data}")  # Debugging line to print the raw file content
            data = json.loads(data)  # Parse the data from JSON into a Python dictionary
        
        # Check if 'items' key exists and is a list
        if "items" in data and isinstance(data["items"], list):
            # Sort items first by 'category' and then by 'date'
            data["items"].sort(key=lambda x: (x["category"], datetime.strptime(x["date"], "%m/%d/%Y")))
            
            # Print the sorted items by category and date
            print("Sorted items by category and date:")
            for item in data["items"]:
                print(item)
        else:
            print("Error: 'items' key is missing or not a list.")
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# This is the entry point of the script
if __name__ == "__main__":
    # Call the functions to sort items by date and by category and date
    sortByDate()
    # sortByCategoryAndDate()
