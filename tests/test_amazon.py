from selenium import webdriver

driver = webdriver.Chrome()


# Open the Python website


data = driver.get("http://www.python.org")

print("Title test:  =======", driver.title)

print("dd===============fgfgfg")
