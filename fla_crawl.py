
import requests
import pprint
from bs4 import BeautifulSoup
import re
import time
import pymysql

#链接，page先不设置
fla_url = "https://search.bilibili.com/all?keyword=J.Fla&from_source=banner_search&page="

def get_av_number(page, fla_url):
    """
    通过获得html页面获得每个视频的av号，以便爬取其信息，其实我们只要图片链接就好了
    """
    #给url加上page的值
    fla_url = fla_url + str(page)
    #获取html页面
    fla_r = requests.get(fla_url)

    # print(fla_r)
    # pprint.pprint(fla_r.text)

    #上bs4，解析，获得带有av号的标签属性
    soup = BeautifulSoup(fla_r.text, 'html.parser')
    data = soup.find_all('a', class_ = 'img-anchor')

    #准备将av号和标题存下来
    av_nums = []
    titles = []

    #link.get获取标签内容
    for link in data:
        #构造正则表达式，匹配之前获取的标签内容，获取av号
        pattern = re.compile(r'av(.*?)\?')
        av_nums.append(pattern.findall(link.get('href'))[0])
        #直接get titile
        titles.append(link.get('title'))
    return av_nums, titles



def get_img_url(aids):
    """
    获取图片的url
    """
    img_urls = []
    for aid in aids:
        #随便点进去一个视频链接，可以看到其封面url存在这样一个链接里：
        av_url = "https://api.bilibili.com/x/web-interface/view?aid={}".format(aid)
        #get到，转成json，便于获取pic即封面链接
        av_json = requests.get(av_url).json()
        img_urls.append(av_json['data']['pic'])
    return img_urls

def get_pages(fla_url):
    #这是获取咱们搜到的结果一共有多少页
    fla_r = requests.get(fla_url)
    soup = BeautifulSoup(fla_r.text, 'html.parser')
    data = soup.find_all('button', class_ = 'pagination-btn')
    return int(data[-1].string)

def download_imgs(img_urls, av_nums):
    #下载图片ing！！！
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
        #print(av_number, img_url, title)
        print('save: {}'.format(av_number))
        #插入字符串要加引号，用repr函数加上
        cur.execute("insert into jfla_infor (av_number,img_url,title) values({},{},{});".format(av_number, repr(img_url), repr(title)))
        cur.fetchall()
        conn.commit()

#获取页数
pages = get_pages(fla_url)
#循环爬完所有页的Jfla！！！
for i in range(1, pages+1):
    av_nums, titles = get_av_number(i, fla_url)
    img_urls = get_img_url(av_nums)
    #开始下载
    download_imgs(img_urls, av_nums)
    print('\n')
    #开始保存到数据库
    save_sql(av_nums, img_urls, titles)
    #不要爬太快，停一下
    time.sleep(0.4)
    print("Finish the {}th page".format(i))

print('Download Finish!')
print("Save Finish!")


