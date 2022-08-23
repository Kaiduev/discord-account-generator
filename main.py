import os
import random
import sys
import uuid

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from twocaptcha import TwoCaptcha
from webdriver_manager.chrome import ChromeDriverManager


class GenerateDiscordAccount:

    def __init__(self, email, username):
        self.email = email
        self.username = username
        self.password = self.generate_password()

    def generate_password(self):
        return str(uuid.uuid4().__hash__())[:4] + str(uuid.uuid4().__str__())[:8]

    def solvehCaptcha(self, url):
        sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

        api_key = '7c289ca1720428cede9d26880d8a384f'

        solver = TwoCaptcha(api_key)

        try:
            result = solver.hcaptcha(
                sitekey='4c672d35-0701-42b2-88c3-78380b0db560',
                url=url,
            )

        except Exception as e:
            print(e)
            return False

        else:
            return result

    def selenium_steps(self):
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get('https://discord.com/register')
        WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        browser.find_element(By.XPATH, "//input[@type='email']").send_keys(self.email)
        browser.find_element(By.XPATH, "//input[@type='text']").send_keys(self.username)
        browser.find_element(By.XPATH, "//input[@type='password']").send_keys(self.password)
        browser.find_element(By.XPATH,
                             '//*[@id="app-mount"]/div[2]/div/div[1]/div/div/div/form/div/div/div[4]/div[1]/div[1]/div/div/div/div/div[2]/div').click()

        actions = ActionChains(browser)
        month = str(random.randint(1, 12))
        actions.send_keys(month)
        actions.send_keys(Keys.ENTER)
        day = str(random.randint(1, 28))
        actions.send_keys(day)
        actions.send_keys(Keys.ENTER)
        year = str(random.randint(1989, 2000))
        actions.send_keys(year)
        actions.perform()
        date = year + "-" + month.zfill(2) + "-" + day.zfill(2)

        browser.find_element(By.XPATH,
                             '//*[@id="app-mount"]/div[2]/div/div[1]/div/div/div/form/div/div/div[5]/label/input').click()
        browser.find_element(By.XPATH,
                             '//*[@id="app-mount"]/div[2]/div/div[1]/div/div/div/form/div/div/div[6]/button').click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             '#app-mount > div.appDevToolsWrapper-1QxdQf > div > div.app-3xd6d0 > div > div > div > section > div > div.flexCenter-1Mwsxg.flex-3BkGQD.justifyCenter-rrurWZ.alignCenter-14kD11 > div > iframe')))

        result = self.solvehCaptcha(browser.current_url)
        print(result)

        if result:
            code = result['code']
            resp = requests.post(
                url="https://discord.com/api/v9/auth/register",
                json={
                    "captcha_key": code,
                    "consent": True,
                    "date_of_birth": date,
                    "email": self.email,
                    "gift_code_sku_id": None,
                    "invite": None,
                    "password": self.password,
                    "promotional_email_opt_in": True,
                    "username": self.username,
                },
                headers={
                    "Content-Type": "application/json"
                }
            )

            print(resp.status_code)

            print("Token {}".format(resp.json()))
            print("Email: {}".format(self.email))
            print("Password: {}".format(self.password))
            print("Username: {}".format(self.username))

            print("Finished...")


email = str(input("Email: "))
username = str(input("Username: "))

account = GenerateDiscordAccount(email=email, username=username)
account.selenium_steps()
