import logging


class Sorter(object):
    def __init__(self, city, centre_pref_list, date_pref, time_pref):
        self.logger = logging.getLogger(__name__)

        self.city = city

        f = open("configs/preferences_{0}.txt".format(self.city),'r')
        preferences = f.readlines()
        f.close()
        PREF_FORMAT_ERROR = "preferences.txt format is invalid, please refers to project doc"
        if len(preferences) != 4:
            raise ValueError(PREF_FORMAT_ERROR)
        preferences_dict = {}
        for line in preferences:
            key_value = line.split(': ',1)
            if len(key_value) != 2:
                raise ValueError(PREF_FORMAT_ERROR)
            if key_value[0] in preferences_dict:
                raise ValueError(PREF_FORMAT_ERROR)
            preferences_dict[key_value[0]] = key_value[1].split(", ")

        if "factor_orders" not in preferences_dict:
            raise ValueError(PREF_FORMAT_ERROR)
        factor_order_list = preferences_dict["factor_orders"]
        if sorted(factor_order_list) != ["centre", "date", "time"]:
            raise ValueError("factor_order_list is invalid")
        self.factor_order_list = factor_order_list

        if len(set(centre_pref_list)) != len(centre_pref_list):
            raise ValueError("centre_pref_list is not unique")

        self.centre_weight_dict = {}
        weight = 1
        for centre in centre_pref_list:
            self.centre_weight_dict[centre] = weight
            weight *= 2

        if date_pref not in ["end","medium","start"]:
            raise ValueError("date_pref is invalid")
        self.date_pref = date_pref

        if time_pref not in ["end","medium","start"]:
            raise ValueError("time_pref is invalid")
        self.time_pref = time_pref

    def sort_data(self, centre_date_time_list):
        #TODO: finish the function
        return
