import queue

from session_pool import SessionPool, TaskRequest

comm_queue = queue.Queue()
r1_queue = queue.Queue()
sp = SessionPool(comm_queue)
sp.start()

url = 'http://127.0.0.1:8000/accounts/login/'
kwargs = {dict(data={'username': 'test', 'password': '123!@#qweqweasdasd'})}
tr1 = TaskRequest('get', r1_queue, (url, kwargs))

