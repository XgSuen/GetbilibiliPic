
import requests
import pprint
from bs4 import BeautifulSoup
import re
import time
import pymysql

fla_url = "https://search.bilibili.com/all?keyword=J.Fla&from_source=banner_search&page="

def get_av_number(page, fla_url):
    fla_url = fla_url + str(page)
    fla_r = requests.get(fla_url)
    # print(fla_r)
    # pprint.pprint(fla_r.text)

    soup = BeautifulSoup(fla_r.text, 'html.parser')
    data = soup.find_all('a', class_ = 'img-anchor')

    av_nums = []
    titles = []
    #link.get获取标签内容
    for link in data:
        pattern = re.compile(r'av(.*?)\?')
        av_nums.append(pattern.findall(link.get('href'))[0])
        titles.append(link.get('title'))
    return av_nums, titles


# print(fla_lst)
def get_img_url(aids):
    img_urls = []
    for aid in aids:
        av_url = "https://api.bilibili.com/x/web-interface/view?aid={}".format(aid)
        av_json = requests.get(av_url).json()
        img_urls.append(av_json['data']['pic'])
    return img_urls

def get_pages(fla_url):
    fla_r = requests.get(fla_url)
    soup = BeautifulSoup(fla_r.text, 'html.parser')
    data = soup.find_all('button', class_ = 'pagination-btn')
    return int(data[-1].string)

def download_imgs(img_urls, av_nums):

    for img_url, av_num in zip(img_urls, av_nums):
        print("downloading: {}".format(av_num))
        img_r = requests.get(img_url)
        with open('./fla_images/{}.png'.format(av_num), 'wb') as f:
            f.write(img_r.content)


def save_sql(av_nums, img_urls, titles):
    #连接数据库
    conn = pymysql.connect(user = "root", passwd = "123456", db = 'pytest', charset = 'utf8')
    cur = conn.cursor()
    for av_number, img_url, title in zip(av_nums, img_urls, titles):
        print(av_number, img_url, title)
        print('save: {}'.format(av_number))
        #插入字符串要加引号，用repr函数加上
        cur.execute("insert into jfla_infor (av_number,img_url,title) values({},{},{});".format(av_number, repr(img_url), repr(title)))
        cur.fetchall()
        conn.commit()

#获取页数
pages = get_pages(fla_url)
#循环爬完所有
for i in range(1, pages+1):
    av_nums, titles = get_av_number(i, fla_url)
    img_urls = get_img_url(av_nums)
    download_imgs(img_urls, av_nums)
    print('\n')
    save_sql(av_nums, img_urls, titles)
    time.sleep(0.4)
    print("Finish the {}th page".format(i))

print('Download Finish!')
print("Save Finish!")



