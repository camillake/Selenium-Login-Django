__author__ = 'Camilla'

import unittest
import io
import time
import re
import logging
from django.utils import timezone
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException
from selenium.common.exceptions import ErrorInResponseException, WebDriverException
from .personal import *

# you need to download chromdriver and put it under specified directory

logger = logging.getLogger(__name__)

TARGET_URL = 'https://www.kkbox.com/play/'

DRIVER_DIRS = {'Chrome': settings.WEB_DRIVER_DIRS[0],
               'Ie': settings.WEB_DRIVER_DIRS[1],
               'Safari': settings.WEB_DRIVER_DIRS[2],
               }

class Test_Login(unittest.TestCase):

    def setUp(self):

        browser = 'Chrome'
        driver_dir = DRIVER_DIRS[browser]

        self.target_url = TARGET_URL

        if browser == 'Chrome':
            self.driver = webdriver.Chrome(driver_dir)
        elif browser == 'Ie':
            self.driver = webdriver.Ie(driver_dir)
        elif browser == 'Safari':
            self.driver = webdriver.Safari()
        else:
            logger.debug('Browser Not Matched')
            self.driver.quit()

        try:
            self.driver.get(self.target_url)
            self.driver.maximize_window()
        except (ErrorInResponseException, WebDriverException)as ec:
            logger.exception(ec)

    def tearDown(self):
        logger.debug('teardown')
        self.driver.quit()

    def log_out(self):

        if settings.DEBUG:
            time.sleep(2)

        driver = self.driver
        # check the disabled menu is disaplayed
        if not (driver.find_element_by_css_selector("li.disabled").is_displayed()):
            logger.debug("drop-down menu not displayed")
            driver.find_element_by_css_selector("i.icon.icon-user-dropdown").click()
        else:
            logger.debug('drop-down menu displayed')
            # press logout button
            driver.find_element_by_xpath("//li[5]/a").click()
            logger.debug('press Logout')

    def close_pop(self):
        driver = self.driver
        try:
            driver.implicitly_wait(5)
            close_element = driver.find_element_by_xpath("//div[@class='close ng-scope']/img")
        except (NoSuchElementException, ElementNotVisibleException) as ec:
            logger.exception(ec)
            logger.debug('Pop up window not displayed')
            return
        except TimeoutException as ec:
            logger.exception(ec)
            return

        logger.debug('Pop-up window closed')
        close_element.click()

    def check_id(self, uid):
        driver = self.driver

        # close pop window if there is
        self.close_pop()

        '''
        if settings.DEBUG:
            time.sleep(2)
        '''
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "i.icon.icon-user-dropdown")
            ))
        except TimeoutException as ec:
            logger.exception(ec)
            driver.quit()

        logger.debug("Window title:%s" % driver.title)

        driver.find_element_by_css_selector("i.icon.icon-user-dropdown").click()
        info = driver.find_element_by_css_selector("a.ng-binding").text.split()
        string_info = info[0]

        # make sure TEST_ID is same as id on the use-info-area
        logger.debug("user account: %s" % string_info)

        self.assertIn(uid, string_info)

    # @unittest.skip('temporarily')
    def test_basic_login(self):

        driver = self.driver
        try:
             WebDriverWait(driver,0).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[ng-model='loginObj.uid']")
            ))
        except TimeoutException as ec:
            logger.exception(ec)
            driver.quit()

        id_box = driver.find_element_by_css_selector("input[ng-model='loginObj.uid']")
        id_box.clear()
        id_box.send_keys(TEST_ID)

        pwd_box = driver.find_element_by_css_selector("input[ng-model='loginObj.pwd']")
        pwd_box.clear()
        pwd_box.send_keys(TEST_PWD)

        click_btn = driver.find_element_by_class_name('btn-confirm')
        click_btn.click()
        self.check_id(TEST_ID)

        self.log_out()

    # @unittest.skip('FB')
    def test_fb_test(self):

        driver = self.driver

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-invite")
                                               ))
        except TimeoutException as ec:
            logger.exception(ec)
            driver.quit()
        # Get current window handler
        kkbox_wnd = driver.current_window_handle

        driver.find_element_by_css_selector('button.btn-invite').click()

        # Select a frame by its (zero-based) index.
        # switch window to popup window of FaceBook
        wnd_num = len(driver.window_handles)

        if wnd_num > 1:
            driver.switch_to.window(driver.window_handles[wnd_num-1])
            logger.debug("Window title:%s" % driver.title)
        else:
            logger.error('Cant get Facebook Login wnd')
            driver.quit()

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "pass")
                                               ))
        except (TimeoutException, NoSuchElementException) as ec:
            logger.exception(ec)
            driver.quit()

        account_box = driver.find_element_by_id('email')
        account_box.clear()
        account_box.send_keys(FB_TEST_ID)

        pwd_box = driver.find_element_by_id('pass')
        pwd_box.clear()
        pwd_box.send_keys(FB_PWD)

        driver.find_element_by_id('u_0_2').click()

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.NAME, "__SKIP__")
                                           ))
        except TimeoutException:
            driver.quit()

        logger.debug('find skip btn')
        driver.find_element_by_name('__SKIP__').click()

        driver.switch_to.window(kkbox_wnd)

        self.check_id(FB_TEST_ID)

        self.log_out()

    @unittest.skip('elapsed time confirmation purpose')
    def test_sleep(self):

        #self.assertIn('3','bbb')
        self.assertEqual(0, 2/0)
        time.sleep(2)

# error msg :Permission denied to access property "_isWrap" self.log_out()

class Test_Login_Safari(Test_Login):

    def setUp(self):
        self.target_url = TARGET_URL

        self.driver_dir = DRIVER_DIRS['Safari']
        self.driver = webdriver.Safari()

        self.driver.get(self.target_url)


class Test_Login_Ie(Test_Login):

    def setUp(self):
        self.target_url = TARGET_URL

        self.driver = webdriver.Ie()

        if self.driver:
            self.driver.get(self.target_url)

def handle_result(testresult, detail):

    failure_cnt = len(testresult.failures)
    errors_count = {}
    for error in testresult.errors:
        errors_count[error[0]] = errors_count.get(error[0], 0)+1

    logger.debug("Error total is : %d\n" % len(errors_count))

    failures = failure_cnt + len(errors_count)
    total = testresult.testsRun
    passrun = total - failures

    # fill in test result

    report = {}

    # use regular expression to retrive elpased time

    stringlines = detail.strip().splitlines()

    logger.debug("\n****test report :\n%s\n********\n", stringlines)

    # match elpased time from the last 3rd line in stringline
    elapsed_time = re.findall('tests\sin\s([0-9]*\.?[0-9]*)s', stringlines[-3])

    report['elapsed'] = float(elapsed_time[0]) if len(elapsed_time) else 0

    # record the rest result

    report['total'] = testresult.testsRun

    report['failure'] = failures
    report['pass'] = passrun

    report['detail'] = detail

    return report


def load_test(browser):
    # pack test suite

    if browser == 'Chrome':
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_Login)
    elif browser == 'Safari':
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_Login_Safari)
    elif browser == 'Ie':
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_Login_Ie)

    # output stream collector
    outputio = io.StringIO()

    # get start time, type is aware datetime (include timezone)
    starttime = timezone.now()

    result = unittest.TextTestRunner(stream=outputio, verbosity=2).run(suite)

    outputstr = outputio.getvalue()
    outputio.close()
    resultdict = handle_result(result, outputstr)
    resultdict['start'] = starttime

    return resultdict
