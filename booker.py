import logging
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class Booker(object):
    url = "https://www1.pearsonvue.com/testtaker/signin/SignInPage.htm?clientCode=PEARSONLANGUAGE"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1124, 850)

    def book(self, centre_date_time):
        self.logger.info("START BOOKING")
        self.driver.get(self.url)

        self.driver.find_element_by_id("inputUserName").send_keys("YOUR USERNAME")
        self.driver.find_element_by_id("inputPassword").send_keys("YOUR PASSWORD")
        self.driver.find_element_by_id("submitButton").click()

        self.driver.find_element_by_id("j_id160").click()
        self.driver.find_element_by_id("nextButton").click()

        self.driver.find_element_by_id("component1_SELECT_ONE_RADIOBUTTON_3422:0").click()
        Select(self.driver.find_element_by_id("component1_SELECT_ONE_LISTBOX_2945")).select_by_value("CMN")
        self.driver.find_element_by_id("component1_SELECT_ONE_CHECKBOX_2970").click()
        self.driver.find_element_by_id("component1_SELECT_ONE_CHECKBOX_3395").click()
        self.driver.find_element_by_id("component1_SELECT_ONE_CHECKBOX_3016").click()
        self.driver.find_element_by_id("component1_SELECT_MANY_CHECKBOX_5145:0").click()
        Select(self.driver.find_element_by_id("component1_SELECT_ONE_LISTBOX_3858")).select_by_value("Friend or family")
        Select(self.driver.find_element_by_id("component1_SELECT_ONE_LISTBOX_4560")).select_by_value("Australia")
        Select(self.driver.find_element_by_id("component1_SELECT_ONE_LISTBOX_3860")).select_by_value(
            "Skilled migration / Permanent Residency")
        Select(self.driver.find_element_by_id("component1_SELECT_ONE_LISTBOX_3862")).select_by_value("Not Studying")
        Select(self.driver.find_element_by_id("component1_SELECT_ONE_LISTBOX_4567")).select_by_value("Not Studying")
        Select(self.driver.find_element_by_id("component1_SELECT_ONE_LISTBOX_5155")).select_by_value("No")
        self.driver.find_element_by_id("nextButton").click()

        search_bar = self.driver.find_element_by_id("testCentersNearAddress")
        search_bar.clear()
        search_bar.send_keys("melbourne")
        self.driver.find_element_by_id("addressSearch").click()

        WebDriverWait(self.driver, 60).until(ec.invisibility_of_element_located((By.ID, "ui-id-2")))
        self.driver.save_screenshot("0.png")
        centre_id = self.driver.find_element_by_xpath(
            "//td[label='{0}']/label".format(centre_date_time[0])).get_attribute("for")
        tickbox = self.driver.find_element_by_id(centre_id)
        tickbox.click()
        self.driver.find_element_by_id("continueBottom").click()

        WebDriverWait(self.driver, 60).until(ec.invisibility_of_element_located((By.ID, "ui-id-4")))
        self.driver.save_screenshot("screenshot.png")


        self.driver.close()