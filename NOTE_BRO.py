from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import time, random, re
import requests
class post:
    def __init__(self, year, f_type, f_name, post_link):
        self.year = year
        self.f_type = f_type
        self.f_name = f_name
        self.post_link = post_link

class NOTE_BRO:
    def __init__(self):
        self.__driver = wb.Chrome()
        self.page_src = ''
        self.__cookie = ''
        self.__pages = 0
        ##give a global id to count the files
        ##and used to name the files
        self.__file_id = 1


    def random_headers(self):
        headers = [
            'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 ' +
            '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
            '(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
            '(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 ' +
            '(KHTML, like Gecko) Mwendo/1.1.5 Safari/537.21',
            'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)'
        ]
        index = random.randint(0, 5)
        return headers[index]


    def login(self):
        home_url = 'http://www.notebro.com/forum/'
        self.__driver.get(url=home_url)
        self.__driver.find_element_by_css_selector('input#modlgn-username').send_keys('LuckyE')
        self.__driver.find_element_by_css_selector('input#modlgn-passwd').send_keys('haoyangliu96')
        self.__driver.find_element_by_css_selector('input#autologin').click()
        self.__driver.find_element_by_name('login').click()

    def search(self, kw1, kw2=''):
        start = time.time()
        while True:
            try:
                end = time.time()
                search = self.__driver.find_element_by_css_selector('input#roksearch_search_str')
                break
            except NoSuchElementException:
                if((end - start) > 10):
                    raise TimeoutError
        search.clear()
        search.send_keys(kw1)
        search.send_keys(Keys.ENTER)

        search_result = self.__driver.find_element_by_id('add_keywords')
        search_result.send_keys(kw2)
        search_result.send_keys(Keys.ENTER)
        self.__cookie = self.__driver.get_cookies()
        self.page_src = self.__driver.page_source
        print(self.__cookie)

    def open_post(self, url):
        #url = 'http://www.notebro.com/forum/viewtopic.php?f=2&t=52087&p=55070&hilit' \
        #       '=crm+1300#p55070'
        user_agent = self.random_headers()
        headers = requests.utils.default_headers()
        headers.update({'User-Agent': user_agent})
        req = requests.request('get', url=url, cookies=self.__cookie)

        print()

    def get_content_list(self):
        soup = bs(self.page_src, 'lxml')
        search_post = []
        post_list = []
        for post in soup.find_all(name='div', class_='search post bg2'):
            search_post.append(post)
        for post in soup.find_all(name='div', class_='search post bg1'):
            search_post.append(post)

        for post in search_post:
            post_link = 'http://www.notebro.com/forum/' + post.find(name='a')['href'][2:]
            year = re.search('.*(20\d{2}).*', post.find(name='div', class_='content').text)
            if (year):
                year = year.group(1)
            Post = {'link':post_link, 'year':year}
            post_list.append(Post)

        return post_list

def main():
    note_bro = NOTE_BRO()
    note_bro.login()
    note_bro.search(kw1='crm', kw2='1300')
    search_list = note_bro.get_content_list()
    print(search_list[0])

def get_content_list(page_src):
    soup = bs(page_src, 'lxml')
    search_post = []
    post_list = []
    for post in soup.find_all(name='div', class_='search post bg2'):
        search_post.append(post)
    for post in soup.find_all(name='div', class_='search post bg1'):
        search_post.append(post)

    for post in search_post:
        post_link = 'http://www.notebro.com/forum/' + post.find(name='a')['href'][1:]
        year = re.search('.*(20\d{2}).*', post.find(name='div', class_='content').text)
        if (year):
            year = year.group(1)
        name = ''
        Post = {'link':post_link, 'year':year, 'f_name':name}
        post_list.append(Post)

    return post_list

def get_embedded_doc_url(notebro_url):
    driver = wb.Chrome()
    # doc_url = 'http://notebro.com/viewer.php?' \
    #           'url=http%3A%2F%2Fnotebro.com%2Fforum' \
    #           '%2Fdownload%2Ffile.php%3Fid%3D42286'
    doc_url = notebro_url
    driver.get(url=doc_url)
    page_src = driver.page_source
    soup = bs(page_src, 'lxml')
    embedded_doc_src = soup.find(name='iframe', id='')['src']
    return embedded_doc_src

if __name__ == '__main__':
    file = open('temp.txt', 'r', encoding='utf-8')
    page_src = ''
    for line in file:
        page_src = page_src + line
    content_list = get_content_list(page_src)
    # name = content_list[1].find(name='dt', class_='author').text
    # name = re.search('.*by ()', name)
    # print(name)
    # note_bro = NOTE_BRO()
    # note_bro.login()
    # note_bro.search(kw1='crm', kw2='1300')
    # url = note_bro.get_content_list()[0]['link']
    # note_bro.open_post(url)
    #url = get_embedded_doc_url('http://notebro.com/viewer.php?url=http%3A%2F%2Fnotebro.com%2Fforum%2Fdownload%2Ffile.php%3Fid%3D63183')
    print(content_list[0][:])






