from Step_GetAssemblyPNG import GetAssemblyPNG
from Step_GetName import *
from Step_GetTopology import *
from Step_FileReader import StepFileReader
from Step_GetGeometricFeatures import *
# from Step_GetGeometryInformation import *
# from Step_GetColor import *
from Step_GetColor_2 import get_part_colors
from Step_GetProperties import *
from utils import Utils


# sys.path.append(r"/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION")
# sys.path.append(r"C:/Users/Varun Kaarthik/Documents/cad_data_extraction/STP_Data_Extraction/CAD/pick-up_heavy-duty_single-cab/") 

#filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/test_Uhlmann.stp"

#filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/Truck_komplett(stp)/pick-up_classic_king-size.stp"
# filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/fertiges_bauteil_asm_2.stp"
# filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/bt_asm.stp"
# filename = "C:/Users/Varun Kaarthik/Documents/cad_data_extraction/STP_Data_Extraction/CAD/bt_asm.stp"
# filename = "C:/Users/Varun Kaarthik/Documents/CAD/fertiges_bauteil_asm_2.stp"
filename = "C:/Users/Varun Kaarthik/Documents/IP_files/EDH-Schildmontage/EDH-Schildmontage/2022-05-11-Dateneingang/KOPRO_E2013-010-004_EDH_Schildbeschlag_schmal_einseitig_elektronisch_ZSB.stp"

#filename = "/home/fabian/Desktop/KoPro/Planning_Algorithm/Code/STP_DATA_EXTRACTION/CAD/Wittenstein/Step-KoPro V1.stp"

if __name__ == "__main__":

 
    '''############# Returns color values for every single component in the assembly. 
    ############# Returns dimension, physical properties and origins of every component in the assembly.'''

    get_part_colors = get_part_colors()

    color_parts, dimension_df, physical_properties_df, origins_df = get_part_colors.color_parts(filename)
    print('No of color parts: ', len(color_parts))
    print('')

    print('Dimensions: \n ', dimension_df)
    print('')
    print('Physical properties: \n ', physical_properties_df)
    print('')
    print('Origin Locations: \n ', origins_df)
    print('')   

        
    '''##### PNG Images Generation ####'''

    #creates a new folder to save the images and returns its path. Named images_assembly_name
    png_save_path = Utils.create_folder(filename, 'images_')

    assembly = GetAssemblyPNG(StepFileReader(filename).getShape())

    # Calls function to save step-by-step assembly images
    assembly.saveAssemblySequenzToPNG(png_save_path, color_parts)
    
    # Calls function to save step-by-step assembly images
    assembly.SaveAssemblyPartsToPNG(png_save_path, color_parts)

    ''' #### Step file generation for every part in the assembly ####'''
    # Creates a folder and saves all individual parts of assembly as step files
    step_save_path = Utils.create_folder(filename, 'step_')    
    assembly.Export_Step_File(step_save_path, color_parts)

    
    names =getNamesComponents(filename)
   
    print('Topology:', len(names))
    # get_Colors_to_Names(filename)

    shape = StepFileReader(filename).getShape()

    explorer = TopologyExplorer(shape)
    # explorer._loop_topo()
    
    print(explorer.number_of_faces())
    topo, shapes = dump_topology_to_string(shape)

    '''###### Prints the relationship matrix of the assembly #####'''


    matrix = Utils.relationship_matrix(names, topo)
    print('')
    print('Relationship Matrix:')
    print(matrix)
    
    # geometry = getGeometryInformation(filename)
