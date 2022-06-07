import requests
import contextlib,sys
from io import StringIO

class Dynamic_Code_Exec():
    '''
    This class is used to execute dynamic code in python.
    '''
    @classmethod
    @contextlib.contextmanager
    def stdoutIO(cls, stdout=None):
        '''
        This method is used to redirect the output of the code to a variable.

        Parameters:
        -----------
        stdout: StringIO
            This is the variable that will hold the output of the code.
        '''
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    @classmethod
    def run_code(cls, block, variables={}):
        '''
        This method is used to execute the code.

        Parameters:
        -----------
        block: String
            This is the code that will be executed.
        variables: Dict
            This is the variables that will be used in the code.
        '''
        compiled_python = []
        if (variables != {}):
            for key in variables.keys():
                block = block.replace(key, str(variables[key]))
        compiled_python.append(compile(block, "<string>", "exec"))
        
        with cls.stdoutIO() as s:
            for python_block in compiled_python:
                exec(python_block)
        return s.getvalue()

    @classmethod
    def run_remote_code(cls, url, variables={}):
        '''
        This method is used to execute the code on a remote server.

        Parameters:
        -----------
        url: String
            This is the url of the server.
        variables: Dict
            This is the variables that will be used in the code.
        '''
        script = requests.get(url).text
        cls.run_code(script, variables)