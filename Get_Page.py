import json
from Env import Env
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class Get_Page:

    def __init__(self):
        # self.data = data
        self.env = Env()

    def get_page(self):
    
        # read old data from json file
        old_data = {}
        with open('data.json') as f:
            old_data = json.load(f)

        
        # read data from json file
        new_data = {}
        with open('jobs_befor_exp_yrs_sort_2023-12-02_00:07:44482473.json') as f:
            new_data = json.load(f)    
        

        # setup driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # login
        driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        time.sleep(4)
        # username
        username = driver.find_element_by_xpath("//input[@id='username']")
        username.send_keys(self.env.LinkedIn_USER_NAME)
        # password
        password = driver.find_element_by_xpath("//input[@id='password']")
        password.send_keys(self.env.LinkedIn_PASSWORD)
        #log in btn
        log_in_btn = driver.find_element_by_xpath("//button[@class='btn__primary--large from__button--floating']")
        log_in_btn.click()
        
        # sleep for Verification issue (captcha)
        time.sleep(20)
        #time.sleep(2)

        # all data
        all_data = {}
        error = {}

        # Find required years of experience
        for key in new_data:
        
            # Duplicate wright over
            # TODO: removed Expired jobs before this for loop
            # if key in old_data:
            #     new_data[key] = old_data[key]

            if("job_desc" in new_data[key]):
                continue
            else:
                
                
                # get content from href
                driver.get(new_data[key]["href"])
                # time.sleep(2)

                try:
                    # expand job description
                    see_more_less = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'jobs-description__footer-button')]"))
                    )
                    see_more_less.click()

                    # Scroll down page
                    see_more_less = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'jobs-description__footer-button')]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", see_more_less)

                    # Find job description
                    time.sleep(1) # wait for job description to load
                    job_description = driver.find_element_by_xpath("//div[@id='job-details']").text

                    new_data[key]["job_desc"] = job_description
                except:
                    error[key] = new_data[key]
                    continue

            # all_data[key] = new_data[key]


        with open('error_jobs_wth_desc.json', 'w', encoding='utf-8') as file:
            json.dump(error, file, ensure_ascii=False, indent=4)
                

        # all data
        with open('jobs_wth_desc.json', 'w', encoding='utf-8') as file:
            json.dump(new_data, file, ensure_ascii=False, indent=4)

        driver.quit()
