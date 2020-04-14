# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent
import logging
import hashlib
import time
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from scrapy.http import HtmlResponse
from twisted.internet import defer
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.web.client import ResponseFailed
from LianjiaDeal.items import SpiderErrorItem

logger = logging.getLogger(__name__)

class RandomUserAgentDownloaderMiddleware(object):
    """该类使用使用fake_useragent库，实现随机获取User-Agent，并赋值给请求头"""

    def process_request(self, spider, request):
        agent = UserAgent()
        user_agent = agent.random
        request.headers['User-Agent']=user_agent
        logger.debug('正在使用RandomUserAgentDownloaderMiddleware：{}'.format(user_agent))


class ProxyDownloaderMiddlerware(object):
    """编写下载器中间件ProxyDownloaderMiddleware类，
    接入讯代理动态转发接口，实现ip切换。"""

    def __init__(self, secret, orderno):
        self.secret = secret
        self.orderno = orderno

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            secret = crawler.settings.get('SECRET'),
            orderno = crawler.settings.get('ORDERNO')
        )

    def process_request(self, request, spider):
        timestamp = str(int(time.time()))
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        string = string.encode()
        md5_string = hashlib.md5(string).hexdigest()
        sign = md5_string.upper()
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp

        request.meta['proxy'] = 'http://forward.xdaili.cn:80'
        request.headers["Proxy-Authorization"] = auth
        logger.debug('正在使用动态转发')



class ExceptionDownloaderMiddleware(object):
    '''捕获状态码为4开头或者是5开头的响应，将出现该状态码的请求记录在文件中；
    将出现异常TCPTimedOutError和TimeoutError的请求对象，重新放回调度器中；
    对于下载器中出现其他异常的请求，记录在文件中。'''
    SOME_EXCEPTIONS = (defer.TimeoutError,  DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost,  ResponseFailed,
                           IOError, TunnelError)

    def __init__(self,settings):
        self.retry_enabled = settings.getbool('RETRY_ENABLED')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self,request,response,spider):
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            with open(str(spider.name) + ".txt", "a") as f:
                f.write('{}got a response.status:{}'.format(request.url, response.status) + "\n")
            response = HtmlResponse(url='')
            logger.debug('{}got a response.status:{}'.format(request.url, response.status))
            return response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception,TCPTimedOutError) or isinstance(exception,TimeoutError):
            # 没有设定不能重试的情况，将request对象重新放入调度器中
            if self.retry_enabled and not request.meta.get('dont_retry', False):
                # 将请求对象meta中的retry_times设置为0
                request.meta['retry_times'] = 0
                # 将请求对象重新放入调度器
                logger.info('{}被重新放入调度器'.format(request.url))
                return request
            else:
                with open(str(spider.name) + ".txt", "a") as f:
                    f.write('{}got a exception:{}'.format(request.url, exception) + "\n")
                logger.debug('{}got a exception:{}'.format(request.url, exception))
                response = HtmlResponse(url='')
                return response

        elif isinstance(exception,self.SOME_EXCEPTIONS):

            with open(str(spider.name) + ".txt", "a") as f:
                f.write('{}got a exception:{}'.format(request.url,exception) + "\n")
            logger.debug('{}got a exception:{}'.format(request.url, exception))
            response = HtmlResponse(url='')
            return response

        logger.debug('{}got a exception:{},but not return response obj'.format(request.url, exception))

class ExceptionSpiderMiddleware(object):
    """编写方法process_spider_exception，用来捕获发生spider和spider中间件的异常。"""

    def process_spider_exception(self, response, exception, spider):
        logger.debug('{}got a spider exception:{}'.format(response.url, exception))
        item = SpiderErrorItem()
        item['url'] = response.url()
        item['error_reason'] = exception
        yield item