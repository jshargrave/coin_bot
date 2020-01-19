"""
    This file is responsible for handling all date and time functions
"""

import datetime as dt


def btc_all_data_date_range():
    """
    Desc: This function is used to get a tuple of two strings which represent a date range of the entire
    :return:
    """
    return ["2010-07-17", display_date(dt.datetime.now())]


def parse_datetime(datetime_str):
    return dt.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S UTC')


def display_datetime(datetime_obj):
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S UTC")


def parse_date(date_str):
    return dt.datetime.strptime(date_str, '%Y-%m-%d')


def display_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")


def add_time_format(date_str):
    return date_str + " 00:00:00 UTC"


def remove_time_format(datetime_str):
    return datetime_str.split(' ')[0]


def increment_datetime_generator(datetime_obj, timedelta):
    while True:
        yield datetime_obj + timedelta
        datetime_obj += timedelta


def decrement_datetime_generator(datetime_obj, timedelta):
    while True:
        yield datetime_obj - timedelta


def average_datetime(datetime_list):
        max_datetime = max(datetime_list)
        total_time_delta = dt.timedelta()

        for date_item in datetime_list:
            total_time_delta += max_datetime - date_item

        return max_datetime - total_time_delta / len(datetime_list)


def get_current_date():
    return display_datetime(dt.datetime.now())
