from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from dotenv import load_dotenv
load_dotenv()

print("BUP UCAM Automation")

browser = webdriver.Firefox()
browser.get('https://ucam.bup.edu.bd/')

print("Logging In...")

user_elem = browser.find_element(By.ID, 'UserId')
user_elem.send_keys(os.environ["USERID"])

password_elem = browser.find_element(By.ID, 'Password')
password_elem.send_keys(os.environ["PASSWORD"])
password_elem.submit()

WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'ctl00_lblLogout')))
student_name = browser.find_element(By.ID, 'ctl00_lblAvatarName').text

print("Login Successful")
print("Welcome, " + student_name)

examMark_elem = browser.find_element(By.LINK_TEXT, 'Current Exam Mark')
examMark_elem.click()

# WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/div[3]/div/div/div/div[1]/label')))

select_element = browser.find_element(By.NAME, 'ctl00$MainContainer$ddlSession')
select = Select(select_element)
select.select_by_value('1066')

#WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'ctl00_MainContainer_gvExamMarkSummary')))
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_MainContainer_gvExamMarkSummary_ctl02_btnViewDetails"]')))


viewdetail_elem1 = browser.find_element(By.NAME, 'ctl00$MainContainer$gvExamMarkSummary$ctl02$btnViewDetails')
viewdetail_elem1.click()

WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl02_lblMarks"]')))

class TheoryCourse:
    def __init__(self, serial, code, title):
        self.serial = serial
        self.code = code
        self.title = title
        self.CT1 = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl02_lblMarks').text
        self.CT2 = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl03_lblMarks').text
        self.CT3 = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl04_lblMarks').text
        self.CT4 = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl05_lblMarks').text
        self.mid = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl06_lblMarks').text
        self.assignment = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl07_lblMarks').text
        self.attendance = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl08_lblMarks').text

class LabCourse:
    def __init__(self, serial, code, title):
        self.serial = serial
        self.code = code
        self.title = title
        self.quiz = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl02_lblMarks').text
        self.report = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl03_lblMarks').text
        self.performance = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl04_lblMarks').text
        self.viva = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl05_lblMarks').text
        self.attendance = browser.find_element(By.ID, 'ctl00_MainContainer_gvgvExamMarkSummaryDetails_ctl06_lblMarks').text
        
c1 = TheoryCourse(browser.find_element(By.XPATH, "(//b[contains(text(),'1')])[1]").text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl02_lblFormalCode').text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl02_lblTitle').text)

viewdetail_elem2 = browser.find_element(By.NAME, 'ctl00$MainContainer$gvExamMarkSummary$ctl03$btnViewDetails')
viewdetail_elem2.click()
time.sleep(3)
c2 = LabCourse(browser.find_element(By.XPATH, "(//b[contains(text(),'2')])[1]").text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl03_lblFormalCode').text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl03_lblTitle').text)

viewdetail_elem3 = browser.find_element(By.NAME, 'ctl00$MainContainer$gvExamMarkSummary$ctl04$btnViewDetails')
viewdetail_elem3.click()
time.sleep(3) # Had to implement time.sleep() because i cant find any new to presence_of_element_located() . Otherwise it takes the previous course values because Table loads fast with same elements and IDs.
c3 = TheoryCourse(browser.find_element(By.XPATH, "(//b[contains(text(),'3')])[1]").text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl04_lblFormalCode').text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl04_lblTitle').text)

viewdetail_elem4 = browser.find_element(By.NAME, 'ctl00$MainContainer$gvExamMarkSummary$ctl05$btnViewDetails')
viewdetail_elem4.click()
time.sleep(3)
c4 = TheoryCourse(browser.find_element(By.XPATH, "(//b[contains(text(),'4')])[1]").text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl05_lblFormalCode').text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl05_lblTitle').text)

viewdetail_elem5 = browser.find_element(By.NAME, 'ctl00$MainContainer$gvExamMarkSummary$ctl06$btnViewDetails')
viewdetail_elem5.click()
time.sleep(3)
c5 = LabCourse(browser.find_element(By.XPATH, "(//b[contains(text(),'5')])[1]").text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl06_lblFormalCode').text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl06_lblTitle').text)

viewdetail_elem6 = browser.find_element(By.NAME, 'ctl00$MainContainer$gvExamMarkSummary$ctl07$btnViewDetails')
viewdetail_elem6.click()
time.sleep(3)
c6 = TheoryCourse(browser.find_element(By.XPATH, "(//b[contains(text(),'6')])[1]").text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl07_lblFormalCode').text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl07_lblTitle').text)

viewdetail_elem7 = browser.find_element(By.NAME, 'ctl00$MainContainer$gvExamMarkSummary$ctl08$btnViewDetails')
viewdetail_elem7.click()
time.sleep(3)
c7 = LabCourse(browser.find_element(By.XPATH, "(//b[contains(text(),'7')])[1]").text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl08_lblFormalCode').text, browser.find_element(By.ID, 'ctl00_MainContainer_gvExamMarkSummary_ctl08_lblTitle').text)

print(c1.serial)
print(c1.code)
print(c1.title)
print(c1.CT1)
print(c1.CT2)
print(c1.CT3)
print(c1.CT4)
print(c1.mid)
print(c1.assignment)
print(c1.attendance)
print("==================")
print(c2.serial)
print(c2.code)
print(c2.title)
print(c2.quiz)
print(c2.report)
print(c2.performance)
print(c2.viva)
print(c2.attendance)
print("==================")
print(c3.serial)
print(c3.code)
print(c3.title)
print(c3.CT1)
print(c3.CT2)
print(c3.CT3)
print(c3.CT4)
print(c3.mid)
print(c3.assignment)
print(c3.attendance)
print("==================")
print(c4.serial)
print(c4.code)
print(c4.title)
print(c4.CT1)
print(c4.CT2)
print(c4.CT3)
print(c4.CT4)
print(c4.mid)
print(c4.assignment)
print(c4.attendance)
print("==================")
print(c5.serial)
print(c5.code)
print(c5.title)
print(c5.quiz)
print(c5.report)
print(c5.performance)
print(c5.viva)
print(c5.attendance)
print("==================")
print(c6.serial)
print(c6.code)
print(c6.title)
print(c6.CT1)
print(c6.CT2)
print(c6.CT3)
print(c6.CT4)
print(c6.mid)
print(c6.assignment)
print(c6.attendance)
print("==================")
print(c7.serial)
print(c7.code)
print(c7.title)
print(c7.quiz)
print(c7.report)
print(c7.performance)
print(c7.viva)
print(c7.attendance)

# TODO: add JSON functionality