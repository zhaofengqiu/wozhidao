# wozhidao
User类有两个方法分别是登录和退出方法。还有一些属性：cid指的是序列号这个是通过序列号的生成规则，通过random函数自动生成。
user指的是这个实例的名字，password是将名码通过MD5加密获取到的

其中最主要的是获取到token这个，为什么因为这个app是将token放到headers里面去判断是哪个用户
我在这里写了几个函数
1. getAlluser()是获取到excel里面的用户名和密码，本来是想用数据库的但是一般人不会用数据库，反而是excel用的多一点。
2. getRecodes()是获取到这个用户的积分是多少
3. getNews(sort,page)是获取到一面的新闻大标题，其中sort是分类，page是第几面。
4. getNewdetail(newId,user)是获取到新闻的细节因为用户是靠访问新闻去获取到积分。
5. process(user,sum)这个就是处理一个用户登录到访问新闻结束到退出的过程。

这里我采用的是一个用户开辟一个进程，因为用户是知道有几个的所以没必要开辟进程池。
这里要注意的是二点：
1、头文件里面如果有'application/json'，那么一点要把表单转换成json格式再传输，这里可以看出json格式和字典格式是不一样的。
2、如果是多进程打包成exe文件的话，if __name__=='__main__'的下面一点要加上multiprocessing.freeze_support()；

(baidu)[https://www.baidu.com)
现在以及升级到了2.0版本呢。其中增加了一些功能，点赞功能。这个有什么地方要学习的呢？就是http里面的post不一定要有东西传过去，

1】点赞功能就是post了一次，其中比较新颖的是就是这个。
2】发送评论这里，其实比较新颖的是json格式和字典格式是不同的，在'Content-Type'= 'application/json'其中就必须先将字典dump成json才能发送表单。
3】获取评论这里是通过一次while和cnt来控制获取全部的评论。
