
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import argparse, json, os
from logic import run
ROOT=Path(__file__).resolve().parent
PERSIST=False
class Handler(BaseHTTPRequestHandler):
    def send(self,status,body,kind='application/json'):
        data=body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type',kind+'; charset=utf-8')
        self.send_header('Content-Length',str(len(data)))
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path=='/': self.send(200,(ROOT/'index.html').read_text(encoding='utf-8'),'text/html')
        elif self.path=='/api/health': self.send(200,json.dumps({'status':'ok'}))
        else: self.send(404,json.dumps({'error':'Not found'}))
    def do_POST(self):
        if self.path!='/api/run': return self.send(404,json.dumps({'error':'Not found'}))
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<1 or size>32768: raise ValueError('Body must be 1 to 32768 bytes')
            payload=json.loads(self.rfile.read(size))
            if not isinstance(payload,dict): raise ValueError('JSON object required')
            path=ROOT/'state.json' if PERSIST and (ROOT/'state.json').exists() else ROOT/'sample_data.json'
            records=json.loads(path.read_text(encoding='utf-8'))
            result=run(payload,records)
            if PERSIST:
                temp=ROOT/'state.json.tmp'
                temp.write_text(json.dumps(records,indent=2),encoding='utf-8')
                os.replace(temp,ROOT/'state.json')
            self.send(200,json.dumps(result))
        except (ValueError,TypeError) as exc: self.send(400,json.dumps({'error':str(exc)}))
        except Exception:
            self.send(500,json.dumps({'error':'Internal error. Check dataset or local storage.'}))
if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--port',type=int,default=8000)
    args=parser.parse_args()
    print(f'Open http://127.0.0.1:{args.port}',flush=True)
    HTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
