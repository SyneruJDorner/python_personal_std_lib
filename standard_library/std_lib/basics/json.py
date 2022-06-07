import json
from collections import Mapping

class JSON():
    '''
    This class is used to convert python objects to json and vice versa.
    '''
    @classmethod
    def load(cls, location):
        '''
        Loads a JSON file and returns a dictionary.

        Parameters
        ----------
        location : str
            The location of the JSON file.
        '''
        data = None
        f = open(location)
        data = json.load(f)
        return data


    @classmethod
    def loads(cls, string_item):
        '''
        Loads a JSON string and returns a dictionary.

        Parameters
        ----------
        string_item : str
            The JSON string.
        '''
        data = json.loads(string_item)
        return data


    @classmethod
    def dumps(cls, list_items):
        '''
        Dumps a list of items into a JSON string.

        Parameters
        ----------
        list_items : list
            The list of items to be dumped.
        '''
        data = json.dumps(list_items)
        return data

    @classmethod
    def dump(cls, list_items, file_name, buffer_type="w+"):
        '''
        Dumps a list of items into a JSON file.

        Parameters
        ----------
        list_items : list
            The list of items to be dumped.
        file_name : str
            The name of the file to be created.
        buffer_type : str
            The type of buffer to be used.
        '''
        with open(file_name, buffer_type) as f:
            json.dump(list_items, f)

    @classmethod
    def find_by_key_value(cls, location, match_key, match_value):
        '''
        Finds a JSON item by matching a key and value.

        Parameters
        ----------
        location : str
            The location of the JSON file.
        match_key : str
            The key to be matched.
        match_value : str
            The value to be matched.
        '''
        info = []
        data = JSON.load(location)
        def _find_by_key_value(data, match_key, match_value, info):
            for key, value in data.items():
                if (isinstance(match_value, list) == False):
                    if (match_key == key and match_value == value):
                        info.append(data)
                else:
                    for matched_value in match_value:
                        if (match_key == key and matched_value == value):
                            info.append(data)
                if type(value) == type(dict()):
                    _find_by_key_value(value, match_key, match_value, info)
                elif type(value) == type(list()):
                    for val in value:
                        if type(val) == type(str()):
                            pass
                        elif type(val) == type(list()):
                            pass
                        else:
                            _find_by_key_value(val, match_key, match_value, info)
            return info
        
        if (isinstance(match_value, list) == False):
            returned_data = _find_by_key_value(data, match_key, match_value, info)[0]
        else:
            returned_data = _find_by_key_value(data, match_key, match_value, info)
        return returned_data


    @classmethod
    def find_by_key(cls, location, match_key):
        '''
        Finds a JSON item by matching a key.
        
        Parameters
        ----------
        location : str
            The location of the JSON file.
        match_key : str
            The key to be matched.
        '''
        info = []
        data = JSON.load(location)
        def _find_by_key(data, match_key, info):
            for key, value in data.items():
                if (match_key == key):
                    info.append(value)
                if type(value) == type(dict()):
                    _find_by_key(value, match_key, info)
                elif type(value) == type(list()):
                    for val in value:
                        if type(val) == type(str()):
                            pass
                        elif type(val) == type(list()):
                            pass
                        else:
                            _find_by_key(val, match_key, info)
            return info
        
        returned_data = _find_by_key(data, match_key, info)
        return returned_data


    @classmethod
    def get_item_len(cls, data):
        '''
        Gets the length of a JSON item.

        Parameters
        ----------
        data : dict
            The JSON item.
        '''
        return len(data[0])


    @classmethod
    def get_keys(cls, data):
        '''
        Gets the keys of a JSON item.

        Parameters
        ----------
        data : dict
            The JSON item.
        '''
        keys = []
        if isinstance(data, dict):
            keys += data.keys()
            map(lambda x: cls.get_keys(x, keys), data.values())
        elif isinstance(data, list):
            map(lambda x: cls.get_keys(x, keys), data)
        return keys


    @classmethod
    def print(cls, parsed):
        print(json.dumps(parsed, indent=4, sort_keys=True))
