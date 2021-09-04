import time

import model.Logging as log
import model.Utils as util
import model.SyncCore as sc
import model.ReadDatas as data


def check_param(threadCount, requestUrl, methods, params):
    if threadCount <= 0:
        log.logger.error("请求数量不能小于0")
        exit(0)
    if str(methods).lower() != 'get' and str(methods).lower() != 'post':
        log.logger.error("请求方法错误")
        exit(0)
    if util.check_url(requestUrl) is False:
        log.logger.error("请求地址格式错误")
        exit(0)
    if util.check_json(params) is False:
        log.logger.error("JSON格式错误")
        exit(0)


if __name__ == '__main__':
    thread_count = 500
    method = 'POST'
    param = '{}'
    request_url = 'http://xxxxxx'
    # 多少秒执行完成
    slowTime = 0
    # 循环执行次数
    roundCount = 1
    # 是否从文件读取数据
    read = False

    startTime = time.time()
    # 读取压测数据
    # data.loadRequestData('/Users/xxx/Desktop/StressTestData-202007161112.txt')
    log.logger.info("读取数据消耗时间{}毫秒".format(time.time() - startTime))
    check_param(thread_count - 1, request_url, method, param)
    sc.start(slowTime, roundCount, thread_count, request_url, method, param, read)
