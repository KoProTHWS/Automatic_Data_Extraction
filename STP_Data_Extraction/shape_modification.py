
''' This code apprears to be creating 2 new boxes and stacking one above the other'''

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRep import BRep_Tool
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_XYZ
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, brepgprop_LinearProperties
from OCC.Display.OCCViewer import rgb_color
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs, STEPControl_ShellBasedSurfaceModel

# Create a basic box
box = BRepPrimAPI_MakeBox(10, 10, 10).Shape()

# Define the new length for one of its edges
new_length = 10

# Get the vertices of the box
vertices = []
vertex_explorer = TopExp_Explorer()
vertex_explorer.Init(box, TopAbs_VERTEX)
while vertex_explorer.More():
    vertex = vertex_explorer.Current()
    vertex_point = BRep_Tool.Pnt(vertex)
    print('vertex_point', vertex_point.X(), vertex_point.Y(), vertex_point.Z())
    vertices.append(vertex_point)
    vertex_explorer.Next()
print('len of original vertices', len(vertices))

# Calculate the new vertices based on the new length
new_vertices = []
for i in range(len(vertices)):
    print('i', vertices[i])

    x = gp_Pnt(vertices[i].XYZ())
    y = gp_Pnt(vertices[(i+1) % len(vertices)].XYZ())
    
    print('X', x.X(), x.Y(), x.Z())
    print('Y', y.X(), y.Y(), y.Z())
          
    # vec = gp_Vec(gp_Pnt(vertices[i].XYZ()), gp_Pnt(vertices[(i+1) % len(vertices)].XYZ()))
    # Get the coordinates of two consecutive vertices in a polygon or polyline
    vertex1_coords = vertices[i].XYZ()
    vertex2_coords = vertices[(i+1) % len(vertices)].XYZ()

    # Create two points using the vertex coordinates
    vertex1 = gp_Pnt(vertex1_coords)
    vertex2 = gp_Pnt(vertex2_coords)

    

    # Create a vector that points from vertex1 to vertex2
    vec = gp_Vec(vertex1, vertex2)
    
    print(vec.X(), vec.Y(), vec.Z())
    if vec.Magnitude() == 10:
        vec_normalized = gp_Vec(vec.XYZ())
        vec_normalized.Normalize() #Vec_noramlised is has same direction as vec but length of 1
        print('vec_normalized', vec_normalized.X(), vec_normalized.Y(), vec_normalized.Z())
        # vec_normalized.Multiply((new_length - 10) / 2)
        vec_normalized.Multiply(new_length)
        print('vec_multip', vec_normalized.X(), vec_normalized.Y(), vec_normalized.Z())
        new_vertices.append(vertices[i].Translated(vec_normalized)) # .translated is a function to translate the vector in the direction of a gp_vec
        print('new_vertices1', new_vertices[0].X(), new_vertices[0].Y(), new_vertices[0].Z())
        # new_vertices.append(vertices[(i+1) % len(vertices)].Translated(vec_normalized))
        new_vertices.append(vec)
        print('new_vertices2', new_vertices[1].X(), new_vertices[1].Y(), new_vertices[1].Z())
        break

print('len of new vertices', len(new_vertices))
# Modify the box by moving the vertices
transformation1 = gp_Trsf()
transformation1.SetTranslation(vertices[new_vertices.index(new_vertices[0])], new_vertices[0])
transformation2 = gp_Trsf()
# transformation2.SetTranslation(vertices[new_vertices.index(new_vertices[1])], new_vertices[1])
# transformation2.SetTranslation(vertices[5], new_vertices[1])

move1 = BRepBuilderAPI_Transform(box, transformation1)
move2 = BRepBuilderAPI_Transform(move1.Shape(), transformation2)

new_box = move2.Shape()

##########
new_box_1 = box

# Get the vertices of the box
vertices = []
vertex_explorer = TopExp_Explorer()
vertex_explorer.Init(new_box_1, TopAbs_VERTEX)
while vertex_explorer.More():
    vertex = vertex_explorer.Current()
    # print(type(vertex))
    vertex_point = BRep_Tool.Pnt(vertex)
    if vertex_point.X() == 0 and vertex_point.Y() == 0 and vertex_point.Z() == 10:
        print('yes')
        x = gp_XYZ(11,8, 15)
        vertex_point = gp_Pnt(x)
        # break
    # print('vertex_point', vertex_point.X(), vertex_point.Y(), vertex_point.Z())
    vertices.append(vertex_point)
    vertex_explorer.Next()
    
print('len of copy vertices', len(vertices))

vertex_explorer.Init(new_box_1, TopAbs_VERTEX)

while vertex_explorer.More():
    vertex = vertex_explorer.Current()
    # print(type(vertex))
    vertex_point = BRep_Tool.Pnt(vertex)

    print('vertex_point', vertex_point.X(), vertex_point.Y(), vertex_point.Z())
    vertices.append(vertex_point)
    vertex_explorer.Next()
print('len of copy vertices', len(vertices))
###########

sewing = BRepBuilderAPI_Sewing()

sewing.Add(box)
sewing.Add(new_box)
sewing.Perform()
sewed_shape = sewing.SewedShape()

# Export the new box to a STEP file
# step_writer = STEPControl_Writer()
# step_writer.Transfer(sewed_shape, STEPControl_AsIs) #STEPControl_ShellBasedSurfaceModel is another option if the interior need to be hollow.
# filename = "C:/Users/Varun Kaarthik/Documents/CAD/test04.stp"
# step_writer.Write(filename)

# Show the output
from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()
# display.DisplayShape(box, update=True, transparency=0.7)
# display.DisplayShape(new_box_1, update=True, transparency=0.5)
display.DisplayShape(sewed_shape, update=True, transparency=0.5)
start_display()
