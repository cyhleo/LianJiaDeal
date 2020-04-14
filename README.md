# LianJiaDeal

用来爬取链家网中所有厦门市二手网交易信息。
# 部分结果展示

![]()
# 项目说明
1. 使用scrapy框架来编写爬虫程序。  

2. 编写下载器中间件ProxyDownloaderMiddleware类，接入讯代理动态转发接口，实现ip切换。   
在setting中设置讯代理动态转发SECRET值和ORDERNO值。

3. 在middlewares.py文件中编写下载器中间件RandomUserAgentDownloaderMiddleware类，使用fake_useragent库来随机获取User-Agent。

4. 在middlewares.py文件中编写下载器中间件ExceptionDownloaderMiddleware类，捕获状态码为4开头或者是5开头的响应，将出现该状态码的请求记录在文件中；将出现异常TCPTimedOutError和TimeoutError的请求对象，重新放回调度器中；对于下载器中出现其他异常的请求，记录在文件中。     
在settings中设置布尔值RETRY_ENABLED（是否允许重试）。     
应注意，在settings中设置该中间件的级别时，该级别应小于重试和重定向中间件的优先级。在下载器处理器返回响应到响应被调度器捕捉的过程中，保证ExceptionDownloaderMiddleware类的方法被最后执行。

5. 在middlewares.py文件中编写爬虫中间件ExceptionSpiderMiddleware类，编写方法process_spider_exception，用来捕获发生spider和spider中间件的异常。

6. 在.py文件中编写LianjiadealItem类，该类继承于scrapy.Item，用于封装交易信息。

7. 在.py文件中编写SpiderErrorItem类，该类继承于scrapy.Item，该item类用来存储spider、spider中间件中产生的异常信息。

8. 在pipelines.py文件中编写 MongoPipeline类，将LianjiadealItem保存至MongoDB数据库。     
在settings中设置MONGO_URI值（mongodb的uri），设置MONGO_DB值（数据库名）。

9. 在pipelines.py文件中编写 SpiderErrorFile类，将SpiderErrorItem保存至文件中。 

10. 在settings中编写DEFAULT_REQUEST_HEADERS列表，构造包含Host、Accept-Encoding等信息的请求头，模拟浏览器行为。

11. 编写扩展Latencies类，实现每隔5秒测试一次吞吐量和响应延迟及处理延迟，    
在settings中设置LATENCIES_INTERVAL值（测试间隔时间）。

12. 编写爬虫类DealLianjiaSpider，实现爬虫在链家网按一定规则自动流窜，获取数据，并使用正则和xpath解析库解析response内容，提取Item字段。

13. 启用自动限速扩展，根据所爬网站的负载自动限制爬取速度。    在seting中设置AUTOTHROTTLE_ENABLED值为True，设置AUTOTHROTTLE_START_DELAY（初始的下再延迟）， 设置AUTOTHROTTLE_MAX_DELAY（最大下载延迟），AUTOTHROTTLE_TARGET_CONCURRENCY（发送到服务器的请求并发量）。

14. 使用scrapy_redis内置调度器类和请求去重类，使用redis集合作为消息队列数据结构，使用redis列表作为请求指纹存储的数据结构。    在settings中设置SCHEDULER = 'scrapy_redis.scheduler.Scheduler'，DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'， SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'。
在settings中设置REDIS_HOST、REDIS_PORT、REDIS_PASSWORD值（请求队列和去重指纹队列存储使用的redis数据库info）。


# 告示
本代码仅作学习交流，切勿用于商业用途。如涉及侵权，会尽快删除。
