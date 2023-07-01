import os
import OCC.Core.BRepBndLib

from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.TopAbs import TopAbs_SOLID, TopAbs_SHELL, TopAbs_COMPOUND
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.StlAPI import stlapi_Read, StlAPI_Writer
from OCC.Core.BRep import BRep_Builder
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pnt2d
from OCC.Core.Bnd import Bnd_Box2d
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.IGESControl import (
    IGESControl_Controller,
    IGESControl_Reader,
    IGESControl_Writer,
)
from OCC.Core.STEPControl import (
    STEPControl_Reader,
    STEPControl_Writer,
    STEPControl_AsIs,
)
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.XCAFDoc import (
    XCAFDoc_DocumentTool_ShapeTool,
    XCAFDoc_DocumentTool_ColorTool,
    XCAFDoc_DocumentTool_MaterialTool,
    XCAFDoc_DocumentTool_LayerTool,
)
from OCC.Core.STEPCAFControl import STEPCAFControl_Reader
from OCC.Core.TDF import TDF_LabelSequence, TDF_Label, TDF_Data
from OCC.Core.TCollection import TCollection_ExtendedString, TCollection_HAsciiString
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform

from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, brepgprop_LinearProperties
from OCC.Core.GProp import GProp_GProps, GProp_Mass
from OCC.Core.GeomAPI import GeomAPI_PointsToBSplineSurface
from OCC.Core.GeomAbs import GeomAbs_C2

from OCC.Extend.ShapeFactory import measure_shape_volume



def getProperties(filename):
    """Returns list of tuples (topods_shape, label, color)
    Use OCAF.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")
    # the list:
    output_shapes = {}

    color_parts = []

    # create an handle to a document
    #TCollection_ExtendedString("pythonocc-doc")
    doc = TDocStd_Document(TCollection_ExtendedString("XDE"))

    # Get root assembly
    shape_tool = XCAFDoc_DocumentTool_ShapeTool(doc.Main())
    color_tool = XCAFDoc_DocumentTool_ColorTool(doc.Main())
    layer_tool = XCAFDoc_DocumentTool_LayerTool(doc.Main())
    mat_tool = XCAFDoc_DocumentTool_MaterialTool(doc.Main())

    step_reader = STEPCAFControl_Reader()
    step_reader.SetColorMode(True)
    step_reader.SetLayerMode(True)
    step_reader.SetNameMode(True)
    step_reader.SetMatMode(True)
    step_reader.SetGDTMode(True)
    step_reader.SetPropsMode(True)
    step_reader.SetViewMode(True)
    step_reader.SetSHUOMode(True)

    status = step_reader.ReadFile(filename)
    if status == IFSelect_RetDone:
        step_reader.Transfer(doc)

    locs = []

    mat_lab = TDF_LabelSequence()
    mat_tool.GetMaterialLabels(mat_lab)
    

    for i in range(len(mat_lab)):
        print(mat_lab.Value(i+1).GetLabelName())



    def _get_sub_shapes(lab, loc):

        
        l_subss = TDF_LabelSequence()
        shape_tool.GetSubShapes(lab, l_subss)
        # print("Nb subshapes   :", l_subss.Length())
        l_comps = TDF_LabelSequence()
        shape_tool.GetComponents(lab, l_comps)
        # print("Nb components  :", l_comps.Length())
        # print()
        
        aName =  TCollection_HAsciiString()
        aDescription = TCollection_HAsciiString()
        aDensName = TCollection_HAsciiString()
        aDensValType = TCollection_HAsciiString()

        
     
        TDF_Label()

        name = lab.GetLabelName()

        print("Name :", name)

        mat_lab = TDF_LabelSequence()
        mat_tool.GetMaterialLabels(mat_lab)
        ret = mat_tool.GetMaterial

        # print("Farben: ", ret.GetLabelName())
        #test = mat_tool.GetMaterial(lab, aName, aDescription, aDensName, aDensValType)
        
        
        print("Dichte: ", mat_tool.GetDensityForShape(lab))
        print("Sonstiges")
        print()

      

        

        if shape_tool.IsAssembly(lab):
            l_c = TDF_LabelSequence()
            shape_tool.GetComponents(lab, l_c)
           
            for i in range(l_c.Length()):
                label = l_c.Value(i + 1)
                if shape_tool.IsReference(label):
                    # print("\n########  reference label :", label)
                    label_reference = TDF_Label()
                    shape_tool.GetReferredShape(label, label_reference)
                    loc = shape_tool.GetLocation(label)
                    locs.append(loc)

                    _get_sub_shapes(label_reference, loc)

                    locs.pop()
                    

        elif shape_tool.IsSimpleShape(lab):
            # print("\n########  simpleshape label :", lab)
            shape = shape_tool.GetShape(lab)
            # print("    all ass locs   :", locs)

            props = GProp_GProps()
    
            # brepgprop_VolumeProperties(shape, props)

            brepgprop_SurfaceProperties(shape, props)
            # props.

        

            volume = props.Mass()
            
            print("Trägheitsmomente" ,props.PrincipalProperties().Moments())
            # print("Trägheitsmomente", props.MatrixOfInertia())
            print(props.PrincipalProperties())
            com = props.CentreOfMass()
            print("Volumen", volume)

            print('coordinates', com.Coord())
            box_volume = measure_shape_volume(shape)

            print('box_volume', box_volume)

            loc = TopLoc_Location()
            for l in locs:
                print("    take loc       :", l)
                loc = loc.Multiplied(l)



                

    def _get_shapes():
        labels = TDF_LabelSequence()
       
        shape_tool.GetFreeShapes(labels)
       
        for i in range(labels.Length()):

            root_item = labels.Value(i + 1)
            _get_sub_shapes(root_item, None)

    _get_shapes()
    return color_parts


from Step_FileReader import *

if __name__ == "__main__":
    #filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/fertiges_bauteil_asm_2.stp"
    # filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/test_Uhlmann.stp"
    filename = "C:/Users/Varun Kaarthik/Documents/cad_data_extraction/STP_Data_Extraction/CAD/fertiges_bauteil_asm_2.stp"

    #filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/Truck_komplett(stp)/pick-up_classic_king-size.stp"
    getProperties(filename)




    # doc = TDocStd_Document(TCollection_ExtendedString("XDE"))

    # # Get root assembly
    # shape_tool = XCAFDoc_DocumentTool_ShapeTool(doc.Main())
    # color_tool = XCAFDoc_DocumentTool_ColorTool(doc.Main())
    # layer_tool = XCAFDoc_DocumentTool_LayerTool(doc.Main())
    # mat_tool = XCAFDoc_DocumentTool_MaterialTool(doc.Main())

    # step_reader = STEPCAFControl_Reader()
    # step_reader.SetColorMode(True)
    # step_reader.SetLayerMode(True)
    # step_reader.SetNameMode(True)
    # step_reader.SetMatMode(True)
    # step_reader.SetGDTMode(True)
    # step_reader.SetPropsMode(True)
    # step_reader.SetViewMode(True)
    # step_reader.SetSHUOMode(True)

    # status = step_reader.ReadFile(filename)
    # if status == IFSelect_RetDone:
    #     ret = step_reader.Transfer(doc)
    #     print("Successful transfer")


   

    # topExp = TopExp_Explorer()
    # topExp.Init(StepFileReader(filename).getShape(), TopAbs_SOLID)

    # props = GProp_GProps()
    

    

    # while topExp.More():
    #     item = topExp.Current()
    #     brepgprop_VolumePropertiesGK(item, props)
    #     print(props.Mass())

    #     topExp.Next()
