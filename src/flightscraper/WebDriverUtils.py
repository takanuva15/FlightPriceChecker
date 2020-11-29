import pyglet
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

'''
Created on Feb 9, 2020

@author: takanuva15
'''


def start_new_chrome_browser(driver_exe_path: str) -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("incognito")
    if __debug__:
        options.add_experimental_option('detach', True)
    else:
        options.add_argument("headless")
    driver = webdriver.Chrome(executable_path=driver_exe_path, chrome_options=options)

    if __debug__ and len(pyglet.canvas.get_display().get_screens()) == 2:
        driver.set_window_position(1921, 0)
    return driver
