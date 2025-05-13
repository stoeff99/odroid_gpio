from http.server import BaseHTTPRequestHandler, HTTPServer
import gpiod

chip = gpiod.Chip("gpiochip0")
line = chip.get_line(14)  # GPIO0B.6 == Pin 7
line.request(consumer="ha_gui", type=gpiod.LINE_REQ_DIR_OUT, default_val=0)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/on":
            line.set_value(1)
            print("GPIO set HIGH")
        elif self.path == "/off":
            line.set_value(0)
            print("GPIO set LOW")
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()