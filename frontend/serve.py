#!/usr/bin/env python3
"""
Simple development server for English Assistant frontend
"""
import http.server
import socketserver
import os
import sys
from pathlib import Path

def main():
    # Change to frontend directory
    frontend_dir = Path(__file__).parent
    os.chdir(frontend_dir)
    
    # Configuration
    PORT = 3000
    HOST = 'localhost'
    
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add CORS headers for API requests
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            super().end_headers()
        
        def do_OPTIONS(self):
            # Handle preflight requests
            self.send_response(200)
            self.end_headers()
        
        def log_message(self, format, *args):
            # Custom logging format
            print(f"[{self.address_string()}] {format % args}")
    
    try:
        with socketserver.TCPServer((HOST, PORT), CustomHTTPRequestHandler) as httpd:
            print("🌐 English Assistant Frontend Server")
            print(f"   URL: http://{HOST}:{PORT}")
            print(f"   Directory: {frontend_dir}")
            print()
            print("📁 Available files:")
            for file in sorted(frontend_dir.glob('*')):
                if file.is_file():
                    print(f"   • {file.name}")
            print()
            print("🔗 Quick Links:")
            print(f"   • Main App: http://{HOST}:{PORT}/")
            print(f"   • API Docs: http://localhost:8000/docs (if backend is running)")
            print()
            print("Press Ctrl+C to stop the server")
            print("=" * 60)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use")
            print(f"   Try a different port or stop the existing server")
        else:
            print(f"❌ Server error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()