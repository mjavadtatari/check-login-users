import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# global variables
LOGIN_URL_ADDRESS = 'http://192.168.5.3/login?'
STATUS_URL_ADDRESS = 'http://192.168.5.3/status'
LOGOUT_URL_ADDRESS = 'http://192.168.5.3/logout?'
LOG_FILE_PATH = 'login.log'
LOG_FORMAT = '[%(asctime)s] %(levelname)-9s %(name)-10s %(funcName)-30s %(message)s'
ALERT_TEXT = 'کاربر گرامی کلمه عبور شما منقضی شده است، لطفا به منظور تغییر کلمه عبور به حساب کاربری خود مراجه نمایید'


def create_logger(path, log_format):
    """
    Create and configuring the logger
    """

    logger = logging.getLogger(__name__)
    logger.setLevel('INFO')

    file_handler = logging.FileHandler(path, mode='w', encoding='utf-8')

    file_format = logging.Formatter(log_format)
    file_handler.setFormatter(file_format)

    logger.addHandler(file_handler)

    return logger


# global variables
LOGGER_FILE = create_logger(LOG_FILE_PATH, LOG_FORMAT)


def create_driver():
    """
    creates a driver object and returns it
    """
    global LOGGER_FILE

    driver = None

    try:
        driver = webdriver.Firefox()
        LOGGER_FILE.info('Driver Created Successfully')
    except Exception as e:
        LOGGER_FILE.error(e.stacktrace[1])

    return driver


def login_into_page(driver, url, username, password, logger):
    """
    tries to log in to LinkedIn by email and password
    """
    global LOGIN_URL_ADDRESS, STATUS_URL_ADDRESS, LOGOUT_URL_ADDRESS, ALERT_TEXT

    try:
        driver.get(url)
        time.sleep(3)

        if driver.current_url == LOGOUT_URL_ADDRESS:
            login_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div/div/div/div/div/div/form/button/span')))
            login_btn.click()
            driver.get(url)
        elif driver.current_url == STATUS_URL_ADDRESS:
            login_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[1]/div/div/div/div/div/form/button/span')))
            login_btn.click()
            driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="username"]')))

        username_input = driver.find_element(
            by=By.XPATH, value='//*[@id="username"]')
        username_input.send_keys(username)

        password_input = driver.find_element(
            by=By.XPATH, value='//*[@id="password"]')
        password_input.send_keys(password)

        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/form/div[3]/button')))
        login_btn.click()

        time.sleep(3)

        alert_div = driver.find_element(
            by=By.XPATH, value='/html/body/div[1]/div[2]/div/div/div/div/div/div[1]').text

        if alert_div == ALERT_TEXT:
            logger.info(f'Logged in Successfully, But Needed Change Password, username={username}, password={password}')
            return True

        # logout_btn = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/div/div/form/button/span')))

        if driver.current_url == STATUS_URL_ADDRESS:
            logger.info(f'Logged in Successfully, username={username}, password={password}')
            return True
        else:
            raise Exception
    except Exception as e:
        logger.info(f'Failed Login Attempt, username={username}, password={password}')
        # logger.error(e.stacktrace[1])


def close_program(driver, logger):
    driver.close()
    logger.info('Program Finished Successfully')


def run_module(users_data):
    global LOGGER_FILE

    success_logged_in = []

    driver = create_driver()

    size_of_data = len(users_data)

    for index, item in enumerate(users_data):
        if login_into_page(driver, LOGIN_URL_ADDRESS, item[1], item[0], LOGGER_FILE):
            success_logged_in.append(item)
        print(f'{index + 1} of {size_of_data} done!')
        time.sleep(3)

    close_program(driver, LOGGER_FILE)

    return success_logged_in
