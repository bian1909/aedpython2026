# modulo para gestion de socios, membresias y cuotas

from utils import ( ##traigo todo lo del otro archivo
    mostrar_titulo, pausar,
    validar_dni, validar_email, validar_texto, validar_entero, validar_flotante,
    leerARCH, agregarREG, escribirARCH, buscarREG, generar_id, contarREG,
    socio_a_linea, linea_a_socio,
    cuota_a_linea, linea_a_cuota,
    membresia_a_linea, linea_a_membresia,
    obtener_fecha_actual, corte_de_control, validar_fecha_input
)
from registros import Socio, control_cuot, tipo_membre, Fecha_nac, Fecha_venc, Fecha_pag

# rutas de archivos, aca deberian de aparecer
rutasocios = "datos/socios.txt"
rutacuotas = "datos/cuotas.txt"
rutamembresias = "datos/membresias.txt"

# menus

def menu_socios():
    while True:
        mostrar_titulo("gestion de socios")
        print("  1. alta de socio")
        print("  2. baja de socio")
        print("  3. modificar socio")
        print("  4. buscar socio")
        print("  5. listar socios")
        print("  0. volver")
        opcion = input("\n  opcion: ").strip()#le saco espacios accidentales
        if opcion == "1":
            alta_socio() #opero cada cosa con funciones
        elif opcion == "2":
            baja_socio()
        elif opcion == "3":
            modificar_socio()
        elif opcion == "4":
            buscar_socio()
        elif opcion == "5":
            listar_socios()
        elif opcion == "0":
            break
        else:
            print("  opcion invalida")
            pausar()

def menu_membresias():
    while True:
        mostrar_titulo("gestion de membresias")
        print("  1. alta de membresia")
        print("  2. ver membresias")
        print("  0. volver")
        opcion = input("\n  opcion: ").strip()
        if opcion == "1":
            alta_membresia() #todo lo que sea operacional está en funciones aparte
        elif opcion == "2":
            ver_membresias()
        elif opcion == "0":
            break
        else:
            print("  opcion invalida")
            pausar()

def menu_cuotas():
    while True:
        mostrar_titulo("control de cuotas")
        print("  1. registrar pago")
        print("  2. ver morosos")
        print("  0. volver")
        opcion = input("\n  opcion: ").strip()
        if opcion == "1":
            registrar_pago()
        elif opcion == "2":
            ver_morosos()
        elif opcion == "0":
            break
        else:
            print("  opcion invalida")
            pausar()

# logica de socios

def alta_socio():
    mostrar_titulo("alta de socio")
    dni = input("  dni: ").strip() 
    dni_valido = validar_dni(dni)
    if dni_valido is None: #en base a los criterios del otro archivo 
        print("  dni invalido")
        pausar()
        return
    existentes = buscarREG(rutasocios, linea_a_socio, "docu_identi", dni_valido)
    if existentes:
        print("  ya existe un socio con ese dni")
        pausar()
        return
    nombre = input("  apellido y nombre: ").strip()
    nombre_valido = validar_texto(nombre, 3, 50)
    if nombre_valido is None:
        print("  nombre invalido (3-50 caracteres)")
        pausar()
        return
    telefono = input("  telefono: ").strip()
    email = input("  email: ").strip()
    email_valido = validar_email(email)
    if email_valido is None:
        print("  email invalido")
        pausar()
        return
    print("  fecha de nacimiento (dd/mm/aaaa):")
    año, mes, dia = validar_fecha_input("  fecha: ")
    fecha_nac = Fecha_nac(año, mes, dia)
    nuevo_socio = Socio(
        apeynom=nombre_valido,
        docu_identi=dni_valido,
        num_tele=telefono,
        correo_elec=email_valido,
        Fecha_nac=fecha_nac,
        membresia_act=1,
        estado="Activo"
    )
    if agregarREG(rutasocios, nuevo_socio, socio_a_linea):
        print(f"  socio {nombre_valido} registrado correctamente")
    else:
        print("  error al registrar socio")
    pausar()

def baja_socio():
    mostrar_titulo("baja de socio")
    dni = input("  dni del socio a dar de baja: ").strip()
    dni_valido = validar_dni(dni)
    if dni_valido is None:
        print("  dni invalido")
        pausar()
        return
    socios = leerARCH(rutasocios, linea_a_socio)
    encontrado = None
    for s in socios:
        if s.docu_identi == dni_valido:
            encontrado = s
            break
    if encontrado is None:
        print("  socio no encontrado")
        pausar()
        return
    if encontrado.estado == "Baja":
        print("  el socio ya esta dado de baja")
        pausar()
        return
    encontrado.estado = "Baja"
    encabezado = "docu_identi;apeynom;num_tele;correo_elec;fecha_nac;membresia_act;estado"
    if escribirARCH(rutasocios, socios, encabezado, socio_a_linea):
        print(f"  socio {encontrado.apeynom} dado de baja correctamente")
    else:
        print("  error al actualizar")
    pausar()

def modificar_socio():
    mostrar_titulo("modificar socio")
    dni = input("  dni del socio a modificar: ").strip()
    dni_valido = validar_dni(dni)
    if dni_valido is None:
        print("  dni invalido")
        pausar()
        return
    socios = leerARCH(rutasocios, linea_a_socio)
    encontrado = None
    for s in socios:
        if s.docu_identi == dni_valido:
            encontrado = s
            break
    if encontrado is None:
        print("  socio no encontrado")
        pausar()
        return
    print(f"  datos actuales: {encontrado.apeynom}  tel: {encontrado.num_tele}  email: {encontrado.correo_elec}")
    nuevo_tel = input("  nuevo telefono (enter para mantener): ").strip()
    if nuevo_tel:
        encontrado.num_tele = nuevo_tel
    nuevo_email = input("  nuevo email: ").strip()
    if nuevo_email:
        email_valido = validar_email(nuevo_email)
        if email_valido:
            encontrado.correo_elec = email_valido
        else:
            print("  email invalido, no se modifico")
    encabezado = "docu_identi;apeynom;num_tele;correo_elec;fecha_nac;membresia_act;estado"
    if escribirARCH(rutasocios, socios, encabezado, socio_a_linea):
        print("  socio modificado correctamente")
    else:
        print("  error al actualizar")
    pausar()

# busqueda y listado

def buscar_socio():
    mostrar_titulo("buscar socio")
    dni = input("  dni a buscar: ").strip()
    dni_valido = validar_dni(dni)
    if dni_valido is None:
        print("  dni invalido")
        pausar()
        return
    resultados = buscarREG(rutasocios, linea_a_socio, "docu_identi", dni_valido)
    if not resultados:
        print("  socio no encontrado")
    else:
        s = resultados[0]
        print(f"\n  dni: {s.docu_identi}")
        print(f"  nombre: {s.apeynom}")
        print(f"  telefono: {s.num_tele}")
        print(f"  email: {s.correo_elec}")
        if s.Fecha_nac:
            print(f"  f. nacimiento: {s.Fecha_nac.dia}/{s.Fecha_nac.mes}/{s.Fecha_nac.año}")
        print(f"  membresia: {s.membresia_act}")
        print(f"  estado: {s.estado}")
    pausar()

def listar_socios():
    mostrar_titulo("listado de socios")
    socios = leerARCH(rutasocios, linea_a_socio)
    if not socios:
        print("  no hay socios registrados")
        pausar()
        return
    contador = 0
    for s in socios:
        print(f"  dni: {s.docu_identi}  nombre: {s.apeynom}  estado: {s.estado}")
        contador += 1 #incremento
    print(f"\n  total de socios: {contador}")
    pausar()

def listar_socios_tabla():
    mostrar_titulo("listado de socios (tabla)")
    socios = leerARCH(rutasocios, linea_a_socio)
    if not socios:
        print("  no hay socios registrados")
        pausar()
        return
    print(f"  {'dni':<12} {'nombre':<25} {'telefono':<15} {'estado':<10}")
    print("  " + "-" * 62)
    contador = 0
    for s in socios:
        print(f"  {s.docu_identi:<12} {s.apeynom:<25} {s.num_tele:<15} {s.estado:<10}") ##el:<num es para darle formato y alinearlo a la izquierda
        contador += 1
    print("  " + "-" * 62)
    print(f"  total: {contador} socios")
    pausar()

# membresias

def alta_membresia():
    mostrar_titulo("alta de membresia")
    descripcion = input("  descripcion: ").strip()
    desc_valida = validar_texto(descripcion, 3, 50)
    if desc_valida is None:
        print("  descripcion invalida")
        pausar()
        return
    duracion = input("  duracion en dias: ").strip()
    duracion_valida = validar_entero(duracion, 1, 365)
    if duracion_valida is None:
        print("  duracion invalida (1-365 dias)")
        pausar()
        return
    precio = input("  precio mensual: ").strip()
    precio_valido = validar_flotante(precio, 0)
    if precio_valido is None:
        print("  precio invalido")
        pausar()
        return
    descuento = input("  descuento % (0 si no tiene): ").strip()
    descuento_valido = validar_entero(descuento, 0, 100)
    if descuento_valido is None:
        print("  descuento invalido (0-100)")
        pausar()
        return
    cod = generar_id(rutamembresias)
    nueva = tipo_membre(
        cod_tip=cod,
        descrip=desc_valida,
        dura_dias=duracion_valida,
        monto=precio_valido,
        descuen=descuento_valido,
        estado=1
    )
    if agregarREG(rutamembresias, nueva, membresia_a_linea):
        print(f"  membresia {desc_valida} creada con codigo {cod}")
    else:
        print("  error al crear membresia")
    pausar()

def ver_membresias():
    mostrar_titulo("membresias disponibles")
    membresias = leerARCH(rutamembresias, linea_a_membresia)
    if not membresias:
        print("  no hay membresias registradas")
        pausar()
        return
    print(f"  {'cod':<6} {'descripcion':<25} {'dias':<8} {'precio':<12} {'desc%':<8} {'estado':<8}")
    print("  " + "-" * 67)
    contador = 0
    for m in membresias:
        estado_str = "activa" if m.estado == 1 else "inactiva"
        print(f"  {m.cod_tip:<6} {m.descrip:<25} {m.dura_dias:<8} ${m.monto:<11.2f} {m.descuen:<8} {estado_str:<8}")
        if m.estado == 1:
            contador += 1
    print("  " + "-" * 67)
    print(f"  total de membresias activas: {contador}")
    pausar()

# cuotas

def registrar_pago():
    mostrar_titulo("registrar pago de cuota")
    dni = input("  dni del socio: ").strip()
    dni_valido = validar_dni(dni)
    if dni_valido is None:
        print("  dni invalido")
        pausar()
        return
    socios = buscarREG(rutasocios, linea_a_socio, "docu_identi", dni_valido)
    if not socios:
        print("  socio no encontrado")
        pausar()
        return
    socio = socios[0]
    cuotas = leerARCH(rutacuotas, linea_a_cuota)
    pendientes = [c for c in cuotas if c.socio_docu == dni_valido and c.estado in ("Impagada", "Vencida")]
    if not pendientes:
        print("  el socio no tiene cuotas pendientes")
        pausar()
        return
    print(f"\n  cuotas pendientes de {socio.apeynom}:")
    for i, c in enumerate(pendientes, 1):
        print(f"  {i}. cuota #{c.num_cuot} - venc: {c.Fecha_venc.dia}/{c.Fecha_venc.mes}/{c.Fecha_venc.año} - ${c.monto:.2f}")
    total_cobrado = 0.0
    opcion = input("\n  pagar todas (t) o elegir numero (1,2...): ").strip().lower()
    if opcion == "t":
        for c in pendientes:
            c.estado = "Pagada"
            c.Fecha_pag = obtener_fecha_actual()
            total_cobrado += c.monto
    else:
        try:
            num = int(opcion)
            if 1 <= num <= len(pendientes):
                cuota = pendientes[num - 1]
                cuota.estado = "Pagada"
                cuota.Fecha_pag = obtener_fecha_actual()
                total_cobrado = cuota.monto
            else:
                print("  numero invalido")
                pausar()
                return
        except ValueError:
            print("  opcion invalida")
            pausar()
            return
    if escribirARCH(rutacuotas, cuotas, "num_cuot;socio_docu;fecha_venc;monto;estado;fecha_pag", cuota_a_linea):
        print(f"\n  pago registrado. total cobrado: ${total_cobrado:.2f}")
    else:
        print("  error al registrar pago")
    pausar()

def ver_morosos():
    mostrar_titulo("morosos por tipo de membresia")
    cuotas = leerARCH(rutacuotas, linea_a_cuota)
    morosas = [c for c in cuotas if c.estado in ("Impagada", "Vencida")]
    if not morosas:
        print("  no hay cuotas morosas")
        pausar()
        return
    socios = leerARCH(rutasocios, linea_a_socio)
    grupos = {}
    for c in morosas:
        socio = None
        for s in socios:
            if s.docu_identi == c.socio_docu:
                socio = s
                break
        if socio:
            memb = socio.membresia_act
            if memb not in grupos:
                grupos[memb] = []
            grupos[memb].append((socio, c))
    total_general = 0.0
    contador_general = 0
    for memb_id in sorted(grupos.keys()):
        lista = grupos[memb_id]
        print(f"\n  membresia tipo {memb_id}:")
        print("  " + "-" * 50)
        subtotal = 0.0
        for socio, cuota in lista:
            print(f"  - {socio.apeynom} (dni: {socio.docu_identi}) - ${cuota.monto:.2f}")
            subtotal += cuota.monto
            contador_general += 1
        print(f"  subtotal: ${subtotal:.2f} ({len(lista)} morosos)")
        total_general += subtotal
    print("\n" + "=" * 50)
    print(f"  total morosos: {contador_general}")
    print(f"  total adeudado: ${total_general:.2f}")
    pausar()