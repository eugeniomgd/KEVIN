import os
import sys
import subprocess
from pathlib import Path
import webbrowser
from time import sleep
import tkinter as tk
from tkinter import messagebox
import socket

def is_port_in_use(port):
    """Verifica si un puerto está en uso"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return False
    except OSError:
        return True

def find_free_port(start_port=8505, max_attempts=10):
    """Encuentra un puerto libre comenzando desde start_port"""
    port = start_port
    for _ in range(max_attempts):
        if not is_port_in_use(port):
            return port
        port += 1
    raise RuntimeError(f"No se encontró un puerto libre después de {max_attempts} intentos")

def launch_kevin():
    try:
        # Ruta específica al proyecto
        operations_dir = Path(r"C:\Users\eugenio.garcia\OneDrive\AIProjects\OPERATIONS")
        
        # Construir rutas absolutas
        venv_dir = operations_dir / "venv"
        activate_script = venv_dir / "Scripts" / "activate.bat"
        streamlit_exe = venv_dir / "Scripts" / "streamlit.exe"
        app_path = operations_dir / "main.py"

        # Verificar que existan todas las rutas
        paths_to_check = {
            "Operations": operations_dir,
            "Activate": activate_script,
            "Streamlit": streamlit_exe,
            "App": app_path
        }
        
        missing_paths = [name for name, path in paths_to_check.items() if not path.exists()]
        
        if missing_paths:
            raise FileNotFoundError(
                "No se encontraron los siguientes archivos necesarios:\n" +
                "\n".join(f"- {name}: {paths_to_check[name]}" for name in missing_paths)
            )

        # Encontrar un puerto disponible
        port = find_free_port()
        
        # Comando para ejecutar la app con puerto específico y sin abrir navegador
        cmd = f'"{activate_script}" && set PYTHONPATH={operations_dir} && "{streamlit_exe}" run "{app_path}" --server.port={port} --server.headless=true'
        
        # Ejecutar Streamlit en segundo plano
        process = subprocess.Popen(
            cmd, 
            shell=True,
            cwd=str(operations_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={
                **os.environ, 
                'PYTHONPATH': str(operations_dir),
                'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false',
                'STREAMLIT_SERVER_PORT': str(port),
                'STREAMLIT_SERVER_HEADLESS': 'true'
            }
        )
        
        # Esperar un momento para que el servidor inicie
        sleep(3)
        
        # Verificar si el proceso sigue vivo
        if process.poll() is not None:
            # Leer error si el proceso falló
            _, stderr = process.communicate()
            raise RuntimeError(f"Streamlit falló al iniciar: {stderr.decode()}")
        
        # Abrir en el navegador una sola vez
        webbrowser.open(f'http://localhost:{port}')
        
        # Mantener el proceso vivo
        process.wait()
        
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error",
            f"No se pudo iniciar Kevin.\n\nError: {str(e)}\n\n"
            "Por favor, verifica que todos los archivos estén en su lugar."
        )
        sys.exit(1)

if __name__ == "__main__":
    launch_kevin() 