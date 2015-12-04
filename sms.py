import xlwt
from xlwt import Workbook
import os.path
import xlrd

completeName = os.path.join(os.path.dirname(__file__), '/sms.xls')
completeName = 'sms.xls'
book = xlrd.open_workbook(completeName)
sheet = book.sheet_by_index(0)

book1 = Workbook()
sheet1 = book1.add_sheet('Sheet1')
row = 0


for i in range(0, sheet.nrows):
    s = sheet.cell(i,0).value
    print(s)
    b = int(s)
    a = str(b)
    url = 'http://bhashsms.com/api/sendmsg.php?user=zostel&pass=zostel&sender=ZoRoom&phone=' + a + '&' + 'text=Dear ZO Captain,You are cordially invited to the ZO Rooms BONUS SCHEME LAUNCH.Address : Hotel Oyster, SCO 1-2-3, Sector 17 A, Opposite TAJ. Time : 11:00 AM. Lunch : 1:30 PM -Team ZO Rooms' + '&priority=ndnd&stype=normal?'
    sheet1.write(row,0,url)
    row+=1
    path = 'C:/Users/lenovo-pc/Desktop/'
    completeName = os.path.join(path, 'sms1.xls')
    book1.save(completeName+'.xls')
