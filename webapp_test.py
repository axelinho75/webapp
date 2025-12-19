import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestWebAppCase(unittest.TestCase):

    def test_webapp(self):
        driver = webdriver.Firefox()
        driver.get("http://127.0.0.1:5000")
        a_item = driver.find_element(by=By.TAG_NAME, value="a")
        a_item.click()