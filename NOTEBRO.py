import random, re, time#, SCRIBD
from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

#SCRIBD.login()
browser = wd.Chrome()


def wait(Expected_Conditions):
    return WebDriverWait(browser, 10).until(Expected_Conditions)

def random_sleep():
    sleep_time = random.uniform(1.0, 3.0)
    time.sleep(sleep_time)


def login(remember=True):
    try:
        home_url = 'http://www.notebro.com/forum/'
        browser.get(home_url)
        account_field = wait(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#modlgn-username")))
        pw_field = wait(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#modlgn-passwd")))
        submit = wait(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#login-form > fieldset > input.button")))
        if remember:
            remember_login = wait(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#autologin")))
            remember_login.click()
        random_sleep()
        account_field.send_keys("LuckyE")
        pw_field.send_keys("haoyangliu96")
        submit.click()
    except TimeoutException:
        login()

def search(kw1, school='uottawa'):
    if school.lower() == 'uottawa':
        url = 'http://www.notebro.com/forum/viewforum.php?f=2'
    elif school.lower() == 'carleton':
        url = 'http://www.notebro.com/forum/viewforum.php?f=4'
    try:
        browser.get(url)
        search_field = wait(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#roksearch_search_str")))
        search_field.clear()
        search_field.send_keys(kw1)
        search_field.send_keys(Keys.ENTER)

        try:
            total_page = WebDriverWait(browser, 2).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#page-body > ul > li > a > strong:nth-child(2)"))).text
        except TimeoutException:
            try:
                total_page = WebDriverWait(browser, 2).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#page-body > ul > li > strong:nth-child(2)"))).text
            except TimeoutException:
                return browser.close()
        return int(total_page)
    except TimeoutException:
        return search(kw1, school)


def get_post_links(pages):
    links = []
    for i in range(1, pages):
        ##download each post
        page_src = browser.page_source
        soup = bs(page_src, 'lxml')
        for post in soup.find_all(name='div', class_='search post bg2'):
            links.append('http://www.notebro.com/forum/' + post.find(name='a')['href'][1:])
        for post in soup.find_all(name='div', class_='search post bg1'):
            links.append('http://www.notebro.com/forum/' + post.find(name='a')['href'][1:])
        flip_page()

    ## last page links
    page_src = browser.page_source
    soup = bs(page_src, 'lxml')
    for post in soup.find_all(name='div', class_='search post bg2'):
        links.append('http://www.notebro.com/forum/' + post.find(name='a')['href'][1:])
    for post in soup.find_all(name='div', class_='search post bg1'):
        links.append('http://www.notebro.com/forum/' + post.find(name='a')['href'][1:])
    return links


def notebro_post(url):
    browser.get(url)
    random_sleep()
    page_src = browser.page_source
    soup = bs(page_src, 'lxml')
    title = soup.find(name='h3', class_='first').text
    content = soup.find(name='div', class_='content').text
    year = re.search('.*(20\d{2}).*', title)
    if not year:
        year = re.search('.*(20\d{2}).*', content)
    if year:
        year = year.group(1)

    try:
        files = soup.find_all(name='a', class_='postlink')
        file_list = []
        for file in files:
            file_name = file.text
            file_link = get_embedded_doc_url(file['href'])
            file_list.append({'file name': file_name, 'file link': file_link})
        return {'title': title, 'content': content, 'year': year, 'file list': file_list}
    except Exception:
        return {'title': title, 'content': content, 'year': year}

def get_embedded_doc_url(notebro_url):
    try:
        browser.get(notebro_url)
        random_sleep()
        page_src = browser.page_source
        soup = bs(page_src, 'lxml')
        embedded_doc_src = soup.find(name='iframe', id='')['src']
        return embedded_doc_src
    except Exception:
        return None

def download_post(file_link):
    try:
        browser.get(file_link)
        page_src = browser.page_source
        soup = bs(page_src, 'lxml')
        download_url = soup.find(name='a', class_='toolbar_btn icon-ic_download_with_line',
                                 target='_blank')
        #SCRIBD.download(download_url['href'])
    except Exception:
        print(Exception)

def flip_page():
    try:
        next_page = wait(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#page-body > form:nth-child(14) > fieldset > "
                              "a.right-box.right")))
        next_page.click()
    except TimeoutException:
        print('Last page')

def main(subject, code, school):
    login()
    pages = search(subject + ' ' + code, school)
    if not pages == None:
        for post_url in get_post_links(pages):
            post_info = notebro_post(post_url)
            print(post_info)

        pages = search(subject+code, school)
        if not pages == None:
            for post_url in get_post_links(pages):
                post_info = notebro_post(post_url)
                print(post_info)





if __name__ == '__main__':
    main('chst', '2503', 'carleton')
    # doc_url = get_embedded_doc_url('http://notebro.com/viewer.php?url=http%3A%2F%2Fnotebro.com%2Fforum%2Fdownload%2Ffile.php%3Fid%3D19739')
    # download_post(doc_url)