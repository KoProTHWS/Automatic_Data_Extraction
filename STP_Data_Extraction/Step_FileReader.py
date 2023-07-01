from OCC.Core.STEPControl import STEPControl_Reader

class StepFileReader:


    def __init__(self, filename):
        self.filename = filename
        self.createStepControlReader()
        

    def createStepControlReader(self):
        self.step_reader = STEPControl_Reader()
        self.step_reader.ReadFile(self.filename)
        self.step_reader.TransferRoot()
        self.shape = self.step_reader.Shape()

    def getShape(self):
        return self.shape
