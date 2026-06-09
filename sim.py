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

mode = input("Wybierz algorytm (FIFO/LRU/random)")
if mode not in ["FIFO","LRU","random"]:
    print(f"Nieznany algorytm ({mode})")
    exit
match mode:
    case "FIFO":
        memoryManagementUnit=memory.FIFO(vram,drive)
    case "LRU":
        memoryManagementUnit=memory.LRU(vram,drive)
    case "random":
        memoryManagementUnit=memory.MMU(vram,drive)

memoryManagementUnit.run()