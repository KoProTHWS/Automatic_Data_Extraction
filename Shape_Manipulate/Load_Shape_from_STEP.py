from OCC.Core.XCAFDoc import (
    XCAFDoc_DocumentTool_ShapeTool,
    XCAFDoc_DocumentTool_ColorTool,
    XCAFDoc_DocumentTool_MaterialTool,
    XCAFDoc_DocumentTool_DimTolTool,
    XCAFDoc_DocumentTool_LayerTool
)
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.STEPCAFControl import STEPCAFControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TDF import TDF_LabelSequence
from OCC.Core.TopoDS import TopoDS_Shape


class LoadShapeFromStep:

    def __init__(self, filename):
        self.filename = filename
        self.createStepControlReader()

    def createStepControlReader(self):
        # create a handle to a document
        doc = TDocStd_Document(TCollection_ExtendedString("pythonocc-doc"))

        shape_tool = XCAFDoc_DocumentTool_ShapeTool(doc.Main())


        # XCAFDoc_DocumentTool_ColorTool is used to manipulate color data from the XCAF document
        color_tool = XCAFDoc_DocumentTool_ColorTool(doc.Main())


        # XCAFDoc_DocumentTool_MaterialTool is used to manipulate material/ physical data (density, centerofgravity, etc)
        material_tool = XCAFDoc_DocumentTool_MaterialTool(doc.Main()) ## move this out

        dimension_tool = XCAFDoc_DocumentTool_DimTolTool(doc.Main())


        step_reader = STEPCAFControl_Reader()
        step_reader.SetColorMode(True)
        step_reader.SetLayerMode(True)
        step_reader.SetNameMode(True)
        step_reader.SetMatMode(True)
        step_reader.SetGDTMode(True)

        ########## Read STEP file ##########
        status = step_reader.ReadFile(self.filename)

        if status == IFSelect_RetDone:
            step_reader.Transfer(doc)

        #Label of entire assembly
        labels = TDF_LabelSequence()
        shape_tool.GetFreeShapes(labels) # In this use case- free shape is basically the entire assembly.


        print(len(labels))
        lab = labels.Value(1)
        name = lab.GetLabelName()
        print("Name of Full Assembly :", name)
        shape = shape_tool.GetShape(lab)

        if shape:
            print(f"Shape entity '{name}' successfully loaded from STEP file")
            self.shape = TopoDS_Shape(shape)

        else:
            print("No shape found within STEP file")
            exit()


    def getShape(self):
        return self.shape
   
