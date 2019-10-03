# coding:utf-8 -*-

import copy
import numpy as np
import random
import os
import sys
sys.setrecursionlimit(5**10)  # set the maximum depth as 5的10次方

origin =[
        ["1", "1", "1", "1", "1"],
        ["1", "4", "2", "2", "1"],
        ["1", "5", "2", "2", "1"],
        ["1", "0", "0", "11", "1"],
        ["1", "-1", "-1", "1", "1"]
    ]

dirMap = {
        "u": {"i": -1, "j": 0},
        "r": {"i": 0, "j": 1},
        "d": {"i": 1, "j": 0},
        "l": {"i": 0, "j": -1},
    }

file_path = "files/"

def read_data(file):
    data = []
    with open(file, "rt") as f:
        index = 1
        for line in f:
            if index == 1:
                index += 1
                continue
            else:
                item = line.split("\n")[0].split(",")
                item.remove("")
                data.append(item)
            index += 1
    data = np.array(data)
    return data

def get_origin_state():
    file_list = os.listdir(file_path)
    file_json = {}
    for i in range(0, len(file_list)):
        print(str(i)+ ": "+ file_list[i])
        file_json[i] = file_list[i]
    number = input("please select the number of file :")
    try:
        number = int(number)
        if number > len(file_list):
            print("invalid number")
            return False
    except Exception,e:
        print("invalid number")
        return False
    filename = file_json[number]
    if not "txt" in filename:
        filename += ".txt"
    if not os.path.exists(file_path + filename):
        print("file not existed!")
        return False
    else:
        data = read_data(file_path+filename)
        return data

def printMatrix():
    filename = input("please input file name:")
    if not "txt" in filename:
        filename += ".txt"
    if not os.path.exists(file_path + filename):
        print("file not existed!")
        return False
    else:
        with open(file_path+filename, "rt") as f:
            index = 1
            for line in f:
                if index > 2:
                    line = line.replace("\n","")
                print(line)
                index += 1

class MoveAction():
    def __init__(self, key, blockMap):
        self.key = key
        self.blockMap = blockMap

    def move(self, action):
        relation = {"u": "up", "d": "down", "l": "left", "r": "right"}
        action_true = relation.get(action, "")
        if action_true:
            return eval("self."+action_true)()
        else:
            print("actio_invalid")
    
    def up(self):
        return moveBlock(self.key, self.blockMap, dirMap["u"])

    def down(self):
        return moveBlock(self.key, self.blockMap, dirMap["d"])

    def left(self):
        return moveBlock(self.key, self.blockMap, dirMap["l"])

    def right(self):
        return moveBlock(self.key, self.blockMap, dirMap["r"])

def deepClone(target):
    return copy.deepcopy(target)

def getStateFillBy(char, origin):
    state = deepClone(origin)
    h = len(state)
    w = len(state[0])
    for i in range(1, h-1):
        for j in range(1, w-1):
            state[i][j] = char
    return state

def getBlock(row, col, state):
    if not  state[row][col] in  ["1","0"]:
        data = []
        for i in range(0,len(state)):
            for j in range(0, len(state[0])):
                if state[i][j] == state[row][col]:
                    data.append({"i": i, "j": j})
        return data
    else:
        return []

def getBlockMapByState(state):
    blockMap = {}
    h = len(state)
    w = len(state[0])
    flagState = getStateFillBy("*", state)
    for i in range(len(flagState)):
        for j in range(len(flagState[0])):
            if flagState[i][j] == "-1":
                flagState[i][j] = "*"
    for i in range(0, h):
        for j in range(0, w):
            cell = state[i][j]
            block = getBlock(i, j, state)
            if len(block) and cell != "0":
                blockMap[cell] = block
    blockMap["w"] = w
    blockMap["h"] = h
    return blockMap

def getBoard(blockMap):
    origin = deepClone([["1"]*blockMap['w'] for i in range(0,blockMap['h'])])
    # origin = deepClone(list(np.ones((blockMap['h'], blockMap['w']))))
    if blockMap.get("-1"):
        for p in blockMap["-1"]:
            i = p["i"]
            j = p["j"]
            origin[i][j] = "-1"
    return origin

def getStateByBlockMap(blockMap):
    state = getStateFillBy("0", getBoard(blockMap))
    for key in blockMap.keys():
        if key in ["w", "h", "-1", "parent"]:
            continue
        block = blockMap[key]
        for p in block:
            i = p["i"]
            j = p["j"]
            state[i][j] = key
    return state

def isSuccess(blockMap):
    state = getStateByBlockMap(blockMap)
    for item in state:
        if "-1" in item:
            return False
    return True

def getNormalState(bMap):
    state = getStateByBlockMap(bMap)
    map = {}
    idx = 0
    for row in state:
        for j in row:
            index = row.index(j)
            cell = row[index]
            if not map.get(cell):
                map[cell] = idx
                idx += 1
            row[index] = str(map[cell]) + ""
    return state

def isIdentical(bMap1, bMap2):
    state1= getNormalState(bMap1)
    state2 = getNormalState(bMap2)
    for i in range(0, len(state1)):
        for j in range(0, len(state1[0])):
            if state1[i][j] != state2[i][j]:
                return False
    return True

def isRepeatRoad(blockMap, road):
    for bMapIt in road:
        if isIdentical(bMapIt, blockMap):
            return True
    return False

def validMove(blockMap):
    state = getStateFillBy("0", getBoard(blockMap))
    for key in blockMap.keys():
        if key in ["w","h","-1","parent"]:
            continue
        block = blockMap[key]
        for p in block:
            i = p["i"]
            j = p["j"]
            cell = state[i][j]
            if cell != "0" and not (key == "2" and cell == "-1"):
                return False
            else:
                state[i][j] = key
    return True

def moveBlock(key, blockMap, d):
    block = blockMap[key]
    for item in block:
        item["i"] += d["i"]
        item["j"] += d["j"]
    return blockMap

def moveDSF(blockMap, road, limit = float("inf")):
    if isRepeatRoad(blockMap, road) or len(road) >= limit:
        return {"succeed": False, "road": road}
    if isRepeatRoad(blockMap, road):
        return {"succeed": False, "road": road}
    road.append(blockMap)
    if isSuccess(blockMap):
        return {"succeed": True, "road": road}
    newBlockMap = None
    for key in blockMap.keys():
        if key in ["w","h","-1","parent"]:
            continue
        # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["u"])
        newBlockMap = MoveAction(key,deepClone(blockMap)).move("u")
        if validMove(newBlockMap):
            res = moveDSF(newBlockMap, deepClone(road), limit)
            if res["succeed"]:
                return res
        
        # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["r"])
        newBlockMap = MoveAction(key,deepClone(blockMap)).move("r")
        if validMove(newBlockMap):
            res = moveDSF(newBlockMap, deepClone(road), limit)
            if res["succeed"]:
                return res

        # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["d"])
        newBlockMap = MoveAction(key,deepClone(blockMap)).move("d")
        if validMove(newBlockMap):
            res = moveDSF(newBlockMap, deepClone(road), limit)
            if res["succeed"]:
                return res

        # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["l"])
        newBlockMap = MoveAction(key,deepClone(blockMap)).move("l")
        if validMove(newBlockMap):
            res = moveDSF(newBlockMap, deepClone(road), limit)
            if res["succeed"]:
                return res
    return {"succeed": False, "road": road}

def moveBSF(parents):
    def getList(value):
        item_list = []
        item_list.append(value)
        while value.get("parent"):
            value = value["parent"]
            item_list.append(value) 
        return item_list
    while len(parents):
        move_list = []
        for blockMap in parents:
            newBlockMap = None
            for key in blockMap.keys():
                if key in ["w","h","-1","parent"]:
                    continue
                # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["u"])
                newBlockMap = MoveAction(key,deepClone(blockMap)).move("u")
                if validMove(newBlockMap):
                    move_list.append(newBlockMap)
                    newBlockMap["parent"] = blockMap
                    if isSuccess(newBlockMap):
                        return getList(newBlockMap).reverse()
                
                # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["r"])]
                newBlockMap = MoveAction(key,deepClone(blockMap)).move("r")
                if validMove(newBlockMap):
                    move_list.append(newBlockMap)
                    newBlockMap["parent"] = blockMap
                    if isSuccess(newBlockMap):
                        return getList(newBlockMap).reverse()

                # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["d"])
                newBlockMap = MoveAction(key,deepClone(blockMap)).move("d")
                if validMove(newBlockMap):
                    move_list.append(newBlockMap)
                    newBlockMap["parent"] = blockMap
                    if isSuccess(newBlockMap):
                        return getList(newBlockMap).reverse()

                # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["l"])
                newBlockMap = MoveAction(key,deepClone(blockMap)).move("l")
                if validMove(newBlockMap):
                    move_list.append(newBlockMap)
                    newBlockMap["parent"] = blockMap
                    if isSuccess(newBlockMap):
                        return getList(newBlockMap).reverse()
            parents = move_list
    return []
               
def getAvailableMoves(blockMap):
    move_list = []
    newBlockMap = None
    for key in blockMap.keys():
        if key in ["w","h","-1","parent"]:
            continue
        # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["u"])
        newBlockMap = MoveAction(key,deepClone(blockMap)).move("u")
        if validMove(newBlockMap):
            move_list.append(newBlockMap)

        # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["r"])
        newBlockMap = MoveAction(key,deepClone(blockMap)).move("r")
        if validMove(newBlockMap):
            move_list.append(newBlockMap)

        # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["d"])
        newBlockMap = MoveAction(key,deepClone(blockMap)).move("d")
        if validMove(newBlockMap):
            move_list.append(newBlockMap)

        # newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["l"])
        newBlockMap = MoveAction(key,deepClone(blockMap)).move("l")
        if validMove(newBlockMap):
            move_list.append(newBlockMap)
    return move_list

def randomStep(blockMap):
    availableMoves = getAvailableMoves(blockMap)
    index =  random.randint(0,len(availableMoves)-1)
    return availableMoves[index]

def moveRandom(count, state):
    road = []
    newBlockMap = getBlockMapByState(state)
    for i in range(0, count):
        newBlockMap = randomStep(newBlockMap)
        road.append(newBlockMap)
        if isSuccess(newBlockMap):
            return road
    return road

def moveIDS(blockMap):
    limit = 4
    while True:
        res = moveDSF(blockMap, [], limit)
        if res["succeed"]:
            return res
        limit += 1
    return {"succeed": True, "road": []}

def print_matrix(data):
    print(np.array(data))

def write_file(data, flag=False):
    if not flag:
        with open("output-hw1.txt", "a+") as f:
            f.write(data)
    else:
        with open("output-hw1.txt", "a+") as f:
            for row in data:
                f.write("                 " + ",".join(row) + "\n")

if __name__ == "__main__":
    data = get_origin_state()
    if data != False:
        print("begin....")
        write_file("\n\nbegin....\n")
        write_file("origin state is ....\n")
        print_matrix(data)
        write_file(data, True)
        methods = ["moveRandom","moveDSF","moveIDS"]
        print("methods as: ")
        for i in range(0, len(methods)):
            print(str(i)+ ": "+ methods[i])
        method = input("please select the method:")

        if methods[method] == "moveIDS":
            print("IDS is doing.....")
            write_file("method is IDS:  \n")
            res = moveIDS(getBlockMapByState(data))
            if res["succeed"]:
                index = 1
                for road in res["road"]:
                    print("step:", index)
                    write_file("step: "+ str(index) + "\n")
                    print_matrix(getStateByBlockMap(road))
                    write_file(getStateByBlockMap(road), True)
                    index += 1
            else:
                write_file("IDS failed")
        elif methods[method] == "moveDSF":
            print("DSF is doing....")
            write_file("method is DSF:  \n")
            res = moveDSF(getBlockMapByState(data), [])
            if res["succeed"]:
                index = 1
                for road in res["road"]:
                    print("step:", index)
                    write_file("step: "+ str(index) + "\n")
                    print_matrix(getStateByBlockMap(road))
                    write_file(getStateByBlockMap(road), True)
                    index += 1
            else:
                write_file("DSF failed")
        elif methods[method] == "moveRandom":
            print("random walk is doing....")
            write_file("method is random walk:  \n")
            step = input("please input random walk step:")
            write_file("random walk step is: "+ str(step) + "\n")
            roads = moveRandom(step, origin)
            index = 1
            for road in roads:
                print("step:", index)
                write_file("step: "+ str(index))
                print_matrix(getStateByBlockMap(road))
                write_file(getStateByBlockMap(road), True)
                index += 1
