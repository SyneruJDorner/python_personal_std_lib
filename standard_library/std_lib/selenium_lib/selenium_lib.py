import sys, os, atexit, time
from pathlib import Path
from enum import Enum

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



class By(str, Enum):
    '''
    Enum for By.
        - By.ID
        - By.NAME
        - By.CLASS_NAME
        - By.CSS_SELECTOR
        - By.LINK_TEXT
        - By.PARTIAL_LINK_TEXT
        - By.TAG_NAME
        - By.XPATH
    '''
    ID = By.ID
    XPATH = By.XPATH
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    NAME = By.NAME
    TAG_NAME = By.TAG_NAME
    CLASS_NAME = By.CLASS_NAME
    CSS_SELECTOR = By.CSS_SELECTOR


class selenium():
    '''
    Selenium class for interacting with a web browser.
    '''
    __driver = None
    __wait = None
    __default_wait = None
    __downloads_path = ""
    __current_target_elem = None
    __actions = None

    @classmethod
    def init(cls, default_wait=20):
        '''
        Initialize the selenium class.

        Parameters:
        -----------
        default_wait : int
            Default wait time for selenium. (Default: 20)
        '''
        cls.__driver_init()
        cls.driver_set_timeout(default_wait)
        cls.__default_wait = default_wait
        cls.__actions = ActionChains(cls.__driver)
        atexit.register(cls.quit)

    @classmethod
    def quit(cls):
        '''
        Private Function
        Quits the selenium driver.
        '''
        print("Closing all selenium windows, not the drivers! This means we can still run the sselenium refs.")
        cls.__driver.quit()

    @classmethod
    def __driver_init(cls):
        '''
        Private Function
        Initializes the selenium driver.
        '''
        cls.__downloads_path = str(Path.home() / "Downloads")
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--start-maximized")
        options.add_argument('--no-sandbox')
        options.page_load_strategy = 'eager'
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs',  {
            "download.default_directory": cls.__downloads_path,
            "plugins.always_open_pdf_externally": True,
            "download.directory_upgrade": True,
            "plugins.plugins_disabled": ["Chrome PDF Viewer"]
        })
        cls.__driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())

    @classmethod
    def driver_set_timeout(cls, seconds=20):
        '''
        Set the timeout for the selenium driver.
        
        Parameters:
        -----------
        seconds : int
            Timeout in seconds. (Default: 20)
        '''
        cls.__wait = WebDriverWait(cls.__driver, seconds)

    @classmethod
    def driver_set_timeout_to_default_wait(cls):
        '''
        Set the timeout for the selenium driver to the default wait time.
        '''
        cls.__wait = WebDriverWait(cls.__driver, cls.__default_wait)

    @classmethod
    def has_page_loaded(cls):
        '''
        Check if the page has loaded.
        '''
        page_state = cls.__driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    @classmethod
    def wait_for_page_to_load(cls):
        '''
        Wait for the page to load.
        '''
        countdown = 10
        
        while (True):
            page_state = cls.__driver.execute_script('return document.readyState;')
            if (page_state == 'complete'):
                time.sleep(1)
                cls.__driver.implicitly_wait(1)
                return True

            countdown = countdown - 1
            if (countdown == 0):
                time.sleep(1)
                cls.__driver.implicitly_wait(1)
                return False



    @classmethod
    def __scroll_to_element_automated(cls, element):
        '''
        Private Function
        Scrolls to the element.

        Parameters:
        -----------
        element : selenium.webdriver.remote.webelement.WebElement
            The element to scroll to.
        '''
        cls.__actions.move_to_element(element).perform()

    @classmethod
    def goto(cls, link):
        '''
        Go to a link.

        Parameters:
        -----------
        link : str
            The link to go to.
        '''
        if ("https://" in link):
            cls.__driver.get(link)
        elif ("http://" in link):
            cls.__driver.get(link)
        else:
            print("An invalid link was provided, please provide a link containing 'http://' or 'https://'")
            cls.__quit()


    @classmethod
    def __find_matching_element(cls, defined_by, identifier):
        '''
        Private Function
        Finds a matching element.

        Parameters:
        -----------
        defined_by : selenium.webdriver.common.by.By
            The type of element to find.
        identifier : str
            The identifier of the element to find.
        '''
        elem = None
        if (defined_by == By.ID):
            elem = cls.__driver.find_element_by_id(identifier)
        elif (defined_by == By.XPATH):
            elem = cls.__driver.find_element_by_xpath(identifier)
        elif (defined_by == By.LINK_TEXT):
            elem = cls.__driver.find_element_by_link_text(identifier)
        elif (defined_by == By.PARTIAL_LINK_TEXT):
            elem = cls.__driver.find_element_by_partial_link_text(identifier)
        elif (defined_by == By.NAME):
            elem = cls.__driver.find_element_by_name(identifier)
        elif (defined_by == By.TAG_NAME):
            elem = cls.__driver.find_element_by_tag_name(identifier)
        elif (defined_by == By.CLASS_NAME):
            elem = cls.__driver.find_element_by_class_name(identifier)
        elif (defined_by == By.CSS_SELECTOR):
            elem = cls.__driver.find_element_by_css_selector(identifier)
        cls.__current_target_elem = elem
        return elem


    @classmethod
    def __find_element_steps(cls, json_data, interactable=False):
        '''
        Private Function
        Finds an element.

        Parameters:
        -----------
        json_data : dict
            The json data to use.
        interactable : bool
            Whether or not to interact with the element. (Default: False)
        '''
        cls.wait_for_page_to_load()
        cls.__wait = WebDriverWait(cls.__driver, 10)

        while (True):
            try:
                cls.__wait.until(EC.presence_of_element_located((json_data["by"], json_data["identifier"])))
                break
            except:
                print("Could not find element By: " + str(json_data["by"]) + " & XPath: " + str(json_data["identifier"]) + ", refreshing page!")
                cls.__driver.execute_script("location.reload(true);")
                time.sleep(2)
                cls.__driver.implicitly_wait(2)
                cls.wait_for_page_to_load()
            time.sleep(1)

        if (interactable == True):
            while (True):
                try:
                    cls.__wait.until(EC.element_to_be_clickable((json_data["by"], json_data["identifier"])))
                    break
                except:
                    print("Could not find element, refreshing page!")
                    cls.__driver.execute_script("location.reload(true);")
                    time.sleep(2)
                    cls.__driver.implicitly_wait(2)
                    cls.wait_for_page_to_load()
                time.sleep(1)

        elem = cls.__find_matching_element(json_data["by"], json_data["identifier"])
        
        cls.__scroll_to_element_automated(elem)
        return elem

    @classmethod
    def close_current_window(cls):
        '''
        Close the current window.
        '''
        cls.__driver.close()


    @classmethod
    def swicth_to_new_window(cls, index=1):
        '''
        Switch to a new window.

        Parameters:
        -----------
        index : int
            The index of the window to switch to. (Default: 1)
        '''
        popup_window = cls.__driver.window_handles[index]
        cls.__driver.switch_to_window(popup_window)


    @classmethod
    def get_window_title(cls):
        '''
        Get the title of the current window.
        '''
        return cls.__driver.title


    @classmethod
    def swicth_to_default_window(cls):
        '''
        Switch to the default window.
        '''
        cls.__driver.switch_to_window(cls.__driver.window_handles[0])


    @classmethod
    def send_keys(cls, input_text):
        '''
        Send keys to the current target element.

        Parameters:
        -----------
        input_text : str
            The text to send to the current target element.
        '''
        actions = ActionChains(cls.__driver)
        actions.send_keys(input_text)
        actions.perform()


    @classmethod
    def find_element_by_inner_text(cls, inner_text):
        '''
        Find an element by inner text.

        Parameters:
        -----------
        inner_text : str
            The inner text to find.
        '''
        by_info = By.XPATH
        xpath_info = "//*[contains(text(), '" + inner_text + "')]"
        cls.__wait.until(EC.presence_of_element_located((by_info, xpath_info)))
        cls.__wait.until(EC.element_to_be_clickable((by_info, xpath_info)))
        elem = cls.__driver.find_element_by_xpath(xpath_info)
        return elem


    @classmethod
    def enter_iframe(cls, data={"by": By.XPATH, "identifier": ""}):
        '''
        Enter an iframe.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": ""})
        '''
        iframe = cls.__find_matching_element(data["by"], data["identifier"])
        cls.__driver.switch_to.frame(iframe)


    @classmethod
    def leave_iframes(cls):
        '''
        Leave all iframes.
        '''
        cls.__driver.switch_to.default_content()


    @classmethod
    def switch_to_default_content(cls):
        '''
        Switch to the default content.
        '''
        cls.__driver.switch_to.default_content()


    @classmethod
    def inputbox(cls, data={"by": By.XPATH, "identifier": "", "text": ""}):
        '''
        Input text into an input box.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": "", "text": ""})
        '''
        elem = cls.__find_element_steps(json_data=data, interactable=True)
        elem.clear()
        elem.send_keys(data["text"])
        return cls


    @classmethod    
    def input_file_type(cls, data={"by": By.XPATH, "identifier": "", "path": ""}):
        '''
        Input a file type into an input box.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": "", "path": ""})
        '''
        elem = cls.__find_element_steps(json_data=data, interactable=False)
        elem.send_keys(data["path"])
        return cls


    @classmethod
    def submit(cls):
        '''
        Submit the current target element.
        '''
        cls.__current_target_elem.send_keys(Keys.RETURN)


    @classmethod
    def click(cls, data={"by": By.XPATH, "identifier": ""}):
        '''
        Click on an element.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": ""})
        '''
        elem = cls.__find_element_steps(json_data=data, interactable=True)
        elem.click()

    @classmethod
    def hover(cls, data={"by": By.XPATH, "identifier": ""}):
        '''
        Hover over an element.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": ""})
        '''
        elem = cls.__find_element_steps(json_data=data, interactable=False)
        hover = ActionChains(cls.__driver).move_to_element(elem)
        hover.perform()


    @classmethod
    def dropdown(cls, data={"by": By.XPATH, "identifier": "", "option": ""}):
        '''
        Select an option from a dropdown.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": "", "option": ""})
        '''
        elem = cls.__find_element_steps(json_data=data, interactable=True)
        elem.click()

        for option in elem.find_elements_by_tag_name('option'):
            if option.text.lower().strip() == data["option"].lower().strip():
                cls.__current_target_elem = option
                option.click()
                return cls


    @classmethod
    def listbox(cls, data={"by": By.XPATH, "identifier": "", "option": ""}):
        '''
        Select an option from a listbox.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": "", "option": ""})
        '''
        if "by" not in data and "identifier" not in data:
            time.sleep(1)
            elem_children = cls.__current_target_elem.find_elements_by_xpath(".//*")
        else:
            elem = cls.__find_element_steps(json_data=data, interactable=True)
            elem_children = elem.find_elements_by_xpath(".//*")

        for option in elem_children:
            if option.get_attribute('innerText') == data["option"]:
                cls.__current_target_elem = option
                option.click()
                return cls


    @classmethod
    def get_child_count(cls, data={"by": By.XPATH, "identifier": ""}):
        '''
        Get the number of children of an element.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": ""})
        '''
        elem = cls.__find_element_steps(json_data=data, interactable=False)
        elem_children = elem.find_elements_by_xpath("./*")
        return len(elem_children)


    @classmethod
    def click_child_with_name(cls, data={"by": By.XPATH, "identifier": "", "text": ""}):
        '''
        Click on a child element with a specific name.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": "", "text": ""})
        '''
        elem = cls.__find_element_steps(json_data=data, interactable=False)
        child_list = elem.find_elements_by_xpath("./*")
        for child in child_list:
            child_inner_text = child.get_attribute('innerText')

            if (child_inner_text == data["text"]):
                child.click()
                break


    @classmethod
    def get_sub_tree_child_count(cls, data={"by": By.XPATH, "identifier": ""}):
        '''
        Get the number of children of an element.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": ""})
        '''
        elem = cls.__find_element_steps(json_data=data, interactable=False)
        elem_children = elem.find_elements_by_xpath(".//*")
        return len(elem_children)


    @classmethod
    def wait_for_download(cls, timeout, nfiles=None):
        '''
        Wait for a download to complete.

        Parameters:
        -----------
        timeout : int
            The timeout to wait for the download to complete.
        nfiles : int
            The number of files to wait for. (Default: None)
        '''
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < timeout:
            time.sleep(0.1)
            dl_wait = False
            files = os.listdir(cls.__downloads_path)
            if nfiles and len(files) != nfiles:
                dl_wait = True
            for fname in files:
                if fname.endswith('.crdownload'):
                    dl_wait = True
            seconds += 1
        return seconds


    @classmethod
    def get_downloaded_file_name(cls):
        '''
        Get the name of the last downloaded file.
        '''
        cls.__driver.execute_script("window.open()")
        cls.__driver.switch_to.window(cls.__driver.window_handles[-1])
        cls.__driver.get('chrome://downloads')
        time.sleep(0.5)
        return cls.__driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content #file-link').text")


    @classmethod
    def get_inner_text(cls, data={"by": By.XPATH, "identifier": ""}):
        '''
        Get the inner text of an element.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": ""})
        '''
        elem = cls.__find_element_steps(json_data=data, interactable=False)
        return elem.get_attribute('innerText')

    @classmethod
    def element_exists(cls, data={"by": By.XPATH, "identifier": ""}):
        '''
        Check if an element exists.

        Parameters:
        -----------
        data : dict
            The data to use. (Default: {"by": By.XPATH, "identifier": ""})
        '''
        try:
            cls.__find_matching_element(data["by"], data["identifier"])
            return True
        except NoSuchElementException:
            return False