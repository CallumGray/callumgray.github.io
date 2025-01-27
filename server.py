import http.server
import socketserver
import threading
import os

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        print('Path before:',self.path)

        # Serve index.html for root path
        if self.path == '/':
            self.path = '/index.html'

        # If path doesn't have an extension and .html version exists, use that
        if '.' not in os.path.basename(self.path):
            html_path = self.path.rstrip('/') + '.html'
            if os.path.exists(os.path.join(os.getcwd(), html_path.lstrip('/'))):
                self.path = html_path

        print('Path after:', self.path)
        print()
        print("Press enter to exit")
        print()

        try:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        except FileNotFoundError:
            self.send_error(404, "File not found")


def run_server(port=8000):

    handler = CustomHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Hosting on http://localhost:{port}")

        httpd_thread = threading.Thread(target=httpd.serve_forever)
        httpd_thread.start()

        input("Press enter to exit\n")
        print("Shutting down (This might take a while...)")
        httpd.shutdown()
        httpd_thread.join()

if __name__ == "__main__":
    run_server()