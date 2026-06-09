import memory
import json
procInfo = memory.generateReferences(
    totalPages=50,
    workingSetSize=16,
    nRefs=5000,
)
path="procInfo.json"
with open(path, "w") as file:
    json.dump(procInfo,file)