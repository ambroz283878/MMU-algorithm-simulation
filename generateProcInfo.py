import memory
import json
procInfo = memory.generateReferences(
    totalPages=100,
    workingSetSize=8,
    nRefs=500,
)
path="procInfo.json"
with open(path, "w") as file:
    json.dump(procInfo,file)