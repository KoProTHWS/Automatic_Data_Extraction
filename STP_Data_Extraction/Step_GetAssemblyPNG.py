from OCC.Display.SimpleGui import init_display
from OCC.Core.Aspect import  Aspect_GFM_VER
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_SOLID
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TDocStd import TDocStd_Document

from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.XCAFDoc import XCAFDoc_ColorGen
from OCC.Core.TDF import TDF_LabelSequence, TDF_ChildIDIterator
from OCC.Core.XCAFApp import XCAFApp_Application
from OCC.Core.STEPCAFControl import STEPCAFControl_Writer
from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.TDataStd import TDataStd_Name
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.XCAFDoc import (
    XCAFDoc_DocumentTool_ShapeTool,
    XCAFDoc_DocumentTool_ColorTool,
    XCAFDoc_DocumentTool_LayerTool,
    XCAFDoc_DocumentTool_MaterialTool
)
class GetAssemblyPNG:

    def __init__(self, shape):
        self.shape = shape
        self.setup_display()  
        self.create_explorer() 

    def setup_display(self):

        self.display, self.start_display, _, _ = init_display()
        # Set background to solid white
        self.display.set_bg_gradient_color([255, 255, 255], [255, 255, 255], Aspect_GFM_VER)

    def create_explorer(self):
        top_exp = TopExp_Explorer()
        top_exp.Init(self.shape, TopAbs_SOLID)
        self.occ_seq = []

        while top_exp.More():
            item = top_exp.Current()
            self.occ_seq.append(item)
            # print('lenexp', len(self.occ_seq))
            top_exp.Next()


    def saveAssemblySequenzToPNG(self, filename, color):

        self.display.EraseAll()
        for i in range(len(self.occ_seq)):
            
            # display.DisplayShape(self.occ_seq[i], update=True, color=206, transparency=0.35)
            self.display.DisplayShape(self.occ_seq[i], update=True, color=color[i], transparency=0.35)
            self.display.ExportToImage(filename+"Assembly_step_"+ str(i)+".png")
        
        # print total no of sub-assmebly images saved
        print( f'Saved "{len(self.occ_seq)}" sub-assembly images in PNG format')

    def SaveAssemblyPartsToPNG(self, filename, color):
        
        for i in range(len(self.occ_seq)):
            self.display.EraseAll()
            
            # display.DisplayShape(self.occ_seq[i], color=206, update=True)
            self.display.DisplayShape(self.occ_seq[i], update=True, color=color[i], transparency=0.35)
            self.display.ExportToImage(filename+"Parts_"+ str(i)+".png")

        print( f'Saved "{len(self.occ_seq)}" individual component images in PNG format')

    def Export_Step_File(self, filename, color):
        #Colors are not retained. Approach to do it is not straightforward

        for i in range(len(self.occ_seq)):
            # Export to STEP file
            self.display.DisplayShape(self.occ_seq[i], color=color[i], update=True)
            step_writer = STEPControl_Writer()
            Interface_Static_SetCVal("write.step.schema", "AP242DIS")
 
            step_writer.Transfer(self.occ_seq[i], STEPControl_AsIs)
            step_writer.Write(filename+"part_"+ str(i)+".stp")

        print( f'Saved "{len(self.occ_seq)}" individual component images in STEP format')          

