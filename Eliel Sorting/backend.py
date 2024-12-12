#!/usr/bin/env python3
"""
Program: Assignment Manager App
Author: Eliel Cortes & Logan Gardner
Professor: Prof. Ordonez
Date: 2024-12-16
"""
import json
from datetime import datetime
import os

# Get the directory of the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Utility function to read and write JSON data to the file
def read_json_file(filename):
    """
    Reads a JSON file and returns the parsed data.
    
    >>> read_json_file('storage.json')  # Example with a valid file
    {'items': [{"name": "item1", "date": "12/12/2024", "category": "A", "id": 1}]}
    
    >>> read_json_file('nonexistent.json')  # Example with a nonexistent file
    Traceback (most recent call last):
        ...
    FileNotFoundError: [Errno 2] No such file or directory: 'nonexistent.json'
    """
    filepath = os.path.join(SCRIPT_DIR, filename)
    with open(filepath, 'r') as file:
        return json.load(file)

def write_json_file(filename, data):
    """
    Writes data to a JSON file.
    
    >>> write_json_file('output.json', {"items": [{"name": "item1", "date": "12/12/2024", "category": "A", "id": 1}]})  # Writes to file
    >>> write_json_file('output.json', {"items": []})  # Writes empty list to file
    """
    filepath = os.path.join(SCRIPT_DIR, filename)
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


def createID():
    """
    Creates a new ID based on the highest ID in storage.
    
    >>> createID()  # Assuming 'storage.json' contains [{"id": 1}, {"id": 2}]
    3
    
    >>> createID()  # When 'storage.json' is empty
    1
    """
    storage = read_json_file('storage.json')
    ids = [item['id'] for item in storage["items"]]
    ids.sort()
    return ids[-1] + 1 if ids else 1  # Return 1 if the list is empty


def addToJSON(id: int, name: str, date: str, category: str = ''):
    """
    Adds an item to the JSON storage file.
    
    >>> addToJSON(1, "Item A", "12/12/2024", "Category 1")  # Adds a new item
    >>> addToJSON(2, "Item B", "12/13/2024")  # Adds an item without category
    """
    storage = read_json_file('storage.json')
    items = storage["items"]
    items.append({
        "name": name,
        "date": date,
        "category": category,
        "id": id
    })
    write_json_file('storage.json', storage)


def removeFromJSON(id: int):
    """
    Removes an item from the JSON storage file by its ID.
    
    >>> removeFromJSON(1)  # Removes item with id 1
    >>> removeFromJSON(999)  # Tries to remove non-existent item
    """
    storage = read_json_file('storage.json')
    items = storage["items"]
    storage["items"] = [item for item in items if item["id"] != id]
    write_json_file('storage.json', storage)


def editJSONItem(id: int, name: str, date: str, category: str = ''):
    """
    Edits an existing item in the JSON storage file.
    
    >>> editJSONItem(1, "New Item", "12/14/2024", "New Category")  # Updates item with id 1
    >>> editJSONItem(999, "Nonexistent Item", "12/14/2024")  # Attempts to edit non-existent item
    """
    removeFromJSON(id)  # Remove the item first
    addToJSON(id, name, date, category)  # Add the new item


def resetJSON():
    """
    Resets the JSON storage file to an empty state.
    
    >>> resetJSON()  # Resets the storage to an empty list
    """
    empty_data = {
        "items": []
    }
    write_json_file('storage.json', empty_data)
    print("JSON file has been reset to an empty state.")


def sortByDate(): 
    """
    Sorts the items in the storage file by date.
    
    >>> sortByDate()  # Sorts items by date (assuming 'storage.json' contains dates)
    >>> sortByDate()  # Edge case: file is missing or contains invalid date format
    """
    try:
        if not os.path.exists(os.path.join(SCRIPT_DIR, "storage.json")):
            print("Error: 'storage.json' file does not exist.")
            return

        data = read_json_file("storage.json")
        if "items" in data and isinstance(data["items"], list):
            data["items"].sort(key=lambda x: datetime.strptime(x["date"], "%m/%d/%Y"))
            write_json_file("sorted_storage.json", data)
            print("Sorted data has been written to 'sorted_storage.json'.")
        else:
            print("Error: 'items' key is missing or not a list.")
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def sortByCategoryAndDate():
    """
    Sorts the items in the storage file by category and then by date.
    
    >>> sortByCategoryAndDate()  # Sorts by category and date
    >>> sortByCategoryAndDate()  # Edge case: file is missing or contains invalid date format
    """
    try:
        if not os.path.exists(os.path.join(SCRIPT_DIR, "storage.json")):
            print("Error: 'storage.json' file does not exist.")
            return

        data = read_json_file("storage.json")
        if "items" in data and isinstance(data["items"], list):
            data["items"].sort(key=lambda x: (x["category"], datetime.strptime(x["date"], "%m/%d/%Y")))
            write_json_file("sorted_storage.json", data)
            print("Sorted data has been written to 'sorted_storage.json'.")
        else:
            print("Error: 'items' key is missing or not a list.")
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def getInfo(id: int):
    """
    Retrieves information for an item by its ID.
    
    >>> getInfo(1)  # Returns item with id 1
    >>> getInfo(999)  # Item with id 999 does not exist
    """
    try:
        if not os.path.exists(os.path.join(SCRIPT_DIR, "storage.json")):
            print("Error: 'storage.json' file does not exist.")
            return

        data = read_json_file("storage.json")
        items = data.get("items", [])
        item_list = []

        for item in items:
            if item["id"] == id:
                item_list.append(item)
                print(item_list)
                return item_list

        print(f"No item found with ID: {id}")
        return None

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def removeCategory(cat: str):
    """
    Removes a category from all items in the JSON file, setting it to 'None'.
    
    >>> removeCategory("Category A")  # Removes the category from all items
    >>> removeCategory("Nonexistent Category")  # Tries to remove a category that does not exist
    """
    try:
        if not os.path.exists(os.path.join(SCRIPT_DIR, "storage.json")):
            print("Error: 'storage.json' file does not exist.")
            return

        storage = read_json_file("storage.json")
        items = storage.get("items", [])
        cats = storage.get("cats", [])

        for cate in cats:
            if cate == cat:
                cats.remove(cat)

        updated = False
        for item in items:
            if "category" in item and item["category"] == cat:
                item["category"] = 'None'
                updated = True

        if updated:
            write_json_file("storage.json", storage)
            print(f"All items with category '{cat}' have been updated to 'None'.")
        else:
            print(f"No items found with category '{cat}'.")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main___":
    import doctest
    doctest.testmod()
