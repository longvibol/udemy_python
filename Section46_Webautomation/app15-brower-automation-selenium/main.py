from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import os
import time

class WebAutomation:
    def __init__(self):
        download_path = os.path.abspath(os.getcwd())
        # print("Download folder:", download_path)

        chrome_options = Options()
        chrome_options.add_argument("--disable-search-engine-choice-screen")

        prefs = {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # ----- FIX HERE -----
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def login(self, username, password):
        self.driver.get("https://demoqa.com/login")

        username_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "userName"))
        )
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        login_button = self.driver.find_element(By.ID, 'login')

        username_field.send_keys(username)
        password_field.send_keys(password)

        self.driver.execute_script("arguments[0].click();", login_button)

    def fill_form(self, fullname, email, current_address, permanent_address):
        elements = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div/div/div[1]/span')
            )
        )
        elements.click()

        text_box_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "item-0"))
        )
        text_box_field.click()

        fullname_field = self.wait.until(EC.visibility_of_element_located((By.ID, "userName")))
        email_field = self.wait.until(EC.visibility_of_element_located((By.ID, "userEmail")))
        current_address_field = self.wait.until(EC.visibility_of_element_located((By.ID, "currentAddress")))
        permanent_address_field = self.wait.until(EC.visibility_of_element_located((By.ID, "permanentAddress")))
        submit_button = self.wait.until(EC.element_to_be_clickable((By.ID, "submit")))

        fullname_field.send_keys(fullname)
        email_field.send_keys(email)
        current_address_field.send_keys(current_address)
        permanent_address_field.send_keys(permanent_address)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", submit_button
        )

        ActionChains(self.driver).move_to_element(submit_button).click().perform()

    def download(self):
        download = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="item-7"]/span'))
        )
        download.click()

        download_button = self.wait.until(
            EC.visibility_of_element_located((By.ID, "downloadButton"))
        )
        download_button.click()

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    webautomation = WebAutomation()
    webautomation.login(username='tech', password='Money@168')
    webautomation.fill_form("Kh camtech","hello@gmail.com","Phnom Penh","Turk Thlar")
    webautomation.download()
    input("werwer")
    webautomation.close()


