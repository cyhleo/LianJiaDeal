# -*- coding: utf-8 -*-


BOT_NAME = 'LianjiaDeal'

SPIDER_MODULES = ['LianjiaDeal.spiders']
NEWSPIDER_MODULE = 'LianjiaDeal.spiders'

# 布尔值
ROBOTSTXT_OBEY = ''

# mongo_db存储设置
MONGO_URI = ''
MONGO_DB = ''


# 设置最小的下载延迟时间
DOWNLOAD_DELAY = ''
# 开启自动限速设置
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# 发送到每一个服务器的并行请求数量
AUTOTHROTTLE_TARGET_CONCURRENCY = ''


# 设置并发数
CONCURRENT_REQUESTS = ''
CONCURRENT_REQUESTS_PER_DOMAIN = ''
CONCURRENT_REQUESTS_PER_IP = ''

# 禁用cookies
COOKIES_ENABLED = True

# 关闭telnet
TELNETCONSOLE_ENABLED = True

# 设置请求头
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language':'zh-CN,zh;q=0.9',
   'Cache-Control':'max-age=0',
   'Connection':'keep-alive',
   'Host':'xm.lianjia.com',
   'Upgrade-Insecure-Requests':'1',
}

# 设置spider中间件
SPIDER_MIDDLEWARES = {
   'LianjiaDeal.middlewares.ExceptionSpiderMiddleware': 544,
}

# 下载器中间件
DOWNLOADER_MIDDLEWARES = {
   'LianjiaDeal.middlewares.RandomUserAgentDownloaderMiddleware': 543,
   'LianjiaDeal.middlewares.ProxyDownloaderMiddlerware': 553,
   'LianjiaDeal.middlewares.ExceptionDownloaderMiddleware': 100,
}


# 设置扩展
EXTENSIONS = {
   'LianjiaDeal.latencies.Latencies': 500,
}

# 设置设置吞吐量和延迟的时间间隔
LATENCIES_INTERVAL = 5


ITEM_PIPELINES = {
   'LianjiaDeal.pipelines.MongoPipeline': 300,
   'LianjiaDeal.pipelines.SpiderErrorFile': 400,
}

# 开启日志记录
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'

#logger输出格式设置
LOG_FORMATTER = 'scrapy.logformatter.LogFormatter'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# 如果为True，则进程的所有标准输出（和错误）将重定向到日志。 例如，如果您打印（'hello'）它将出现在Scrapy日志中。
LOG_STDOUT = False

# 显示的日志最低级别
LOG_LEVEL = 'INFO'

import datetime
t = datetime.datetime.now()
log_file_path = './log_{}_{}_{}.log'.format(t.month,t.day,t.hour)
# log磁盘保存地址
LOG_FILE = log_file_path


# 在爬虫结束的时候不清空请求队列和去重指纹队列
SCHEDULER_PERSIST = True
# 在爬虫开始的时候不清空请求队列
SCHEDULER_FLUSH_ON_START = False

# 启用scrapy_redis内置的调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# # 启动scrapy_redis内置的请求去重类
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# 启用scrapy_redis内置的先进先出队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'

#请求队列和去重指纹队列存储使用的redis数据库info
REDIS_HOST = ''
REDIS_PORT = ''
REDIS_PASSWORD = ''



# 动态转发设置
SECRET = ''
ORDERNO = ''