import json
from datetime import datetime
import os


# Utility function to read and write JSON data to the file
def read_json_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def write_json_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def createID():
    storage = read_json_file('storage.json')
    ids = [item['id'] for item in storage["items"]]
    ids.sort()
    return ids[-1] + 1 if ids else 1  # Return 1 if the list is empty


def addToJSON(id: int, name: str, date: str, category: str = ''):
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
    storage = read_json_file('storage.json')
    items = storage["items"]
    storage["items"] = [item for item in items if item["id"] != id]
    write_json_file('storage.json', storage)


def editJSONItem(id: int, name: str, date: str, category: str = ''):
    removeFromJSON(id)  # Remove the item first
    addToJSON(id, name, date, category)  # Add the new item


def resetJSON():
    # Create an empty "items" list.
    empty_data = {
        "items": []
    }
    write_json_file('storage.json', empty_data)
    print("JSON file has been reset to an empty state.")


def sortByDate(): 
    try:
        # Check if the file exists
        if not os.path.exists("storage.json"):
            print("Error: 'storage.json' file does not exist. Make sure it's in the same directory.")
            return

        data = read_json_file("storage.json")
        if "items" in data and isinstance(data["items"], list):
            # Sort items by date
            data["items"].sort(key=lambda x: datetime.strptime(x["date"], "%m/%d/%Y"))

            # Write the sorted data to a new file
            write_json_file("sorted_storage.json", data)
            print("Sorted data has been written to 'sorted_storage.json'.")
        else:
            print("Error: 'items' key is missing or not a list.")
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def sortByCategoryAndDate():
    try:
        # Check if the file exists
        if not os.path.exists("storage.json"):
            print("Error: 'storage.json' file does not exist. Make sure it's in the same directory.")
            return

        data = read_json_file("storage.json")
        if "items" in data and isinstance(data["items"], list):
            # Sort by category first, then by date
            data["items"].sort(key=lambda x: (x["category"], datetime.strptime(x["date"], "%m/%d/%Y")))

            # Write the sorted data to a new file
            write_json_file("sorted_storage.json", data)
            print("Sorted data has been written to 'sorted_storage.json'.")
        else:
            print("Error: 'items' key is missing or not a list.")
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
