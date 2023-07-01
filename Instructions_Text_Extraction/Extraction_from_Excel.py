import pandas as pd

class ExcelTableExtractor:

    def extract(file_path, target_column):
        # Read Excel file

        xl = pd.read_excel(file_path, sheet_name=None, header=None)

        result = pd.DataFrame(columns=['Step Number', target_column])

        for sheet_name, sheet_data in xl.items():
            for index, row in sheet_data.iterrows():
                if row.str.contains(target_column).any():
                    matches = row[row == target_column]
                    if not matches.empty:
                        target_index = matches.index[0]
                        step_index = target_index - 2 # U&Z excel sheet has the step number 2 columns to the left of 

                        # Extract data from the table until 10 empty rows are encountered- done to avoid loop exit if there are few empty cells under the columns names
                        table_data = []
                        empty_rows_count = 0
                        for i in range(index + 1, len(sheet_data)):
                            row_data = sheet_data.loc[i, [step_index, target_index]]
                            if row_data.isnull().all():
                                empty_rows_count += 1
                                if empty_rows_count >= 10:
                                    break
                            else:
                                empty_rows_count = 0
                                table_data.append(row_data.values)

                        # Append table data to the result DataFrame
                        result = result.append(pd.DataFrame(table_data, columns=['Step Number', target_column]), ignore_index=True)
                        break

        if not result.empty:
            print(result)
            return result
        else:
            print(f"No table with '{target_column}' column was found.")
            return None




