# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib
import cx_Oracle
import sys

# 80   22400
#if __name__ == "__main__":
    # for i in range(10):
    #     html = requests.get("http://www.80s.tw/movie/"+str((i+590)),verify=False)
    #     soup = BeautifulSoup(html.text,'lxml')
    #     for mv in soup.find_all('div',{'class','info'}):
    #         print("名称："+mv.find_all('h1')[0].get_text())
    #         for sp in mv.find_all('span',{'class','font_888'}):
    #             if sp.get_text()=="又名：":
    #                 print(str(sp.parent.get_text()).replace("\n","").replace(" ",""))
    #             if sp.get_text() == "演员：":
    #                 actor=""
    #                 for children in sp.parent.find_all('a'):
    #                     actor = actor+" "+str(children.get_text());
    #                 print("演员 "+actor)
    #             if sp.get_text() == "类型：":
    #                 type=""
    #                 for children in sp.parent.find_all('a'):
    #                     type = type+" "+str(children.get_text());
    #                 print("类型 "+type)
    #             if sp.get_text() == "地区：":
    #                 area=""
    #                 for children in sp.parent.find_all('a'):
    #                     area = area+" "+str(children.get_text());
    #                 print("地区 "+area)
    #             if sp.get_text() == "语言：":
    #                 language=""
    #                 for children in sp.parent.find_all('a'):
    #                     language = language+" "+str(children.get_text());
    #                 print("语言 "+language)
    #             if sp.get_text() == "导演：":
    #                 dao=""
    #                 for children in sp.parent.find_all('a'):
    #                     dao = dao+" "+str(children.get_text());
    #                 print("导演 "+dao)
    #             if sp.get_text()=="上映日期：":
    #                 print(str(sp.parent.get_text()).replace("\n","").replace(" ",""))
    #             if sp.get_text()=="片长：":
    #                 print(str(sp.parent.get_text()).replace("\n","").replace(" ",""))
    #             if sp.get_text()=="更新日期：":
    #                 print(str(sp.parent.get_text()).replace("\n","").replace(" ",""))
    #             if sp.get_text()=="豆瓣评分：":
    #                 print(str(sp.parent.get_text()).replace("\n","").replace(" ",""))
    #             if sp.get_text()=="剧情介绍：":
    #                 print(str(sp.parent.get_text()).replace("\n","").replace(" ",""))
    #     print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# from log.models import Movie80


def grapdata():
    for i in range(1):
        html = requests.get("http://www.80s.tw/movie/"+str((i+592)),verify=False)
        soup = BeautifulSoup(html.text,'lxml')

        for mv in soup.find_all('div',{'class','info'}):
            mname=mv.find_all('h1')[0].get_text()
            print(mname)
            for sp in mv.find_all('span',{'class','font_888'}):
                if sp.get_text()=="又名：":
                    mname2=str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("又名：","")
                    print(mname2)
                if sp.get_text() == "演员：":
                    actor=""
                    for children in sp.parent.find_all('a'):
                        actor = actor+"|"+str(children.get_text());
                    mactor=actor
                    print(mactor)
                if sp.get_text() == "类型：":
                    type=""
                    for children in sp.parent.find_all('a'):
                        type = type+" "+str(children.get_text());
                    mtype = type
                    print(mtype)
                if sp.get_text() == "地区：":
                    area=""
                    for children in sp.parent.find_all('a'):
                        area = area+" "+str(children.get_text());
                    marea = area
                    print(marea)
                if sp.get_text() == "语言：":
                    language=""
                    for children in sp.parent.find_all('a'):
                        language = language+" "+str(children.get_text());
                    mlanguage = language
                    print(mlanguage)
                if sp.get_text() == "导演：":
                    dao=""
                    for children in sp.parent.find_all('a'):
                        dao = dao+" "+str(children.get_text());
                    mdirector = dao
                    print(mdirector)
                if sp.get_text()=="上映日期：":
                    mstartdate = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("上映日期：","")
                    print(mstartdate)
                if sp.get_text()=="片长：":
                    mlength = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("片长：","")
                    print(mlength)
                if sp.get_text()=="更新日期：":
                    mupdatedate = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("更新日期：","")
                    print(mupdatedate)
                if sp.get_text()=="豆瓣评分：":
                    mscore = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("豆瓣评分：","")
                    print(mscore)
                if sp.get_text()=="剧情介绍：":
                    mintroduce = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("剧情介绍：","")
                    print(mintroduce)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        db = cx_Oracle.connect('scott', 'tiger', 'localhost:1521/orcl')
        db.close()
        # Movie80.objects.create(mid=str((i+100)),mname=mname,mname2=mname2,mactor=mactor,mtype=mtype,marea=marea,
        #                        mlanguage=mlanguage,mdirector=mdirector,mstartdate=mstartdate,mlength=mlength,
        #                        mupdatedate=mupdatedate,mscore=mscore,mintroduce=mintroduce)




def grapimg():
    for i in range(1):
        start=1014
        html = requests.get("http://www.80s.tw/movie/"+str((i+start)),verify=False)
        print(str(i+start))
        soup = BeautifulSoup(html.text,'lxml')
        for mv in soup.select('.img') :#find_all('div',{'class','img'}):
            src="http:"+mv.find_all('img')[0].attrs['src']
            urllib.request.urlretrieve(src, str(i+start)+mv.find_all('img')[0].attrs['title']+'.jpg')
            #print(mv.find_all('img')[0].attrs['src'])
            #print(mv.find_all('img')[0].attrs['title'])

def grapdataandimg():
    start=1115
    for i in range(1):
        html = requests.get("http://www.80s.tw/movie/"+str((i+start)),verify=False)
        print(str((i+start)))
        soup = BeautifulSoup(html.text,'lxml')
        for mv in soup.select('.img') :
            src="http:"+mv.find_all('img')[0].attrs['src']
            urllib.request.urlretrieve(src, "../static/image/"+str(i+start)+mv.find_all('img')[0].attrs['title']+'.jpg')
        mname=""
        mname2=""
        mactor=""
        mintroduce=""
        mscore=""
        mupdatedate=""
        mlength=""
        mstartdate=""
        mdirector=""
        mlanguage=""
        marea=""
        mtype=""
        for mv in soup.find_all('div',{'class','info'}):
            mname=mv.find_all('h1')[0].get_text()
            #print(mname)
            for sp in mv.find_all('span',{'class','font_888'}):
                if sp.get_text()=="又名：":
                    mname2=str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("又名：","")
                    #print(mname2)
                if sp.get_text() == "演员：":
                    actor=""
                    for children in sp.parent.find_all('a'):
                        actor = actor+"|"+str(children.get_text());
                    mactor=actor
                    #print(mactor)
                if sp.get_text() == "类型：":
                    type=""
                    for children in sp.parent.find_all('a'):
                        type = type+" "+str(children.get_text());
                    mtype = type
                    #print(mtype)
                if sp.get_text() == "地区：":
                    area=""
                    for children in sp.parent.find_all('a'):
                        area = area+" "+str(children.get_text());
                    marea = area
                    #print(marea)
                if sp.get_text() == "语言：":
                    language=""
                    for children in sp.parent.find_all('a'):
                        language = language+" "+str(children.get_text());
                    mlanguage = language
                    #print(mlanguage)
                if sp.get_text() == "导演：":
                    dao=""
                    for children in sp.parent.find_all('a'):
                        dao = dao+" "+str(children.get_text());
                    mdirector = dao
                    #print(mdirector)
                if sp.get_text()=="上映日期：":
                    mstartdate = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("上映日期：","")
                    #print(mstartdate)
                if sp.get_text()=="片长：":
                    mlength = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("片长：","")
                    #print(mlength)
                if sp.get_text()=="更新日期：":
                    mupdatedate = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("更新日期：","")
                    #print(mupdatedate)
                if sp.get_text()=="豆瓣评分：":
                    mscore = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("豆瓣评分：","")
                    #print(mscore)
                if sp.get_text()=="剧情介绍：":
                    mintroduce = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("剧情介绍：","")
                    #print(mintroduce)
       #  db = cx_Oracle.connect('scott', 'tiger', 'localhost:1521/orcl',encoding='utf-8')
       #  cr = db.cursor()
       #  mid = str(( i + start));
       #  sql = "insert into movie_80(mid,mname,mname2,mactor,mtype,marea,mlanguage,mdirector,mstartdate,mlength,mupdatedate,mscore,mintroduce)" \
       #        " values("+str((i+start))+","+mname+","+mname2+","+mactor+","+mtype+","+marea+","+mlanguage+","+mdirector+","+mstartdate+","+mlength+","+mupdatedate+","+mscore+","+mintroduce+")"
       #  # sql = "insert into movie_80(mid,mname,mname2,mactor,mtype,marea,mlanguage,mdirector,mstartdate,mlength,mupdatedate,mscore,mintroduce)" \
       #  #       " values( mid , mname , mname2 , mactor , mtype ,marea , mlanguage ,mdirector , mstartdate , mlength , mupdatedate ,mscore ,mintroduce )"
       #  # sql = "insert into movie_80(mid,mname,mname2,mactor,mtype,marea,mlanguage,mdirector,mstartdate,mlength,mupdatedate,mscore,mintroduce)" \
       #  #       " values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"
       #  sql = "insert into movie_80(mid,mname) values(:mid,:mname)"
       #  mname = mname.encode('utf-8')
       #  print(mname)
       #  mname = mname.decode()
       #  print(mname)
       # # mname = unicode(mname, 'GBK').encode('UTF-8')
       #  param = {'mid': mid, 'mname': mname}
       #  cr.execute(sql,param)
       #  cr.close()
       #  db.commit()
        # Movie80.objects.create(mid=str((i+start)),mname=mname,mname2=mname2,mactor=mactor,mtype=mtype,marea=marea,
        #                        mlanguage=mlanguage,mdirector=mdirector,mstartdate=mstartdate,mlength=mlength,
        #                        mupdatedate=mupdatedate,mscore=mscore,mintroduce=mintroduce)


if __name__ == "__main__":
    grapdataandimg()
