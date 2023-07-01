import os
import json
import pandas as pd

class Utils:

    @staticmethod
    def create_folder(filename, type):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        print('Current directory:', current_directory)

        # Here we prepend 'images_' to the folder name
        new_folder_name = str(type) + os.path.splitext(os.path.basename(filename))[0]

        print('New folder name:', new_folder_name)
        new_folder_path = os.path.join(current_directory, new_folder_name)

        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print(f"Folder '{new_folder_name}' created successfully.")
        else:
            print(f"Folder '{new_folder_name}' already exists.")

        png_save_path = new_folder_path + "/"

        return png_save_path


# topo = [0, 1, 1, 2, 2, 1, 2, 2]

# names = ['FERTIGES_BAUTEIL_ASM', 'DUPLO_2X2_ROT', 'BG_1_ASM', 'DUPLO_8X2_BLAU', 'DUPLO_2X2_BLAU', 'BG_2_ASM', 'DUPLO_4X2_GELB', 'DUPLO_2X2_GRUEN']

    @staticmethod
    def relationship_matrix(names, topo):
        '''convert the topology and names of the assembly parts into JSON-format'''
        dic = {}
        dic_assembly = {}
        component = []

        for i in range(len(topo)):

            if topo[i] == 1:
                dic_assembly[names[i]] = {}

                if len(topo)>i+1 and topo[i+1] == 2:
                    j = i+1
                    while (j < len(topo) and topo[j]==2):
                        component.append(names[j])
                        j = j+1

                dic_assembly[names[i]] = component
                component = []

        dic[names[0]] = dic_assembly

        data = json.loads(json.dumps(dic))

        # print(json.dumps(dic))

        # Transform data into list of relationships
        relationships = []
        for parent, children in data.items():
            for child, grand_children in children.items():
                for grand_child in grand_children:
                    relationships.append([parent, child, grand_child])

        # Convert relationships to DataFrame
        df = pd.DataFrame(relationships, columns=['Parent', 'Child', 'Grandchild'])

        # Create relationship matrix
        matrix = pd.pivot_table(df, index=['Parent', 'Child'], columns='Grandchild', aggfunc=len, fill_value=0)

        # print()
        # print(matrix)

        return matrix



