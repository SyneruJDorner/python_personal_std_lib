import inspect

DEBUG = False

def overload(func):
    return func

def debug_overload(index, optional_1=None, optional_2=None):
    global DEBUG

    if DEBUG == True and index == 1:
        print("\n\n==========================================================")
        print(optional_1)
        print(optional_2)

    if DEBUG == True and index == 2:
        print("==========================================================")

    if DEBUG == True and index == 3:
        print("Found matching function: ", optional_1)
        print("==========================================================")

def overload_class(cls):
    def get_line_number_of_function(func):
        return func.__code__.co_firstlineno

    def get_functions_from_module(app_module):
        list_of_functions = dict(inspect.getmembers(app_module, inspect.isfunction))
        return sorted(list_of_functions.values(), key=lambda x: get_line_number_of_function(x))

    def determine_matching_function_by_args(functions, *args, **kwargs):
        items = list(functions)
        return_func = None
        initializing = False
        for func in items:
            params = inspect.signature(func).parameters
            if len(list(params)) == len(list(args)):
                anotation_args = [item.__class__.__name__ for item in list(args)]
                anotation_params = [item[1].annotation.__name__ for item in list(params.items())]
                
                debug_overload(1, anotation_args, anotation_params)
                    
                if anotation_params == anotation_args:
                    debug_overload(3, func.__name__)
                    return_func = func
                    break
                initializing = True
                debug_overload(2)

        if return_func == None and initializing == True:
            FAILCOLOR = '\033[91m'
            ENDCOLOR = '\033[0m'
            raise Exception(FAILCOLOR + "No matching overload method was found, please ensure all names are unique and that you have created a method with the matching signature." + ENDCOLOR)
        return return_func

    def apply_overload(*functions):
        determine_matching_function_by_args(functions, *functions)
        return lambda *args, **kwargs: determine_matching_function_by_args(list(functions), *args, **kwargs)(*args, **kwargs)

    function_from_module = get_functions_from_module(cls)
    overloaded_cls = apply_overload(*function_from_module)
    return overloaded_cls