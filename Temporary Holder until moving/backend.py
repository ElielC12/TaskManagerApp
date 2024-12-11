import json
from datetime import datetime
import os

# Get the directory of the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Utility function to read and write JSON data to the file
def read_json_file(filename):
    filepath = os.path.join(SCRIPT_DIR, filename)
    with open(filepath, 'r') as file:
        return json.load(file)


def write_json_file(filename, data):
    filepath = os.path.join(SCRIPT_DIR, filename)
    with open(filepath, 'w') as file:
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
        if not os.path.exists(os.path.join(SCRIPT_DIR, "storage.json")):
            print("Error: 'storage.json' file does not exist. Make sure it's in the same directory.")
            return

        data = read_json_file("storage.json")
        if "items" in data and isinstance(data["items"], list):
            # Sort items by date
            data["items"].sort(key=lambda x: datetime.strptime(x["date"], "%m/%d/%Y"))

            # Write the sorted data to a new file
            write_json_file("storage.json", data)
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
        if not os.path.exists(os.path.join(SCRIPT_DIR, "storage.json")):
            print("Error: 'storage.json' file does not exist. Make sure it's in the same directory.")
            return

        data = read_json_file("storage.json")
        if "items" in data and isinstance(data["items"], list):
            # Sort by category first, then by date
            data["items"].sort(key=lambda x: (x["category"], datetime.strptime(x["date"], "%m/%d/%Y")))

            # Write the sorted data to a new file
            write_json_file("storage.json", data)
            print("Sorted data has been written to 'sorted_storage.json'.")
        else:
            print("Error: 'items' key is missing or not a list.")
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def getInfo(id: int):
    try:
        # Check if the file exists
        if not os.path.exists(os.path.join(SCRIPT_DIR, "storage.json")):
            print("Error: 'storage.json' file does not exist. Make sure it's in the same directory.")
            return

        # Read the JSON data
        data = read_json_file("storage.json")
        # print("JSON data loaded:", data)  # Debug: Print loaded data
        items = data.get("items", [])
        # print("Items in JSON:", items)  # Debug: Print items list
        item_list = []

        # Find the item with the specified ID
        for item in items:
            # print("Checking item:", item)  # Debug: Print each item being checked
            if item["id"] == id:
                # print("Item found:", item)  # Debug: Print the found item
                item_list.append(item)
                print(item_list)
                return item_list # Return the matching item's details

        # If the item is not found, return None
        print(f"No item found with ID: {id}")
        return None

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def removeCategory(cat: str):
    """
    Remove a specific category from all items in the JSON file.
    For all items with the specified category, change their category to 'None'.
    """
    try:
        # Check if the file exists
        if not os.path.exists(os.path.join(SCRIPT_DIR, "storage.json")):
            print("Error: 'storage.json' file does not exist. Make sure it's in the same directory.")
            return

        # Read the JSON data
        storage = read_json_file("storage.json")
        items = storage.get("items", [])

        # Update the category to 'None' for all matching items
        updated = False
        for item in items:
            if "category" in item and item["category"] == cat:
                item["category"] = 'None'
                updated = True

        if updated:
            # Write the updated data back to the JSON file
            write_json_file("storage.json", storage)
            print(f"All items with category '{cat}' have been updated to 'None'.")
        else:
            print(f"No items found with category '{cat}'.")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    # removeCategory("Calculus")
    pass
