import os
from pathlib import Path
import winshell
from win32com.client import Dispatch
import tkinter as tk
from tkinter import messagebox
import sys

def create_desktop_shortcut():
    try:
        # Ruta específica al proyecto
        operations_dir = Path(r"C:\Users\eugenio.garcia\OneDrive\AIProjects\OPERATIONS")
        
        # Verificar que existe el directorio y archivos necesarios
        required_paths = {
            "Directorio del proyecto": operations_dir,
            "Script principal": operations_dir / "Kevin.pyw",
            "Logo": operations_dir / "assets" / "logo.ico"  # Cambiado a .ico
        }
        
        missing_paths = [name for name, path in required_paths.items() if not path.exists()]
        
        if missing_paths:
            raise FileNotFoundError(
                "No se encontraron los siguientes elementos:\n" +
                "\n".join(f"- {name}: {required_paths[name]}" for name in missing_paths)
            )
        
        # Obtener escritorio
        desktop = winshell.desktop()
        
        # Ruta del script Kevin.pyw
        kevin_script = required_paths["Script principal"]
        
        # Crear acceso directo
        shortcut_path = os.path.join(desktop, "Kevin.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        
        # Configurar acceso directo
        pythonw_path = str(Path(sys.executable).parent / "pythonw.exe")
        shortcut.Targetpath = pythonw_path
        shortcut.Arguments = f'"{str(kevin_script)}"'
        shortcut.WorkingDirectory = str(operations_dir)
        shortcut.IconLocation = str(required_paths["Logo"])
        shortcut.Description = "Asistente Kevin - IA de Operaciones"
        shortcut.save()
        
        messagebox.showinfo(
            "Kevin",
            "¡Acceso directo creado con éxito!\n"
            "Puedes encontrar 'Kevin' en tu escritorio."
        )
        
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Error en la configuración:\n{str(e)}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    create_desktop_shortcut() 