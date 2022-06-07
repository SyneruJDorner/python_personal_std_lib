from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    '''
    This is the base class for the settings.
    The settings are loaded from the environment variables.
    '''
    ROOT_PATH: Optional[str] = ""
    DOWNLOAD_DIRECTORY: Optional[str] = ""
    
    class Config:
        '''
        This is the configuration for the settings.
        Variables are loaded from the .env file.
        '''
        case_sensitive = True
        env_file = ".env"

settings = Settings()