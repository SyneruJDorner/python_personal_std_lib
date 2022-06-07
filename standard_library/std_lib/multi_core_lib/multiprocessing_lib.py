import time, math, multiprocessing, collections
from multiprocessing import shared_memory, Process, Queue, Lock, Manager

class MultiProc:
    '''
    Multi-Processing Class for multiprocessing
    '''
    logical_processor_count = 0
    process_queue = []
    is_alive = False
    activate_procs = []
    manager = None


    @classmethod
    def __get_cpu_count(cls):
        '''
        Get the number of logical processors
        '''
        return multiprocessing.cpu_count()


    @classmethod
    def __shared_memory(cls):
        '''
        Private funtion
        Create a shared memory object
        '''
        cls.manager = Manager()
        shared_mem = MultiProc.manager.list()

        #shared_mem = batch_work

        # print(batch_work[0]["x"])
        # time.sleep(10000)
        # for i in range(0, len(batch_work)):
        #     name = "'" + str(batch_work[i]["x"]) + "_" + str(batch_work[i]["y"]) + "'"
        #     shared_mem = batch_work
        #     print(name)
        # print(shared_mem)

        return shared_mem

    @classmethod
    def freeze_support(cls):
        '''
        Freeze the support for multiprocessing
        '''
        multiprocessing.freeze_support()


    @classmethod
    def wait_for_multiprocess(cls):
        '''
        Wait for all the processes to finish
        '''
        while len(cls.activate_procs) > 0:
            for i in range(len(cls.activate_procs)):
                if (i >= len(cls.activate_procs)):
                    continue
                if (cls.activate_procs[i] == None):
                    continue
                cls.activate_procs[i].join()
                if cls.activate_procs[i].is_alive():
                    continue
                cls.activate_procs.remove(cls.activate_procs[i])
        return True


    @classmethod
    def execute(cls, target, batch_work, lock_main_process=False, process_count=0, debug_msg=False):
        '''
        Execute the target function in a multiprocessing environment

        Parameters:
        -----------
        target: function
            The function to be executed
        batch_work: list
            The list of work to be executed
        lock_main_process: bool
            Lock the main process (Default: False)
        process_count: int
            The number of processes to be used (Default: 0)
        debug_msg: bool
            Print debug messages (Default: False)
        '''
        MultiProc.freeze_support()
        
        cls.is_alive = True
        cls.__set_logical_processor_count(process_count, debug_msg)
        shared_mem = cls.__shared_memory()
        mutex = Lock()
        current_processes =  [{ "id":(x + 1), "is_alive":False, "process":None, "work_arg":None } for x in range(cls.logical_processor_count)]
        processed_list = []
        cls.process_queue = Queue()

        for queue_item in batch_work:
            cls.process_queue.put(queue_item)
        
        while cls.process_queue.empty() == False:
            for proc_info in current_processes:
                if proc_info["is_alive"] == True or cls.process_queue.empty():
                    continue
                
                # Lets check if the process is still alive, if not, lets start a new one.
                # This portion is responsible for handling the target function, as well as the args.
                # The args passed through are the id, work_args, shared_mem, and mutex.
                # All functions whould be made to accept these args.
                # Example:
                # def target_function(id, work_args, shared_mem, mutex):
                if proc_info["is_alive"] == False:
                    proc_info["work_arg"] = cls.process_queue.get()
                    proc_info["is_alive"] = True
                    proc_info["process"] = Process(target=target, args=[proc_info["id"], proc_info["work_arg"], shared_mem, mutex])
                    processed_list.append(proc_info["process"])
                    cls.activate_procs.append(proc_info["process"])
                    proc_info["process"].start()
                    continue
            
            # Lets wait for the current processes to finish...
            # We want to check if any failed, if they did fail (exit code above 0)
            # we have to process the item again, so we place it back into the 'process_queue'
            for proc_info in current_processes:
                if (proc_info["process"] != None):
                    proc_info["process"].join()

                    if proc_info["process"].exitcode > 0:
                        cls.process_queue.put(proc_info["work_arg"])

                    proc_info["process"] = None
                    proc_info["is_alive"] = False
                    proc_info["work_arg"] = None

        if (lock_main_process == True):
            cls.wait_for_multiprocess()

        return shared_mem


    @classmethod
    def __set_logical_processor_count(cls, process_count, debug_msg):
        '''
        Private function
        Set the logical processor count

        Parameters:
        -----------
        process_count: int
            The number of processes to be used
        debug_msg: bool
            Print debug messages
        '''
        if (process_count == 0):
            cls.logical_processor_count = cls.__get_cpu_count()
        elif (process_count > 0 and process_count <= cls.__get_cpu_count()):
            cls.logical_processor_count = process_count
        else:
            cls.logical_processor_count = cls.__get_cpu_count()
        if (debug_msg == True):
            print("Logical process count: ", cls.logical_processor_count)


#region do work examples
def do_work(id, value, shared_mem, mutex):
    '''
    An example function that executes a total_count calculation

    Parameters:
    -----------
    id: int
        The id of the process
    value: int
        The value to be calculated
    shared_mem: list
        The shared memory object
    mutex: Lock
        The mutex object
    '''
    print("Starting work on process ID - " + str(id) + ". Counting to: " + str(value))
    i = 0
    for _ in range(value):
        i += 1
    mutex.acquire(block=True)
    if ('total_count' not in shared_mem):
        shared_mem['total_count'] = 0
    shared_mem['total_count'] += i
    mutex.release()
    print("Finished work on process ID - " + str(id) + ". Counted to: " + str(value))


def do_work_single():
    '''
    An example function that executes a total_count calculation on a single process
    '''
    mp_info = [10000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000, 80000000, 90000000, 100000000, 110000000, 120000000, 130000000, 140000000, 150000000, 160000000, 170000000]
    shared_mem = 0
    for id in range(len(mp_info)):
        print("Starting work on process ID - " + str(id) + ". Counting to: " + str(mp_info[id]))
        i = 0
        for _ in range(mp_info[id]):
            i += 1
        shared_mem += i
        print("Finished work on process ID - " + str(id) + ". Counted to: " + str(mp_info[id]))
    print(shared_mem)#Correct value should be '1530000000'


def do_work_multiproc():
    '''
    An example function that executes a total_count calculation on multiple processes
    '''
    #multiprocessing.set_start_method('spawn')
    #shared_mem = multiprocessing.Array('i', [0] * 1, lock=True)
    batch_work = [[10000000], [20000000], [30000000], [40000000], [50000000], [60000000], [70000000], [80000000], [90000000], [100000000], [110000000], [120000000], [130000000], [140000000], [150000000], [160000000], [170000000]]
    result = MultiProc.execute(target=do_work, batch_work=(batch_work), process_count=16, lock_main_process=True)
    print(result['total_count'])#Correct value should be '1530000000'
#endregion


#region Prim number calculate
def is_prime(id, start, end, shared_mem, mutex):
    '''
    An example function that calculates prime numbers

    Parameters:
    -----------
    id: int
        The id of the process
    start: int
        The start value
    end: int
        The end value
    shared_mem: list
        The shared memory object
    mutex: Lock
        The mutex object
    '''
    for num in range(start, end):
        if (is_prime_bool(num) == True):
            mutex.acquire(block=True)
            shared_mem[num] = True
            mutex.release()
        #else:
            #shared_mem[num] = False


def is_prime_bool(number):
    '''
    An example function that calculates prime numbers

    Parameters:
    -----------
    number: int
        The number to be checked
    '''
    for i in range (2, 1+ int(math.sqrt(number))):
        if number % i == 0:
            return False
    return True


def prime_number_search():
    '''
    An example function that calculates prime numbers
    '''
    batch_work = [[0, 10000],
                    [10000, 20000],
                    [20000, 30000],
                    [30000, 40000],
                    [40000, 50000],
                    [50000, 60000],
                    [60000, 70000],
                    [70000, 80000],
                    [80000, 90000],
                    [90000, 100000],
                    [100000, 110000],
                    [110000, 120000],
                    [120000, 130000],
                    [130000, 140000],
                    [140000, 150000],
                    [150000, 160000],
                    [160000, 170000]]
    result = MultiProc.execute(target=is_prime, batch_work=(batch_work), process_count=16, lock_main_process=True)
    ordered_prime_nums = dict(collections.OrderedDict(sorted(result.items())))
    print(ordered_prime_nums)
#endregion

'''
def main():
    start = time.time()
    #do_work_single()
    do_work_multiproc()
    #prime_number_search()
    end = time.time()
    print("Total processing time: ", end - start)

if __name__ == "__main__":
    main()
'''