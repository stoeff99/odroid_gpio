from http.server import BaseHTTPRequestHandler, HTTPServer
import gpiod
import re

CHIP_NAME = "gpiochip0"
chip = gpiod.Chip(CHIP_NAME)
active_lines = {}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        match = re.match(r"^/pin/(\d+)/(on|off)$", self.path)
        if not match:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid URL. Use /pin/{line}/on or /off")
            return

        line_number = int(match.group(1))
        action = match.group(2)

        try:
            if line_number not in active_lines:
                line = chip.get_line(line_number)
                # libgpiod v1.x-style request
                line.request(consumer="ha_gpio", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
                active_lines[line_number] = line
            else:
                line = active_lines[line_number]

            if action == "on":
                line.set_value(1)
                print(f"GPIO {line_number} set HIGH")
            else:
                line.set_value(0)
                print(f"GPIO {line_number} set LOW")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"GPIO {line_number} set {action.upper()}".encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            error = f"Error setting GPIO {line_number}: {e}"
            self.wfile.write(error.encode())
            print(error)

print(f"GPIO server ready on {CHIP_NAME} port 8000")
HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
