import queue

from session_pool import SessionPool, TaskRequest, W

comm_queue = queue.Queue()
r1_queue = queue.Queue()
sp = SessionPool(comm_queue)
sp.start()

# url = 'http://127.0.0.1:8000/accounts/login/'
url = 'http://testing-ground.scraping.pro'
url_l = 'http://testing-ground.scraping.pro/login?mode=login'
kwargs = dict(data={'username': 'test', 'password': '123!@#qweqweasdasd'})
tr1 = TaskRequest('get', r1_queue, (url, kwargs))

comm_queue.put(tr1)
response = r1_queue.get()
workers = [W(comm_queue) for i in range(3)]
[w.start() for w in workers]



