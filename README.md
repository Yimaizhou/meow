# Sliding Brick Puzzle

## Function List
* [how to start](#start)
* [moveRandom](#moveRandom)
* [moveBFS](#moveBFS)
* [moveDFS](#moveDFS)
* [moveIDS](#moveIDS)

## <a name="start">how to start</a>
* Install dependencies
```python
    pip install numpy -i https://pypi.mirrors.ustc.edu.cn/simple/
```
* * set permissions (if you are not root)
```python
     chmod 777 hw.sh
```
* Execute the hw.sh script

## <a name="moveRandom">moveRandom</a>
```python
    def moveRandom(count, state):
        road = []
        newBlockMap = getBlockMapByState(state)
        for i in range(0, count):
            newBlockMap = randomStep(newBlockMap)
            road.append(newBlockMap)
            if isSuccess(newBlockMap):
                return road
        return road
```

## <a name="moveBFS">moveBFS</a>
```python
    def moveBSF(parents):
        while len(parents):
            move_list = []
            for blockMap in parents:
                newBlockMap = None
                for key in blockMap.keys():
                    if key in ["w","h","-1","parent"]:
                        continue
                    newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["u"])
                    if validMove(newBlockMap):
                        move_list.append(newBlockMap)
                        newBlockMap["parent"] = blockMap
                        if isSuccess(newBlockMap):
                            return getList(newBlockMap).reverse()

                    newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["r"])
                    if validMove(newBlockMap):
                        move_list.append(newBlockMap)
                        newBlockMap["parent"] = blockMap
                        if isSuccess(newBlockMap):
                            return getList(newBlockMap).reverse()

                    newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["d"])
                    if validMove(newBlockMap):
                        move_list.append(newBlockMap)
                        newBlockMap["parent"] = blockMap
                        if isSuccess(newBlockMap):
                            return getList(newBlockMap).reverse()

                    newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["l"])
                    if validMove(newBlockMap):
                        move_list.append(newBlockMap)
                        newBlockMap["parent"] = blockMap
                        if isSuccess(newBlockMap):
                            return getList(newBlockMap).reverse()
                parents = move_list
        def getList(value):
            item_list = []
            item_list.append(value)
            while value.get("parent"):
                value = value["parent"]
                item_list.append(value)
            return item_list
        return []
```

## <a name="moveDFS">moveDFS</a>
```python
    def moveDSF(blockMap, road, limit = float("inf")):
        if isRepeatRoad(blockMap, road) or len(road) >= limit:
            return {"succeed": False, "road": road}
        road.append(blockMap)
        if isSuccess(blockMap):
            return {"succeed": True, "road": road}
        newBlockMap = None
        for key in blockMap.keys():
            if key in ["w","h","-1","parent"]:
                continue
            newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["u"])
            if validMove(newBlockMap):
                res = moveDSF(newBlockMap, deepClone(road), limit)
                if res["succeed"]:
                    return res

            newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["r"])
            if validMove(newBlockMap):
                res = moveDSF(newBlockMap, deepClone(road), limit)
                if res["succeed"]:
                    return res

            newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["d"])
            if validMove(newBlockMap):
                res = moveDSF(newBlockMap, deepClone(road), limit)
                if res["succeed"]:
                    return res

            newBlockMap = moveBlock(key, deepClone(blockMap), dirMap["l"])
            if validMove(newBlockMap):
                res = moveDSF(newBlockMap, deepClone(road), limit)
                if res["succeed"]:
                    return res
        return {"succeed": False, "road": road}
```

## <a name="moveIDS">moveIDS</a>
```python
    def moveIDS(blockMap):
        limit = 4
        while True:
            res = moveDSF(blockMap, [], limit)
            if res["succeed"]:
                return res
            limit += 1
        return {"succeed": True, "road": []}
```


