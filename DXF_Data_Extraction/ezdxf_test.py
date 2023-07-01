import ezdxf
import math
import pandas as pd

# Returns dimension entity which has a name instead of the usual measurement 
def get_dimension_entity(modelspace, dimension_name):
    # Find the dimension entity with the given name
    entities = [entity for entity in modelspace if entity.dxftype() == 'DIMENSION']
    entity = None
    for e in entities:
        if e.dxf.text.split(";")[-1].strip(" }") == dimension_name:
            entity = e

            print(f"Dimension '{dimension_name}' found!")
            break

    if entity:
        print(f"DIMSTYLE {entity.dxf.dimstyle}")
        print(f"DIMTYPE {entity.dxf.dimtype}")
        print(f"End_point1 {entity.dxf.defpoint2}")
        print(f"End_point1 {entity.dxf.defpoint3}")
        print(f"DIMENSION {entity.get_measurement()}")

        return entity

    else:
        print(f"Dimension '{dimension_name}' not found- check spelling")

        return None

def find_key_by_value(my_dict, value):
    for key, val in my_dict.items():
        if val == value:
            return key
    return None 

# returns dict with leader handles and its associated text
def leader_text_relation(leader_text_string):
    leader_text_dict = {}
    for entity in modelspace:
        if entity.dxftype() == 'LEADER':

            arrowhead_location = entity.vertices[-1]
            # print(arrowhead_location)
            print(entity.dxf.has_arrowhead)
            # closest_point = entity.closest_point(arrowhead_location)
                        
            if entity.dxf.annotation_type == 0: #checks if leader is attached to a text entity
                # print('respone code:', entity.dxf.annotation_type, " (Created with text annotation)" )
            
                # print(entity.dxf.annotation_handle) # mtext handle
                
                mtext = doc.entitydb[entity.dxf.annotation_handle]
                new_string = mtext.plain_text(split=True, fast=True) # mtext handle
                
                # leader_text_dict[entity.dxf.handle]= new_string[0] # dict with leader handle and its associated text
                leader_text_dict[entity]= new_string[0] # dict with leader handle and its associated text
                

    print('leader_text_dict', leader_text_dict)

    leader = find_key_by_value(leader_text_dict, leader_text_string )

    if leader:
        vertices = list(leader.vertices)

        arrow_point_location = vertices[0]

        print('arrow_point_location', arrow_point_location)
        return arrow_point_location
    else:
        print(f"Leader (Textual Callout) with text '{leader_text_string}' not found- check spelling")
        return None


#return circle attached to arrowhead of leader
def get_shape_entity_attached_to_leader_arrowhead(arrow_point_location):
    circle_handle = None
    for entity in modelspace:
        if entity.dxftype() == "CIRCLE" or entity.dxftype() == "ARC":
            center = entity.dxf.center
            radius = entity.dxf.radius
            # print('radius', radius) 
            end_point = arrow_point_location

            # calculate distance between center of circle and end point of leader
            distance = math.sqrt((end_point[0]-center[0])**2 + (end_point[1]-center[1])**2)
            # print( 'distance', distance)
            
            tolerance = 1e-7

            if math.isclose(radius, distance, rel_tol=tolerance, abs_tol=tolerance):

                print(f" Arrow of Leader {arrow_point_location} is at boundary of {entity} with tolerance of {tolerance}")
                entity_handle  = doc.entitydb.get(entity.dxf.handle)

          
    return entity_handle #return handle of circle or arc


# Extract the extra table from the dxf file. Name of table should be provided as per how it is in the dxf file
def extract_entity_table(entity_table_block_name, column_names):

    table_data_list = []
    # Find the block with name "Tabelle1" - tentity_table_block_namehis basically loops through all blocks
    block = next((b for b in block_section if b.name == entity_table_block_name), None)
    if block:
        # Loop through each entity in the block
        for entity in block:
            # Check if the entity is MTEXT
            if entity.dxftype() == 'MTEXT':
                value = entity.dxf.text
                # Append text to the table data list
                table_data_list.append(value)

        # Check if the first few elements match the column names
        if table_data_list[:len(column_names)] == column_names:
            # Determine number of columns
            num_cols = len(column_names)
            # Split the list into data rows
            data_rows = [table_data_list[i:i+num_cols] for i in range(num_cols, len(table_data_list), num_cols)]

            df = pd.DataFrame(data_rows, columns=column_names)

            print(df)
            return df
        else:
            print("Error (Entity Table): first few elements of input list do not match column names provided by user")

        return None 
    else:
        print(f"Block named {entity_table_block_name} not found in the dxf file")
        return None


# Retrieve the revisions table from the dxf file. Name of table should be provided as per how it is in the dxf file
def get_revisions_table(revision_table_name):
    block_section = doc.blocks
    component_list = []
    
    for block in block_section:
        # Get block name
        block_name = block.name
        # print(f"Block name: {block_name}")
        # print('\n')
        if block.name == revision_table_name:
            print(f"Block name1: {block_name}")

            for entity in block:
                # print(f"Entity type: {entity_type}")
                # print(entity.dxf.handle)

                if entity.dxftype() == 'MTEXT':
                    component_list.append(entity.dxf.text)
                if entity.dxftype() == 'LINE':
                    component_list.append('LINE')
   
            table = []
            row = []

            for element in component_list:
                if element == 'LINE':
                    table.append(row)
                    row = []
                else:
                    row.append(element)

            if len(row) > 0:
                table.append(row)

            df = pd.DataFrame(table)
            df = df.dropna() #drop None values, they are the empty rows in this case
            print(df)
            return df
        
    print(f'Block named {revision_table_name} not found in the dxf file ')
    return None



def get_Title_block_information(title_block_name):

    rows_list = []
    for block in block_section:

            if block.name == title_block_name:
                for entity in block:
                    if entity.dxftype() == 'ATTDEF':
                        
                        dict1 = [str(entity.dxf.prompt), str(entity.dxf.text)]
                        # print(dict1)
                        rows_list.append(dict1)

                        # print(rows_list)   
                
                
                df = pd.DataFrame(rows_list) 
                print(df)

                return df
            
    print(f'Title Block named {title_block_name} not found in the dxf file ')
    return None
            
   


##################################################
filename = "C:/Users/Varun Kaarthik/Documents/IP_files/EDH-Schildmontage/EDH-Schildmontage/2023-03-28-Escutcheon-Variants/E2013-010-901_EDH_Grundplatte_schmal-Index-M.dxf"
# filename = "C:/Users/Varun Kaarthik/Documents/CAD/dxf_test_with_table.dxf"
# filename = "C:/Users/Varun Kaarthik/Documents/CAD/fertiges_bauteil_asm_2.dxf"


doc = ezdxf.readfile(filename)
modelspace = doc.modelspace()
# Get the block section of the DXF file
block_section = doc.blocks


dimension_name = 'A'

get_dimension_entity(modelspace, dimension_name) # returns dimension entity


# User should provide this
column_names = ["Maß A", "Artikelnummer (CH)", "Artikelnummer (PZ)"]

entity_table = extract_entity_table('Tabelle1', column_names)

# Get the location of the arrow point of the leader
arrow_point_location = leader_text_relation('Alternative Ausführung (CH)')

entity_handle = get_shape_entity_attached_to_leader_arrowhead(arrow_point_location)

# Get the dimesnions of the entity returned by previous functions. For circle and ARC this is the radius

print('Entity_handle radius if Circle or Arc (mm):', entity_handle.dxf.radius)


get_revisions_table('REVISIONSVERLAUF')

print('\n')

get_Title_block_information('Schriftfelder DIN') 
