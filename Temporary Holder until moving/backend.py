import json


# with open('storage.json', 'r') as storage:
#     print(json.load(storage))

def createID():
    with open('storage.json', 'r+') as storage:
        storage = json.load(storage)
    ids = []
    for item in storage["items"]:
        ids.append(item['id'])
        ids.sort()
    return ids[-1] + 1


def addToJSON(id: int, name: str, date: str, category: str = ''):
    with open('storage.json', 'r+') as file:
        storage = json.load(file)
    items = storage["items"]
    items.append({
        "name": name,
        "date": date,
        "category": category,
        "id": id
        })
    with open('storage.json', 'w') as newfile:
        json.dump(storage, newfile, indent=4)


def removeFromJSON(id: int):
    with open('storage.json', 'r+') as file:
        storage = json.load(file)

    items = storage["items"]
    for index, obj in enumerate(items):
        if obj["id"] == id:
            items.pop(index)
    

    with open('storage.json', 'w') as newfile:
        json.dump(storage, newfile, indent=4)


def editJSONItem(id: int, name: str, date: str, category: str = ''):
    # with open('storage.json', 'r+') as file:
    #     storage = json.load(file)
    removeFromJSON(id)
    addToJSON(id, name, date, category)

def resetJSON():
    pass
