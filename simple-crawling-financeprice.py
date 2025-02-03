# pip3 install requests
import requests
from bs4 import BeautifulSoup
codelist = ['005930', '066575', '005380', '035720', '034220', '003490']
def getPrice(code):
    data = requests.get(f'https://finance.naver.com/item/sise.nhn?code={code}')
    soup = BeautifulSoup(data.content, 'html.parser')
    return soup.find_all('strong', id="_nowVal")[0].text
for i in codelist:
    print(getPrice(i))
