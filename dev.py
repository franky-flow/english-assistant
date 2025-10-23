#!/usr/bin/env python3
"""
English Assistant Development Server Manager
Unified script to manage both frontend and backend development servers
"""
import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class DevServerManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = False
        
    def start_backend(self):
        """Start the backend API server"""
        print("🚀 Starting Backend API Server...")
        try:
            backend_dir = Path(__file__).parent / "backend"
            self.backend_process = subprocess.Popen(
                [sys.executable, "run_server.py"],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor backend output in a separate thread
            def monitor_backend():
                for line in iter(self.backend_process.stdout.readline, ''):
                    if line.strip():
                        print(f"[BACKEND] {line.strip()}")
                        
            threading.Thread(target=monitor_backend, daemon=True).start()
            
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
        
        return True
    
    def start_frontend(self):
        """Start the frontend development server"""
        print("🌐 Starting Frontend Server...")
        try:
            frontend_dir = Path(__file__).parent / "frontend"
            self.frontend_process = subprocess.Popen(
                [sys.executable, "serve.py"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor frontend output in a separate thread
            def monitor_frontend():
                for line in iter(self.frontend_process.stdout.readline, ''):
                    if line.strip():
                        print(f"[FRONTEND] {line.strip()}")
                        
            threading.Thread(target=monitor_frontend, daemon=True).start()
            
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
        
        return True
    
    def stop_servers(self):
        """Stop both servers"""
        print("\n🛑 Stopping development servers...")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend server stopped")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("⚠️  Backend server force killed")
            except Exception as e:
                print(f"❌ Error stopping backend: {e}")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend server stopped")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("⚠️  Frontend server force killed")
            except Exception as e:
                print(f"❌ Error stopping frontend: {e}")
        
        self.running = False
    
    def run(self, mode="both"):
        """Run development servers"""
        print("🔧 English Assistant Development Environment")
        print("=" * 50)
        
        # Handle Ctrl+C gracefully
        def signal_handler(sig, frame):
            self.stop_servers()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        try:
            if mode in ["both", "backend"]:
                if not self.start_backend():
                    return False
                time.sleep(2)  # Give backend time to start
            
            if mode in ["both", "frontend"]:
                if not self.start_frontend():
                    return False
                time.sleep(2)  # Give frontend time to start
            
            self.running = True
            
            print("\n✅ Development servers started successfully!")
            print()
            print("🔗 Quick Links:")
            if mode in ["both", "frontend"]:
                print("   • Frontend: http://localhost:3000")
            if mode in ["both", "backend"]:
                print("   • Backend API: http://localhost:8000")
                print("   • API Docs: http://localhost:8000/docs")
                print("   • Health Check: http://localhost:8000/health")
            print()
            print("📝 Development Tips:")
            print("   • Frontend auto-reloads on file changes")
            print("   • Backend auto-reloads on Python file changes")
            print("   • Check browser console for frontend errors")
            print("   • Check terminal for backend errors")
            print()
            print("Press Ctrl+C to stop all servers")
            print("=" * 50)
            
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
                
                # Check if processes are still running
                if mode in ["both", "backend"] and self.backend_process:
                    if self.backend_process.poll() is not None:
                        print("❌ Backend server stopped unexpectedly")
                        break
                
                if mode in ["both", "frontend"] and self.frontend_process:
                    if self.frontend_process.poll() is not None:
                        print("❌ Frontend server stopped unexpectedly")
                        break
            
        except Exception as e:
            print(f"❌ Development server error: {e}")
            return False
        finally:
            self.stop_servers()
        
        return True

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="English Assistant Development Server")
    parser.add_argument(
        "mode", 
        nargs="?", 
        default="both",
        choices=["both", "frontend", "backend"],
        help="Which servers to start (default: both)"
    )
    parser.add_argument(
        "--check", 
        action="store_true",
        help="Check if required dependencies are installed"
    )
    
    args = parser.parse_args()
    
    if args.check:
        check_dependencies()
        return
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  No .env file found. Creating from template...")
        env_example = Path(".env.example")
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("✅ Created .env file from .env.example")
        else:
            print("❌ No .env.example file found")
    
    # Start development servers
    manager = DevServerManager()
    success = manager.run(args.mode)
    
    if not success:
        print("❌ Failed to start development environment")
        sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print(f"✅ Python {sys.version.split()[0]}")
    
    # Check backend dependencies
    backend_deps = [
        "fastapi", "uvicorn", "transformers", "torch", 
        "language_tool_python", "psycopg2", "pydantic"
    ]
    
    missing_backend = []
    for dep in backend_deps:
        try:
            __import__(dep.replace("-", "_"))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing_backend.append(dep)
    
    # Check frontend dependencies (Node.js)
    frontend_dir = Path("frontend")
    node_modules = frontend_dir / "node_modules"
    
    if node_modules.exists():
        print("✅ Frontend dependencies (node_modules)")
    else:
        print("❌ Frontend dependencies missing")
        print("   Run: cd frontend && npm install")
    
    # Check if TailwindCSS is built
    styles_css = frontend_dir / "css" / "styles.css"
    if styles_css.exists() and styles_css.stat().st_size > 1000:
        print("✅ TailwindCSS compiled")
    else:
        print("❌ TailwindCSS not compiled")
        print("   Run: cd frontend && npm run build")
    
    if missing_backend:
        print(f"\n❌ Missing backend dependencies: {', '.join(missing_backend)}")
        print("   Run: cd backend && pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies check passed!")
    return True

if __name__ == "__main__":
    main()