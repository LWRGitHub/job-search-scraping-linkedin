from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from Env import Env
from Read_Write import Read_Write
import json
import datetime
import re



class Scrp:

    def __init__(self):
        # dotenv
        self.env = Env()

    def scrp(self):
        # setup driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # login
        driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        time.sleep(2)
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
        # time.sleep(20)
        time.sleep(4)

        # job search url
        driver.get(self.env.URL)

        # sleep for manual scrolling to load more jobs
        time.sleep(2)

        list_len_error_data = {}
        res = {}
        do = True

        while do:
            # Wait until the ul element is available
            ul_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ul[@class='scaffold-layout__list-container']"))
            )

            # Find all li elements within the ul
            li_elements = driver.find_elements_by_xpath("//ul[@class='scaffold-layout__list-container']/li")

            # Loop through each li element and scroll it into view
            for li in li_elements:
                driver.execute_script("arguments[0].scrollIntoView(true);", li)

            # wait for page to load 
            time.sleep(3)

            # grab data
            max_pays = driver.find_elements_by_xpath("//li[@class='job-card-container__metadata-item']") 
            companys = driver.find_elements_by_xpath("//span[@class='job-card-container__primary-description ']")
            job_titles = driver.find_elements_by_xpath("//a[@class='disabled ember-view job-card-container__link job-card-list__title']")
                
            max_pay_list = []
            company_list = []
            job_title_list = []
            hrefs = []
            

            # add elements to lists
            def add_to_list(list, elements, hasHref = False):
                for element in elements:
                    list.append(element.text)
                    if(hasHref):
                        hrefs.append(element.get_attribute("href"))
            add_to_list(max_pay_list, max_pays)
            add_to_list(company_list, companys)
            add_to_list(job_title_list, job_titles, True)

            error_count = 0
            if(len(max_pay_list) != len(company_list) or len(max_pay_list) != len(job_title_list) or len(company_list) != len(job_title_list) or len(max_pay_list) != len(hrefs)):

                error_data = {
                    "lengths": {
                        "max_pay_list": len(max_pay_list),
                        "company_list": len(company_list),
                        "job_title_list": len(job_title_list),
                        "hrefs": len(hrefs)
                    },
                    "URL": driver.current_url,
                    "max_pay_list": max_pay_list,
                    "company_list": company_list,
                    "job_title_list": job_title_list,
                    "hrefs": hrefs
                }

                # create error file for debugging
                list_len_error_data[f"error_{error_count}"] = error_data
                
                error_count += 1

            else:

                # get max pay & add to res only if it's greater than the minimum acceptable pay
                for i in range(len(max_pay_list)):

                    try:
                        txt = max_pay_list[i]
                    
                        d_sign_idx_1 = txt.index("$")        
                        d_sign_idx_2 = txt.index("$", d_sign_idx_1+ 1) 

                        txt = txt[d_sign_idx_2+1:]
                        k_idx = txt.index("K")

                        txt = txt[0 : k_idx]

                        try:
                            txt = int(txt)
                        except:
                            txt = float(txt)
                        if(txt > int(self.env.MINIMUM_ACCEPTABLE_PAY) ):
                            res[F"{txt},{company_list[i]},{job_title_list[i]}"] = {"max_pay":txt, "company":company_list[i], "job_title":job_title_list[i], "href":hrefs[i]}
                    except:
                        res[F"__ERROR__,{company_list[i]},{job_title_list[i]}"] = {"max_pay":"__ERROR__", "company":company_list[i], "job_title":job_title_list[i], "href":hrefs[i]}

            # try to click on the next page
            try:
                ul_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']"))
                )

                # Locate the active li element
                active_li = ul_element.find_element_by_xpath(".//li[contains(@class, 'active')]")

                # Find the next li element
                next_li = active_li.find_element_by_xpath("following-sibling::li")

                # Click on the next li element
                next_li.click()
            except:
                do = False
                    
        # add to JSON fil
        # f = open("jobs.txt", "a")
        # f.write(str(res))
        # f.close()

        
 
        # get current time & clean it up
        current_time = re.sub('\s+', '_', str(datetime.datetime.now()))
        current_time = re.sub('[\.]+', '', current_time)

        with open(f"error_{error_count}_{current_time}.json", 'w', encoding='utf-8') as f:
            json.dump(list_len_error_data, f, ensure_ascii=False, indent=4)

        with open(f"jobs_befor_exp_yrs_sort_{current_time}.json", 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=4)
        
        # Read_Write(res).read_write()
                
        print("\ndone\n")
        driver.quit()
