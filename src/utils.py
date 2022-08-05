import json
import yaml

def readJson(path='userData.json'):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def addData(user, path='userData.json'):
    with open(path, 'r+') as file:
        data = json.load(file)
        data.update(user)
        file.seek(0)
        json.dump(data, file)

def writeJson(data, path):
    with open(path, 'w') as file:
        json.dump(data, file)

def getConfig(yaml_file='./config.yml'):
    with open(yaml_file, 'r') as f:
        cfgs = yaml.load(f, Loader=yaml.FullLoader)
    return cfgs

def readJsonByRole(role, path='userData.json'):
    allData = readJson(path)
    data = {}
    for d in allData:
        if allData[d].split('/')[0] == role:
            data.update({d: allData[d]})
    return data

def getClassName(c):
    c += 1
    if c == 1:
        return "Nam ngua duoi tay chan"
    elif c == 2:
        return "Nam ngua vat tay len bung"
    elif c == 3:
        return "Nam ngua vat tay len dau"
    elif c == 4:
        return "Nam ngua co chan trai"
    elif c == 5:
        return "Nam ngua co chan phai"
    elif c == 6:
        return "Nam ngua co bep 2 chan"
    elif c == 7:
        return "Nam ngua dung 2 chan"
    elif c == 8:
        return "Nam ngua vat chan sang trai"
    elif c == 9:
        return "Nam ngua vat chan sang phai"
    elif c == 10:
        return "Nam nghieng trai duoi 2 chan"
    elif c == 11:
        return "Nam nghieng trai co 1 chan"
    elif c == 12:
        return "Nam nghieng trai co 2 chan"
    elif c == 13:
        return "Nam nghieng trai co 1 chan, cuon nguoi"
    elif c == 14:
        return "Nam nghieng trai duoi 2 chan gan sap nguoi"
    elif c == 15:
        return "Nam nghieng phai duoi 2 chan"
    elif c == 16:
        return "Nam nghieng phai co 1 chan"
    elif c == 17:
        return "Nam nghieng phai co 2 chan"
    elif c == 18:
        return "Nam nghieng phai co 1 chan, cuon nguoi"
    elif c == 19:
        return "Nam nghieng phai duoi 2 chan gan sap nguoi"
    elif c == 20:
        return "Nam sap duoi 2 chan"
    elif c == 21:
        return "Nam sap co 1 chan trai"
    elif c == 22:
        return "Nam sap co 1 chan phai"
    elif c == 23:
        return "Nam sap co 2 chan"

def updateJsonByKey(key, value, path):
    data = readJson(path)
    data[key] = value
    writeJson(data, path)

if __name__ == '__main__':
    # print(getClassName(0))
    # nurses = readJsonByRole('nurse', 'userData.json')
    # updateJsonByKey('nurse1', '123', 'nurseData.json')
    
    pass