import json
import pandas as pd
from .json import JSON
from enum import Enum
from prettytable import PrettyTable

class CSV():
    '''
    This class is used to read and write csv files.
    '''
    @classmethod
    def load(cls, location, formatting="DATAFRAME"):
        '''
        Loads a CSV file into a Pandas DataFrame.

        Parameters
        ----------
        location : str
            The location of the CSV file.
        formatting : enum
            The format of the CSV file.
            Options:
                - DATAFRAME
                - JSON
        '''
        df = pd.read_csv(location, dtype=str, index_col=False)
        
        if (formatting == cls.CSV_FORMAT.DATAFRAME):
            return df
        elif (formatting == cls.CSV_FORMAT.JSON):
            result = df.to_json(orient="records")
            parsed = json.loads(result)
            return parsed

    
    @classmethod
    def print_as_table(cls, data, formatting="DATAFRAME"):
        '''
        Prints a Pandas DataFrame as a table.

        Parameters
        ----------
        data : Pandas DataFrame
            The data to be printed.
        formatting : enum
            The format of the data.
            Options:
                - DATAFRAME
                - JSON
        '''
        if (formatting == cls.CSV_FORMAT.DATAFRAME):
            pass
        elif (formatting == cls.CSV_FORMAT.JSON):
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
    class CSV_FORMAT(str, Enum):
        '''
        Enum for the CSV file formats.

        Options:
            - DATAFRAME
            - JSON
        '''
        DATAFRAME = "DATAFRAME"
        JSON = "JSON"
