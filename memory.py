import numpy

class Page():
    def __init__(self, page_number: int):
        self.page_number = page_number
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

class MMU():
    def __init__(self):
        self.vram = VRAM()
        self.disk = HardDrive()
    def pageCheckOK(self, pageID):
        for page in self.vram.pages:
            if pageID == page.page_number: return True # if page is loaded into memory, page check OK
        return False # else - page fault
    def pageToRemove(self): # select page to free from memory
        for i in range(len(self.vram.pages)):
            if self.vram.pages[i] == None:
                return i # by default return address of the first empty memory segment
        else: return numpy.random.randint(self.vram.size-1) # if no segments are empty, return random address
    def removePage(self):
        pass
    def loadPage(self):
        pass