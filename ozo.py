__author__ = 'lenovo-pc'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import xlwt
from xlwt import Workbook
import os.path
import xlrd

completeName = os.path.join(os.path.dirname(__file__), '/href.xls')
completeName = 'href.xls'
book = xlrd.open_workbook(completeName)
sheet = book.sheet_by_index(0)

book1 = Workbook()
sheet1 = book1.add_sheet('Sheet1')
row = 0

for i in range(0, sheet.nrows):
    s = sheet.cell(i,0).value
    print(s)
    list = []
    driver = webdriver.Firefox()
    driver.get(s)
    driver.implicitly_wait(5)
    try :
        container = driver.find_elements_by_css_selector('html > body > table > tbody > tr > td')
        for i in range (1,15) :
            if (i%2 == 1):
                list.append(container[i].text)
        # z = len(container)
        # print(z)
    except :
        pass

    try :
        container1 =  driver.find_elements_by_css_selector('html > body > table > tbody > tr > td > a')
        list.append(container1[0].text)
        list.append(container1[1].text)
    except :
        pass

    z = len(list)
    for j in range (0,z) :
        sheet1.write(row,j,list[j])
    row += 1
    path = 'C:/Users/lenovo-pc/Desktop/'
    completeName = os.path.join(path, 'ta.xls')
    book1.save(completeName+'.xls')
    driver.close()
