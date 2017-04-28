from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
import time
import utils

START_YEAR = 2017
START_MONTH = 4
START_DAY = 24

# binary = FirefoxBinary('/usr/bin/geckodriver')
browser = webdriver.Firefox()
# browser.set_window_size(1200, 800)
browser.implicitly_wait(30)


def init_browser():
    homepage = 'https://vms.zerochaos.com/ZCW/Login/Login?TabId=1'
    browser.get(homepage)


def login():
    account_filename = 'account.txt'

    with open(account_filename, 'r') as ins:
        username = ins.readline().strip()
        password = ins.readline().strip()

    username_elem = browser.find_element_by_id('Username')
    username_elem.send_keys(username)
    password_elem = browser.find_element_by_id('Password')
    password_elem.send_keys(password)
    password_elem.submit()


def navigate_to_add_timesheets_page():
    timesheets_elem = browser.find_element_by_link_text('Timesheets')
    timesheets_elem.click()
    time.sleep(1)
    add_timesheets_elem = browser.find_element_by_link_text('Add Timesheets')
    add_timesheets_elem.click()


def choose_ending_date():
    date_val = utils.get_date_by_days_after_with_weekday(year=START_YEAR, month=START_MONTH, day=START_DAY,
                                                         days_after=6)

    ending_elem = Select(browser.find_element_by_id('TimesheetEnding'))
    time.sleep(3)
    ending_elem.select_by_visible_text(date_val)
    time.sleep(3)


def add_line(days_after, pay_code, in_time, out_time):
    date_val = utils.get_date_by_days_after_with_weekday(year=START_YEAR, month=START_MONTH, day=START_DAY,
                                                         days_after=days_after)

    Select(browser.find_element_by_id('SelectedEntryDate')).select_by_visible_text(date_val)

    paycode_elem = Select(browser.find_element_by_id('SelectedPayCodeId'))
    time.sleep(3)
    paycode_elem.select_by_visible_text(pay_code)

    target_date = utils.get_date_by_days_after(year=START_YEAR, month=START_MONTH, day=START_DAY, days_after=days_after)
    add_time(in_or_out='TimeIn', pay_code=pay_code, target_date=target_date, in_out_time=in_time)
    add_time(in_or_out='TimeOut', pay_code=pay_code, target_date=target_date, in_out_time=out_time)

    add_line_elem = browser.find_element_by_id('addLine')
    add_line_elem.click()
    print('Added new line for pay code %s on %d days after first day\n' % (pay_code, days_after))
    time.sleep(3)


def add_time(in_or_out, pay_code, target_date, in_out_time):
    if in_or_out != 'TimeIn' and in_or_out != 'TimeOut':
        raise Exception()

    in_out_time = str(in_out_time)
    time_elem = browser.find_element_by_id(in_or_out)

    dates = []
    while len(dates) == 0:
        time_elem.click()
        time.sleep(3)
        dates = browser.find_elements_by_css_selector("div[style*='display: block'].xdsoft_datetimepicker td")

    print('Number of dates found: %d' % len(dates))
    print('Target date is ' + str(target_date.day))
    for d in dates:
        if d.is_displayed() and d.get_attribute('data-date') == str(target_date.day):
            if 'xdsoft_other_month' not in d.get_attribute('class') or target_date.day < START_DAY:
                d.click()
                print('clicked on date')
                time.sleep(3)
                break

    while pay_code == 'BP_Lunch_Time' and True:
        times = browser.find_elements_by_css_selector("div[style*='display: block'].xdsoft_datetimepicker div")
        print('Number of times found: %d' % len(times))
        print('Target time is ' + in_out_time)
        for t in times:
            try:
                if t.get_attribute('data-hour') == in_out_time:
                    browser.execute_script('arguments[0].scrollIntoView()', t)
                    t.click()
                    return
            except StaleElementReferenceException as e:
                print(e)
                break


if __name__ == '__main__':
    init_browser()
    login()
    navigate_to_add_timesheets_page()
    choose_ending_date()

    for i in range(5):
        add_line(days_after=i, pay_code='Regular Time', in_time=9, out_time=17)
        add_line(days_after=i, pay_code='BP_Lunch_Time', in_time=17, out_time=18)
    Select(browser.find_element_by_id('UserDefinedFieldListForTS_0__value')).select_by_visible_text('No')
