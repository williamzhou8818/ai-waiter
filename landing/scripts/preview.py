"""Local static preview with explicit media MIME types on Windows and Linux."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer

args=argparse.ArgumentParser(description=__doc__)
args.add_argument('--directory',default='dist')
args.add_argument('--port',type=int,default=4173)
config=args.parse_args()
class Preview(SimpleHTTPRequestHandler):
    extensions_map={**SimpleHTTPRequestHandler.extensions_map,'.vtt':'text/vtt','.webm':'video/webm','.mp4':'video/mp4','.js':'text/javascript','.css':'text/css','.xml':'application/xml'}

with ThreadingHTTPServer(('127.0.0.1',config.port),partial(Preview,directory=config.directory)) as server:
    print(f'Preview at http://127.0.0.1:{config.port}/',flush=True)
    server.serve_forever()
