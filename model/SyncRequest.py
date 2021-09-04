import threading
from threading import Lock
import time
import requests

import model.Logging as log

sessions = requests.sessions
sessions.HTTPAdapter.max_retries = 5
lock = Lock()
# 成功处理的请求
success = []
# 服务端限制客户端请求的客户端数
limit = 0
# 失败的线程处理列表
fail = []
# 线程id列表
ids = []
# 响应时间列表
response_time = []


def data_build(id, s):
    log.logger.info('ID:{}, 响应:{:.2f} 毫秒'.format(id, s * 1000))
    ids.append(id)
    response_time.append(s * 1000)


class SyncRequestTask(threading.Thread):

    def __init__(self, threadId, url, method, params, header, timeout=10):
        threading.Thread.__init__(self)
        # super().__init__()
        self.setName(f"sync--{threadId}")
        self.url = url
        self.method = method
        self.params = params
        self.timeout = timeout
        self.header = header

    # 发送请求
    def request(self):
        req = None
        try:
            if self.method == 'GET':
                req = self.doGet()
                self.add(req)
            else:
                req = self.doPost()
                self.add(req)
        except Exception as e:
            print(e)
            fail.append(req)

    def doGet(self):
        startTime = time.time()

        s = sessions.session()
        req = s.get(self.url, headers=self.header, timeout=self.timeout)
        data_build(self.getName(), time.time() - startTime)
        req.close()
        return req

    def doPost(self):
        startTime = time.time()

        s = sessions.session()
        req = s.post(self.url, data=self.params, headers=self.header, timeout=self.timeout)
        data_build(self.getName(), time.time() - startTime)
        req.close()
        return req

    @staticmethod
    def add(request):
        global lock
        global limit
        lock.acquire()
        if request.status_code == 200:
            success.append(request)
        elif requests.status_codes == 429:
            limit += 1
        else:
            fail.append(request)
        lock.release()

    def run(self):
        # 开始发送请求
        self.request()
