from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "127.0.0.1")
profile.set_preference("network.proxy.socks_port", 9050)

profile.update_preferences()

driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.FIREFOX, browser_profile=profile)

driver.get('http://icanhazip.com/')

print(driver.page_source)

driver.quit()