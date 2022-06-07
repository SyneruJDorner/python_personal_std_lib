import os, sys
import inspect

class FILE_PATH():
    '''
    This class is used to get the file path of the current file.
    '''
    __file_path = ""

    @staticmethod
    def get_path():
        '''
        This method is used to get the file path of the current file.
        '''
        basePath = os.path.dirname(sys.modules['__main__'].__file__)
        from_file = os.path.relpath(inspect.stack()[1][1], basePath)

        if getattr(sys, 'frozen', False):
            FILE_PATH.__file_path = sys._MEIPASS
        else:
            FILE_PATH.__file_path = os.path.dirname(os.path.abspath(from_file))
        os.chdir(FILE_PATH.__file_path)
        return str(FILE_PATH.__file_path).replace("\\.\\", "\\").replace("/./", "/")