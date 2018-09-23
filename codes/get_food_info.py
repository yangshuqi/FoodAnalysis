# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 20:18:42 2018

@author: shuqi
"""

import requests
import json
import urllib

def get_ndbno(food_name):
    ndb_no = None
    resp_err = None
    url = 'https://api.nal.usda.gov/ndb/search/?format=json&q={}&sort=n&max=25&offset=0&api_key=xyL0hiueReFGrbI3yR3Y36I2ZMsfFl8caH3foP3u'.format(
        urllib.parse.quote(food_name))
    # print(url)
    response = requests.get(url)
    resp_text = json.loads(response.text)

    # print(response.status_code)

    if 400 <= response.status_code < 500:
        resp_err = "A client-side error occurred. Error {}: Could not fetch data for {} from API".format(response.status_code, food_name)
        print(resp_err)
        return ndb_no, resp_err

    elif 500 <= response.status_code < 600:
        resp_err = 'A server-side error occurred. Error {}: Could not fetch data for {} from API'.format(response.status_code, food_name)
        print(resp_err)
        return ndb_no, resp_err

    for key in resp_text:
        if key == 'errors':
            resp_err = "The USDA database has no information about the identified dish i.e. {}".format(food_name)
            print(resp_err)
            return ndb_no, resp_err

    ndb_no = resp_text['list']['item'][0]['ndbno']
    return ndb_no, resp_err


def get_food_nutrients(ndb_number):
    nutrients = None
    resp_err = None
    url = 'https://api.nal.usda.gov/ndb/V2/reports?ndbno={}&type=b&format=json&api_key=xyL0hiueReFGrbI3yR3Y36I2ZMsfFl8caH3foP3u'.format(
            ndb_number)
    print(url)
    response = requests.get(url)

    if 400 <= response.status_code < 500:
        resp_err = "A client-side error occurred. Error {}: Could not fetch data for {} from API".format(response.status_code, ndb_number)
        print(resp_err)
        return nutrients, resp_err

    elif 500 <= response.status_code < 600:
        resp_err = 'A server-side error occurred. Error {}: Could not fetch data for {} from API'.format(response.status_code, ndb_number)
        print(resp_err)
        return nutrients, resp_err

    resp_text = json.loads(response.text)
    for key in resp_text['foods'][0]:
        if key == "error":
            resp_err = "The USDA database has no information about the identified dish number i.e. {}".format(ndb_number)
            print(resp_err)
            return nutrients, resp_err

    nutrients = resp_text['foods'][0]['food']['nutrients']
    return nutrients, resp_err


def get_details(nutrients, ndb_no):
    res = 'The nutrients for ndbno: ' + str(ndb_no) + ' are: ' + '\n'

    i = 0
    while i < len(nutrients):
        res += str(nutrients[i]['name']) + ' : ' + str(nutrients[i]['value']) + ' ' + str(nutrients[i]['unit']) + '\n'
        i += 1
    
    return res

def get_nutrients_data_from_usda(food_name):
    nutrients = None
    ndb_no, error = get_ndbno(food_name)
    if ndb_no is not None:
        nutrients, error = get_food_nutrients(ndb_no)
        if nutrients is not None:
            res = get_details(nutrients, ndb_no)
    return res #, nutrients, error


if __name__ == '__main__':
    food_name = 'Apple Pie'
    r = get_nutrients_data_from_usda(food_name)
    print(r)
    # print(n)
    # print(e)