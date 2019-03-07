import queue
from collections import namedtuple
from functools import partial
from random import randint
from threading import Thread
from time import sleep
from types import SimpleNamespace

from requests_futures.sessions import FuturesSession

import requests
proxies = {'https': 'http://PRG-DC\srv_prgdc-OATQualys:b&Gw@2w5H7Q!xLQf@globalproxy.goc.dhl.com:8080'}
TaskRequest = namedtuple('TaskRequest', 'method result_queue url kwargs',defaults)

class T(namedtuple('T', 'method result_queue args_kwargs')):
    def __init__(self):
        super().__init__()
        self.args_kwargs = SimpleNamespace(args=(), kwargs={})

class SessionPool(Thread):
    '''

    Todo: add check limitation for input queue
    '''
    def __init__(self, comm_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.future_session = FuturesSession()
        self.comm_queue = comm_queue
        self.futures = {}

        self.method = {'post': partial(self.future_session.post, proxies=proxies),
                       'get': partial(self.future_session.get, proxies=proxies)
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
                future = self.method[task_request.method](task_request.args_kwargs[0], **task_request.args_kwargs[1])
                self.futures[future] = task_request.result_queue

            finished = [future for future in self.futures.keys() if future.done()]

            for future in finished:
                try:
                    result = (0, future.result())  # add exception hadling
                except BaseException as e:
                    result = (900,) #errorcode sessionpool 900 general_error
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
        t = TaskRequest('get',self.result_q, ('http://slowwly.robertomurray.co.uk/delay/{}/url/http://google.co.uk'.format(randint(1,5)*1000),))
        self.comm_q.put(t)
        response = self.result_q.get()
        print('{}\n{}'.format(*response))


if __name__ == 'request_pool':
    q = queue.Queue()
    q_r = queue.Queue()

