import logging.config
import os
import time
from datetime import date
from emailer import SeatAlertEmailer
from scraper import Scraper
from urllib.error import URLError


class SeatSecurer(object):
    def __init__(self):
        if not os.path.exists("logs/"):
            os.makedirs("logs/")
        config_dict = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'filename': 'logs/ST.log',
                    'when': 'D',
                    'interval': 1,
                    'backupCount': 7
                },
            },
            'root': {
                'handlers': ['console', 'file'],
                'level': 'INFO'
            }
        }
        logging.config.dictConfig(config_dict)

        self.logger = logging.getLogger(__name__)

        f = open("configs/settings.txt", 'r')
        settings = f.readlines()
        f.close()
        
        FORMAT_ERROR = "settings.txt format is invalid, please refers to project doc"
        if len(settings) != 6:
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
            self.interval = float(settings_dict["scraping_interval"])
            self.do_email_alert = (str(settings_dict["do_email_alert"]).lower() == "true")

            start_date_parts = settings_dict["start_date"].split('-')
            end_date_parts = settings_dict["end_date"].split('-')

            self.scraper = Scraper(date(int(start_date_parts[0]), int(start_date_parts[1]), int(start_date_parts[2])), date(int(end_date_parts[0]), int(end_date_parts[1]), int(end_date_parts[2])), settings_dict["do_check_time"].lower() == "true", settings_dict["city"])

        except:
            raise ValueError(FORMAT_ERROR)

        self.alert = SeatAlertEmailer()

    def start(self):
        i = 0
        flag = True
        while flag:
            i += 1
            self.logger.info("####### START SCRAPING {0} #######".format(i))
            try:
                scrape_result = self.scraper.scrape()
                if scrape_result[1] and self.do_email_alert:
                    self.alert.send(scrape_result[0])
                self.logger.info(
                    "####### SCRAPING {0} FINISHED, STARTING AGAIN IN {1} MIN #######\n".format(i, self.interval))
                time.sleep(self.interval * 60)

            except (ConnectionRefusedError, URLError):
                self.logger.error(
                    "******* CONNECTION ERROR, STARTING AGAIN IN {0} MIN *******".format(self.interval * 3))
                time.sleep(self.interval * 3 * 60)
            except KeyboardInterrupt:
                self.logger.info("####### EXIT PROGRAM #######")
                flag = False
            except:
                self.logger.exception("******* EXCEPTION RAISED WHEN SCRAPING, EXIT PROGRAM *******")
                flag = False
