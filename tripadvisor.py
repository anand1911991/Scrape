import selenium
import math
import xlwt
from xlwt import Workbook
import os.path
from selenium.webdriver.common.keys import Keys

driver = selenium.webdriver.Firefox()
driver.get("http://www.tripadvisor.in/Hotels-g1222155-Uttarkashi_Uttarakhand-Hotels.html")
hotel_names = driver.find_elements_by_css_selector("div.listing_title > a.property_title")
property_list = []
for hotel in hotel_names :     
    property_list.append(hotel.get_attribute('id'))
#print(property_list)
driver.close()
for x in property_list:
    endpoint = x.replace('property_', 'd')
    test = '.html'
    url = 'http://www.tripadvisor.in/Hotel_Review-g1222155-' + endpoint + test
    driver = selenium.webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(30)
    hotel_name = driver.find_element_by_css_selector('div#HEADING_GROUP > div.headingWrapper.easyClear > div.heading_name_wrapper > h1#HEADING.heading_name')
    name = hotel_name.text
    print(name, '\n')
    driver.implicitly_wait(100)
    n_pages = driver.find_element_by_css_selector('div#HEADING_GROUP > div.headingWrapper.easyClear > div.heading_ratings > div.heading_rating.separator > div.rs.rating > a.more.taLnk > span').text
    n_pages = n_pages.replace(',','')
    y = float(n_pages)
    y = y/10
    z = math.ceil(y)
    z1 = int(z) + 1
    #print (z1)
    book = Workbook(encoding = 'utf-8')
    sheet1 = book.add_sheet('Sheet1')
    row = 0
    driver.close()
    for i in range(1,z1) :
        a = (i-1)*10
        #print(a)
        ext = 'Reviews-or%d' % a
        n_endpoint = 'http://www.tripadvisor.in/Hotel_Review-g1222155-' + endpoint
        f_endpoint = n_endpoint + ext
        url2 = f_endpoint + test
        #print(url2)
        driver = selenium.webdriver.Firefox()
        driver.get(url2)
        driver.implicitly_wait(100)
        expansion = driver.find_element_by_css_selector('p.partial_entry > span.partnerRvw > span')
        expansion.click()
        driver.implicitly_wait(150)
        container = driver.find_elements_by_css_selector("div#REVIEWS > div.reviewSelector")
        #print (container)
        for each_container in container :
            all_ratings = each_container.find_element_by_css_selector('span.rate.sprite-rating_s.rating_s > img.sprite-rating_s_fill').get_attribute('alt')
            all_reviews = each_container.find_elements_by_css_selector('div > div.entry > p')
            length = len(all_reviews)
            reviews = all_reviews[length-1].text
            print(all_ratings, '\t', reviews, '\n')
            sheet1.write(row,0,all_ratings)
            sheet1.write(row,1,reviews)
            row += 1
        row = row
        path = 'C:/Users/lenovo-pc/Desktop/Uttarkashi'
        completeName = os.path.join(path, name+'.xls')
        book.save(completeName+'.xls')
        driver.close()



