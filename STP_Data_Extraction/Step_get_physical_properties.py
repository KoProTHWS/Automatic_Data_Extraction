from OCC.Core.TDF import TDF_LabelSequence
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Extend.ShapeFactory import measure_shape_volume, measure_shape_mass_center_of_gravity
from prettytable import PrettyTable
import pandas as pd


class Physical_Properties:

    def extract(shape_tool, material_tool, label, name):

        # https://github.com/tpaviot/pythonocc-core/blob/2e9505bb32099aae1c1c7058a94a68bab81de6af/test/core_extend_shapefactory_unittest.py

        
        mat_lab = TDF_LabelSequence()
        shape = shape_tool.GetShape(label)
        material_tool.GetMaterialLabels(mat_lab)

        # console_output_table.header = False

        # print(f"Physical Properties of shape: {name}:")
        # print("Density: ", material_tool.GetDensityForShape(label))

        
        props = GProp_GProps()
        brepgprop_SurfaceProperties(shape, props)


        surface_area = props.Mass() / 10**6 # Converted to SI units
        volume = measure_shape_volume(shape) / 10**9 # Converted to SI units
        
        cog, _, _ = measure_shape_mass_center_of_gravity(shape)

        density = material_tool.GetDensityForShape(label) * 10**6 # Converted to SI units
        mass = (density*volume)
        
        # print("Moment of Intertia" ,props.PrincipalProperties().Moments())
        # print("Trägheitsmomente", props.MatrixOfInertia())
        # print(props.PrincipalProperties())
        # com = props.CentreOfMass()
        # print("Total Surface Area (mm^2): ", surface_area)
        # print(f"Total volume (mm^3): {volume}")
        # print('mass', mass)

        # Center of gravity of just the chosen shape. While cross-verifying in CAD software, individual shapes have to be exported as separate files first.
        # print(f"Center of Gravity (mm): {cog.Coord()}")

        print(' ')

        # console_output_table = PrettyTable(border  = True)
        # console_output_table.border = True
        # console_output_table.field_names = ["Shape Name", name]
        # console_output_table.add_row(["Density (Kg/m^3)", density])
        # console_output_table.add_row(["mass (kg)", mass])
        # console_output_table.add_row(["Moment of Intertia", props.PrincipalProperties().Moments()])
        # console_output_table.add_row(["Total Surface Area (m^2)", surface_area])
        # console_output_table.add_row(["Total volume (m^3)", volume])
        # console_output_table.add_row(["Center of Gravity (mm)", cog.Coord()])

        df_row = pd.DataFrame({
                                "Shape Name": [name],
                                "Density (Kg/m^3)": [density],
                                "mass (kg)": [mass],
                                "Moment of Intertia": [props.PrincipalProperties().Moments()],
                                "Total Surface Area (m^2)": [surface_area],
                                "Total volume (m^3)": [volume],
                                "Center of Gravity (mm)": [cog.Coord()]
                                })

        # print(df_row)
        # print(console_output_table)

        return df_row

