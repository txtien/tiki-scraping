import requests
from bs4 import BeautifulSoup
import re
import time
import pandas
import random

def category_link():
    #Get category name and (web address when it is clicked)
    
    # output: 
    # d:dict
    # d = {category_name: path} https://tiki.vn/path
    
    BASE_DIR = 'https://tiki.vn/'
    r = requests.get(BASE_DIR)
    c = r.content 
    soup = BeautifulSoup(c)
    
    d = dict()

    
    span_name = soup.find('ul', {'class':'Navigation__Wrapper-s3youc-0 hWakax'}).find_all('span',{'class':'text'})
    a_path = soup.find('ul', {'class':'Navigation__Wrapper-s3youc-0 hWakax'}).find_all('a',href = re.compile('^https'))
    for x, y in zip(span_name, a_path):
        name = x.text
        path = y['href'][15:]
        d[name] = path
    return d


def scrap_img(category_path):
    BASE_DIR = 'https://tiki.vn' + category_path
    r = requests.get(BASE_DIR)
    c = r.content 
    soup = BeautifulSoup(c)
    img_src = ''
    try:
        img_src = soup.find('div',{'class','product-box-list'}).find('img',{'src': re.compile('^https://')})['src']
    except:
        img_src = '../static/not_found.jpg'

    return img_src


def subcategory_link(category_path):
    #Get sub category's name and (web address when it is clicked)
    
    # output: 
    # d:dict
    # d = {sub_category_name: path} https://tiki.vn/path
    
    BASE_DIR = 'https://tiki.vn/' + category_path
    time.sleep(2)
    r = requests.get(BASE_DIR)
    c = r.content 
    soup = BeautifulSoup(c)
    
    d = dict()

    sub_cate_name_list = soup.find_all('div', {'class':'list-group-item is-child'})
    sub_cate_name_path_list = soup.find_all('div', {'class':'list-group-item is-child'})
   
    for x, y in zip(sub_cate_name_list, sub_cate_name_path_list):
        name = ' '.join((x.find('a').text.split()[:-1]))
        path = y.find('a')['href']
        d[name] = path
    return d

# for name, path in subcategory_link('dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner').items():
#     print(path.split('/')[1])

def identify_current_tag(link):
    time.sleep(random.uniform(0.2,2))
    BASE_URL = 'https://tiki.vn' + link
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text)
    
    r = re.compile('^is.*current$') 
    z = re.compile('[0-9]')
    a = []
    # for item in soup.find_all('div', {'class':re.compile('^i.*current$')}):
    #     print(item.find('a').text,' '.join(item.find('a').text.split()[:item.find('a').text.split().index('(')]))
    # soup.find_all('div', {'class':re.compile('^i.*current$')})
    list_text = soup.find_all('div', {'class':re.compile('^i.*current$')})
    for item in list_text:
        a.append(item.find('a')['href'])

    
    return a


def recursion(link):
    # Tìm category thật
    time.sleep(random.uniform(2, 4))
    BASE_URL ='https://tiki.vn' + link
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        print('Success!', BASE_URL)
    elif response.status_code == 404:
        time.sleep(5)
        response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text)
    
    
    if len(soup.find_all('div',{'class':re.compile('^i.*current$')})) == 0:
        if len(list_link) == 0:
            for name, sub_link in subcategory_link(link).items():
                list_link.append(sub_link)
        return list_link 
    else:
        for name, sub_link in subcategory_link(link).items():
            if sub_link in list_link:
                return list_link
            else:
                if name not in a:
                    list_link.append(sub_link)
                    recursion(sub_link)
                else:
                    return list_link


def scrap_product(link):
    l = []
    i = 1
    while True:
        try:
            time.sleep(random.uniform(2, 4))
            BASE_URL ='https://tiki.vn' + link + '&page=' + str(i)
            response = requests.get(BASE_URL)
            soup = BeautifulSoup(response.text)
            test = soup.find('div', {'class':'product-box-list'})
            divs = test.find_all('div')
        except Exception as e:
            print(f'ERROR:{e}')
            break
        
        

#         if (len(divs)==0) or (divs ==None):
#             break
        
        for item in divs: 
            d = dict()
            if 'data-id' in item.attrs:
                d['title'] = item['data-title']
                d['price'] = item.find('span',{'class':'final-price'}).text.strip().split()[0]
                d['img_link'] = item.find('img').attrs['src']
                
               
                d['category'] = test['data-impress-list-title'].split('|')[1].strip()
             
                if item.find('i',{'class':'tikicon icon-tikinow'}) is None:
                    d['tikiNow'] = 'False'
                else:
                    d['tikiNow'] = 'True'
                    
                if item.find('span',{'style':re.compile('^width.*%$')}) is None:
                    d['rating'] = 'No'
                else:
                    d['rating'] = item.find('span',{'style':re.compile('^width.*%$')})['style'].split(':')[1]
                
                if not item.find('p',{'class':'review'}).text.split()[0].strip('(').isdigit():
                    d['Number of Review'] = 0
                else:
                    d['Number of Review'] = item.find('p',{'class':'review'}).text.split()[0].strip('(')
                    
                l.append(d)
                
        if soup.find('a',{'rel':'next'}) is None :
            break
            
        i += 1
        time.sleep(2)
        
    return(l)




