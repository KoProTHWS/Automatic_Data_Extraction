
import os
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
import OCC.Core.Bnd
import OCC.Core.BRepBndLib
from OCC.Core.STEPControl import (
    STEPControl_Reader,
    STEPControl_Writer,
    STEPControl_AsIs,
)
from prettytable import PrettyTable
import pandas as pd

class Bounding_box:

    def dimensions(shape_tool, label_reference1, name):

        # TDF_Label is converted to a Topo_DS shape
        shape = shape_tool.GetShape(label_reference1)
        # print('Shape Type', type(shape))

        '''Save individual shapes as a step file'''

        # filename1 = "C:/Users/Varun Kaarthik/Documents/cad_data_extraction/STP_Data_Extraction/CAD/export" + str(i) + ".stp"

        # get_part_colors.write_step_file(jj, filename1, application_protocol="AP203")


        # Get the bounding box of the shape
        bbox = OCC.Core.Bnd.Bnd_Box()
        OCC.Core.BRepBndLib.brepbndlib_Add(shape, bbox)

        # Get the dimensions of the bounding box
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        width = xmax - xmin
        height = ymax - ymin
        depth = zmax - zmin

        console_output_table = PrettyTable()
        console_output_table.field_names = ["_", "__"]
        console_output_table.header = False

        # Print the (bounding box) dimensions of the shape
        print(f"Dimensions of shape: {name}:")
        # print(f"Width: {width}")
        # print(f"Height: {height}")
        # print(f"Depth: {depth}")
        # console_output_table.add_row(["Width", width])
        # console_output_table.add_row(["Height", height])
        # console_output_table.add_row(["Depth", depth])
        # print(console_output_table)

        # Loading everything to a DF so that it can be concatenated later for full assembly
        df_row = pd.DataFrame({"Shape": [name], "Width": [width], "Height": [height], "Depth": [depth]})

        return df_row

    
    def write_step_file(a_shape, filename, application_protocol="AP203"):
        # a_shape = shape
        # filename = "C:/Users/Varun Kaarthik/Documents/cad_data_extraction/STP_Data_Extraction/CAD/testexport" + str('1') + ".obj"

        application_protocol="AP203"
        """exports a shape to a STEP file
        a_shape: the topods_shape to export (a compound, a solid etc.)
        filename: the filename
        application protocol: "AP203" or "AP214IS" or "AP242DIS"
        """
        # a few checks
        if a_shape.IsNull():
            raise AssertionError(f"Shape {a_shape} is null.")
        if application_protocol not in ["AP203", "AP214IS", "AP242DIS"]:
            raise AssertionError(
                f"application_protocol must be either AP203 or AP214IS. You passed {application_protocol}."
            )
        if os.path.isfile(filename):
            print(f"Warning: {filename} file already exists and will be replaced")
        # creates and initialise the step exporter
        step_writer = STEPControl_Writer()
        Interface_Static_SetCVal("write.step.schema", application_protocol)

        # transfer shapes and write file
        step_writer.Transfer(a_shape, STEPControl_AsIs)
        status = step_writer.Write(filename)

        if not status == IFSelect_RetDone:
            raise IOError("Error while writing shape to STEP file.")
        if not os.path.isfile(filename):
            raise IOError(f"{filename} not saved to filesystem.")
        

        