# [体验传送门](https://www.darkbuddy.cn)

# Dark_buddy

这是一个基于钉钉机器人的outgoing机制，做的一个机器人应答服务。基于PYTHON3开发。

由于钉钉企业群开放了企业外部用户，这种机器人一下子就有了业务价值，这是我没想到的。于是想着写一下它的README吧，在已经码了上千行代码后...

有 [DockerFile](https://github.com/genji9071/Dark_buddy/blob/master/Dockerfile) ，也有 [docker-compose](https://github.com/genji9071/Dark_buddy/blob/master/docker-compose.yml) ，如果讲究的话还可以用 [gitlab-ci](https://github.com/genji9071/Dark_buddy/blob/master/.gitlab-ci.yml) 做自我构建。



# Happy path

1. 准备一台机器
    - 最低配置不要太低就行，一般阿里云腾讯云的最低配置，加上一个内存升级包，2GB就ok。
    - 承载的服务包括但不限于：一个redis，一个mysql，dark-buddy本buddy，dark-buddy的daemon（可选）

2. 安装redis和mysql
    - 在 [DataSource.py](https://github.com/genji9071/Dark_buddy/blob/master/config/DataSource.py) 中配置连接信息

3. mysql -> 执行 [setup.sql](https://github.com/genji9071/Dark_buddy/blob/master/resource/setup.sql)

4. pip3 install -r requirements.txt

5. python3 app.py



# 模块导航

### config
+ 整个服务的配置信息，包括整个服务的菜单项配置，各种api的配置信息，以及数据库连接等等。

### dark_cai_hong_pi
+ 彩虹屁功能，几个不好好整活的前端码农，做出的一个互相夸赞的小功能，我可是非常鄙视这种行为的！这明显夸我的力度都不够啊！

### dark_chat
+ 机器人自动应答功能，根据不同的模式选择，可以切换不同的机器人回复实现。
+ 目前所用到的实现有：
    + [dark_jikipedia](https://github.com/genji9071/Dark_buddy/blob/master/dark_chat/dark_jikipedia) 网络常见用语解答；
    + [dark_qa](https://github.com/genji9071/Dark_buddy/blob/master/dark_chat/dark_qa) 通过百度等搜索引擎匹配应答；
    + [simsimi_chat](https://github.com/genji9071/Dark_buddy/blob/master/dark_chat/simsimi_chat) 调用韩国成人鸡simsimi的api实现成人应答；
    + [zuan_chat](https://github.com/genji9071/Dark_buddy/blob/master/dark_chat/zuan_chat) 通过爬虫爬取祖安应答；

### dark_guess_number
+ 一个猜数字的游戏，自定义位数和两种难度实现

### dark_listener
+ 一种监听器机制。用来配置并实现任何一个模块的坚挺需求。监听行为可以理解成机器人的"上下文"概念，需要用户通过多轮对话完整请求。比如  

    用户："请告诉我今天的天气"  
    机器人："你是在说哪个城市呢？"  
    用户："北京"  
    机器人："北京今天晴"  

    上述的交互中，作为一个天气查询模块，需要在机器人询问后进行特定用户的特定文字的监听，以分辨用户是在寻求别的帮助还是在回答机器人的问题。这便是监听器的使用场景。
    
+ [BaseListener.py](https://github.com/genji9071/Dark_buddy/blob/master/dark_listener/BaseListener.py) 监听器的抽象类实现，功能模块可以继承此类实现自己的监听器

+ [BaseOperation.py](https://github.com/genji9071/Dark_buddy/blob/master/dark_listener/BaseOperation.py) 监听器的监听规则配置实现，实现了一种布尔型语法，可以实现基本的compare和正则match，以及或与的逻辑组合

+ [DarkListener.py](https://github.com/genji9071/Dark_buddy/blob/master/dark_listener/DarkListener.py) 监听器的调用流程实现，实现了不同维度检索监听器等功能。


### dark_maze
+ 一个迷宫游戏。感谢xhd的交互实现贡献！  
    由于聊天群机器人的交互特性，我们借鉴了mud游戏的交互，通过实时渲染迷宫画面的方式实现此游戏。
    
+ [DarkMaze.py](https://github.com/genji9071/Dark_buddy/blob/master/dark_maze/DarkMaze.py) 迷宫游戏的主类，继承至BaseHandler

+ [MazeBuilder.py](https://github.com/genji9071/Dark_buddy/blob/master/dark_maze/MazeBuilder.py) 迷宫的生成类，用两种算法实现了两种不同的迷宫绘制逻辑  
    + **prime_maze** 扭曲迷宫，由prime算法生成迷宫，追求高复杂性，分岔路的步数高，迷惑性强。
    + **tortuous_maze** 曲折迷宫，某种意义上这不算是迷宫了，因为只有一条路，只不过是一条非常曲折的迷宫路线，步数高，观赏性强，后期想用作RPG元素 

+ [MazePainter.py](https://github.com/genji9071/Dark_buddy/blob/master/dark_maze/MazePainter.py) 迷宫的图片绘制类，包含镜头剪辑功能，用定焦镜头代替原先~~战争迷雾~~的设计，并增加了导航箭头辅助锁定迷宫终点


### dark_menu
+ 机器人的功能菜单。做成了可快速增加功能及修改配置的样子

+ [BaseHandler.py](https://github.com/genji9071/Dark_buddy/blob/master/dark_menu/BaseHandler.py) 所有菜单功能模块的抽象类，实现doHandler后即可根据用户的操作触发功能

+ [DarkMenu.py](https://github.com/genji9071/Dark_buddy/blob/master/dark_menu/DarkMenu.py) 菜单的实现类，通过读取 [ManuConfig.py](https://github.com/genji9071/Dark_buddy/blob/master/config/ManuConfig.py) 内的配置，实现菜单向导


### dark_quiz
+ 调题库接口，实现了一个机器人出题的功能

+ [DarkQuiz.py](https://github.com/genji9071/Dark_buddy/blob/master/dark_quiz/DarkQuiz.py) 问答题的实现类，是非和单选题两种选项，redis做缓存


### dark_show_hand
+ 一个梭哈的纸牌游戏。  
    由ai策略模块，主流程模块，道具模块，监听器（以及第三方插件集成）模块，四个大块组成一个长流程功能模块。具体看代码。
    
    
### dark_spy
+ 一个多人协作，由机器人主持的"谁是卧底"游戏  
    用到了redis缓存json，动态反序列化成obj的做法。~~由于没有找到一个不错的方法来抽离出公共模块，放弃这种模式~~


### dark_word_cloud
+ 生成词云图片的模块，提供一种由词入文的新型推送新闻等消息的思路  


### juhe_api
+ 调用各种各样的api来实现的功能集合，没啥好说的


### lib
+ 公共方法大合集。涉及机器人发送消息，接口返回，日志打印等等的纯工程非业务功能，还有例如延迟加载等等提升部署速度的骚操作


### mapper
+ 数据库读写操作实现。  
    一开始用pony的orm来做，后来发现还是直接pymysql比较方便。
    

### playground
+ 一些demo代码，自己平时写的一些松散的东西


### resource
+ sql语句备份啥的


### user
+ 一套机器人的用户管理功能，实现用户对机器人发送消息的记录等等，还实现了涉及用户属性如积分等等的功能实现


### web
+ 一个前端工程，由于机器人可以发送页面链接，所以需要一个前端工程支持，再次感谢xhd的贡献


