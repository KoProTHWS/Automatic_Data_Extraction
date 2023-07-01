import os

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
    XCAFDoc_DocumentTool_LayerTool,
)
from OCC.Core.STEPCAFControl import STEPCAFControl_Reader
from OCC.Core.TDF import TDF_LabelSequence, TDF_Label
from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform



def getGeometryInformation(filename):
    """Returns list of tuples (topods_shape, label, color)
    Use OCAF.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")
    # the list:
    output_shapes = {}
    return_elements = []

    dic_elements = {}
    dic_rot = {}
    dic_tran = {}
    dic_kombo = {}

    # create an handle to a document
    doc = TDocStd_Document(TCollection_ExtendedString("pythonocc-doc"))

    # Get root assembly
    shape_tool = XCAFDoc_DocumentTool_ShapeTool(doc.Main())
    color_tool = XCAFDoc_DocumentTool_ColorTool(doc.Main())
    layer_tool = XCAFDoc_DocumentTool_LayerTool(doc.Main())
    # mat_tool = XCAFDoc_DocumentTool_MaterialTool(doc.Main())

    step_reader = STEPCAFControl_Reader()
    step_reader.SetColorMode(True)
    step_reader.SetLayerMode(True)
    step_reader.SetNameMode(True)
    step_reader.SetMatMode(True)
    step_reader.SetGDTMode(True)

    status = step_reader.ReadFile(filename)
    if status == IFSelect_RetDone:
        step_reader.Transfer(doc)

    locs = []

    def _get_sub_shapes(lab, loc):
    

        l_subss = TDF_LabelSequence()
        shape_tool.GetSubShapes(lab, l_subss)
        #print("Nb subshapes   :", l_subss.Length())
        l_comps = TDF_LabelSequence()
        shape_tool.GetComponents(lab, l_comps)
        #print("Nb components  :", l_comps.Length())
        print()
        name = lab.GetLabelName()
        
        print("Name :", name)

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
                    shape_tool.GetShape(label)
                    print("    loc          :", loc)
                    trans = loc.Transformation()
                    print("    tran form    :", trans.Form())
                    rot = trans.GetRotation()
                    print("    rotation     :", rot)
                    print("    X            :", rot.X())
                    print("    Y            :", rot.Y())
                    print("    Z            :", rot.Z())
                    print("    W            :", rot.W())
                    tran = trans.TranslationPart()
                    print("    translation  :", tran)
                    print("    X            :", tran.X())
                    print("    Y            :", tran.Y())
                    print("    Z            :", tran.Z())

                    

                    locs.append(loc)
                    # print(">>>>")
                    # lvl += 1
                    _get_sub_shapes(label_reference, loc)
                    # lvl -= 1
                    # print("<<<<")
                    locs.pop()

        elif shape_tool.IsSimpleShape(lab):
            print("\n########  simpleshape label :", lab)
            shape = shape_tool.GetShape(lab)
            # print("    all ass locs   :", locs)

            loc = TopLoc_Location() #Constructs an empty local coordinate system object
            for l in locs:
                # print("    take loc       :", l)
                loc = loc.Multiplied(l) #essential to get correct x, y, z relative values

            trans = loc.Transformation()
            print("    FINAL loc    :")
            print("    tran form    :", trans.Form())
            rot = trans.GetRotation()

            print("    rotation     :", rot)
            print("    X            :", rot.X())
            print("    Y            :", rot.Y())
            print("    Z            :", rot.Z())
            print("    W            :", rot.W())
            tran = trans.TranslationPart()
            print("    translation  :", tran)
            print("    X            :", tran.X())
            print("    Y            :", tran.Y())
            print("    Z            :", tran.Z())
            

    def _get_shapes():
        labels = TDF_LabelSequence()
        shape_tool.GetFreeShapes(labels)
        # global cnt
        # cnt += 1

        print()
        print("Number of shapes at root :", labels.Length())
        print()
        for i in range(labels.Length()):
            root_item = labels.Value(i + 1)
            _get_sub_shapes(root_item, None)

    _get_shapes()
    return return_elements
        


            