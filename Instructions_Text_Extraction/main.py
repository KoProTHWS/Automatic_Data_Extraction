from  Extraction_from_Excel import ExcelTableExtractor 
from Language_process import LanguageProcessor
 

file_path = "C:/Users/Varun Kaarthik/Documents/instruction_text_samples/AA_EDH außen Rosette_10C7.xlsx"
# file_path = "C:/Users/Varun Kaarthik/Documents/instruction_text_samples/evaluation_dataset.xlsx"
target_column = 'Beschreibung / text'

# Returns Dataframe with the extracted data from target_column with corresponding step number
extracted_dataframe = ExcelTableExtractor.extract(file_path, target_column)

# Returns Dataframe with instruction sentences split into: Action, Components, Tools, orignal instruction
# DF is also saved as Instructions.xlsx
LanguageProcessor.combine(extracted_dataframe)


if __name__ == '__main__':
    pass