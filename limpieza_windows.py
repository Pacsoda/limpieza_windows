import os
import subprocess
import shutil
import ctypes
import time

def es_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()

def ejecutar_comando(comando, descripcion):
    print(f"\n[+] {descripcion}")
    try:
        resultado = subprocess.run(comando, shell=True, check=True, text=True)
        print("[OK] Comando ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Falló el comando: {e}")

def limpiar_temp():
    print("\n[+] Limpiando archivos temporales...")
    temp_path = os.getenv('TEMP')
    try:
        for archivo in os.listdir(temp_path):
            archivo_path = os.path.join(temp_path, archivo)
            try:
                if os.path.isfile(archivo_path) or os.path.islink(archivo_path):
                    os.unlink(archivo_path)
                elif os.path.isdir(archivo_path):
                    shutil.rmtree(archivo_path, ignore_errors=True)
            except Exception as e:
                print(f"[!] No se pudo borrar {archivo_path}: {e}")
        print("[OK] Archivos temporales eliminados.")
    except Exception as e:
        print(f"[ERROR] No se pudo acceder a TEMP: {e}")

def menu():
    opciones = {
        "1": ("Escanear y reparar archivos del sistema (sfc /scannow)", lambda: ejecutar_comando("sfc /scannow", "Escaneo de integridad del sistema")),
        "2": ("Limpiar caché de archivos temporales", limpiar_temp),
        "3": ("Limpiar caché de la Tienda de Microsoft", lambda: ejecutar_comando("wsreset.exe", "Limpiar caché de la Tienda de Microsoft")),
        "4": ("Borrar caché de DNS", lambda: ejecutar_comando("ipconfig /flushdns", "Borrar caché de DNS")),
        "5": ("Limpiar caché de iconos", lambda: ejecutar_comando("ie4uinit.exe -ClearIconCache", "Limpiar caché de iconos")),
        "6": ("Limpiar caché de miniaturas", lambda: ejecutar_comando('del /f /s /q %localappdata%\\Microsoft\\Windows\\Explorer\\thumbcache_*.db', "Limpiar caché de miniaturas")),
        "7": ("Reparar imagen del sistema (DISM)", lambda: ejecutar_comando("Dism.exe /Online /Cleanup-image /Restorehealth", "Reparar imagen del sistema")),
        "8": ("Limpieza de componentes obsoletos (DISM)", lambda: ejecutar_comando("Dism.exe /Online /Cleanup-Image /StartComponentCleanup", "Limpieza de componentes antiguos")),
        "9": ("Salir", lambda: exit(0)),
    }

    while True:
        print("\n========== MENÚ DE MANTENIMIENTO ==========")
        for key, (desc, _) in opciones.items():
            print(f"{key}. {desc}")
        opcion = input("Selecciona una opción: ").strip()
        if opcion in opciones:
            _, accion = opciones[opcion]
            accion()
            time.sleep(2)
        else:
            print("[!] Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    if not es_admin():
        print("[!] Este script debe ejecutarse como administrador.")
        input("Presiona ENTER para salir...")
        exit(1)
    menu()
