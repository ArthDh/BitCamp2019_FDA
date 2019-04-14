from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pickle
import os
import re

driver = webdriver.Chrome('/Users/arth/Downloads/chromedriver')
path_barred_broker = '/Users/arth/Desktop/Finra/net/barred_brokers.pickle'


def getCRDs(employeeCRD):
    wait = WebDriverWait(driver, 5)
    driver.get("https://brokercheck.finra.org/individual/summary/" + employeeCRD)
    print("Working..", employeeCRD)
    try:
        prev_history = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='previousEmploymentsSection']"))).click()
        barred_firms = wait.until(EC.element_to_be_clickable((By.XPATH, "//md-list[@class='flex']")))
        firm_info = barred_firms.text
        crds = []
        wrd = ""
        if firm_info == "":
            driver.close()
            return
        for c in firm_info:
            if not c == " " or c == "\n":
                wrd += c
            else:
                if wrd.startswith('('):
                    end = wrd.find(')')
                    crds.append(wrd[6:end])
                wrd = ""
        return crds
        driver.close()
    except:
        return


if __name__ == '__main__':
    barred_firms = []
    path = "/Users/arth/Desktop/Finra/net/"
    with open(path_barred_broker, 'rb') as handle:
        dict_barred = pickle.load(handle)

    for k in dict_barred.keys():
        barred_firms.append(getCRDs(k))

    with open(path + 'barred_firms.pickle', 'wb') as file:
        pickle.dump(set(barred_firms), file, protocol=pickle.HIGHEST_PROTOCOL)
