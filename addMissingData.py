import json
import requests

CORRECT_DATA_FILE = "buildingsFixed.json"
#WRONG_DATA_FILE = "response_1587582776888.json"
SOURCE_URL = 'https://uci-tippers.ics.uci.edu/api/entity/'
DEST_URL = 'https://uci-tippers.ics.uci.edu/api/entity/'

COORDINATE_SYSTEM = 'cartesian2hfd'
EXTENT_CLASS = 'polygon'

def main():
    with open(CORRECT_DATA_FILE) as inF:
        correctData = json.load(inF)
    
    incompleteData = requests.get(SOURCE_URL).json()
        
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
    
    for datum in incompleteData:
        if datum["entityTypeId"] == 5 and datum["payload"]["geo"]["extent"] == None and datum["name"] in correctVertecies.keys():
            newElement = datum
            id = datum["id"]
            del newElement["id"]
            del newElement["entityClassName"]
            del newElement["entityClassId"]
            del newElement["entityTypeName"]
            newElement["payload"]["geo"]["extent"] = {"verticies": correctVertecies[datum["name"]], "extentClassName":EXTENT_CLASS}
            newElement["payload"]["geo"]["coordinateSystem"] = {"coordinateSystemClassName": COORDINATE_SYSTEM}
            
            print(id)
            print(requests.put(DEST_URL+str(id), json=newElement))
        

if __name__ == '__main__':
    main()
