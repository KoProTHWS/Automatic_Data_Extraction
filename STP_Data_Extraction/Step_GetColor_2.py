import os
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.XCAFDoc import (
    XCAFDoc_DocumentTool_ShapeTool,
    XCAFDoc_DocumentTool_ColorTool,
    XCAFDoc_DocumentTool_LayerTool,
    XCAFDoc_DocumentTool_MaterialTool
)
from OCC.Core.STEPCAFControl import STEPCAFControl_Reader
from OCC.Core.TDF import TDF_LabelSequence, TDF_Label
from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from bounding_box import Bounding_box
from Step_get_physical_properties import Physical_Properties 
from origin_positions import Origin
import pandas as pd

'''https://github.com/tpaviot/pythonocc-core/blob/master/src/Extend/DataExchange.py'''


class get_part_colors:


    def __init__(self):
        
        # self.filename = filename
        self.doc =TDocStd_Document(TCollection_ExtendedString("pythonocc-doc"))# create a handle to a document
        self.shape_tool = XCAFDoc_DocumentTool_ShapeTool(self.doc.Main())
        self.color_tool = XCAFDoc_DocumentTool_ColorTool(self.doc.Main())
        self.material_tool = XCAFDoc_DocumentTool_MaterialTool(self.doc.Main()) ## move this out


        # Get root assembly
        # XCAFDoc_DocumentTool_ShapeTool holds information regarding geometry and topology
        

        # XCAFDoc_DocumentTool_ColorTool is used to manipulate color data from the XCAF document
        
        # XCAFDoc_DocumentTool_MaterialTool is used to manipulate material/ physical data (density, centerofgravity, etc)

    ''' This script converts a assembly into individual parts as a TopoDS shape'''

    # Function which returns no of subshapes and components according to the supplied Label object- could be sub assembly or individial obj
    def get_no_of_components(self, lab):
        l_subss = TDF_LabelSequence()
        
        # print('l_subss',l_subss)
        self.shape_tool.GetSubShapes(lab, l_subss) ## changed
        # shape_tool.GetFreeShapes(l_subss)
        print("Nb subshapes   :", l_subss.Length()) #Not used at the moment
        l_comps = TDF_LabelSequence()
        self.shape_tool.GetComponents(lab, l_comps)
        print("Nb components  :", l_comps.Length())

        return l_comps.Length()


    #Function to retrieve components referred to the main shape.
    def comp_refShape_location(self, lab, _):
            l_c = TDF_LabelSequence()

            self.shape_tool.GetComponents(lab, l_c)
            label = l_c.Value(_ + 1)
            label_reference = TDF_Label()
            # shape_tool.GetSubShapes(label, label_reference)
            self.shape_tool.GetReferredShape(label, label_reference)
            print('Is shape an Assembly?',self.shape_tool.IsAssembly(label_reference))
            # shape_tool.GetShape(, label_reference)
            # print('jojo',label_reference.Depth())
            
            loc = self.shape_tool.GetLocation(label)
            print('\n')

            return label_reference, label_reference.GetLabelName(), loc
      
    def color_parts(self, filename):


        # Dimension data for all shapes are appended into this dataframe
        dimensions_df = pd.DataFrame(columns=["Shape", "Width", "Height", "Depth"])
        physical_properties_df = pd.DataFrame(columns=["Shape Name", "Density (Kg/m^3)", "mass (kg)", "Moment of Intertia", 
                                  "Total Surface Area (m^2)", "Total volume (m^3)", "Center of Gravity (mm)"])

        origins_df = pd.DataFrame(columns=['Shape Name', 'Translation', 'X', 'Y', 'Z'])
        # filename = "C:/Users/Varun Kaarthik/Documents/cad_data_extraction/STP_Data_Extraction/CAD/fertiges_bauteil_asm_2.stp"

        if not os.path.isfile(filename):
                raise FileNotFoundError(f"{filename} not found.")
            # the list:
        output_shapes = {}


        print('color_tool', self.color_tool)

        ############
        step_reader = STEPCAFControl_Reader()
        step_reader.SetColorMode(True)
        step_reader.SetLayerMode(True)
        step_reader.SetNameMode(True)
        step_reader.SetMatMode(True)
        step_reader.SetGDTMode(True)

        status = step_reader.ReadFile(filename)

        if status == IFSelect_RetDone:
            step_reader.Transfer(self.doc)
        #############

        #Label of entire assembly
        labels = TDF_LabelSequence()
        self.shape_tool.GetFreeShapes(labels) # In this use case- free shape is basically the entire assembly.

        
        print('labels', labels.Length())
        # print('labels', labels)
        # label_reference = TDF_Label()
        # # shape_tool.GetComponents(lab, l_c)
        # # label = labels.Value(0)

        label_references = []
        extra_shapes = []
        location_references = []
        # shape_tool.GetReferredShape(label, label_reference)

        if labels.Length() == 1:
            lab = labels.Value(1)
            name = lab.GetLabelName()
            print("Name of Full Assembly :", name)

            if self.shape_tool.IsAssembly(lab) == True:

                _, _, loc = get_part_colors.comp_refShape_location(self, lab, 0)
                
                label_references.append(lab)

                # location_references.append(loc)
                print('locc', loc)
                
            else:
                label_references.append(lab)
                loc = self.shape_tool.GetLocation(lab)
                location_references.append(loc)
                print('locc', loc)
                print(location_references)

                # dimensions = Bounding_box.dimensions(shape_tool, lab, name)
                # df_row = Bounding_box.dimensions(shape_tool, lab, name)
                dimensions_df = pd.concat([dimensions_df, Bounding_box.dimensions(self.shape_tool, lab, name)], ignore_index=True)

                physical_properties_df = pd.concat([physical_properties_df, Physical_Properties.extract(self.shape_tool, self.material_tool, lab, name)], ignore_index=True)

                origins_df = pd.concat([origins_df, Origin.location(location_references, name)], ignore_index=True)
                # Origin.location(location_references)

        else:
            print('No main assembly')
            quit()


        no_of_comps = get_part_colors.get_no_of_components(self, lab) #no of componenents within the main assembly
        if no_of_comps > 0:
            x = 1
            for i in range(no_of_comps):

                # location_references = location_references[:1]
                location_references = []
                print('_', i)
                print('\n')

                label_reference1, name, loc = get_part_colors.comp_refShape_location(self, lab, i)
                print("Name1 :", name)
                

                # Bounding_box.dimensions(shape_tool, label_reference1, name)
                # df_row = Bounding_box.dimensions(shape_tool, label_reference1, name)
                dimensions_df = pd.concat([dimensions_df, Bounding_box.dimensions(self.shape_tool, label_reference1, name)], ignore_index=True)

                # Physical.physical_properties(shape_tool, material_tool, label_reference1, name)

                physical_properties_df = pd.concat([physical_properties_df, Physical_Properties.extract(self.shape_tool, self.material_tool, label_reference1, name)], ignore_index=True)
                location_references.append(loc)
                origins_df = pd.concat([origins_df, Origin.location(location_references, name)], ignore_index=True)

                # Origin.location(location_references)

                no_of_comps = get_part_colors.get_no_of_components(self, label_reference1) #No of componenents within. For example when a sub assembly has a sub assembly within
                if no_of_comps == 0: 
                    label_references.append(label_reference1)
                    print('no_of_comps = 0')
      
                
                if no_of_comps > 0: #Need to scale this. If a subcomp has more sub comps within then this alg won't work
                    
                    # print('no of comps', no_of_comps)
                    label_reference1, name, loc = get_part_colors.comp_refShape_location(self, lab, i)
                    for _ in range(no_of_comps) :

                        label_reference, name, loc = get_part_colors.comp_refShape_location(self, label_reference1, _)
                        
                        label_references.append(label_reference)

                        location_references.append(loc)
                        

                        dimensions_df = pd.concat([dimensions_df, Bounding_box.dimensions(self.shape_tool, label_reference, name)], ignore_index=True)

                        physical_properties_df = pd.concat([physical_properties_df, Physical_Properties.extract(self.shape_tool, self.material_tool, label_reference, name)], ignore_index=True)

                        origins_df = pd.concat([origins_df, Origin.location(location_references, name)], ignore_index=True)
                        # Origin.location(location_references)
                  

                        no_of_comps = get_part_colors.get_no_of_components(self, label_reference)

                        
                        # print("Name3 :", name)

        # For when there is only a single component in the step file                
        elif no_of_comps == 0: 
            label_reference = TDF_Label()
            
            loc = self.shape_tool.GetLocation(lab)
            #  label_references.append(label_reference)
    
                
        print('No of labels: ', len(label_references))
        # print('len(label_references)', label_references)
         

        # for l_subss in label_references:
        # shape = shape_tool.GetShape(label_reference)

        #     c = Quantity_Color(0.9, 0.9, 0.9, Quantity_TOC_RGB)  # default color
        #     color_set = False
        #     shape_disp = BRepBuilderAPI_Transform(shape, loc.Transformation()).Shape()
        #     if not shape_disp in output_shapes:
        #         output_shapes[shape_disp] = [lab.GetLabelName(), c]

        '''############
        Retrieving colors of each component and storing it in a list
        ############'''

        

        color_parts = [] #List that will hold all the color values of various parts

        for i in range(len(label_references)):
            # print('range(len(label_references)', range(len(label_references)))

            lab_subs = label_references[i]
            shape = self.shape_tool.GetShape(label_references[i])
            
            # print("\n########  simpleshape subshape label :", lab)
            shape_sub = self.shape_tool.GetShape(lab_subs)

            c = Quantity_Color(0.5, 0.5, 0.5, Quantity_TOC_RGB)  # default color
            color_set = False
            if (
                self.color_tool.GetInstanceColor(shape_sub, 0, c)
                or self.color_tool.GetInstanceColor(shape_sub, 1, c)
                or self.color_tool.GetInstanceColor(shape_sub, 2, c)
            ):
                self.color_tool.SetInstanceColor(shape_sub, 0, c)
                self.color_tool.SetInstanceColor(shape_sub, 1, c)
                self.color_tool.SetInstanceColor(shape_sub, 2, c)
                color_set = True
                n = c.Name(c.Red(), c.Green(), c.Blue())
                # print('n1',n)
                color_parts.append(n)
            

            if not color_set:
                if (
                    self.color_tool.GetColor(lab_subs, 0, c)
                    or self.color_tool.GetColor(lab_subs, 1, c)
                    or self.color_tool.GetColor(lab_subs, 2, c)
                ):
                    self.color_tool.SetInstanceColor(shape, 0, c)
                    self.color_tool.SetInstanceColor(shape, 1, c)
                    self.color_tool.SetInstanceColor(shape, 2, c)
                    n = c.Name(c.Red(), c.Green(), c.Blue())        
                    color_parts.append(n)

                
            shape_to_disp = BRepBuilderAPI_Transform(
                shape_sub, loc.Transformation()
            ).Shape()
            # position the subshape to display
            if not shape_to_disp in output_shapes:
                output_shapes[shape_to_disp] = [lab_subs.GetLabelName(), c]


        return color_parts, dimensions_df, physical_properties_df, origins_df
            
