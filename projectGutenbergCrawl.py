from bs4 import BeautifulSoup as bs
import requests as req
import os
import re

folderPath = 'data'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

url = "https://www.gutenberg.org/browse/languages/zh"
res = req.get(url) 
soup = bs(res.text, "lxml") 

linkList = []
numList = []
bookNames = []
upper = 1000
count = 0

for a in soup.select('body > div.container > div > div.pgdbbylanguage > ul > li > a'):
    link='https://www.gutenberg.org'+a['href'] 
    
    num_split = a['href'].split('/')
    num = num_split[-1]
    numList.append(num)
    bookNames.append(a.get_text())
    
    linkList.append('https://www.gutenberg.org/files/'+num+'/'+num+'-0.txt')
    
    count += 1
    if count == upper:
        break

print(f"取得{len(linkList)}個連結!")

def writeBook(i):
    if (i >= len(linkList)):
        print("沒那麼多書")
        return

    subRes = req.get(linkList[i])
    subRes.encoding='utf-8' 
    subSoup = bs(subRes.text, "lxml")
    
    txt = subSoup.get_text()
    r = r'[A-Z]|[a-z]|\d|,|\.|-|:|\/|\s|\#|\[|\]|\*|\(|\)|\"|\!|@|\$|\%|\''
    txtChinese = re.sub(r, '', txt)
    
    rd = r'\W'
    bookNames[i] = re.sub(rd, '', bookNames[i])
    bookNames[i] = bookNames[i].split("\r")[0]
    bookNames[i] = bookNames[i].split("/")[0]
    txtChinese = bookNames[i] + " " + txtChinese
    
    file = open(f"{folderPath}/{bookNames[i]}.txt", 'w', encoding='UTF-8')
    file.write(txtChinese)
    print(f"第{str(i)}本：{bookNames[i]}寫好了")

for i in range(5):
    writeBook(i)