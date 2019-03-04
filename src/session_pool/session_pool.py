import queue
from collections import namedtuple
from threading import Thread
from time import sleep

import requests
from requests_futures.sessions import FuturesSession

TaskRequest = namedtuple('TaskRequest','method result_queue args_kwargs')

class SessionPool(Thread):
    '''
    C
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
                future = self.method[task_request.method](task_request.args_kwargs)
                self.futures[future] = task_request.result_queue

            finished = [future for future in self.futures.keys() if future.done()]

            for future in finished:
                try:
                    result = (0, future.result())  # add exception hadling
                except BaseException as e:
                    result = (900,) #errorcode sessionpool 900 general_error

                self.futures[future].put(result)
                del(self.futures[future])
            sleep(1)



if __name__ == 'request_pool':
    q = queue.Queue()
    q_r = queue.Queue()

