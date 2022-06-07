import os, sys, time, multiprocessing, ctypes
from enum import Enum

class Multi_Processing:
    '''
    This class is used to create a multi-processing object.
    '''
    timer_process = None
    multiprocessing_timer = multiprocessing.Value(ctypes.c_double, 0.0)  # (type, init value)
    jobs = []
    app_list_to_kill = ["java.exe", "wrapper.exe", "python.exe"]


    @staticmethod
    def get_multi_processing_variables():
        '''
        This method is used to get the multi-processing variables.
        '''
        return { "multi_processing_timer": Multi_Processing.multiprocessing_timer }


    @staticmethod
    def exit():
        '''
        This method is used to exit the multi-processing.
        '''
        for process in Multi_Processing.jobs:
            process.terminate()

        if (Multi_Processing.timer_process != None):
            Multi_Processing.timer_process.terminate()
        
        for app_name in Multi_Processing.app_list_to_kill:
            os.system("TASKKILL /F /IM " + app_name)
        
        print("Should have quit!")
        sys.exit(0)


    @staticmethod
    def append_multi_process(target, args):
        '''
        This method is used to append a multi-process to the list of jobs.

        Parameters:
        -----------
        target: function
            The function to be executed.
        args: tuple
            The arguments to be passed to the function.
        '''
        args = list(args)
        args.append(Multi_Processing.get_multi_processing_variables())
        args = tuple(args)

        process = multiprocessing.Process(target=target, args=args)
        Multi_Processing.jobs.append(process)


    @staticmethod
    def start_multi_processing():
        '''
        This method is used to start the multi-processing.
        '''
        for j in Multi_Processing.jobs:
            j.start()

        Multi_Processing.start_timer_multi_process(20)

        for j in Multi_Processing.jobs:
            j.join()


    @staticmethod
    def start_timer_multi_process(limit=20):
        '''
        This method is used to start the timer for the multi-processing.

        Parameters:
        -----------
        limit: int
            The limit of the timer. The default is 20.
        '''
        if (Multi_Processing.timer_process != None):
            Multi_Processing.timer_process.terminate()
        Multi_Processing.timer_process = multiprocessing.Process(target=Multi_Processing.m_timer, args=(Multi_Processing.multiprocessing_timer, limit))
        Multi_Processing.timer_process.start()


    @staticmethod
    def reset_timer_multi_process(multi_process_variables):
        '''
        This method is used to reset the timer for the multi-processing.

        Parameters:
        -----------
        multi_process_variables: dict
            The multi-processing variables.
        '''
        Multi_Processing.m_reset_timer(multi_process_variables)


    @staticmethod
    def stop_timer_multi_process():
        '''
        This method is used to stop the timer for the multi-processing.
        '''
        if (Multi_Processing.timer_process != None):
            Multi_Processing.timer_process.terminate()
            print("Stopped Timer Multi Process.")


    @staticmethod
    def m_reset_timer(multi_process_timer):
        '''
        This method is used to reset the timer for the multi-processing.

        Parameters:
        -----------
        multi_process_timer: multiprocessing.Value
            The multi-processing timer.
        '''
        multi_process_timer.value = 0


    @staticmethod
    def m_timer(multiprocessing_timer, limit):
        '''
        This method is used to start the timer for the multi-processing.

        Parameters:
        -----------
        multiprocessing_timer: multiprocessing.Value
            The multi-processing timer.
        limit: int
            The limit of the timer.
        '''
        multiprocessing_timer.value = 0
        while (multiprocessing_timer.value < limit):
            multiprocessing_timer.value += 0.5
            time.sleep(0.5)
            print("Multicore countdown: " + str(limit - multiprocessing_timer.value))
        Multi_Processing.Exit()
        raise Exception("Timeout error, failed to find the image onscreen.")
