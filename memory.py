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
    def pageCheckOK():
        pass