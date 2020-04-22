import json
import requests

CORRECT_DATA_FILE = "campus.json"

WRONG_DATA_FILE = "response_1587582776888.json"

DEST_URL = 'https://uci-tippers.ics.uci.edu/api/entity/'

def main():
    with open(CORRECT_DATA_FILE) as inF:
        correctData = json.load(inF)
    
    with open(WRONG_DATA_FILE) as outF:
        wrongData = json.load(outF)
        
    correctVertecies = {}
    for datum in correctData:
        if (datum["entityTypeId"] != 5):
            continue
        strVerts = datum["payload"]["geo"]["extent"]["verticies"]
        floatVerts = []
        for vert in strVerts:
            newVert = {}
            newVert["latitude"] = float(vert["latitude"])
            newVert["longitude"] = float(vert["longitude"])
            floatVerts.append(newVert)
        correctVertecies[datum["name"]] = floatVerts
    
    fixedData = []
    for building in wrongData:
        if building["name"] in correctVertecies.keys():
            newBuilding = building
            newBuilding["payload"]["geo"]["extent"]["verticies"] = correctVertecies[building["name"]]
            fixedData.append(newBuilding)
        else:
            fixedData.append(building)
    
    for datum in fixedData:
        if datum["entityTypeId"] != 5:
            continue
        newElement = datum
        id = datum["id"]
        del newElement["id"]
        del newElement["entityClassName"]
        del newElement["entityClassId"]
        del newElement["entityTypeName"]
        print(id)
        print(requests.put(DEST_URL+str(id), json=newElement))
        

if __name__ == '__main__':
    main()
