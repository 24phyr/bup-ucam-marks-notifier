from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time
from dotenv import load_dotenv
load_dotenv()

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

i = 0
while True:
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

    course_data = {
        "Theory Course": [
            {"Serial": c1.serial, "Course Code": c1.code, "Course Title": c1.title, "Class Test 1": c1.CT1, "Class Test 2": c1.CT2, "Class Test 3": c1.CT3, "Class Test 4": c1.CT4, "Mid Term": c1.mid, "Project paper/Assignments /Term Paper (Individual) including Presentation": c1.assignment, "Attendance": c1.attendance},
            {"Serial": c3.serial, "Course Code": c3.code, "Course Title": c3.title, "Class Test 1": c3.CT1, "Class Test 2": c3.CT2, "Class Test 3": c3.CT3, "Class Test 4": c3.CT4, "Mid Term": c3.mid, "Project paper/Assignments /Term Paper (Individual) including Presentation": c3.assignment, "Attendance": c3.attendance},
            {"Serial": c4.serial, "Course Code": c4.code, "Course Title": c4.title, "Class Test 1": c4.CT1, "Class Test 2": c4.CT2, "Class Test 3": c4.CT3, "Class Test 4": c4.CT4, "Mid Term": c4.mid, "Project paper/Assignments /Term Paper (Individual) including Presentation": c4.assignment, "Attendance": c4.attendance},
            {"Serial": c6.serial, "Course Code": c6.code, "Course Title": c6.title, "Class Test 1": c6.CT1, "Class Test 2": c6.CT2, "Class Test 3": c6.CT3, "Class Test 4": c6.CT4, "Mid Term": c6.mid, "Project paper/Assignments /Term Paper (Individual) including Presentation": c6.assignment, "Attendance": c6.attendance}
        ],
        "Lab Course": [
            {"Serial": c2.serial, "Course Code": c2.code, "Course Title": c2.title, "Quiz": c2.quiz, "Home Assignment / Report": c2.report, "Class Performance / Observation": c2.performance, "Viva": c2.viva, "Attendnace": c2.attendance},
            {"Serial": c5.serial, "Course Code": c5.code, "Course Title": c5.title, "Quiz": c5.quiz, "Home Assignment / Report": c5.report, "Class Performance / Observation": c5.performance, "Viva": c5.viva, "Attendnace": c5.attendance},
            {"Serial": c7.serial, "Course Code": c7.code, "Course Title": c7.title, "Quiz": c7.quiz, "Home Assignment / Report": c7.report, "Class Performance / Observation": c7.performance, "Viva": c7.viva, "Attendnace": c7.attendance}
        ]
    }
    
    if i % 2 == 0:
        with open("output1.json", "w") as outfile:
            json.dump(course_data, outfile, indent=4)
    elif i % 2 == 1:
        with open("output2.json", "w") as outfile:
            json.dump(course_data, outfile, indent=4)
    i += 1