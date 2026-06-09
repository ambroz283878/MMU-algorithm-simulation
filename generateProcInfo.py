import memory
import json
procInfo = memory.generateReferences()
path="procInfo.json"
with open(path, "w") as file:
    json.dump(procInfo,file)