import pathlib
import time
import urllib3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


chromedriver_path = pathlib.Path().resolve() / 'chromedriver'


class AvisoYoutube:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def connect(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--mute-audio')
        # chrome_options.add_argument('--user-data-dir=/home/sherlock/.config/google-chrome')
        # chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
        self.driver.get('https://aviso.bz/')
        self.wait = WebDriverWait(self.driver, 20)

    def close(self):
        self.driver.quit()

    def login(self):
        self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Войти'))).click()
        username = self.wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        username.send_keys(self.username)
        password = self.wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
        password.send_keys(self.password)
        time.sleep(10)
        self.wait.until(EC.visibility_of_element_located((By.ID, 'button-login'))).click()
        time.sleep(10)

    def youtube(self):
        self.driver.get('https://aviso.bz/work-youtube')
        window_before = self.driver.window_handles[0]
        links = self.driver.find_elements_by_xpath("//*[starts-with(@id, 'start-ads-')]/span[1]")
        viewed = 0

        for link in links:
            try:
                time.sleep(3)
                link.click()
                link_id = link.get_attribute('onclick')[24:30]
                self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[starts-with(@id, 'ads-lk-{link_id}')]/span[1]"))).click()

                window_after = self.driver.window_handles[1]
                self.driver.switch_to.window(window_after)

                timer = self.wait.until(EC.visibility_of_element_located((By.ID, 'tmr'))).text
                self.driver.switch_to.frame('video-start')
                self.wait.until(EC.visibility_of_element_located((By.ID, 'player'))).click()
                time.sleep(int(timer) + 5)
                self.driver.close()
                self.driver.switch_to.window(window_before)
                time.sleep(3)
            except:
                try:
                    window_before = self.driver.window_handles[1]
                    self.driver.close()
                    self.driver.switch_to.window(window_before)
                except:
                    continue


aviso = AvisoYoutube('aliymaltymyshev@gmail.com', 'Qq18425256')
aviso.connect()
aviso.login()
aviso.youtube()
aviso.close()
