__author__ = 'Camilla'

import time
import logging
from django.conf import settings
import unittest, xmlrunner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#you need to download chromdriver

logger = logging.getLogger(__name__)

TARGET_URL = 'https://www.kkbox.com/play/'

DRIVER_DIRS = {'chrome': settings.WEB_DRIVER_DIRS[0],
               'ie': settings.WEB_DRIVER_DIRS[1],
               'firefox': settings.WEB_DRIVER_DIRS[2],
               }

FB_TEST_ID = ''
FB_PWD = ''
TEST_ID = ''
TEST_PWD = ''



class Test_Login(unittest.TestCase):

    def setUp(self):
        self.browser = 'chrome'

        driver_dir = DRIVER_DIRS[self.browser]
        self.target_url = TARGET_URL
        if self.browser == 'chrome':
            self.driver = webdriver.Chrome(driver_dir)
        elif self.browser == 'ie':
            self.driver = webdriver.Ie(driver_dir)
        elif self.browser == 'firefox':
            self.driver = webdriver.Firefox()

        if self.driver:
            self.driver.get(self.target_url)
            self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def log_out(self):

        driver = self.driver
        #check the disabled menu is disaplayed
        if not (driver.find_element_by_css_selector("li.disabled").is_displayed()):
            logger.error("not displayed")
            driver.find_element_by_css_selector("i.icon.icon-user-dropdown").click()
        else:
            logger.error('show')
            #press logout button
            driver.find_element_by_xpath("//li[5]/a").click()


    def check_id(self, UID):
        driver = self.driver

        self.close_pop()

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "i.icon.icon-user-dropdown")
            ))
        except TimeoutException:
            driver.quit()

        driver.find_element_by_css_selector("i.icon.icon-user-dropdown").click()
        self.info = driver.find_element_by_css_selector("a.ng-binding").text.split()
        self.string_info = self.info[0]

        #make sure TEST_ID is same as id on the use-info-area
        self.assertIn(UID, self.string_info)
        print (self.info)



    #@unittest.skip('basic_login skiped')
    def test_basic_login(self):

        driver = self.driver

        try:
             WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[ng-model='loginObj.uid']")
            ))

        except TimeoutException:

            driver.quit()

        self.id_box = driver.find_element_by_css_selector("input[ng-model='loginObj.uid']")
        self.id_box.send_keys(TEST_ID)

        self.pwd_box = driver.find_element_by_css_selector("input[ng-model='loginObj.pwd']")
        self.pwd_box.send_keys(TEST_PWD)

        self.click_btn = driver.find_element_by_class_name('btn-confirm')
        self.click_btn.click()
        self.check_id(TEST_ID)

        time.sleep(2)

    def test_fb_test(self):

        driver = self.driver

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-invite")
                                               ))
        except TimeoutException:
            driver.quit()

        self.kkbox_wnd = driver.current_window_handle
        driver.find_element_by_css_selector('button.btn-invite').click()

        #switch window to facebook login popup window
        wnd_num = len(driver.window_handles)

        if wnd_num > 1:
            driver.switch_to.window(driver.window_handles[wnd_num-1])
            logger.error(driver.title)

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "pass")
                                               ))
        except TimeoutException:
            driver.quit()


        driver.find_element_by_id('email').clear()

        driver.find_element_by_id('email').send_keys(FB_TEST_ID)
        driver.find_element_by_id('pass').send_keys(FB_PWD)

        driver.find_element_by_id('u_0_2').click()

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.NAME, "__SKIP__")
                                           ))
        except TimeoutException:
            driver.quit()

        logger.error('find skip')
        driver.find_element_by_name('__SKIP__').click()

        driver.switch_to.window(self.kkbox_wnd)
        logger.error(driver.title)

        self.check_id(FB_TEST_ID)
        self.log_out()

class Test_Login_Firefox(Test_Login):
    def setUp(self):
        self.target_url = TARGET_URL

        self.driver = webdriver.Firefox()

        if self.driver:
            self.driver.get(self.target_url)

    def tearDown(self):
        super(Test_Login_Firefox, self).tearDown()


    def test_basic_login(self):
        super(Test_Login_Firefox, self).test_basic_login()

    # permission  problem" compatibility

class Test_Login_Ie(Test_Login):
    def setUp(self):
        self.target_url = TARGET_URL

        self.driver = webdriver.Ie()

        if self.driver:
            self.driver.get(self.target_url)


    def tearDown(self):
        super(Test_Login_Ie,self).tearDown()
    def test_basic_login(self):
        super(Test_Login_Ie,self).test_basic_login
    def test_fb_test(self):
        super(Test_Login_Ie, self).test_fb_test()


def load_test(browser):
    #pack test suite

    if browser== 'Chrome':
    #result = unittest.TestResult()
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_Login)
    elif browser == 'Firefox' :
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_Login_Firefox)
    elif browser == 'Ie':
         suite = unittest.TestLoader().loadTestsFromTestCase(Test_Login_Ie)



    #xmlrunner.XMLTestRunner(output='test.xml').run(suite)

    #suite.run()

    outdir = settings.TEST_REPORT

    result = xmlrunner.XMLTestRunner(
        output='xmlreport', verbosity=2,).run(suite)

    logger.error('********')
    print (result._stdout_data)

    print (result._stderr_data)
    print (result._report_testsuite)
    #logger.error( result.successes, result.failures, result.start_time)

    for s_item in result.successes:
        logger.error (s_item.get_description())

    logger.error("Passed time %s" %(result.elapsed_times))
    logger.error('********')

    report = {}

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result.start_time))
    #calculate elapsed
    elapesed_time = result.stop_time - result.start_time

    logger.error("%s %s "%(start_time, elapesed_time))


    report['start'] = start_time
    report['elapsed'] = elapesed_time
    #record the rest result


    report['total'] = result.testsRun

    report['failure'] = len(result.failures)

    report['pass'] = int(report['total']) - int(report['failure'])

    report['log'] = result

    return report



