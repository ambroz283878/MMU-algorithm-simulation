import memory
import json

path="procInfo.json"
with open(path, "r") as file:
    procInfo=json.load(file)

ramSize = procInfo["workingSetSize"]
pageNum = procInfo["totalPages"]
nRefs = procInfo["nRefs"]
refs = procInfo["references"]

vram = memory.VRAM()
drive = memory.HardDrive(ramSize,memory.generatePages(pageNum), refs)

memoryManagementUnit=memory.MMU(vram,drive)

memoryManagementUnit.run()