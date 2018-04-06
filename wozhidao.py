import requests
import hashlib
import json
import random
import xlrd
import xlwt
import os
import time
from multiprocessing import Process
import multiprocessing
import http
def get_cid():
    list = []
    for x in range(10):
        list.append(str(x))
    for x in range(97, 110):
        a = str(chr(x))
        list.append(a)
    cid = ''
    for x in range(40):
        a = random.choice(list)
        cid = cid + a
    return cid
loginget=''
loginheader={
    'system': 'eyJhcHBJZGVudGlmaWVyIjoiY29tLmd5bWouYXBrLnhqIiwic3lzdGVtVmVyc2lvbiI6IjcuMS4yIiwiYXBwbGljYXRpb24iOiJBTkRST0lEIiwiYXBwVmVyc2lvbiI6IjYuMi40IiwiaGFyZHdhcmUiOiJOMkc0N0gifQ==',

     'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    'Host': 'kp.appwzd.cn',
    'User-Agent': 'okhttp/3.4.1'
}
processheaders=loginheader

class userProcess(Process):
    def __init__(self,user,sum):
        Process.__init__(self)
        self.sum=sum
        self.user=user
    def run(self):
        process(self.user,self.sum)
class User():

    def __init__(self,user,pwd):
        self.cid=get_cid()
        self.user=user
        hl = hashlib.md5()
        hl.update(pwd.encode(encoding='utf-8'))
        password = hl.hexdigest()
        self.password=password
    def login(self):
        parms={"password": self.password,"account":self.user}
        logindata=json.dumps(parms)#注意这里一点要转换
        loginheader['cid']=self.cid
        try:
            r=requests.post('http://kp.appwzd.cn/kepu/user/login/',headers=loginheader,data=logindata)
            self.loginget=r.json()
            self.nickName=self.loginget['data']['nickName']
            self.baseParams=self.loginget['data']['token']
            print(self.nickName+'登录成功')

            return True
        except:
            print(str(self.user)+'密码或者账号错误')
            return False
    def loginout(self):

        http.client._http_vsn = 10
        http.client._http_vsn_str = 'HTTP/1.0'
        processheaders['baseParams'] = self.baseParams
        r = requests.post('http://kp.appwzd.cn/kepu/user/logout ', headers=processheaders)
        message = '\r%s  %s' % (self.nickName, r.json()['message'])
        print(message)
def getAlluser():
    usermessage={}
    path=os.getcwd()
    filename='user.xlsx'
    Data = xlrd.open_workbook(filename)
    table = Data.sheets()[0]
    rows=table.nrows-1
    col =table.ncols
    for i in range(1,rows+1):
        try:
            usermessage[int(table.cell(i, 0).value)]=str(int(table.cell(i, 1).value))
        except:
            usermessage[int(table.cell(i, 0).value)] = str(table.cell(i, 1).value)

    usermessages=[rows,usermessage]
    return usermessages

def getNews(sort,page):
    Newurl='http://kp.appwzd.cn/kepu/news/getNews/%d/%d'%(sort,page)
    news=requests.get(Newurl,headers=processheaders).json()
    news=news['data']['newsList']
    return news
def getNewdetail(newId,user):
    processheaders['baseParams']=user.baseParams
    newUrl='http://kp.appwzd.cn/kepu/news/getNewsDetail/%s'%(newId)
    r=requests.get(newUrl,headers=processheaders)
def process(user,sum):

    news = getNews(1, 1)
    while sum>0:
        for new in news:
            newId=new['newsId']
            getNewdetail(newId,user)
            time.sleep(random.uniform(1,2))
            sum=sum-1
            message= '\ruser {0:{2}^10} also have {1:} now.'.format(user.nickName, sum,chr(12288))
            print(message,end='')
            if sum<=0 :
                break
    user.loginout()
if __name__ == '__main__':
    multiprocessing.freeze_support()#这里这句是多进程用pyinstaller打包成apk时候必须加上的
    usermessages=getAlluser()
    usernum=usermessages[0]
    usermessage=usermessages[1]
    sum=int(input('How many time do you want:'))
    users=[]
    userPs=[]
    for count,pwd in usermessage.items():
        user=User(count,pwd)
        if user.login():

            users.append(user)
    for user in users:
        user=userProcess(user,sum)
        user.daemon=True
        user.start()
        userPs.append(user)

    for user in userPs:
        user.join()
    print('author:qipaqiu\nfinishing in 5 seconds ')
    time.sleep(5)

