from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import time
import datetime
from datetime import date
import pyautogui
import re
import math

#I am not a programmer please excuse the generally bad practices :/

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1



# you can install chrome driver from https://chromedriver.storage.googleapis.com/index.html?path=88.0.4324.96/
driver = webdriver.Chrome()


def declare_first_bool(num):
    #^this directs pyautogui to do the simpler save only on the first file opened in the sequence 
    #it is switched to 1 after first download 
    global first_bool
    first_bool = num    
    #^may not be needed i really dont know how th desktop save is configured         
 
        
global table_nums 
table_nums = [1,2,3]
#^idk how to declare empty 
        
def declare_table_numbers (num1, num2, num3):
    global table_nums 
    table_nums[0] = num1
    table_nums[1] = num2
    table_nums[2] = num3
    
def declare_total_count(x):
    global total_count
    total_count = x 

def declare_run_count(x):
    global run_count
    run_count = x 


def enter_site():
    driver.get("https://wcca.wicourts.gov/advanced.html")

def county():
#Enter County as a search parameter
    driver.find_element(By.XPATH, \
        'html/body/div[1]/div/div[1]/main/div/form/div[3]/div[1]/div/label/div/div/span[1]/div[2]/input') \
        .send_keys('Dane\n')
      
        
def class_codes():
#Enter class codes as parameters on advanced search page
    class_codes = driver.find_element(By.XPATH, \
        'html/body/div[1]/div/div[1]/main/div/form/div[8]/div[1]/div/label/div/div/span[1]/div[2]/input') 
    
    class_codes.send_keys('09250\n', '15100\n', '15401\n', '18598\n', \
                          '10402\n', '10401\n', '09200\n', '16700\n', \
                          '18502\n', '13697\n', '18597\n', '13698\n') 
                   
                           
def date_range(first_date, end_date):
    global start_date
    start_date = first_date
#Enters start and end Date, Max 30 days apart, as parameters on advanced search page
    driver.find_element(By.XPATH, \
        'html/body/div[1]/div/div[1]/main/div/form/div[6]/div/div/label/div/div/div[1]/div/label/div/div[2]/div/div[2]/div/div[1]/div/input') \
        .send_keys(start_date)
    
    driver.find_element(By.XPATH, 
        'html/body/div[1]/div/div[1]/main/div/form/div[6]/div/div/label/div/div/div[2]/div/label/div/div[2]/div/div[2]/div/div[1]/div/input') \
        .click() 
        #^this needs to be clicked before it can be typed in 
    driver.find_element(By.XPATH, \
        'html/body/div[1]/div/div[1]/main/div/form/div[6]/div/div/label/div/div/div[2]/div/label/div/div[2]/div/div[2]/div/div[1]/div/input') \
        .send_keys(end_date)
    
    driver.find_element(By.XPATH, \
        '//button[text()= "Search"]') \
        .click()


def search_results():
#reads table header for case results, (in form: "showing 1-25 of 70 cases" => case_nums = [1, 25, 70])    
    #try:
    w = WebDriverWait(driver, 2).until( \
    EC.presence_of_element_located((By.ID, 'caseSearchResults_info')))
#^wait for the case #s to appear
    #if w:
    print('list of cases')
    case_list_details = driver.find_element(By.ID, 'caseSearchResults_info').text
    print (case_list_details)
    case_nums =  re.findall(r'\d+', case_list_details)
    #^regex to find numerics
    print (case_nums)
    declare_table_numbers(int(case_nums[0]), int(case_nums[1]), int(case_nums[2]))
                          
    #except:
        #print('straight to single case')
        #captcha_wait()
        #open_charge_details()
        #if first_bool == 0: 
            #first_save()
            #declare_first_bool(1)
            #print('first = ', first_bool)
        #else:
            #awful_save()
    #next_date(start_date)

    
def case_pages(): 
    declare_total_count(0)
    pages = 1
    search_results()
    while pages <= math.ceil(table_nums[2]/25) and total_count <= table_nums[2]:
        print('case results page = ', pages, ' out of ', math.ceil(table_nums[2] / 25)) 
        all_cases_on_page()
        pages = pages + 1
        driver.find_element(By.LINK_TEXT, 'Next').click()
        search_results()
    print('Congrats, all files in date range saved!') 
    declare_first_bool(1)
    
    
def all_cases_on_page(): 
    row_num = 1
    while row_num <= (table_nums[1] - table_nums[0] + 1) and total_count <= table_nums[2]:    
        print ('row on page = ', row_num, '/', str(table_nums[1] - table_nums[0] + 1))  
        cases_iter = 'html/body/div[1]/div/div[1]/main/div/div[2]/div/table/tbody/tr[' + str(row_num) + ']/td[1]/a' 
        lnks = driver.find_elements(By.XPATH, cases_iter)
    # cant seem to land any closer to the hyperlink than its containing list via XPATh. So this will traverse list find
    # the hyperlink and go to linked page
        for lnk in lnks:
        # get_attribute() to get all href
            if lnk.get_attribute('href'):
                case_tag = lnk.get_attribute('href')
        driver.get(case_tag)
        # ^hopefully this finds case in case selection table             
        captcha_wait()
        open_charge_details()
        #if first_bool == 0:
            #first_save()
            #print('first save')
            #declare_first_bool(1)
            #declare_total_count((total_count+1))
        #else: 
        awful_save()
        print('awful save')
        row_num = row_num + 1
        declare_total_count(total_count + 1)
        declare_run_count(run_count + 1)
        print('files saved in this run = ', run_count)
        print('Cases in date range = ', total_count, '/', table_nums[2] )
        return_to_results()              
    

def captcha_wait():
    w2 = WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.XPATH, 'html/body/div[1]/div/div[1]/main/div/div/div[2]/div[4]/div/a')))
    
    driver.find_element(By.XPATH, 'html/body/div[1]/div/div[1]/main/div/div/div[2]/div[4]/div/a').click()
    # ^The button you can click after the captcha


def open_charge_details():
    driver.find_element(By.XPATH, '//button[text()= "View history and details of charges/sentences"]').click()
    # ^open charge details, buttons usually searchable


def first_save():
    pyautogui.hotkey('ctrl', 's')
    pyautogui.typewrite(['tab', 'down', 'up', 'enter', 'enter'], interval=0.1)
    # ^basic desktop save, with a bunch of nonsense to select "webpage, single file 


def awful_save():
    #it appears after you tell chrome to save 'webpage as single file' it'll automatically do it from then on 
    #so this is a slightly different save routine that just needs control-s and enter
    pyautogui.hotkey('ctrl', 's')
    pyautogui.typewrite(['tab', 'down', 'down', 'enter', 'down', 'up', 'enter', 'enter'], interval=0.25)
    
    
def return_to_results():
    time.sleep(1)
    pyautogui.hotkey('alt','left')  
    pyautogui.hotkey('alt','left')
    w2 = WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.XPATH, \
        'html/body/div[1]/div/div[1]/main/div/div[2]/div/table/tbody/tr[1]/td[1]/a')))

def next_date(start_date):
    #this is annoying cuz website takes 'MM-DD-YYYY' while datetime wants 'iso' 'YYYY-MM-DD
    date_nums = re.findall(r'\d+', start_date)
    date1 = date(int(date_nums[2]), int(date_nums[0]), int(date_nums[1]))
    
    iso_end_date = (date1 - datetime.timedelta(days=1))
    iso_start_date = (date1 - datetime.timedelta(days=31))
    
    next_end_date = str((iso_end_date).month) + '-' + str((iso_end_date).day) + '-' + str((iso_end_date).year)                 
    next_start_date = str((iso_start_date).month) + '-' + str((iso_start_date).day) + '-' + str((iso_start_date).year) 
    print('showing ', next_start_date, 'to', next_end_date)
    declare_first_bool(1)
    declare_total_count(0)
    main(next_start_date, next_end_date)
  
    
def main(date_1, date_2):
    enter_site()
    county()
    class_codes()
    date_range(date_1, date_2)
    case_pages()
    next_date(date_1)
    

    
declare_first_bool(0)
declare_run_count(0)
main('1-5-2019', '2-4-2019')







