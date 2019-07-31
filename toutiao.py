import requests
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re
import os
from hashlib import md5
from multiprocessing.pool import Pool



def article1(offset):
    headers = {
    "cookie": "csrftoken=957e945bd7c9021add628d4e07c2f1ad; tt_webid=6690773796519233036; s_v_web_id=2d44edde23ebadf3eb32788eff6cf14a; __tasessionId=xcospbenc1558090235428",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
     "referer": "https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D%E7%BE%8E%E5%A5%B3",
     "x-requested-with": "XMLHttpRequest",
    }
    params = {
       'aid': 24,
       'app_name': 'web_search',
       'offset': offset,
       'format': 'json',
       'keyword': '街拍美女',
       'autoload': 'true',
       'count': 20,
       'en_qc': 1,
       'cur_tab': 1,
       'from': 'search_tab',
       'pd': 'synthesis',
       'timestamp': 1557973762622,
    }
    url = 'https://www.toutiao.com/api/search/content/?'+ urlencode(params)
    try:
      r = requests.get(url,headers=headers)
      if r.status_code == 200:
        res=json.loads(r.text)
        return res
    except RequestException:
      print(u'访问错误')
      return None

def article2(res):
  if res and "data" in res.keys():
          for a in res.get('data'):
            if 'article_url' in a:
              art=a.get('share_url')
              yield art

def get_detail(url):
  headers = {
    "cookie": "csrftoken=957e945bd7c9021add628d4e07c2f1ad; tt_webid=6690773796519233036; s_v_web_id=2d44edde23ebadf3eb32788eff6cf14a; __tasessionId=xcospbenc1558090235428",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    }
  r = requests.get(url,headers=headers)
  if r.status_code==200:
    return r.text


def parse_detail(html):
  soup=BeautifulSoup(html,'lxml')
  title=soup.select('title')[0].get_text()
  print(title)
  img=re.compile(r'.*?gallery: JSON.parse\("(.*?)\"\)',re.S)
  result=re.search(img,html)
  if result:
    data = json.loads(result.group(1).replace('\\', ''))
    if data and "sub_images" in data.keys():
      sub=data.get("sub_images")
      for imge in sub:
        yield imge.get("url")


def imges(url):
    headers = {
    "cookie": "csrftoken=957e945bd7c9021add628d4e07c2f1ad; tt_webid=6690773796519233036; s_v_web_id=2d44edde23ebadf3eb32788eff6cf14a; __tasessionId=xcospbenc1558090235428",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    }

    try:
      r = requests.get(url,headers=headers)
      if r.status_code == 200:
        res=r.content
        file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(res).hexdigest(),'jpg')
        f=open(file_path,'wb')
        f.write(res)  
    except RequestException:
      pass


def main(offset):
    html=article1(offset)
    p=article2(html)
    for g in p:
      h=get_detail(g)
      for j in parse_detail(h):
        imges(j)


if __name__=='__main__':
  aa=0
  bb=20
  pool = Pool()
  num = ([x * 20 for x in range(aa,bb + 1)])
  pool.map(main,num)
  pool.close()
  pool.join()