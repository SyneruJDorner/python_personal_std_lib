from pathlib import Path

class DOWNLOAD_PATH():
    '''
    This class is used to store the download path of the application.
    '''
    __download_path = ""

    @staticmethod
    def get_path():
        '''
        This method is used to get the download path of the application.
        '''
        DOWNLOAD_PATH.__download_path = str(Path.home() / "Downloads")
        return str(DOWNLOAD_PATH.__download_path).replace("\\.\\", "\\").replace("/./", "/")