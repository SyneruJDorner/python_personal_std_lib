import os, sys

class ROOT_PATH():
    '''
    This class is used to get the root path of the project.
    '''
    __root_path = ""

    @staticmethod
    def get_path():
        '''
        This method is used to get the root path of the project.
        '''
        ROOT_PATH.__root_path = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        return str(ROOT_PATH.__root_path).replace("\\.\\", "\\").replace("/./", "/")