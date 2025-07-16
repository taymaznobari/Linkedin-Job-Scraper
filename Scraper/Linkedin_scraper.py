from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Savefile.CSV_SQLite import SaveFile
from selenium import webdriver
import time

class Linkdin:
    def __init__(self, username, password):
        self.list1 = []
        self.options = Options()
        #self.options.add_argument("--headless")
        #self.options.add_argument("--disable-gpu")
        #self.options.add_argument("--disable-blink-features=AutomationControlled")
        #self.options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get("https://www.linkedin.com/login")
        user = self.wait.until(EC.presence_of_element_located((By.NAME, "session_key")))
        user.send_keys(username)
        passw = self.wait.until(EC.presence_of_element_located((By.NAME, "session_password")))
        passw.send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.waitfeed = WebDriverWait(self.driver, 100)
        search_bar = self.waitfeed.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search']")))
        search_bar.click()
        time.sleep(1)
    def SearchJob(self,titel_job):
        self.driver.get("https://www.linkedin.com/jobs/search/")
        titles = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
        titles.send_keys(titel_job)
        time.sleep(1)
        country = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")))
        country.send_keys(Keys.CONTROL + "a")
        country.send_keys(Keys.DELETE)
        country.send_keys("United States" + Keys.ENTER)
        time.sleep(10)

    def FilterLevel(self, entry, mid_senior):
        time.sleep(2)
        if entry == 1 or mid_senior == 1:
            experience_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='searchFilter_experience']")))
            experience_button.click()
            time.sleep(1)
            if entry == 1:
                entry_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='experience-2']")))
                entry_button.click()
            if mid_senior == 1:
                mid_senior_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='experience-4']")))
                mid_senior_button.click()
            time.sleep(1)
            try:
                time.sleep(10)
                apply_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[3]/div[4]/section/div/section/div/div/div/ul/li[4]/div/div/div/div[1]/div/form/fieldset/div[2]/button[2]")))
                apply_button.click()
            except:
                print("Oops! Could not find the required element.")
            try:
                time.sleep(10)
                apply_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[3]/div[4]/section/div/section/div/div/div/ul/li[3]/div/div/div/div[1]/div/form/fieldset/div[2]/button[2]")))
                apply_button.click()
            except:
                print("Oops! Could notfind the required element. Please close the app and try again.")
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ESCAPE).perform()
                
            time.sleep(10)

    def Information(self,result):
        time.sleep(5)
        result = int(result)
        new_result = result
        for i in ["Germany", "Spain", "UK", "Canada", "Italy", "Ukraine", "Australia"]:
            if new_result <= 0:
                break
            lis = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,"//li[contains(@class, 'occludable-update') and contains(@class, 'scaffold-layout__list-item')]")))
            for li in lis:
                self.driver.execute_script("arguments[0].scrollIntoView();", li)
            time.sleep(1)
            jobs = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container")))
            time.sleep(5)
            for job in jobs:
                try:
                    if new_result <= 0:
                        break
                    job_titles = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title--link").get_attribute("aria-label")
                    company = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle").text
                    location = job.find_element(By.CSS_SELECTOR, "ul.job-card-container__metadata-wrapper li span").text
                    link = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title--link").get_attribute("href")
                    self.list1.append((job_titles, company, location, link))
                    new_result -= 1
                    time.sleep(3)
                except:
                    print("---")
            if new_result > 0:
                time.sleep(3)
                country = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")
                country.send_keys(Keys.CONTROL + "a")
                country.send_keys(Keys.DELETE)
                country.send_keys(i + Keys.ENTER)
                time.sleep(10)

    def SaveResults(self,CSV_SQLite):
        saver = SaveFile(self.list1)
        if CSV_SQLite == "CSV":
            saver.SaveToCSV()
        elif CSV_SQLite == "SQLite":
            saver.SaveToSQLite()

    def CloseChrome(self):
        self.driver.close()