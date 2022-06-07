from watchgod import watch, run_process

def __execute_func(fun, args=[]):
    if (args == []):
        fun()
    else:
        fun(args)

def __detection_process(path, change_events, fun, args=[]):
    event_type = None
    changed_path = None
    for changes in watch(path):
        for e in changes:
            event_type = e[0]
            changed_path = e[1]
            for change_event in change_events:
                if (str(event_type).strip() == str(change_event).strip()):
                    __execute_func(fun, args)
                    print(event_type)
                    print(changed_path)
                    break

def detected_any(path, fun, args=[]):
    change_events = ["Change.added", "Change.deleted", "Change.modified"]
    __detection_process(path, change_events, fun, args)

def detected_added(path, fun, args=[]):
    change_events = ["Change.added"]
    __detection_process(path, change_events, fun, args)

def detected_deleted(path, fun, args=[]):
    change_events = ["Change.deleted"]
    __detection_process(path, change_events, fun, args)

def detected_modified(path, fun, args=[]):
    change_events = ["Change.modified"]
    __detection_process(path, change_events, fun, args)