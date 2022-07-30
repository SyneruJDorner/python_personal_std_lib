from __future__ import print_function
import builtins as __builtin__
from threading import Timer

import sys, os, datetime, re, atexit, time, traceback
from inspect import getframeinfo, stack
from pathlib import Path
from enum import Enum
from standard_library.std_lib.teams.teams import send_feedback


#region Printing related
class TextColours(object):
    @staticmethod
    def Black():
        return "\x1b[1;30m"

    @staticmethod
    def Red():
        return "\x1b[1;31m"

    @staticmethod
    def Green():
        return "\x1b[1;32m"

    @staticmethod
    def Yellow():
        return "\x1b[1;33m"

    @staticmethod
    def Blue():
        return "\x1b[1;34m"

    @staticmethod
    def Magenta():
        return "\x1b[1;35m"

    @staticmethod
    def Cyan():
        return "\x1b[1;36m"

    @staticmethod
    def White():
        return "\x1b[1;37m"

    @staticmethod
    def BrightBlack():
        return "\x1b[1;90m"

    @staticmethod
    def BrightRed():
        return "\x1b[1;91m"

    @staticmethod
    def BrightGreen():
        return "\x1b[1;92m"

    @staticmethod
    def BrightYellow():
        return "\x1b[1;93m"

    @staticmethod
    def BrightBlue():
        return "\x1b[1;94m"

    @staticmethod
    def BrightMagenta():
        return "\x1b[1;95m"

    @staticmethod
    def BrightCyan():
        return "\x1b[1;96m"

    @staticmethod
    def BrightWhite():
        return "\x1b[1;97m"

    @staticmethod
    def ResetColour():
        #means we reset the colour usage is like <HTML></HTML>
        #after calling a colour you must ens the colour
        return "\x1b[1;0m"     


def print(*args, **kwargs):
    try:
        for arg in args:
            Process_Logger.log(arg, log_level=Process_Logger.LOG_LEVEL.DEBUG, caller=getframeinfo(stack()[1][0]))
    except:
        pass
    return __builtin__.print(*args, **kwargs)


def print_warning(*args, **kwargs):
    try:
        for arg in args:
            Process_Logger.log(arg, log_level=Process_Logger.LOG_LEVEL.WARNING, caller=getframeinfo(stack()[1][0]))
    except:
        pass
    return __builtin__.print(*args, **kwargs)


def print_error(*args, **kwargs):
    try:
        for arg in args:
            Process_Logger.log(arg, log_level=Process_Logger.LOG_LEVEL.ERROR, caller=getframeinfo(stack()[1][0]))
    except:
        pass
    return __builtin__.print(*args, **kwargs)

def print_without_logs(*args, **kwargs):
    return __builtin__.print(*args, **kwargs)

#endregion


#region Decorator
def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as error:
            error_string = traceback.format_exc().split("\n")
            error_msg = error_string[len(error_string) - 2].strip()
            error_file = error_string[len(error_string) - 4].split(", ")[0].replace("File ", "").replace("\"", "").strip()
            
            #TEAMS ERROR MESSAGE
            current_error = "Error: " + Process_Logger.get_process_name() + "\n\n"
            current_error += "======================================\n\n"
            current_error += str(traceback.format_exc())
            current_error += "\n\n======================================"
            send_feedback(current_error)
            
            #TERMINAL ERROR MESSAGE
            print_without_logs("\n\n======================================")
            error_strings = traceback.format_exc().split("\n")
            error_strings = [x.strip(' ') for x in error_strings]
            error_msg = error_strings[len(error_strings) - 2].strip()
            error_file = error_strings[len(error_strings) - 4].split(", ")[0].replace("File ", "").replace("\"", "").strip()
            send_feedback(current_error)

            line_header = ""
            for error_string in error_strings:
                if ("File " in error_string and " line " in error_string and " in " in error_string):
                    error_string = error_string.replace("/", "\\").replace("\\\\", "\\")
                    file_path_header = error_string.split("File ")[1].split(", line ")[0].strip()
                    line_header = error_string.split(", line ")[1].split(", in ")[0].strip()
                    in_file_header = error_string.split(", in ")[1].strip()

                    if "inner_function" not in in_file_header:
                        print_without_logs("Function: " + TextColours.Red() + in_file_header + TextColours.ResetColour())
                    
                    #We print the coloured error message to the terminal
                    if "process_logs.py" not in file_path_header and "inner_function" not in in_file_header:
                        logging_info_msg = ("File " + TextColours.Red() + "{0}" + TextColours.ResetColour() + ", line " + TextColours.Red() + "{1}" + TextColours.ResetColour() + ", in " + TextColours.Red() + "{2}" + TextColours.ResetColour()).format(file_path_header, line_header, in_file_header)
                        print_without_logs(logging_info_msg)

                    #We print the error without colours to the log file
                    logging_info_msg = ("File {0} , line {1}, in {2}").format(file_path_header, line_header, in_file_header)
                    Process_Logger.log(logging_info_msg, log_level=Process_Logger.LOG_LEVEL.ERROR, caller=getframeinfo(stack()[1][0]))
                    continue
                if (error_string not in ["Traceback (most recent call last):", "func(*args, **kwargs)"] and ".<locals>." not in error_string):
                #if ("Traceback (most recent call last):" not in error_string and "func(*args, **kwargs)" not in error_string and ".<locals>." not in error_string):
                    print_without_logs("Line: " + TextColours.Red() + str(line_header) + TextColours.ResetColour() + " | Execution of code: " + TextColours.Cyan() + str(error_string) + TextColours.ResetColour())
            sys.stdout.write("\033[F")
            print_without_logs("======================================\n")
            
            if (len(error_file) >= 2):
                error_line = error_file.replace("line ", "").strip()
            else:
                error_line = "Unknown"

            #PROMPT TO ASK USER IF THEY WANT TO READ MORE INFO ON THIS ERROR
            def quit():
                print_without_logs("Timed out, closing application")
                os._exit(0)

            timeout = 10
            t = Timer(timeout, quit)
            t.start()
            answer = input(TextColours.Red() + "Would you like to display the full stack trace?" + TextColours.ResetColour() + " (Y/N)\n")
            t.cancel()

            sys.stdout.write("\033[F")
            if answer =="yes" or answer =="y":
                sys.stdout.write("\033[K")
                sys.stdout.write("\033[F")
                print_without_logs(" " * 60)
                sys.stdout.write("\033[F")
                print_without_logs("\n======================================")
                traceback.print_exc()
                print_without_logs("======================================\n")
            else:
                sys.stdout.write("\033[F")

            #Ignore quit messages, as these aren't legit errors
            if (error_msg != "SystemExit"):
                #region Handle Error Printing
                Process_Logger.log_exception(error, { "error_file": error_file, "error_line": error_line, "error_msg": error_msg })
                #endregion

                #region Handle Logging Info Printing
                Process_Logger.handle_traceback_log()
                #endregion

                #region Send email failed
                Process_Logger.send_email()
                #endregion

    return inner_function
#endregion


#region Logging
class Process_Logger():
    #region VARIABLES
    __process_name = "log_app"
    __process_name_exception = "log_app_exception"
    __line_handler = 0
    __start_time = None
    __end_time = None
    __application_crash = False
    __saved_params = []
    __current_lifespan = 0
    __eventTime = None
    __email_ready = False
    __application_path = Path(__file__).parent.parent
    __log_path = os.path.join(__application_path, "_Logs")
    #endregion


    #region Init
    @classmethod
    def init(cls, process_name):
        process_name = process_name.replace(" ", "_")
        process_name_exception = process_name + "_Exception"
        cls.__set_process_name(process_name)
        cls.__set_process_name_exception(process_name_exception)
        cls.__log_path = os.path.join(cls.__application_path, "process_logs\\Logs\\")
        cls.__log_text_file = process_name + ".log"

        #CREATE FOLDER PATH
        if not os.path.exists(cls.__log_path):
            Path(cls.__log_path).mkdir(parents=True, exist_ok=True)

        #CLEAR PREVIOUS TRACEBACK
        exception_log_path = cls.__log_path + cls.__process_name_exception + ".log"
        open(exception_log_path, 'w').close()

        #CREATE LOG FILE
        cls.__log_text_file = os.path.join(cls.__log_path, cls.__log_text_file)

        if not os.path.exists(cls.__log_text_file):
            open(cls.__log_text_file, 'w').close()

        cls.__start_header()
        Path(cls.__log_path).mkdir(parents=False, exist_ok=True)
        atexit.register(cls.__exit_header)
        cls.__eventTime = datetime.datetime.now()
    #endregion


    #region Start & Exit Handles
    @classmethod
    def __start_header(cls):
        cls.__start_time = datetime.datetime.now()
        cls.__insert_line(("==========[STARTED PROCESS: {0}]======================================================================================================").format(cls.__start_time))


    @classmethod
    def __exit_header(cls):
        print("Successfully wrote logs for the bot and what was processed/failed!")
        cls.__end_time = datetime.datetime.now()

        cls.__insert_line(("{0}: [APPLICATION LIFESPAN: {1}]").format(cls.__end_time, cls.__get_current_lifespan()))

        if cls.__get_status_result() == True:
            cls.__insert_line(("{0}: [APPLICATION RESULTED IN: {1}]").format(cls.__end_time, "CRASH"))
        else:
            cls.__insert_line(("{0}: [APPLICATION RESULTED IN: {1}]").format(cls.__end_time, "SUCCESS"))
            
            if (cls.__email_ready == True):
                cls.send_email()

        cls.__insert_line(("==========[FINISHED PROCESS: {0}]=====================================================================================================").format(cls.__end_time) + '\n')

    @classmethod
    def __calculate_process_time(cls):
        processTime = datetime.datetime.now() - cls.__eventTime
        cls.__eventTime = datetime.datetime.now()
        return processTime
    #endregion


    #region Extension Functions
    @classmethod
    def __set_column_width(cls, writer, dataframe):
        def get_col_widths(dataframe):
            idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
            return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]

        worksheet = writer.sheets["Standard"]
        for i, width in enumerate(get_col_widths(dataframe)):
            worksheet.set_column(i, i, width)


    @classmethod
    def __insert_line(cls, line):
        f = open(cls.__log_text_file, "r")
        contents = f.readlines()
        f.close()

        contents.insert(cls.__line_handler, str(line) + '\n')

        f = open(cls.__log_text_file, "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()
        cls.__line_handler += 1


    @classmethod
    def __set_process_name(cls, defined_name):
        cls.__process_name = defined_name


    @classmethod
    def __set_process_name_exception(cls, defined_name):
        cls.__process_name_exception = defined_name


    @classmethod
    def get_process_name(cls):
        return cls.__process_name


    @classmethod
    def __number_of_fails(cls):
        count = 0

        with open(cls.__log_text_file) as f:
            for line in f:
                count += line.count("[APPLICATION RESULTED IN: CRASH]")
        return count


    @classmethod
    def __number_of_success(cls):
        count = 0
        
        with open(cls.__log_text_file) as f:
            for line in f:
                count += line.count("[APPLICATION RESULTED IN: SUCCESS]")
        return count


    @classmethod
    def __success_to_fail_ratio(cls):
        return (cls.__number_of_success() / cls.__number_of_fails())


    @classmethod
    def __get_start_time(cls):
        return cls.__start_time


    @classmethod
    def __get_end_time(cls):
        return cls.__end_time


    @classmethod
    def __get_current_lifespan(cls):
        cls.__current_lifespan = cls.__end_time - cls.__start_time
        return (cls.__current_lifespan)


    @classmethod
    def __average_lifespan(cls):
        pattern = re.compile(r'\[APPLICATION LIFESPAN: (?:2[0-3]|[01]?[0-9]):[0-5][0-9]:[0-5][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]\]')
        parretnTime = re.compile(r'(?:2[0-3]|[01]?[0-9]):[0-5][0-9]:[0-5][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]')
        items = []

        for _, line in enumerate(open(cls.__log_text_file)):
            for _ in re.finditer(pattern, line):
                convertedTime = datetime.datetime.strptime(re.findall(parretnTime, line)[1], "%H:%M:%S.%f")
                items.append(datetime.timedelta(hours=convertedTime.hour, minutes=convertedTime.minute, seconds=convertedTime.second, microseconds=convertedTime.microsecond))
                break

        average_timedelta = sum(items, datetime.timedelta(0)) / len(items)
        return average_timedelta


    @classmethod
    def __shortest_lifespan(cls):
        pattern = re.compile(r'\[APPLICATION LIFESPAN: (?:2[0-3]|[01]?[0-9]):[0-5][0-9]:[0-5][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]\]')
        parretnTime = re.compile(r'(?:2[0-3]|[01]?[0-9]):[0-5][0-9]:[0-5][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]')
        items = []

        for _, line in enumerate(open(cls.__log_text_file)):
            for _ in re.finditer(pattern, line):
                convertedTime = datetime.datetime.strptime(re.findall(parretnTime, line)[1], "%H:%M:%S.%f")
                items.append(datetime.timedelta(hours=convertedTime.hour, minutes=convertedTime.minute, seconds=convertedTime.second, microseconds=convertedTime.microsecond))
                break

        min_timedelta = min(items)
        return min_timedelta


    @classmethod
    def __longest_lifespan(cls):
        pattern = re.compile(r'\[APPLICATION LIFESPAN: (?:2[0-3]|[01]?[0-9]):[0-5][0-9]:[0-5][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]\]')
        parretnTime = re.compile(r'(?:2[0-3]|[01]?[0-9]):[0-5][0-9]:[0-5][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]')
        items = []

        for _, line in enumerate(open(cls.__log_text_file)):
            for _ in re.finditer(pattern, line):
                convertedTime = datetime.datetime.strptime(re.findall(parretnTime, line)[1], "%H:%M:%S.%f")
                items.append(datetime.timedelta(hours=convertedTime.hour, minutes=convertedTime.minute, seconds=convertedTime.second, microseconds=convertedTime.microsecond))
                break

        max_timedelta = max(items)
        return max_timedelta


    @classmethod
    def __get_status_result(cls):
        return cls.__application_crash


    @classmethod
    def __save_parameter(cls, param):
        cls.__saved_params.append(param)


    @classmethod
    def __get_parameters(cls):
        string_params = ','.join(cls.__saved_params)
        return string_params


    @classmethod
    def __convert_timedelta(cls, duration):
        days, seconds = duration.days, duration.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return days, hours, minutes, seconds
    #endregion


    #region Public Methods
    class LOG_LEVEL(str, Enum):
        INFO = 'INFO',
        DEBUG = 'DEBUG',
        WARNING = 'WARNING',
        ERROR = 'ERROR',
        CRITICAL = 'CRITICAL'


    @classmethod
    def log(cls, param, log_level=LOG_LEVEL.DEBUG, caller=None):
        if (caller == None):
            caller = getframeinfo(stack()[1][0])

        file_name = str(caller.filename).replace(".\\", "")
        if (str(cls.__application_path) in str(caller.filename)):
            file_name = str(caller.filename).replace(str(cls.__application_path), "").split("\\")[1].replace(".\\", "")

        info = { "file": ".\\" + file_name, "line": caller.lineno }
        level = str(log_level).replace("LOG_LEVEL.", "")
        data_param = cls.__print_table_line(datetime.datetime.now(), info["file"], info["line"], level, str(param))
        cls.__insert_line(data_param)
        cls.__save_parameter(param)
        cls.__calculate_process_time()


    @classmethod
    def log_exception(cls, msg, frameinfo=None):
        cls.__application_crash = True
        caller = frameinfo
        level = str(cls.LOG_LEVEL.ERROR).replace("LOG_LEVEL.", "")

        if (caller == None):
            caller = getframeinfo(stack()[1][0])
            
            file_name = str(caller.filename).replace(".\\", "")
            if (str(cls.__application_path) in str(caller.filename)):
                file_name = str(caller.filename).replace(str(cls.__application_path), "").split("\\")[1].replace(".\\", "")

            data_path_tracking = cls.__print_table_line(datetime.datetime.now(), file_name, caller.lineno, level, str(msg))
        else:
            file_name = str(caller["error_file"]).replace(".\\", "")
            if (str(cls.__application_path) in caller["error_file"]):
                file_name = caller["error_file"].replace(str(cls.__application_path), "").split("\\")[1].replace(".\\", "")

            info = { "file": ".\\" + file_name, "line": caller["error_line"] }
            data_path_tracking = cls.__print_table_line(datetime.datetime.now(), info["file"], info["line"], level, str(msg))
        cls.__insert_line(data_path_tracking)


    @classmethod
    def handle_traceback_log(cls):
        logging_file = cls.__log_path + cls.__process_name + ".log"
        logging_info_msg = (TextColours.Green() + "{0:20}" + TextColours.ResetColour() + "{1}").format("Logged History" + ':', str(logging_file).replace(str(cls.__application_path) + "\\", ".\\"))
        print_without_logs(logging_info_msg)

        exception_log_path = cls.__log_path + cls.__process_name_exception + ".log"
        if (os.path.exists(exception_log_path) == False):
            open(exception_log_path, 'w').close()
        
        exception_log = open(exception_log_path, "w")
        exception_log.write(str(traceback.format_exc()).split("func(*args, **kwargs)")[1].strip())
        exception_log.close()

        if (os.path.exists(exception_log_path) == True):
            logging_info_msg = (TextColours.Green() + "{0:20}" + TextColours.ResetColour() + "{1}").format("Logged Traceback" + ':', str(exception_log_path).replace(str(cls.__application_path) + "\\", ".\\"))
            print_without_logs(logging_info_msg)


    @classmethod
    def enable_emails(cls, _to, _email):
        cls.__email_ready = True


    @classmethod
    def send_email(cls):
        if (cls.__email_ready == True):
            #Send emails on errors here
            pass


    @classmethod
    def __print_table_line(cls, time_now, file, line, level, msg):
        data = ["%s: [LOCATION: %s:%s]" % (time_now, file, line), "[LEVEL: %s]" % (level), "[MSG: %s]" % (msg)]

        space_char = ' '
        level_start_point = 75
        message_start_point = 10
        level_start_point = max(5, level_start_point)

        if (level_start_point <= len(data[0])):
            cut_str =  '{:.' + str(level_start_point - 4) + '}'
            data[0] = cut_str.format(data[0]) + '...' + space_char

        if ((level_start_point + message_start_point) <= len(data[1])):
            cut_str =  '{:.' + str(message_start_point - 4) + '}'
            data[1] = cut_str.format(data[1]) + '...' + space_char

        level_str = '{:' + space_char + '>' + str(level_start_point - len(data[0]) + len(str(data[1]))) + '}'
        message_str = '{:' + space_char + '>' + str((message_start_point + 17) - len(data[1]) + len(str(data[2]))) + '}'
        return data[0] + level_str.format(str(data[1])) + message_str.format(str(data[2]))
    #endregion
#endregion