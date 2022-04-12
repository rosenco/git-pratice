
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
link=[] #網址
name=[] #職稱
id=[] #職務id
#翻頁取id
searchname=str(input('搜尋的職務名稱是?'))
pagenumber=int(input('要查找的總頁數?'))
for page in range(pagenumber):
  url=f'https://www.104.com.tw/jobs/search/?ro=0&kwop=11&keyword={searchname}&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page={page}&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'
  res=requests.get(url)
  data=BeautifulSoup(res.text,'html.parser')
  #抓網址
  title=data.find_all('article',{'class':'b-block--top-bord'})
  for i in title:
    title_link=i.find('a').get('href')
    a=title_link.split('//')[1]
    #link.append(a)
    id.append(a.split('/')[2].split('?')[0])
  #從搜尋頁抓職稱 
  for i in title:
      title_name=i.find('a').text
      name.append(title_name)


jobCategory,skill,edu,workexp,major,language=[],[],[],[],[],[]
for i in id:
  job_id=i #工作id
  url = f'https://www.104.com.tw/job/ajax/content/{job_id}'

  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
      'Referer': f'https://www.104.com.tw/job/{job_id}'
  }
  
  r = requests.get(url, headers=headers)

  data = r.json()
  workexp.append(data['data']['condition']['workExp'].split('年')[0]) #要求經歷年份
  if len(data['data']['condition']['edu'])>0:
    edu.append(data['data']['condition']['edu'] )#學歷，長度不同
  else:
    edu.append(None)
  #addressDetail=data['data']['jobDetail']['addressDetail'] #地址
  #addressRegion=data['data']['jobDetail']['addressRegion'] #地區
  #latitude=data['data']['jobDetail']['latitude'] #緯度
  #longitude=data['data']['jobDetail']['longitude'] #經度
  if len(data['data']['condition']['major'])>0:
    major.append(data['data']['condition']['major'][0] )#科系(長度不同)
  else:
    major.append(None)
  if len(data['data']['jobDetail']['jobCategory'])>0:
    jobCategory.append(data['data']['jobDetail']['jobCategory'][0]['description']) #職務類別(長度不同)
  else:
    jobCategory.append(None)
  skillint=[]
  if len(data['data']['condition']['specialty'])>0:
    for i in data['data']['condition']['specialty']:
      skillint.append(i['description']) #需要職能(長度不同)
    skillint=str(skillint)
    skill.append(skillint)
    #skill=data['data']['condition']['specialty'][0]['description']
  else:
    skill.append(None)
  if len(data['data']['condition']['language'])>0:  
    language.append(data['data']['condition']['language'][0]['language']) #語言(長度不同)
  else:  
    language.append(None)

total=pd.DataFrame({
  '職務類別':jobCategory,
  '技能需求':skill,
  '學歷要求':edu,
  '工作經歷':workexp,
  '科系要求':major,
  '語言需求':language
})
total.to_csv('data.csv',encoding='utf-8', index=False)
