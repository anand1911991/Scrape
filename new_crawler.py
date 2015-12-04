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


# chromedriver = "/Users/lenovo-pc/Downloads/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver
# driver = webdriver.Chrome(chromedriver)

for i in range(0, sheet.nrows):
    s = sheet.cell(i,0).value
    print(s)
    driver = webdriver.Firefox()
    driver.get(s)
    driver.implicitly_wait(10)
    try :
        rooms = driver.find_elements_by_css_selector('div.row > div.highlightsWrapper.clearFix >'
                                                     ' div.col.col9.highlightCard.factSheet > div.hInfo.row > '
                                                     'nav > ul.clearFix.hotelStats > li > span')
    except :
        pass

    property5_list = []
    property6_list = []
    for room in rooms :
        d = room.text
        property5_list.append(d)
    z = len(property5_list)
    print(property5_list[z-2])
    print(property5_list[z-1])

    try :
        address = driver.find_element_by_css_selector('div.row > div.highlightsWrapper.clearFix > '
                                                      'div#mapOverview.col.col15.locationCard > div.hInfo.row > '
                                                      'div.colZero.col12 > span.hotelAddress > small.truncate').text
    except:
        address = '-'

    try :
        n_reviews = driver.find_element_by_css_selector('div.row.reviewsContainer.content >'
                                                        'div.clearFix.hotelreviews.pad > div.col.col7.taJist >'
                                                        ' div.taBreakup > nav > ul > li > span > small').text
    except :
        n_reviews = 0
        #ratings = driver.find_elements_by_css_selector('div.row.reviewsContainer.content > div.clearFix.hotelreviews.pad > div.col.col7.taJist > div.taBreakup > nav > ul > li > span.taRating.t4')
    try :
        rating_element = driver.find_element_by_css_selector("div.taBreakup > nav > ul")
    except :
        rating_element = '-'
    try :
        list_items = rating_element.find_elements_by_tag_name("li")
    except :
        pass
    try :
        ta_overall = list_items[0].find_element_by_tag_name("span").get_attribute("title")
    except :
        ta_overall = '-'
    try:
        ta_location = list_items[1].find_element_by_tag_name("span").get_attribute("title")
    except :
        ta_location = '-'
    try :
        ta_rooms = list_items[2].find_element_by_tag_name("span").get_attribute("title")
    except :
        ta_rooms = '-'
    try :
        ta_service = list_items[3].find_element_by_tag_name("span").get_attribute("title")
    except :
        ta_service = '-'
    try :
        ta_value = list_items[4].find_element_by_tag_name("span").get_attribute("title")
    except :
        ta_value = '-'
    try:
        ta_cleanliness = list_items[5].find_element_by_tag_name("span").get_attribute("title")
    except :
        ta_cleanliness = '-'

    #print(address, '\t', n_reviews , '\t', ta_overall , '\t' , ta_location , '\t', ta_rooms , '\t', ta_service , '\t', ta_value , '\t', ta_cleanliness)
    # sheet1.write(row,0,property1_list[i])
    sheet1.write(row,1,address)
    sheet1.write(row,2,property5_list[z-1])
    sheet1.write(row,3,property5_list[z-2])
    sheet1.write(row,4,n_reviews)
    sheet1.write(row,5,ta_overall)
    sheet1.write(row,6,ta_location)
    sheet1.write(row,7,ta_rooms)
    sheet1.write(row,8,ta_service)
    sheet1.write(row,9,ta_value)
    sheet1.write(row,10,ta_cleanliness)
    row += 1
    path = 'C:/Users/lenovo-pc/Desktop/'
    completeName = os.path.join(path, 'pune.xls')
    book1.save(completeName+'.xls')
    driver.close()