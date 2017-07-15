import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging
import datetime
import calendar


class Scraper(object):
    url = "http://pearsonvue.com/Dispatcher?application=SeatSearch&action=actStartApp&v=W2L&clientCode=PEARSONLANGUAGE"

    def __init__(self, start_date, end_date, do_check_time=True, city="melbourne", centre_num=3, load_wait_time=120):
        self.logger = logging.getLogger(__name__)

        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1124, 850)

        self.start_date = start_date
        self.end_date = end_date

        self.start_year_month = datetime.date(self.start_date.year, self.start_date.month, 1)
        self.end_year_month = datetime.date(self.end_date.year, self.end_date.month, 1)

        self.do_check_time = do_check_time
        self.city = city
        self.centre_num = centre_num
        self.load_wait_time = load_wait_time

    def __del__(self):
        self.driver.quit()

    def scrape(self):
        self.driver.get(self.url)
        a1 = self.driver.find_element_by_link_text("Pearson Test of English Academic")
        a1.click()

        next2 = WebDriverWait(self.driver, self.load_wait_time).until(
            ec.presence_of_element_located((By.ID, "nextButton")))
        next2.click()
        search_bar = WebDriverWait(self.driver, self.load_wait_time).until(
            ec.presence_of_element_located((By.ID, "testCentersNearAddress")))
        search_bar.send_keys(self.city)
        search_button = self.driver.find_element_by_id("addressSearch")
        search_button.click()

        WebDriverWait(self.driver, self.load_wait_time).until(
            ec.presence_of_element_located((By.ID, "selectedTestCenters:0")))
        for i in range(self.centre_num):
            centre = self.driver.find_element_by_id("selectedTestCenters:{0}".format(i))
            centre.click()
        next3 = self.driver.find_element_by_id("continueTop")
        next3.click()

        WebDriverWait(self.driver, self.load_wait_time).until(
            ec.presence_of_element_located((By.ID, "inAccessibleCalendar")))

        result_dict = {}
        for i in range(self.centre_num):
            centre = self.driver.find_element_by_id("calendarForm:selectedTestCenterId:{0}".format(i))
            centre_name = self.driver.find_element_by_id("tc_name_{0}".format(centre.get_attribute("value"))).text
            centre.click()
            WebDriverWait(self.driver, self.load_wait_time).until(
                ec.invisibility_of_element_located((By.ID, "ui-id-4")))

            date_times_dict = {}
            self.__get_all_active_seats_in_centre(date_times_dict, [], True)
            if date_times_dict:
                result_dict[centre_name] = date_times_dict
        self.logger.info(result_dict)

        if not os.path.exists("data/"):
            os.makedirs("data/")
        file_name = "data/seat_status_{0}-{1}_{2}.txt".format(self.start_date, self.end_date, self.city)
        f = open(file_name, "a+")
        f.seek(0)
        prev_result_string = f.readline()
        f.close()
        f = open(file_name, "w")
        f.write(repr(result_dict))
        f.close()

        return result_dict, self.__has_new_seats(prev_result_string, result_dict)

    def __get_all_active_seats_in_centre(self, date_times_dict, year_months_read, new_centre):
        if new_centre:
            self.__reset_page_calendar()

        page_year_months = self.__get_page_year_months()
        first_year_month = page_year_months[0]
        second_year_month = page_year_months[1]

        if (not ((self.start_year_month <= first_year_month <= self.end_year_month)
                 and (first_year_month not in year_months_read))
            and not ((self.start_year_month <= second_year_month <= self.end_year_month) and (
                second_year_month not in year_months_read))):
            return

        if self.start_year_month <= first_year_month <= self.end_year_month and (first_year_month not in year_months_read):
            year_months_read.append(self.start_year_month)
            self.__read_active_datetime(first_year_month, date_times_dict)

        if (self.start_year_month <= second_year_month <= self.end_year_month) and (second_year_month not in year_months_read):
            year_months_read.append(second_year_month)
            self.__read_active_datetime(second_year_month, date_times_dict)

        self.driver.find_element_by_class_name("ui-icon-circle-triangle-e").click()

        WebDriverWait(self.driver, self.load_wait_time).until(ec.invisibility_of_element_located((By.ID, "ui-id-4")))

        self.__get_all_active_seats_in_centre(date_times_dict, year_months_read, False)


    def __get_page_year_months(self):
        current_two_months = self.driver.find_elements_by_class_name("ui-datepicker-title")
        if len(current_two_months) != 2:
            raise ValueError("has more or less than two ui-datepicker-title <div>")

        first_year_month = datetime.date(int(current_two_months[0].find_element_by_class_name("ui-datepicker-year").text),
                                list(calendar.month_name).index(
                                    current_two_months[0].find_element_by_class_name("ui-datepicker-month").text), 1)

        second_year_month = datetime.date(int(current_two_months[1].find_element_by_class_name("ui-datepicker-year").text),
                                 list(calendar.month_name).index(
                                     current_two_months[1].find_element_by_class_name("ui-datepicker-month").text), 1)

        return first_year_month, second_year_month

    def __reset_page_calendar(self):
        page_year_months = self.__get_page_year_months()
        curr_year_month = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)
        if page_year_months[0] == curr_year_month:
            return
        if page_year_months[0] > curr_year_month:
            self.driver.find_element_by_class_name("ui-icon-circle-triangle-w").click()
            WebDriverWait(self.driver, self.load_wait_time).until(
                ec.invisibility_of_element_located((By.ID, "ui-id-4")))
            self.__reset_page_calendar()
        else:
            raise ValueError("page first month lower than today's month")

    def __read_active_datetime(self, year_month, date_times_dict):
        day_a_elements = self.driver.find_elements_by_xpath(
            "//td[@data-handler='selectDay' and @data-month='{0}']/a".format(year_month.month - 1))
        if len(day_a_elements) < 1:
            return
        day_iterable = []
        for day_a_element in day_a_elements:
            day_iterable.append(int(day_a_element.text))

        for day in day_iterable:
            # check if day is out of range
            if year_month == self.start_year_month:
                if day < self.start_date.day:
                    continue
            elif year_month == self.end_year_month:
                if day > self.end_date.day:
                    continue

            date_key = datetime.date(year_month.year, year_month.month, day)

            if not self.do_check_time:
                date_times_dict[date_key] = []
                continue

            day_a_elements = self.driver.find_elements_by_xpath(
                "//td[@data-handler='selectDay' and @data-month='{0}']/a".format(year_month.month - 1))
            for day_a_element in day_a_elements:
                if int(day_a_element.text) == day:
                    day_a_element.click()
                    break
            WebDriverWait(self.driver, self.load_wait_time).until(
                ec.invisibility_of_element_located((By.ID, "ui-id-4")))

            time_input_elements = self.driver.find_elements_by_class_name("btn_select")
            time_list = []
            for time_input_element in time_input_elements:
                time_list.append(datetime.datetime.strptime(time_input_element.get_attribute("value"), "%I:%M %p").time())

            if time_list:
                date_times_dict[date_key] = time_list

    @staticmethod
    def __has_new_seats(prev_result_string, result_dict):

        if not prev_result_string:
            if result_dict:
                return True
            return False

        lr_dict = eval(prev_result_string)

        for centre in result_dict:
            if centre not in lr_dict.keys():
                return True
            for date in result_dict[centre]:
                if date not in lr_dict[centre].keys():
                    return True
                for time in result_dict[centre][date]:
                    if time not in lr_dict[centre][date]:
                        return True
        return False
