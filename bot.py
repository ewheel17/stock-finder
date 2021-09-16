from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import info
import sys

# make sure this path is correct
PATH = "/Users/maxwheeler/Documents/WebDriver/chromedriver"

driver = webdriver.Chrome(executable_path=PATH)

RTX3080 = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440"
RTX3070 = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442"
RTX3060TI = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402"
TESTORDER = "https://www.bestbuy.com/site/insignia-monitor-wipes-80-pack-white/8041012.p?skuId=8041012"

def launchGpuSearch(id):
  if (id == '3080'):
    print('Launching RTX3080 bot...')
    driver.get(RTX3080)
  if (id == '3070'):
    print('Launching RTX3070 bot...')
    driver.get(RTX3070)
  if (id == '3060'):
    print('Launching RTX3060ti bot...')
    driver.get(RTX3060TI)
  if (id == 'test'):
    print('Running test...')
    driver.get(TESTORDER)

inputId = sys.argv[1]
launchGpuSearch(inputId)

isComplete = False
n = 0
while not isComplete:
    # find add to cart button
    try:
        if (n % 20 == 0):
          print("Cycle: ", n)
        n += 1
        atcBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
        )
    except:
        driver.refresh()
        continue

    print("Add to cart button found")

    try:
        # add to cart
        atcBtn.click()

        # go to cart and begin checkout as guest
        driver.get("https://www.bestbuy.com/cart")

        checkoutBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".checkout-buttons .btn-primary"))
        )
        checkoutBtn.click()
        print("Successfully added to cart - beginning check out")

        # fill in email and password
        emailField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fld-e"))
        )
        emailField.send_keys(info.email)

        pwField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fld-p1"))
        )
        pwField.send_keys(info.password)

        # click sign in button
        signInBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cia-form__controls__submit"))
        )
        signInBtn.click()
        print("Signing in")

        # fill in card cvv
        cvvField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cvv"))
        )
        cvvField.send_keys(info.cvv)
        print("Attempting to place order")

        # place order
        if (inputId != 'test'):
          placeOrderBtn = WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.CSS_SELECTOR, ".button__fast-track"))
          )
          placeOrderBtn.click()

        isComplete = True
    except:
        # make sure this link is the same as the link passed to driver.get() before looping
        launchGpuSearch(inputId)
        print("Error - restarting bot")
        continue

print(f"Order for ID#{inputId} successfully placed.")
