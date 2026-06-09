import random

def generateReferences(
    totalPages: int=50,       # number of pages used by a process
    workingSetSize:int=4,   # number of pages working at once - same as VRAM.size
    nRefs: int=300,     # total number of page refferences
    localityWeight:float=0.75,  # chance of reference to a page in working set
    spatialWeight: float=0.1,  # chance of reference to a page near outside of working set
    shiftEvery: int=50,       # how many refs before working set shifts
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
        self.arrivalTime = 0
        self.accessCount = 0
        self.mostRecentAccess = 0
    def reset(self):
        self.arrivalTime = 0
        self.accessCount = 0
        self.mostRecentAccess = 0
    def updateData(self, counter):
        self.arrivalTime = counter
        self.accessCount += 1
        self.mostRecentAccess = counter
    def updateAccessTime(self, counter):
        self.mostRecentAccess = counter

class VRAM():
    def __init__(self,size: int = 16):
        self.size = size # max amount of pages loaded at once
        self.pages = [None]*self.size # array of pages
    def findPageByID(self,id):
        for i in range(len(self.pages)):
            try:
                if self.pages[i].page_number==id:
                    return i
            except AttributeError:
                pass
        return None

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
        self.counter = 0

    def pageCheckOK(self, pageID):
        for page in self.vram.pages:
            if page is not None and pageID == page.page_number: 
                return True # if page is loaded into memory, page check OK  
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
        if self.vram.pages[index] is not None:
            self.vram.pages[index].reset()
            self.vram.pages[index]=None
        return index

    def loadPage(self, pageID, mode):
        if mode == "LOAD":
            index = self.pageToRemove()
            self.vram.pages[index] = self.disk.processPages[pageID]
            self.vram.pages[index].updateData(self.counter)
        else:
            index = self.vram.findPageByID(pageID)
            if index is not None:
                self.vram.pages[index].updateAccessTime(self.counter)
            else:
                return None
        return index

    def run(self):
        while self.counter < self.disk.nProc:
            pageID = self.disk.pageRefferences[self.counter]
            if not self.pageCheckOK(pageID):
                print(f"""Frame {self.removePage()} released""")
                frameID=self.loadPage(pageID, "LOAD")
            else:
                frameID=self.loadPage(pageID,"UPDATE")
            print(f"""Loaded Page {pageID} into frame {frameID}""")
            self.counter +=1
            if frameID is not None:
                self.vram.pages[frameID].updateAccessTime(self.counter)
        print(f"---\nPage fault count: {self.pageFaultCount}")

class FIFO(MMU):
    def __init__(self, vram: VRAM, drive: HardDrive):
        super().__init__(vram,drive)
    def pageToRemove(self):
        arrivalTimes = {}
        for page in self.vram.pages:
            if page is None:
                return self.vram.pages.index(page)
            arrivalTimes.update({page.arrivalTime : page})
        try:
            return self.vram.pages.index(arrivalTimes[min(arrivalTimes.keys())])
        except ValueError:
            return 0

class LRU(MMU):
    def __init__(self, vram: VRAM, drive: HardDrive):
        super().__init__(vram,drive)
    def pageToRemove(self):
        recentAccessTimes = {}
        for page in self.vram.pages:
            if page is None:
                return self.vram.pages.index(page)
            recentAccessTimes.update({page.mostRecentAccess : page})
        try:
            return self.vram.pages.index(recentAccessTimes[min(recentAccessTimes.keys())])
        except ValueError:
            return 0
    