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

            getRecodes(self.nickName,self.baseParams)
            return True
        except Exception as ce:
            print(str(self.user)+'密码或者账号错误')
            print(ce)
        return False
    def loginout(self):

        http.client._http_vsn = 10
        http.client._http_vsn_str = 'HTTP/1.0'
        processheaders['baseParams'] = self.baseParams
        r = requests.post('http://kp.appwzd.cn/kepu/user/logout ', headers=processheaders)
        message = '\r%s  %s' % (self.nickName, r.json()['message'])
        print(message)


    def dianzna(self,newsId, action):
        actions = {"d": '1', "p": '0'}
        processheaders['baseParams'] = self.baseParams
        processheaders['cid'] = self.cid
        url = 'http://kp.appwzd.cn/kepu/user/dp/%s/1/%s' % (newsId, actions[action])

        r = requests.post(url, headers=processheaders)
        if action=='d':
            print('%s文章%，s点赞成功'%(newsId,self.nickName))
        else:
            print('%s文章，%s取消点赞成功' % (newsId, self.nickName))

    def postcomment(self, newsId, comment):
        processheaders['baseParams'] = self.baseParams
        processheaders['cid'] = self.cid

        url = 'http://kp.appwzd.cn/kepu/user/sentComment'

        parms = {'newsId': newsId,
                 'comment': comment,
                 }
        postdata = json.dumps(parms)
        r = requests.post(url, headers=processheaders, data=postdata)

        print(self.nickName,'评价成功')



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

def getRecodes(nickName,baseParams):
    
    processheaders['baseParams']=baseParams
    try:
        jsondata=requests.get('http://kp.appwzd.cn/kepu/user/getScore',headers=processheaders).json()
        print("%s 登录成功，其积分为 %s"%(nickName,jsondata['data']['score']))
    except:
        print("%s 登录成功" % (nickName))
def getNews(sort,page=1):
    Newurl='http://kp.appwzd.cn/kepu/news/getNews/%d/%d'%(sort,page)
    news=requests.get(Newurl,headers=processheaders).json()
    news=news['data']['newsList']
    return news
def getNewdetail(newId,user):
    processheaders['baseParams']=user.baseParams

    newUrl='http://kp.appwzd.cn/kepu/news/getNewsDetail/%s'%(newId)
    r=requests.get(newUrl,headers=processheaders)
    return r.text

def getcomment(newId):
    commentlist=[]
    cnt=1
    while True:
        url='http://kp.appwzd.cn/kepu/news/getNewsComment/%s/%s'%(newId,str(cnt))
        jsondata=requests.get(url ).json()
        try:
            comments=jsondata['data']['commentList']
        except:
            return list
        if len(comments)>0:
            for comment in comments:
                commentlist.append(comment)
                cnt+=1
        else:
            break

    return commentlist


def process(user,sum):
    news = getNews(1, 1)
    while sum>0:
        for new in news:
            newId=new['newsId']
            getNewdetail(newId,user)
            time.sleep(random.uniform(0.60,0.7))
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
    users=[]# 337018.25
    userPs=[]#337101.25
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
