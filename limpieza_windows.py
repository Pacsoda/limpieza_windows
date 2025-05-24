
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

def menu_principal():
    while True:
        print("\n=========== MENÚ PRINCIPAL ===========")
        print("1. Eliminar posibles amenazas (verificación y reparación)")
        print("2. Limpiar caché y archivos temporales")
        print("3. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            menu_reparacion()
        elif opcion == "2":
            menu_cache()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

def menu_reparacion():
    opciones = [
        ("Ejecutar sfc /scannow", "sfc /scannow"),
        ("DISM: CheckHealth", "DISM /Online /Cleanup-Image /CheckHealth"),
        ("DISM: ScanHealth", "DISM /Online /Cleanup-Image /ScanHealth"),
        ("DISM: RestoreHealth", "DISM /Online /Cleanup-Image /RestoreHealth"),
        ("Ejecutar análisis con MRT", "MRT"),
        ("Volver", None)
    ]
    while True:
        print("\n====== ELIMINAR POSIBLES AMENAZAS ======")
        for i, (desc, _) in enumerate(opciones, start=1):
            print(f"{i}. {desc}")
        eleccion = input("Selecciona una opción: ").strip()

        if eleccion.isdigit():
            idx = int(eleccion) - 1
            if 0 <= idx < len(opciones):
                if opciones[idx][1] is None:
                    break
                ejecutar_comando(opciones[idx][1], opciones[idx][0])
                time.sleep(2)
            else:
                print("Opción inválida.")
        else:
            print("Entrada no válida.")

def menu_cache():
    print("\n======= LIMPIEZA DE CACHÉ =======")
    print("1. Limpieza automática (recomendada)")
    print("2. Limpieza manual")
    print("3. Volver")
    opcion = input("Selecciona una opción: ").strip()

    if opcion == "1":
        limpieza_automatica()
    elif opcion == "2":
        limpieza_manual()

def limpieza_automatica():
    limpiar_temp()
    ejecutar_comando("del /Q C:\\Windows\\Prefetch\\*", "Limpiar Prefetch")
    ejecutar_comando("ipconfig /flushdns", "Limpiar caché de DNS")
    ejecutar_comando("ie4uinit.exe -ClearIconCache", "Limpiar iconos")
    ejecutar_comando("del /f /s /q %localappdata%\\Microsoft\\Windows\\Explorer\\thumbcache_*.db", "Limpiar miniaturas")
    # ejecutar_comando("wsreset.exe", "Limpiar Tienda Microsoft")
    ejecutar_comando("Dism.exe /Online /Cleanup-Image /StartComponentCleanup", "Eliminar componentes antiguos")

def limpieza_manual():
    opciones = [
        ("Limpiar archivos temporales", limpiar_temp),
        ("Limpiar carpeta Prefetch", lambda: ejecutar_comando("del /Q C:\\Windows\\Prefetch\\*", "Limpiar Prefetch")),
        ("Limpiar caché DNS", lambda: ejecutar_comando("ipconfig /flushdns", "Limpiar DNS")),
        ("Limpiar caché de iconos", lambda: ejecutar_comando("ie4uinit.exe -ClearIconCache", "Limpiar iconos")),
        ("Limpiar miniaturas", lambda: ejecutar_comando("del /f /s /q %localappdata%\\Microsoft\\Windows\\Explorer\\thumbcache_*.db", "Limpiar miniaturas")),
        ("Limpiar caché de Tienda Microsoft", lambda: ejecutar_comando("wsreset.exe", "Limpiar Microsoft Store")),
        ("Eliminar componentes obsoletos", lambda: ejecutar_comando("Dism.exe /Online /Cleanup-Image /StartComponentCleanup", "Eliminar componentes obsoletos")),
        ("Volver", None)
    ]

    while True:
        print("\n====== LIMPIEZA MANUAL ======")
        for i, (desc, _) in enumerate(opciones, start=1):
            print(f"{i}. {desc}")
        eleccion = input("Selecciona una opción: ").strip()

        if eleccion.isdigit():
            idx = int(eleccion) - 1
            if 0 <= idx < len(opciones):
                if opciones[idx][1] is None:
                    break
                opciones[idx][1]()
                time.sleep(1)
            else:
                print("Opción inválida.")
        else:
            print("Entrada no válida.")

if __name__ == "__main__":
    if not es_admin():
        print("[!] Este script debe ejecutarse como administrador.")
        input("Presiona ENTER para salir...")
        exit(1)
    menu_principal()
