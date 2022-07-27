import os, sys, time
from re import T
from standard_library import *

#region Selenium
def handle_selenium_multicore(id, data, shared_mem, mutex):
    try:
        print("Started processing for index: " + str(data["unique_data"]))
        selenium.init(default_wait=15)
        selenium.goto(data["website"])
        selenium.inputbox({"by": By.XPATH, "identifier": "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input", "text": data["initial_search"]}).submit()
        selenium.click({"by": By.TAG_NAME, "identifier": "h3"})
        selenium.goto(data["website"])
        selenium.inputbox({"by": By.XPATH, "identifier": "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input", "text": str(data["unique_data"])}).submit()
        time.sleep(5)

        data["completed"] = True
        print(data)
        
        #This locks the cores so that they cannot do anything else while we process the shared data and also log the info
        mutex.acquire(block=True)
        shared_mem.append({ "website": "https://www.google.com", "initial_search": "ookla", "unique_data": str(data["unique_data"]), "completed": True })
        mutex.release()
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, exiting...")
        selenium.quit()
        sys.exit(0)
    
    exit(0)

def selenium_example():
    print("This process will open chrome windows according to the number of logical processors on your machine.")
    print("They will then google a number based on their process batch number.")
    print("This is to prove that you can multi process and thread in python.")
    print("And use it to collectively get indepenent data from different sources or perform different tasks.")


    print("===================================================================================================================")
    print("Do not cancel with a KeyboardInterrupt, this could leave drivers hanging open in the back when using multi core. Just let it finish, should take 30 secs to complete.")
    print("===================================================================================================================")
    print("Do you wish to continue? (Y/N)")
    captured_input = input()
    if (captured_input.lower().strip() not in ["y", "yes"]):
        return

    #Fetch the worl and data prior before assigning it to the batch_work
    batch_work = []
    for i in range(0, 8):
        data = { "website": "https://www.google.com", "initial_search": "ookla", "unique_data": i, "completed": i }
        batch_work.append(data)
    
    #Call the MultiProc class and tell it what function along with the batch_work to execute
    #process_count tells the class how many processes to spawn and lock_main_process tells it to lock the main process
    result = Multi_Proc.execute(target=handle_selenium_multicore, batch_work=batch_work, debug_msg=True, lock_main_process=True)

    for i in range(0, len(batch_work)):
        contains_num = False
        for item in result:
            if int(item["unique_data"]) == i:
                contains_num = True
                break

        if (contains_num == False):
            print("Missing: ", i)

    result = sorted(result, key=lambda d: int(d['unique_data']))
    print(JSON.dumps(result))
    print(len(result))
    pass
#endregion

#region PC Info
def pc_stats_example():
    print("OS:", PC_INFO.system_info.get_system())
    print("CPU:", PC_INFO.cpu_info.get_cpu_name())
    print("RAM:", PC_INFO.memory_info.get_total())
    print("GPU:", PC_INFO.gpu_info.get_gpu_name()[0])
    pass
#endregion

#region Dynamic Code
def dynamic_code_example():
    block = "import time\na=5\nb=6\nb=a+b\n"
    block += "b=a+b\n"
    block += "print(b)\n"
    block += "print('$msg_1')\ntime.sleep($sleep_time)\nprint('$msg_2')\n"

    d_variables = {"$msg_1": "Started sleeping.", "$sleep_time": 5, "$msg_2": "Done sleeping."}
    output = Dynamic_Code_Exec.run_code(block, d_variables)
    print(output)

    pass
#endregion

#region UI App
def ui_app_example():
    print("UI App Example")
    from standard_library.std_lib.ui_lib.ui_lib import UIApp
    UIApp().run()
    pass
#endregion

#region Password Generator
def password_generator_example():
    print(password_generator(8, True, True, True, True))
#endregion

#region Watch God Events
def watch_god_example_test():
    print("Changed")

def watch_god_example():
    watchgod_path = os.path.join(ROOT_PATH.get_path(), "watchgod_path")
    print("Go create a file at the following location:", watchgod_path)
    print("Once created watch the terminal")
    print("Then delete the file you created and watch the terminal once more.")
    detected_any(watchgod_path, watch_god_example_test)
#endregion

#region Update
def update_test():
    update_pip_manager()
    update_pip_packages()
#endregion

def main(argv):    
    if (len(argv) <= 1):
        print("Please enter one of the following args: 'selenium_example'.")
        return

    execute_option = {
        "selenium_ex": selenium_example,
        "pc_stats_ex": pc_stats_example,
        "dynamic_code_ex": dynamic_code_example,
        "ui_app_ex": ui_app_example,
        "gen_pass_ex": password_generator_example,
        "watchgod_ex": watch_god_example,
        "update_ex": update_test,
        "cython_ex": cython_example
    }

    try:
        execute_option[argv[1]]()
    except KeyError:
        args = ["selenium_example", "pc_stats", "dynamic_code", "ui_test", "gen_test", "watchgod_example", "update"]
        print("Please enter one of the following args:")
        print(args)
        return
    pass

if __name__ == "__main__":
    main(sys.argv)
