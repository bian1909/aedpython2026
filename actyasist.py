# modulo para gestion de actividades, inscripciones y asistencia

from utils import (
    mostrar_titulo, pausar,
    validar_texto, validar_entero,
    leerARCH, agregarREG, escribirARCH, buscarREG, generar_id,
    actividad_a_linea, linea_a_actividad,
    inscripcion_a_linea, linea_a_inscripcion,
    asistencia_a_linea, linea_a_asistencia,
    obtener_fecha_actual, obtener_hora_actual,
    linea_a_socio
)
from registros import actividad, horario, inscripcion, Fecha_inscrip, control_asis, Fecha_asistencia

# rutas de archivos
rutaactividades = "datos/actividades.txt"
rutainscripciones = "datos/inscripciones.txt"
rutaasistencia = "datos/asistencia.txt"
rutasocios = "datos/socios.txt"

# menus

def menu_actividades():
    while True:
        mostrar_titulo("gestion de actividades")
        print("  1. alta de actividad")
        print("  2. listar actividades")
        print("  0. volver")
        opcion = input("\n  opcion: ").strip()
        if opcion == "1":
            alta_actividad()
        elif opcion == "2":
            listar_actividades()
        elif opcion == "0":
            break
        else:
            print("  opcion invalida")
            pausar()

def menu_inscripciones():
    while True:
        mostrar_titulo("inscripciones a actividades")
        print("  1. inscribir socio")
        print("  2. ver inscriptos")
        print("  0. volver")
        opcion = input("\n  opcion: ").strip()
        if opcion == "1":
            inscribir_socio()
        elif opcion == "2":
            ver_inscriptos()
        elif opcion == "0":
            break
        else:
            print("  opcion invalida")
            pausar()

def menu_asistencia():
    while True:
        mostrar_titulo("control de asistencia")
        print("  1. registrar entrada")
        print("  2. asistencia del dia")
        print("  0. volver")
        opcion = input("\n  opcion: ").strip()
        if opcion == "1":
            registrar_asistencia()
        elif opcion == "2":
            asistencia_del_dia()
        elif opcion == "0":
            break
        else:
            print("  opcion invalida")
            pausar()

# actividades

def alta_actividad():
    mostrar_titulo("alta de actividad")
    nombre = input("  nombre de la actividad: ").strip()
    nombre_valido = validar_texto(nombre, 2, 30)
    if nombre_valido is None:
        print("  nombre invalido")
        pausar()
        return
    descripcion = input("  descripcion breve: ").strip()
    dia = input("  dia de la semana (ej: lunes): ").strip().lower()
    hora_ini = input("  hora inicio (hh:mm): ").strip()
    hora_fin = input("  hora fin (hh:mm): ").strip()
    cupo = input("  cupo maximo: ").strip()
    cupo_valido = validar_entero(cupo, 1, 100)
    if cupo_valido is None:
        print("  cupo invalido (1-100)")
        pausar()
        return
    instructor = input("  instructor: ").strip()
    cod = generar_id(rutaactividades)
    hor = horario(hora_ini=hora_ini, hora_fin=hora_fin, dia_semana=dia)
    nueva = actividad(
        cod_activ=cod,
        nomb=nombre_valido,
        descrip=descripcion,
        horario=hor,
        cupo_actu=0,
        estado="Activa"
    )
    if agregarREG(rutaactividades, nueva, actividad_a_linea):
        print(f"  actividad {nombre_valido} creada con codigo {cod}")
    else:
        print("  error al crear actividad")
    pausar()

def listar_actividades():
    mostrar_titulo("listado de actividades")
    actividades = leerARCH(rutaactividades, linea_a_actividad)
    if not actividades:
        print("  no hay actividades registradas")
        pausar()
        return
    contador = 0
    for a in actividades:
        if a.estado == "Activa":
            print(f"  cod: {a.cod_activ} | {a.nomb} | {a.horario.dia_semana} {a.horario.hora_ini}-{a.horario.hora_fin} | cupo: {a.cupo_actu} | estado: {a.estado}")
            contador += 1
    print(f"\n  total de actividades activas: {contador}")
    pausar()

# inscripciones

def inscribir_socio():
    mostrar_titulo("inscribir socio a actividad")
    dni = input("  dni del socio: ").strip()
    dni_valido = int(dni) if dni.isdigit() and len(dni) == 8 else None
    if dni_valido is None:
        print("  dni invalido")
        pausar()
        return
    socios = buscarREG(rutasocios, lambda l: linea_a_socio(l) if False else None, "docu_identi", dni_valido)
    # buscamos manualmente porque no importamos linea_a_socio
    socios = leerARCH(rutasocios, linea_a_socio_importado) if False else []
    # mejor: leemos directamente
    from utils import linea_a_socio as _las
    socios = [s for s in leerARCH(rutasocios, _las) if s.docu_identi == dni_valido]
    if not socios:
        print("  socio no encontrado")
        pausar()
        return
    socio = socios[0]
    if socio.estado != "Activo":
        print("  el socio no esta activo")
        pausar()
        return
    actividades = leerARCH(rutaactividades, linea_a_actividad)
    disponibles = [a for a in actividades if a.estado == "Activa" and a.cupo_actu < 100]
    if not disponibles:
        print("  no hay actividades disponibles con cupo")
        pausar()
        return
    print("\n  actividades disponibles:")
    for i, a in enumerate(disponibles, 1):
        print(f"  {i}. cod {a.cod_activ} - {a.nomb} ({a.horario.dia_semana} {a.horario.hora_ini}-{a.horario.hora_fin})")
    opcion = input("\n  elegir numero de actividad: ").strip()
    try:
        num = int(opcion)
        if 1 <= num <= len(disponibles):
            actividad_elegida = disponibles[num - 1]
        else:
            print("  numero invalido")
            pausar()
            return
    except ValueError:
        print("  opcion invalida")
        pausar()
        return
    inscripciones = leerARCH(rutainscripciones, linea_a_inscripcion)
    ya_inscripto = any(i.socio_docu == dni_valido and i.cod_activ == actividad_elegida.cod_activ and i.estado == "Activa" for i in inscripciones)
    if ya_inscripto:
        print("  el socio ya esta inscripto en esa actividad")
        pausar()
        return
    año, mes, dia = obtener_fecha_actual().año, obtener_fecha_actual().mes, obtener_fecha_actual().dia
    nueva_insc = inscripcion(
        numb_inscrip=generar_id(rutainscripciones),
        socio_docu=dni_valido,
        cod_activ=actividad_elegida.cod_activ,
        Fecha_inscrip=Fecha_inscrip(año, mes, dia),
        estado="Activa"
    )
    actividad_elegida.cupo_actu += 1
    if agregarREG(rutainscripciones, nueva_insc, inscripcion_a_linea):
        escribirARCH(rutaactividades, actividades, "cod_activ;nomb;descrip;hora_ini;hora_fin;dia_semana;cupo_actu;estado", actividad_a_linea)
        print(f"  socio inscripto a {actividad_elegida.nomb}")
    else:
        print("  error al inscribir")
    pausar()

def ver_inscriptos():
    mostrar_titulo("inscriptos por actividad")
    actividades = leerARCH(rutaactividades, linea_a_actividad)
    if not actividades:
        print("  no hay actividades")
        pausar()
        return
    print("\n  actividades:")
    for i, a in enumerate(actividades, 1):
        print(f"  {i}. cod {a.cod_activ} - {a.nomb}")
    opcion = input("\n  elegir actividad: ").strip()
    try:
        num = int(opcion)
        if 1 <= num <= len(actividades):
            act = actividades[num - 1]
        else:
            print("  numero invalido")
            pausar()
            return
    except ValueError:
        print("  opcion invalida")
        pausar()
        return
    inscripciones = leerARCH(rutainscripciones, linea_a_inscripcion)
    inscriptos = [i for i in inscripciones if i.cod_activ == act.cod_activ and i.estado == "Activa"]
    if not inscriptos:
        print("  no hay inscriptos en esta actividad")
        pausar()
        return
    socios = leerARCH(rutasocios, linea_a_socio)
    contador = 0
    print(f"\n  inscriptos en {act.nomb}:")
    for insc in inscriptos:
        socio = next((s for s in socios if s.docu_identi == insc.socio_docu), None)
        if socio:
            print(f"  - {socio.apeynom} (dni: {socio.docu_identi})")
            contador += 1
    print(f"\n  total inscriptos: {contador} / cupo maximo")
    pausar()

# asistencia

def registrar_asistencia():
    mostrar_titulo("registrar entrada")
    dni = input("  dni del socio: ").strip()
    dni_valido = int(dni) if dni.isdigit() and len(dni) == 8 else None
    if dni_valido is None:
        print("  dni invalido")
        pausar()
        return
    socios = leerARCH(rutasocios, linea_a_socio)
    socio = next((s for s in socios if s.docu_identi == dni_valido), None)
    if not socio:
        print("  socio no encontrado")
        pausar()
        return
    if socio.estado != "Activo":
        print("  el socio no esta activo")
        pausar()
        return
    print("  tipo de asistencia:")
    print("  1. gimnasio")
    print("  2. actividad")
    print("  3. libre")
    tipo_op = input("  opcion: ").strip()
    tipos = {"1": "gimnasio", "2": "actividad", "3": "libre"}
    if tipo_op not in tipos:
        print("  opcion invalida")
        pausar()
        return
    tipo = tipos[tipo_op]
    fecha = obtener_fecha_actual()
    hora = obtener_hora_actual()
    nuevo = control_asis(
        num_asis=generar_id(rutaasistencia),
        socio_docu=dni_valido,
        Fecha=Fecha_asistencia(fecha.año, fecha.mes, fecha.dia),
        hora_ing=hora,
        hora_egre=None,
        tipo=tipo
    )
    if agregarREG(rutaasistencia, nuevo, asistencia_a_linea):
        print(f"  entrada registrada para {socio.apeynom} a las {hora}")
    else:
        print("  error al registrar")
    pausar()

def asistencia_del_dia():
    mostrar_titulo("asistencia del dia")
    hoy = obtener_fecha_actual()
    asistencias = leerARCH(rutaasistencia, linea_a_asistencia)
    del_dia = [a for a in asistencias if a.Fecha.año == hoy.año and a.Fecha.mes == hoy.mes and a.Fecha.dia == hoy.dia]
    if not del_dia:
        print("  no hay asistencias hoy")
        pausar()
        return
    socios = leerARCH(rutasocios, linea_a_socio)
    contador_gimnasio = 0
    contador_actividad = 0
    contador_libre = 0
    print(f"\n  asistencias del {hoy.dia}/{hoy.mes}/{hoy.año}:")
    for a in del_dia:
        socio = next((s for s in socios if s.docu_identi == a.socio_docu), None)
        nombre = socio.apeynom if socio else "desconocido"
        print(f"  - {nombre} | entrada: {a.hora_ing} | tipo: {a.tipo}")
        if a.tipo == "gimnasio":
            contador_gimnasio += 1
        elif a.tipo == "actividad":
            contador_actividad += 1
        else:
            contador_libre += 1
    total = len(del_dia)
    print(f"\n  resumen:")
    print(f"  gimnasio: {contador_gimnasio}")
    print(f"  actividad: {contador_actividad}")
    print(f"  libre: {contador_libre}")
    print(f"  total: {total}")
    pausar()