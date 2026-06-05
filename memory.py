import numpy

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

class VRAM():
    def __init__(self,size: int = 16):
        self.size = size #max amount of pages loaded at once
        self.pages = numpy.empty(self.size, dtype=Page) #array of pages

class HardDrive():
    def __init__(self, requiredMem: int, pages: list, refs: list):
        self.requiredMemory = requiredMem
        self.processPages = pages
        self.pageRefferences = refs
        self.nProc = len(self.pageRefferences)

class MMU():
    def __init__(self):
        self.vram = VRAM()
        self.disk = HardDrive()
    def pageCheckOK(self, pageID):
        for page in self.vram.pages:
            if pageID == page.page_number: return True # if page is loaded into memory, page check OK
        return False # else - page fault
    def pageToRemove(self): # select frame to free from memory
        for i in range(len(self.vram.pages)):
            if self.vram.pages[i] == None:
                return i # by default return address of the first empty memory frame
        else: return numpy.random.randint(self.vram.size-1) # if no frames are empty, return random address
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
        counter = 0
        while counter < self.disk.nProc:
            pageID = self.disk.pageRefferences[counter]
            if not self.pageCheckOK(pageID):
                print(f"""Frame {self.removePage()} released""")
            print(f"""Loaded Page {pageID} into frame {self.loadPage(pageID)}""")
            counter +=1