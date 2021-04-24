import flask
from flask import request, jsonify, make_response
import pandas as pd
import requests 
import urllib.request
from bs4 import BeautifulSoup as bs4
import re

url='https://www.mypmp.net/category/ants/page/0/'
title=[]
link=[]
date=[]
subtitle=[]
images=[]
full_desc=[]

page=requests.get(url)
soup=bs4(page.text,'html.parser')
main=soup.findAll('h2',{"class":"post-title"})

for i in main: 
    tit=i.find('a')
    t=tit.getText().replace("\t","").replace("‘","'").replace("’","'").replace("\n\n"," ").replace("\n","").strip().replace("\\u00bb",".")
    title.append(t)
    
    l=tit.get('href')
    link.append(l)
    
dates=soup.findAll('span',{'class':'meta-date'})
for j in dates:
    d=j.getText().replace("‘","'").replace("’","'").replace("\t","").replace("\n\n","").replace("\n","").strip().replace("\\u00bb",".")
    date.append(d)
    
sub=soup.findAll("div",{"class":"entry-content"})
for k in sub:
    s=k.getText().replace("‘","'").replace("’","'").replace("\t","").replace("\n\n","").replace("\n"," ").replace("\'","'").strip().replace("\\u00bb",".")
    subtitle.append(s)

tags=[]
for i in range(0,len(title)):
    tags.append('Ants')

images=[]
div=soup.findAll('div',class_='entry clearfix')
for i in div:
    img_item=i.find('div',class_='entry-feature-item')
    if img_item is not None:
        atag=img_item.find('a')
        img_src=atag.find('img')
        images.append(img_src.get('src'))
    else:
        images.append('NA')

for i in link: 
    page1=requests.get(i)
    soup=bs4(page1.text,'html.parser')
    ptags=soup.findAll('p')
    p_text=[]
    for i in ptags: 

        texts=i.getText()
        p_text.append(texts)

    full_desc.append(". ".join(p_text))

data={'Title':title,'Date':date,'Link':link,'Subtitle':subtitle,'Full Description':full_desc,'Image':images,'Tags':tags}
df=pd.DataFrame(data=data)
print('SCRAPING COMPLETE')
#FLASK APP
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return "<h1>Downloading your files </h1>"

#A route to return all of the available entries in our catalog.
@app.route('/api/v1/intellihub/news/', methods=['GET'])
def api_all():

    resp = make_response(df.to_csv(index=False))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
