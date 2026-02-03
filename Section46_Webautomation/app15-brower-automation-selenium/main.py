from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# ===== CREATE DRIVER =====
driver = webdriver.Chrome()
driver.maximize_window()

# ===== OPEN PAGE =====
driver.get("https://demoqa.com/login")

wait = WebDriverWait(driver, 15)

try:
    # ===== LOCATE ELEMENTS =====
    username_field = wait.until(
        EC.visibility_of_element_located((By.ID, "userName"))
    )

    password_field = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )

    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "login"))
    )

    # ===== FILL FORM =====
    username_field.send_keys("tech")
    password_field.send_keys("Money@168")

    # ===== CLICK LOGIN =====
    login_button.click()

    # ✅ WAIT AFTER LOGIN – VERY IMPORTANT
    wait.until(
        EC.visibility_of_element_located((By.ID, "userName-value"))
    )

    print("✅ Login successful – page stayed open!")

except Exception as e:
    print("❌ ERROR:", e)

# ===== KEEP BROWSER OPEN =====
input("Press Enter to close browser...")
driver.quit()
