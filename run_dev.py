import subprocess
import sys
import time
import logging
import os
import signal
from pathlib import Path


root_dir = Path(__file__).resolve().parent
log_dir = root_dir / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

log_formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("SystemRunner")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(log_dir / "web.log", mode='a', encoding='utf-8')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

def kill_process_tree(process, is_windows):
    if process is None:
        return
    try:
        if is_windows:
            subprocess.call(
                ['taskkill', '/F', '/T', '/PID', str(process.pid)], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except Exception as e:
        logger.error(f"Failed to kill process PID {process.pid}: {e}")


def main():
    logger.info("Starting Fraud Detection System (Cross-Platform)...")
    
    is_windows = sys.platform.startswith('win')
    
    backend_process = None
    frontend_process = None
    

    process_kwargs = {}
    if not is_windows:
        process_kwargs['start_new_session'] = True
        
    try:

        if is_windows:
            backend_cmd = "uv run start_app.py"
        else:
            backend_cmd = ["uv", "run", "python", "start_app.py"]
            
        backend_process = subprocess.Popen(
            backend_cmd, 
            cwd=root_dir,
            shell=is_windows,
            **process_kwargs
        )
        logger.info("[1/2] Backend server (uv) activated successfully.")
        
        frontend_dir = root_dir / "web" / "frontend"
            
        if is_windows:
            frontend_cmd = "pnpm run dev"
        else:
            frontend_cmd = ["pnpm", "run", "dev"]

        frontend_process = subprocess.Popen(
            frontend_cmd, 
            cwd=frontend_dir, 
            shell=is_windows,
            **process_kwargs
        )
        logger.info("[2/2] Frontend server activated successfully.")
        
        logger.info("System is running. Press [Ctrl + C] here to terminate all processes.")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.warning("KeyboardInterrupt detected (Ctrl+C). Initiating shutdown...")
    except Exception as e:
        logger.error(f"A critical error occurred: {e}")
    finally:

        logger.info("Cleaning up zombie processes...")
        kill_process_tree(backend_process, is_windows)
        kill_process_tree(frontend_process, is_windows)
        logger.info("All processes terminated safely. Ports are free. Goodbye!")

if __name__ == "__main__":
    main()

# TODO: file này có bug chưa có sửa đừng có đụ vào
