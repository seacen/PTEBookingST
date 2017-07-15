import logging
from abc import ABCMeta, abstractmethod

import requests


class Emailer(metaclass=ABCMeta):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        f = open("configs/emailer_settings.txt", 'r')
        settings = f.readlines()
        f.close()

        FORMAT_ERROR = "emailer_settings.txt format is invalid, please refers to project doc"

        if len(settings) != 2:
            raise ValueError(FORMAT_ERROR)
        settings_dict = {}
        for line in settings:
            key_value = line.split(': ', 1)
            if len(key_value) != 2:
                raise ValueError(FORMAT_ERROR)
            if key_value[0] in settings_dict:
                raise ValueError(FORMAT_ERROR)
            settings_dict[key_value[0]] = key_value[1].rstrip('\n')

        try:
            self.domain = settings_dict["domain"]
            self.api_key = settings_dict["api_key"]

        except:
            raise ValueError(FORMAT_ERROR)

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def get_email_list(self):
        pass

    @abstractmethod
    def format_data(self, data):
        return ''

    def send(self, data):
        text_string = self.format_data(data)
        self.logger.warning("Request Body:\n" + text_string)

        self.logger.warning("####### SENDING EMAIL ALERT #######")
        response = requests.post(
            "https://api.mailgun.net/v3/{0}/messages".format(self.domain),
            auth=("api", self.api_key),
            data={"from": "PTEBookingST <mailgun@{0}>".format(self.domain),
                  "to": self.get_email_list,
                  "subject": self.title + text_string,
                  "text": text_string})
        self.logger.warning(response.text)

class SeatAlertEmailer(Emailer):
    @property
    def title(self):
        return "New Seat Alert: "

    @property
    def get_email_list(self):
        f = open("configs/emails.txt",'r')
        result = f.readlines()
        f.close()
        return result

    def format_data(self, centre_datetimes_dict):
        text_string = ""
        for centre in centre_datetimes_dict:
            date_times_dict = centre_datetimes_dict[centre]
            centre_string = "{0}:\n".format(centre)
            for date in date_times_dict:
                centre_string += "{0}:  ".format(date)
                for time in date_times_dict[date]:
                    centre_string += (str(time) + ', ')
                centre_string = centre_string[:-2] + '\n'
            text_string += centre_string + "\n"

        return text_string