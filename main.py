# main.py
# punto de entrada principal del sistema

from utils import inicializar_sistema, mostrar_titulo, pausar
from logica import menu_socios, menu_membresias, menu_cuotas
from actyasist import menu_actividades, menu_inscripciones, menu_asistencia

def menu_principal():
    inicializar_sistema() # crea la carpeta y archivos txt si no existen
    while True:
        mostrar_titulo("bienvenido, elija una opción")
        print("  1. gestion de socios")
        print("  2. gestion de membresias")
        print("  3. control de cuotas")
        print("  4. gestion de actividades")
        print("  5. inscripciones")
        print("  6. control de asistencia")
        print("  0. salir")
        
        opcion = input("\n  opcion: ").strip() # le saco espacios accidentales
        
        if opcion == "1":
            menu_socios() # llamo a las funciones de logica.py
        elif opcion == "2":
            menu_membresias()
        elif opcion == "3":
            menu_cuotas()
        elif opcion == "4":
            menu_actividades() # llamo a las funciones del otro archivo
        elif opcion == "5":
            menu_inscripciones()
        elif opcion == "6":
            menu_asistencia()
        elif opcion == "0":
            print("\n  nos vemos")
            break # rompe el bucle y cierra el programa
        else:
            print("  opcion invalida")
            pausar()

if __name__ == "__main__":
    menu_principal() # arranca el sistema
