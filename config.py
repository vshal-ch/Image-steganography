class configs:
    def __init__(self):
        self.NO_OF_BITS = 10
        self.outputpath = 'stegimage'
        self.NO_OF_SIZE_BITS = 24
        self.NO_OF_SIZE_PIXELS = 8
        self.BASE_RES = 1920*1080
        self.NO_OF_IMG_PIXELS = 4
    def getoutputpath(self):
        return self.outputpath
    def setoutputpath(self,outputpath):
        self.outputpath = outputpath
    
config = configs()
