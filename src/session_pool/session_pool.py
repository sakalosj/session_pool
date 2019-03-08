import queue
from collections import namedtuple
from functools import partial
from random import randint
from threading import Thread
from time import sleep
from types import SimpleNamespace

from requests_futures.sessions import FuturesSession

import requests
# proxies = {'https': 'http://PRG-DC\srv_prgdc-OATQualys:b&Gw@2w5H7Q!xLQf@globalproxy.goc.dhl.com:8080'}
proxies = {}
TaskRequest = namedtuple('TaskRequest', 'method result_queue url kwargs', defaults={})



class SessionPool(Thread):
    '''

    Todo: add check limitation for input queue
    '''
    def __init__(self, comm_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.future_session = FuturesSession()
        self.comm_queue = comm_queue
        self.futures = {}

        self.method = {'post': self.future_session.post,
                       'get': self.future_session.get
                       }

    def run(self):
        '''

        Returns:

        '''
        while True:
            while not self.comm_queue.empty():
                task_request = self.comm_queue.get()
                if not isinstance(task_request, TaskRequest):
                    # log error
                    continue
                future = self.method[task_request.method](task_request.url, **task_request.kwargs)
                self.futures[future] = task_request.result_queue

            finished = [future for future in self.futures.keys() if future.done()]

            for future in finished:
                try:
                    result = future.result()  # add exception hadling
                except BaseException as e:
                    result = e
                    print(e)
                    # log error

                self.futures[future].put(result)
                del(self.futures[future])
            sleep(1)


class W(Thread):
    def __init__(self, comm_q):
        super().__init__()
        self.comm_q = comm_q
        self.result_q = queue.Queue()

    def run(self, *args, **kwargs):
        url = 'http://slowwly.robertomurray.co.uk/delay/{}/url/http://google.co.uk'.format(randint(1,5)*1000)
        t = TaskRequest('get', self.result_q, url, proxies)
        self.comm_q.put(t)
        response = self.result_q.get()
        print('response\n{}'.format( response.text))


if __name__ == 'request_pool':
    q = queue.Queue()
    q_r = queue.Queue()

