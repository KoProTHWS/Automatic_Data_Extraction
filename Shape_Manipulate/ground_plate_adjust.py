
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pln, gp_Trsf, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeHalfSpace
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_Transform,
BRepBuilderAPI_Sewing,
BRepBuilderAPI_MakeFace)

from Load_Shape_from_STEP import LoadShapeFromStep



def cut_small_segment(shape, cut_length):
    # cutting planes
    cutting_plane_left = gp_Pln(gp_Pnt(0, cut_length, 0), gp_Dir(0, 1, 0))
    cutting_plane_right = gp_Pln(gp_Pnt(0, cut_length + 1, 0), gp_Dir(0, 1, 0))

    # Create faces from  cutting planes
    cutting_face_left = BRepBuilderAPI_MakeFace(cutting_plane_left).Face()
    cutting_face_right = BRepBuilderAPI_MakeFace(cutting_plane_right).Face()

    # Create two half-spaces for each cutting plane
    cutting_tool_left = BRepPrimAPI_MakeHalfSpace(cutting_face_left, gp_Pnt(0, cut_length - 0.01, 0)).Shape()
    cutting_tool_right = BRepPrimAPI_MakeHalfSpace(cutting_face_right, gp_Pnt(0, cut_length + 1.01, 0)).Shape()

    # Cut the shape using the half-spaces
    cut_shape_left = BRepAlgoAPI_Cut(shape, cutting_tool_left).Shape()
    cut_shape_segment = BRepAlgoAPI_Cut(cut_shape_left, cutting_tool_right).Shape()

    return cut_shape_segment


def stack_segments(segment, num_segments, segment_thickness=1):
    segments = []
    
    for i in range(num_segments):
        translation_vector = gp_Vec(0, i * segment_thickness, 0)
        transformation = gp_Trsf()
        transformation.SetTranslation(translation_vector)
        
        brep_transform = BRepBuilderAPI_Transform(segment, transformation)
        translated_segment = brep_transform.Shape()
        
        segments.append(translated_segment)
        
    return segments

# Slices shape into 2 pieces at the specified point.
def slice_shape(cut_length, shape):


    # Create a dummy shape
    # shape = BRepPrimAPI_Makeshape(200, 60, 60).Shape()

    # Create a cutting plane
    cutting_plane = gp_Pln(gp_Pnt(0, cut_length, 0), gp_Dir(0, 1, 0))


    # Create a face from the cutting plane
    cutting_face = BRepBuilderAPI_MakeFace(cutting_plane).Face()


    # Create two half-spaces (solids, infinite in one direction)
    # cutting_tool_left = BRepPrimAPI_MakeHalfSpace(cutting_face, gp_Pnt(99.99, 0, 0)).Shape()
    # cutting_tool_right = BRepPrimAPI_MakeHalfSpace(cutting_face, gp_Pnt(100.01, 0, 0)).Shape()
    '''Not sure why this I have to have z value for left and Y for right. Found this after trial and errpr'''

    cutting_tool_left = BRepPrimAPI_MakeHalfSpace(cutting_face, gp_Pnt(0, (cut_length - 1), 50)).Shape()
    cutting_tool_right = BRepPrimAPI_MakeHalfSpace(cutting_face, gp_Pnt(0, (cut_length + 1), 0)).Shape()


    cut1 = BRepAlgoAPI_Cut(shape, cutting_tool_left).Shape()
    cut2 = BRepAlgoAPI_Cut(shape, cutting_tool_right).Shape()

    return cut1, cut2

'''##############'''
filename = "C:/Users/Varun Kaarthik/Documents/CAD/groundplate.stp"

shape = LoadShapeFromStep(filename).getShape()

split_distance = 100

cut_length = 120
'''##############'''


cut1, cut2 = slice_shape(cut_length, shape)

# Translate shape to make a gap, which will later be filled with segments
translation = gp_Trsf()
translation.SetTranslation(gp_Vec(0, split_distance, 0))  # Translate along the Y-axis by 20
transform_api = BRepBuilderAPI_Transform(cut1, translation)
cut1_translated = transform_api.Shape()


small_segment = cut_small_segment(shape, cut_length)


# stack multiple copies of the above segment
stacked_segments = stack_segments(small_segment, split_distance)

#Combine everything to a single TopoDS_Shape
sewing = BRepBuilderAPI_Sewing()
sewing.Add(cut2)
sewing.Add(cut1_translated)

for segment in stacked_segments:
    sewing.Add(segment)


sewing.Perform()
sewn_shapes = sewing.SewedShape()
sewn_shapes = TopoDS_Shape(sewn_shapes)


# # Initialize the viewer
display, start_display, add_menu, add_function_to_menu = init_display()

display.EraseAll()
# # ais_shape = display.DisplayShape(shape)[0]
# # display.Context.SetTransparency(ais_shape, 0.8, True)
display.DisplayShape(sewn_shapes, color="blue", transparency=0)
# # display.DisplayShape(cut2)
# # display.DisplayShape(cut1_translated)
# # display.DisplayShape(cut_small_segment(shape, cut_length), color="red", transparency=0)


# #     display.DisplayShape(segment, color="red", transparency=0)

display.FitAll()

# Start the viewer
start_display()
