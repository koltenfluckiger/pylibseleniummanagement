try:
    from time import sleep
    from selenium.webdriver.common.action_chains import ActionChains
    import random
except ImportError as err:
    print("Unable to import: {}".format(err))
    exit()


class presence_of_all_elements_located_if_not_empty(object):

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            elements = driver.find_elements(*self.locator)
            if elements:
                return elements
            else:
                return True
        except Exception as err:
            return True


class window_handle_to_be_available(object):

    def __init__(self, index):
        self.index = index

    def __call__(self, driver):
        try:
            window_handle = driver.window_handles[self.index]
            if window_handle:
                return window_handle
            else:
                return False
        except Exception as err:
            return False


class wait_for_element_ready_state(object):

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            if element:
                ready_state = driver.execute_script(
                    "return document.readyState")
                return element
            else:
                return False
        except Exception as err:
            return False


class window_handle_to_be_available_switch_close_previous(object):

    def __init__(self, index):
        self.index = index

    def __call__(self, driver):
        try:
            window_handle = driver.window_handles[self.index]
            previous_window_handle = driver.window_handles[self.index - 1]
            if window_handle:
                driver.close()
                driver.switch_to.window(window_handle)
                return True
            else:
                return False
        except Exception as err:
            return False


class wait_element_to_be_clickable(object):

    def __init__(self, locator, wait):
        self.locator = locator
        self.wait = wait

    def __call__(self, driver):
        try:
            sleep(self.wait)
            element = driver.find_element(*self.locator)
            if element:
                element.click()
                return True
            else:
                return False
        except Exception as err:
            return False


class wait_for_value_to_change(object):

    def __init__(self, locator):
        self.locator = locator
        self.previous_text = None

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            if not self.previous_text:
                self.previous_text = element.text
                return False
            else:
                if self.previous_text != element.text:
                    return True
                else:
                    return False
        except Exception as err:
            return False


class wait_for_html_load_after_click(object):

    def __init__(self, locator):
        self.locator = locator
        self.clicked = False
        self.html_id = None

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            html = driver.find_element_by_xpath('html')
            if element and self.clicked == False:
                self.html_id = driver.find_element_by_xpath('html').id
                element.click()
                self.clicked = True
                return False
            else:
                if self.html_id != driver.find_element_by_xpath('html').id:
                    return True
                else:
                    return False
        except Exception as err:
            return True


class wait_for_html_load_after_click_element(object):

    def __init__(self, element):
        self.element = element
        self.clicked = False
        self.html_id = None

    def __call__(self, driver):
        try:
            if self.element and self.clicked == False:
                self.html_id = driver.find_element_by_xpath('html').id
                self.element.click()
                self.clicked = True
                return False
            else:
                if self.html_id != driver.find_element_by_xpath('html').id:
                    return True
                else:
                    return False
        except Exception as err:
            return True


class wait_for_load_after_click(object):

    def __init__(self, locator):
        self.locator = locator
        self.clicked = False

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            if element and self.clicked == False:
                element.click()
                self.clicked = True
                return False
            else:
                element.is_enabled()
                return False
        except Exception as err:
            return True

class wait_for_element_after_click(object):

    def __init__(self, locator, waited_locator):
        self.locator = locator
        self.waited_locator = waited_locator
        self.clicked = False

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            if element and self.clicked == False:
                element.click()
                self.clicked = True
                waited_element = driver.find_element(*self.waited_locator)
                if waited_element:
                    return True
                else:
                    return False
            else:
                waited_element = driver.find_element(*self.waited_locator)
                if waited_element:
                    return True
                else:
                    return False
        except Exception as err:
            return True

class wait_for_keys_verification(object):

    def __init__(self, locator, keys):
        self.locator = locator
        self.keys = str(keys)

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            element.click()
            element.clear()
            element.send_keys(self.keys)
            value = str(element.get_property("value"))
            if value == self.keys:
                return True
            else:
                return False
        except Exception as err:
            return False


class wait_for_keys_verification_with_delay(object):

    def __init__(self, locator, keys, delay):
        self.locator = locator
        self.keys_list = keys
        self.keys = keys
        self.delay = delay

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            element.click()
            element.clear()
            for key in self.keys_list:
                action = ActionChains(driver)
                action.key_down(key)
                action.pause(random.uniform(0, 500) / 1000)
                action.key_up(key)
                action.perform()
            value = str(element.get_property("value"))
            if value == self.keys:
                return True
            else:
                return False
        except Exception as err:
            return False
