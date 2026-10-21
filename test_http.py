
import unittest, threading, tempfile, shutil, json
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import server
class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.original=server.ROOT
        server.ROOT=Path(cls.temp.name)
        for name in ('index.html','sample_data.json'): shutil.copy(cls.original/name,server.ROOT/name)
        cls.http=server.HTTPServer(('127.0.0.1',0),server.Handler)
        cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True); cls.thread.start()
        cls.url='http://127.0.0.1:'+str(cls.http.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown(); cls.http.server_close(); cls.thread.join(); server.ROOT=cls.original; cls.temp.cleanup()
    def test_health(self):
        with urlopen(self.url+'/api/health') as r: self.assertEqual(json.load(r)['status'],'ok')
    def test_home(self):
        with urlopen(self.url+'/') as r: self.assertIn(b'<form',r.read())
    def test_success(self):
        request=Request(self.url+'/api/run',data=b'{"query": "refund policy"}',headers={'Content-Type':'application/json'})
        with urlopen(request) as r: self.assertIsInstance(json.load(r),dict)
    def test_invalid_json(self):
        with self.assertRaises(HTTPError) as ctx: urlopen(Request(self.url+'/api/run',data=b'{'))
        self.assertEqual(ctx.exception.code,400)
    def test_object_required(self):
        with self.assertRaises(HTTPError) as ctx: urlopen(Request(self.url+'/api/run',data=b'[]'))
        self.assertEqual(ctx.exception.code,400)
    def test_not_found(self):
        with self.assertRaises(HTTPError) as ctx: urlopen(self.url+'/missing')
        self.assertEqual(ctx.exception.code,404)
