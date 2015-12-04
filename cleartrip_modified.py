from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import xlwt
from xlwt import Workbook
import os.path


book = Workbook()
sheet1 = book.add_sheet('Sheet1')
row = 0
#print os.path.dirname(__file__)
completeName = os.path.join(os.path.dirname(__file__), '/cleartrip_bangalore.xls')
#print completeName
completeName = 'cleartrip_bangalore.xls'
book.save(completeName)

def scrollDown(browser, numberOfScrollDowns):
    body = browser.find_element_by_tag_name("body")
    while numberOfScrollDowns >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        numberOfScrollDowns -= 1
    return browser

browser = webdriver.Firefox()
browser.get("http://www.cleartrip.com/hotels/results?city=Kolkata&state=West+Bengal&country=IN&area=&poi=&hotelId=&hotelName=&dest_code=34600&chk_in=04%2F06%2F2015&chk_out=05%2F06%2F2015&adults1=1&children1=0&num_rooms=1")
browser = scrollDown(browser, 1000)
browser.implicitly_wait(10)

property1_list = []
property2_list = []
property3_list = []

container = browser.find_elements_by_css_selector("nav.hotelsList > "
                                                "ul.listView.clearFix > li.listItem.listUnit.clearFix")
for each_container in container[:700]:
    hotel_list_element = each_container
    hotel_meta_data = {'ota_sender': 'CLRTRP'}
    info_meta_data = dict()

    basic_info = hotel_list_element.find_element_by_css_selector('nav.summary > ul.inline > li.info')
    hotel_name_link = basic_info.find_element_by_css_selector("h2 > a")
    hotel_name = hotel_name_link.text
    print (hotel_name)
    address = 'N/A'
    lat_long = '0.00,0.00'
    try:
        address = hotel_list_element.get_attribute('data-area')
    except:
        address = 'N/A'

    try:
        lat_long = hotel_list_element.get_attribute('data-latlng')
    except:
        lat_long = '0.00,0.00'

    hotel_meta_data['address'] = address
    try:
        hotel_meta_data['lat'] = lat_long.split(',')[0]
        hotel_meta_data['lon'] = lat_long.split(',')[1]
    except:
        hotel_meta_data['lat'] = 0.00
        hotel_meta_data['lon'] = 0.00

    hotel_loc = 'N/A'
    hotel_meta_data['ota_specific_id'] = hotel_list_element.get_attribute('id')
    try:
        hotel_loc = hotel_list_element.find_element_by_class_name('areaName').get_attribute('data-area')
    except:
        hotel_loc = 'N/A'

    hotel_meta_data['hotel_name'] = hotel_name
    hotel_meta_data['locality'] = hotel_loc

    try:
        price_info = hotel_list_element.find_element_by_class_name("perRoomPrDisp")
        el1 = price_info.find_element_by_tag_name("strong")
        product_price = el1.find_element_by_class_name("INR")
        element = product_price.get_attribute("data-pr")
        info_meta_data['price'] = element
    except:
        info_meta_data['price'] = "-"

    link = hotel_name_link.get_attribute('href')
    # print link
    #
    if link == "javascript:void(0)":
        hotel_name_link.click()
        browser.implicitly_wait(10)
        browser.switch_to_frame('modal_window')
        try:
            info_elements = browser.find_element_by_css_selector("div.hInfo.row > nav > ul.clearFix")

            # unordered_list = info_elements.find_element_by_tag_name("ul")
            list_items = info_elements.find_elements_by_tag_name("li")
        except:
            pass

        try:
            rooms_info = list_items[2]
            num_rooms = rooms_info.find_element_by_tag_name("span").text
            info_meta_data['num_rooms'] = num_rooms
        except:
            info_meta_data['num_rooms'] = "-"

        try:
            floors_info = list_items[3]
            num_floors = floors_info.find_element_by_tag_name("span").text
            info_meta_data['num_floors'] = num_floors
        except:
            info_meta_data['num_floors'] = '-'

        try:
            browser.find_element_by_xpath("//a[@rel='taReviews']").click()
            browser.implicitly_wait(1)
            div_element = browser.find_element_by_css_selector("div.taBreakup > nav > ul")

            list_items = div_element.find_elements_by_tag_name("li")

            info_meta_data['reviews'] = list_items[0].find_element_by_css_selector("span > small").text
            info_meta_data['ta_overall'] = list_items[0].find_element_by_tag_name("span").get_attribute("title")
            info_meta_data['ta_location'] = list_items[1].find_element_by_tag_name("span").get_attribute("title")
            info_meta_data['ta_room'] = list_items[2].find_element_by_tag_name("span").get_attribute("title")
            info_meta_data['ta_service'] = list_items[3].find_element_by_tag_name("span").get_attribute("title")
            info_meta_data['ta_value'] = list_items[4].find_element_by_tag_name("span").get_attribute("title")
            info_meta_data['ta_cleanliness'] = list_items[5].find_element_by_tag_name("span").get_attribute("title")

        except:
            info_meta_data['reviews'] = '-'
            info_meta_data['ta_overall'] = '-'
            info_meta_data['ta_location'] = '-'
            info_meta_data['ta_room'] = '-'
            info_meta_data['ta_service'] = '-'
            info_meta_data['ta_value'] = '-'
            info_meta_data['ta_cleanliness'] = '-'

        browser.switch_to_default_content()
        browser.find_element_by_id("close").click()

    else:
        driver = webdriver.Firefox()
        driver.get(link)
        driver.implicitly_wait(20)

        try:
            rooms = driver.find_elements_by_css_selector('div.row > div.highlightsWrapper.clearFix > div.col.col9.highlightCard.factSheet > div.hInfo.row > nav > ul.clearFix.hotelStats > li > span')

            rooms_info = rooms[3]
            floors_info = rooms[2]
            info_meta_data['num_rooms'] = rooms_info.text
            info_meta_data['num_floors'] = floors_info.text

        except :
            info_meta_data['num_rooms'] = "-"
            info_meta_data['num_floors'] = "-"



        try:
            info_meta_data['reviews'] = driver.find_element_by_css_selector('div.row.reviewsContainer.content > '
                                                                            'div.clearFix.hotelreviews.pad > '
                                                                            'div.col.col7.taJist > div.taBreakup > '
                                                                            'nav > ul > li > span > small').text
        except:
            info_meta_data['reviews'] = "-"
        try:
            rating_element = driver.find_element_by_css_selector("div.taBreakup > nav > ul")
        except:
            rating_element = 0
        try:
            list_items = rating_element.find_elements_by_tag_name("li")
        except:
            pass
        try:
            info_meta_data['ta_overall'] = list_items[0].find_element_by_tag_name("span").get_attribute("title")
        except :
            info_meta_data['ta_overall'] = "-"
        try:
            info_meta_data['ta_location'] = list_items[1].find_element_by_tag_name("span").get_attribute("title")
        except:
            info_meta_data['ta_location'] = '-'
        try:
            info_meta_data['ta_room'] = list_items[2].find_element_by_tag_name("span").get_attribute("title")
        except:
            info_meta_data['ta_room'] = '-'
        try:
            info_meta_data['ta_service'] = list_items[3].find_element_by_tag_name("span").get_attribute("title")
        except:
            info_meta_data['ta_service'] = '-'
        try:
            info_meta_data['ta_value'] = list_items[4].find_element_by_tag_name("span").get_attribute("title")
        except:
            info_meta_data['ta_value'] = '-'
        try:
            info_meta_data['ta_cleanliness'] = list_items[5].find_element_by_tag_name("span").get_attribute("title")
        except :
            info_meta_data['ta_cleanliness'] = '-'

        driver.close()

    hotel_meta_data.update(info_meta_data)
    #print hotel_meta_data

    i = 0

    if row == 0:
        for (key, val) in hotel_meta_data.items():
            sheet1.write(row, i, key)
            i += 1
    row += 1
    i = 0
    for (key, val) in hotel_meta_data.items():
        sheet1.write(row, i, val)
        i += 1
    book.save(completeName)
browser.close()
