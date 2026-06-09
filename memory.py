import random

def generateReferences(
    totalPages: int=20,       # number of pages used by a process
    workingSetSize:int=4,   # number of pages working at once - same as VRAM.size
    nRefs: int=100,     # total number of page refferences
    localityWeight:float=0.7,  # chance of reference to a page in working set
    spatialWeight: float=0.15,  # chance of reference to a page outside of working set
    shiftEvery: int=20,       # how many refs before working set shifts
):
    working_set = random.sample(range(totalPages), workingSetSize)
    references = []
    last_page = working_set[0]

    for i in range(nRefs):
        if i > 0 and i % shiftEvery == 0:
            keep = random.sample(working_set, workingSetSize // 2)
            new_pages = random.sample(
                [p for p in range(totalPages) if p not in keep],
                workingSetSize - len(keep)
            )
            working_set = keep + new_pages

        roll = random.random()

        if roll < localityWeight:
            page = random.choice(working_set) # choose a page from working set
        elif roll < localityWeight + spatialWeight:
            offset = random.choice([-1, 1]) # choose a page near the last used page
            page = max(0, min(totalPages - 1, last_page + offset)) # min() to prevent indexError
        else:
            page = random.randint(0, totalPages - 1) # chose a random page

        references.append(page)
        last_page = page

    procInfo={"totalPages":totalPages,
              "workingSetSize":workingSetSize,
              "nRefs":nRefs,
              "references": references,
              "localityWeight":localityWeight,
              "spatialWeight":spatialWeight,
              "shiftEvery":shiftEvery}
    return procInfo

def generatePages(n: int=20):
    return [Page(i) for i in range(n)]

class Page():
    def __init__(self, page_number: int):
        self.page_number = page_number
        self.arrivalTime = None
        self.accessCount = 0
        self.mostRecentAccess = None
    def reset(self):
        self.arrivalTime = None
        self.accessCount = 0
        self.mostRecentAccess = None
    def updateData(self, counter):
        self.arrivalTime = counter
        self.accessCount += 1
        self.mostRecentAccess = counter

class VRAM():
    def __init__(self,size: int = 16):
        self.size = size # max amount of pages loaded at once
        self.pages = [None]*self.size # array of pages

class HardDrive():
    def __init__(self, requiredMem: int, pages: list, refs: list):
        self.requiredMemory = requiredMem
        self.processPages = pages
        self.pageRefferences = refs
        self.nProc = len(self.pageRefferences)

class MMU():
    def __init__(self, vram: VRAM, drive: HardDrive):
        self.vram = vram
        self.disk = drive
        self.pageFaultCount = 0

    def pageCheckOK(self, pageID):
        for page in self.vram.pages:
            if page == None:
                return True
            elif pageID == page.page_number: return True # if page is loaded into memory, page check OK
        # else - page fault
        self.pageFaultCount += 1
        return False

    def pageToRemove(self): # select frame to free from memory
        for i in range(len(self.vram.pages)):
            if self.vram.pages[i] == None:
                return i # by default return address of the first empty memory frame
        else: return random.randint(0,self.vram.size-1) # if no frames are empty, return random address

    def removePage(self):
        index = self.pageToRemove()
        self.vram.pages[index].reset()
        self.vram.pages[index]=None
        return index

    def loadPage(self, pageID):
        index = self.pageToRemove()
        self.vram.pages[index] = self.disk.processPages[pageID]
        return index

    def run(self):
        self.loadPage(self.disk.pageRefferences[0])
        counter = 0
        while counter < self.disk.nProc:
            pageID = self.disk.pageRefferences[counter]
            if not self.pageCheckOK(pageID):
                print(f"""Frame {self.removePage()} released""")
            print(f"""Loaded Page {pageID} into frame {self.loadPage(pageID)}""")
            counter +=1
        print(f"---\nPage fault count: {self.pageFaultCount}")

class FIFO(MMU):
    def __init__(self):
        super().__init__()
    def pageToRemove(self):
        arrivalTimes = {}
        [arrivalTimes.update({page.arrivalTime : page}) for page in self.vram.pages]
        return self.vram.pages.index(arrivalTimes[min(arrivalTimes.keys)])