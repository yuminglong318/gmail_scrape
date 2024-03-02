from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_results import get_result

import json
import time
from random import randint

def init():

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(options=options)
    
    try:
        driver.maximize_window()
    except Exception as e:
        pass

    return driver

def scrape(driver, log_data):

    scroll_panel = driver.find_element(By.XPATH, "//c-wiz[@class='zQTmif SSPGKf eejsDc']")
    
    page_index = log_data.get("page_index") if log_data.get("page_index") else 0
    position = log_data.get("position") if log_data.get("position") else 0

    driver.execute_script("arguments[0].scrollTop = arguments[1];", scroll_panel, position)
    
    while True:
        try:
            if page_index % 100 == 0 and page_index > 0:
                get_result(page_index)
            users = []
            user_elements = scroll_panel.find_elements(By.CSS_SELECTOR, "div.XXcuqd")
            for user_element in user_elements:
                try:
                    info_elements = user_element.find_elements(By.CSS_SELECTOR, "div.JcPRM")
                    name = info_elements[1].text
                    email = user_element.find_element(By.CSS_SELECTOR, "div.JcPRM[aria-describedby*='email-column']").text
                    phone = user_element.find_element(By.CSS_SELECTOR, "div.JcPRM[aria-describedby*='phone-column']").text
                    job_title = user_element.find_element(By.CSS_SELECTOR, "div.JcPRM[aria-describedby*='generated-tagline-column']").text

                    users.append({
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "job_title": job_title
                    })
                except Exception as e:
                    pass
                
            with open(f"./temp/{page_index}.json", "w", encoding="utf-8") as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
            
            pos1 = driver.execute_script("return arguments[0].scrollTop;", scroll_panel)
            driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", scroll_panel)
            pos2 = driver.execute_script("return arguments[0].scrollTop;", scroll_panel)

            if pos1 == pos2:
                get_result(page_index)
                break
            
            time.sleep(randint(40,60))
            page_index += 1

            with open("run.log", "w") as logfile:
                logfile.write(json.dumps({"page_index": page_index, "position": pos2}, indent=4))
            
        except Exception as e:
            get_result(page_index)
        

if __name__ == '__main__':
    
    with open("run.log", "r") as logfile:
        try:
            logdata = json.load(logfile)
        except Exception as e:
            logdata = {}
    
    driver = init()
    scrape(driver, logdata)