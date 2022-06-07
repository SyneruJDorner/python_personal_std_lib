import json
import pandas as pd
from .json import JSON
from enum import Enum
from prettytable import PrettyTable

class EXCEL():
    '''
    This class is used to read and write excel files.
    '''
    @classmethod
    def load(cls, location, formatting="DATAFRAME", sheetname=None):
        '''
        Loads an excel file into a dataframe.

        Parameters
        ----------
        location : str
            The location of the excel file.
        formatting : enum
            The formatting of the excel file.
            Options:
                - DATAFRAME
                - JSON
        sheetname : str
            The name of the sheet to load.
        '''
        df = None

        if (sheetname == None):
            df = pd.read_excel(location, dtype=str)

        if (formatting == cls.EXCEL_FORMAT.DATAFRAME):
            return df
        elif (formatting == cls.EXCEL_FORMAT.JSON):
            result = df.to_json(orient="records")
            parsed = json.loads(result)
            return parsed

    
    @classmethod
    def print_as_table(cls, data, formatting="DATAFRAME"):
        '''
        Prints a dataframe as a table.

        Parameters
        ----------
        data : dataframe
            The dataframe to print.
        formatting : enum
            The formatting of the excel file.
            Options:
                - DATAFRAME
                - JSON
        '''
        if (formatting == cls.EXCEL_FORMAT.DATAFRAME):
            pass
        elif (formatting == cls.EXCEL_FORMAT.JSON):
            keys = (["Index"] + JSON.get_keys(data[0]))
            table = PrettyTable()
            table.field_names = keys
            
            index_cnt = 0
            for i, item in enumerate(data):
                current_data = []
                index_cnt = str(int(index_cnt) + 1).zfill(4)
                current_data.append(str(index_cnt))
                for val in enumerate(list(item.values())):
                    current_data.append(val[1])
                table.add_row(current_data)
            table.align = "r"
            print(table.get_string())


    @classmethod
    def save(cls, data, location, formatting="DATAFRAME"):
        '''
        Saves a dataframe as an excel file.

        Parameters
        ----------
        data : dataframe
            The dataframe to save.
        location : str
            The location to save the excel file.
        formatting : enum
            The formatting of the excel file.
            Options:
                - DATAFRAME
                - JSON
        '''
        if (formatting == cls.EXCEL_FORMAT.DATAFRAME):
            data.to_excel(location)
        elif (formatting == cls.EXCEL_FORMAT.JSON):
            json_to_df = pd.DataFrame.from_dict(data)
            json_to_df.to_excel(location)


    @classmethod
    class EXCEL_FORMAT(str, Enum):
        '''
        Enum for the EXCEL file formats.

        Options:
            - DATAFRAME
            - JSON
        '''
        DATAFRAME = "DATAFRAME"
        JSON = "JSON"

