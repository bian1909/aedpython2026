# funciones y manejo de archivos

import os #trae recursos del sistema
from datetime import datetime #para fechas

# importa registros de registros.py, no necesita una vinculación mas explicita al estar en la misma carpeta
from registros import (
    Fecha, Fecha_nac, Socio,
    Fecha_venc, Fecha_pag, control_cuot,
    horario, actividad,
    Fecha_inscrip, inscripcion,
    fecha_ini, fecha_fin, membre_socio, tipo_membre,
    Fecha_asistencia, control_asis
)

carpetadatos = "datos" # nombre de carpeta para los .txt

# Encabezados de archivos TXT
encabezados = {
    "socios.txt": "docu_identi;apeynom;num_tele;correo_elec;fecha_nac;membresia_act;estado",
    "cuotas.txt": "num_cuot;socio_docu;fecha_venc;monto;estado;fecha_pag",
    "actividades.txt": "cod_activ;nomb;descrip;hora_ini;hora_fin;dia_semana;cupo_actu;estado",
    "inscripciones.txt": "numb_inscrip;socio_docu;cod_activ;fecha_inscrip;estado",
    "membresias.txt": "cod_tip;descrip;dura_dias;monto;descuen;estado",
    "asistencia.txt" : "num_asis;socio_docu;fecha;hora_ing;hora_egre;tipo",
}


def pausar():
    # pausa hasta que el usuario presione Enter
    input("\npresione enter para continuar")

def mostrar_titulo(titulo):
    # muestra un título formateado en mayusculas
    print(f"  {titulo}")

# VALIDACIONES

def validar_dni(dni):
    # valida dni de 8 digitos
    if not dni:
        return None #se fija si el campo completado esta vacio, si lo esta no valida nada porque no hay nada que validar en si
    dni_limpio = str(dni).replace(".", "").replace("-", "").strip() #guarda en otra variable el numero ya como string, le saca los puntos y guiones que ponga el usuario, y los espacios innecesarios
    if dni_limpio.isdigit() and len(dni_limpio) == 8: #isdigit = son TODOS los caracteres dígitos numericos (0-9)? len viene de lenght y verifica que la longitud sea de 8
        return int(dni_limpio) #obtenemos el dni ya bien como numero
    return None #si fallo algo, ya no valida

def validar_email(email):
    if not email:
        return None #si no hay email, no hay nada para validar
    email = email.strip().lower() #saca espacios en blanco innecesarios y hace todo minusculas
    # criterio de validacion: debe tener @ y un punto después del @
    if "@" in email and "." in email.split("@")[1]: # se fija si el string tiene un arroba y con el slit y el 1 se fujan si despues de el arroba hay un punto, ej etc@servicio.com, se fija en el . despues de servicio pero porque servicio y el punto estan despues de @, eso seria valido
        return email #retorna el email valido
    return None #si falla algo, no devuelve nada

def validar_fecha_input(fechaa):
    #solicita fecha y retorna (dia, mes, año)
    while True:
        fecha_str = input(fechaa).strip() #se le sacan los espacios, la fecha debe ser tipo 11/6/2009, con barras, se guarda como caracter
        try:
            dia, mes, año = map(int, fecha_str.split('/')) #como es todo caracter, usa las barras como separadores de subsecuencias, que serian nuestros tres datos, los cuales map los hace una lista de enteros, y el dia,mes,año hace que queden asignados en orden
            if 1 <= dia <= 31 and 1 <= mes <= 12 and 1900 <= año <= 2100: #criterios de congruencia
                return año, mes, dia #si todo está en orden, sale del bucle
            print("fecha invalida.") #si alguna condición falló, vuelve a pedir
        except ValueError:
            print("Use formato (dia/ mes/ año)")

def validar_entero(valor, minimo=None, maximo=None):
    #Valida entero en rango. Retorna int o None, nos sirve para diversos campos ejm edad
    try:
        numero = int(valor) #se le pasa un valor entero
        if minimo is not None and numero < minimo:
            return None
        if maximo is not None and numero > maximo:
            return None
        return numero # si pasa ambos criterios, es un numero valido
    except (ValueError, TypeError):
        return None

def validar_flotante(valor, minimo=None):
    try:
        numero = float(str(valor).replace(",", ".")) #arregla el formato de los numeros con decimales, tambien como string primero 
        if minimo is not None and numero < minimo:
            return None #por si un numero está fuera de rango y no me sirve
        return numero #si no si
    except (ValueError, TypeError):
        return None  #por si fallo el valor o su forma de ingreso

def validar_texto(texto, minimo=1, maximo=None):
    if not texto:
        return None #si no hay nada escrito
    texto = str(texto).strip() #por si hay espacios innecesarios
    if minimo <= len(texto) <= maximo:
        return texto
    return None


def socio_a_linea(socio): #convierte el objeto socio en una línea de texto separada por un ; para poder guardarla en un txt
    fecha_nac = "" #string vacio
    if socio.Fecha_nac:
        fecha_nac = f"{socio.Fecha_nac.año}-{socio.Fecha_nac.mes:02d}-{socio.Fecha_nac.dia:02d}" #se verifica si el socio ya venia con fecha de nacimiento, 02d es para la cantidad de digitos
    return f"{socio.docu_identi};{socio.apeynom};{socio.num_tele};{socio.correo_elec};{fecha_nac};{socio.membresia_act};{socio.estado}" #construye el string

def linea_a_socio(linea): #transforma lo que esté en el txt de socios para que el programa lo pueda utilizar, conersion de secuencia
    try:
        campos = linea.strip().split(';') #siend que todo está separado por ;'s
        if len(campos) != 7: #socio tiene 7 campos, se fija que cumpla esa cantidad preguntando si es distinto de (!=) 7
            return None
        
        fecha_nac = None #si no tiene fecha de nacimiento
        if campos[4] and campos[4] != "None": #refiere a que es el quinto campo, siendo que se cuenta desde el cero, verifica que sean campos en si y no texto literal
            año, mes, dia = map(int, campos[4].split('-')) #conversion a entero del contenido
            fecha_nac = Fecha_nac(año, mes, dia) #lo guarda
        
        return Socio( #le atribuye a cada elemento de la secuencia del txt su campo en socio
            apeynom=campos[1],
            docu_identi=int(campos[0]),
            num_tele=campos[2],
            correo_elec=campos[3],
            Fecha_nac=fecha_nac,
            membresia_act=int(campos[5]),
            estado=campos[6]
        )
    except:
        return None

def cuota_a_linea(cuota): #para pasar al txt de cuotas
    fecha_venc = f"{cuota.Fecha_venc.año}-{cuota.Fecha_venc.mes:02d}-{cuota.Fecha_venc.dia:02d}" #le da formato al subreg
    fecha_pag = "" #por fecha de pago si todavia no se pagó
    if cuota.Fecha_pag:
        fecha_pag = f"{cuota.Fecha_pag.año}-{cuota.Fecha_pag.mes:02d}-{cuota.Fecha_pag.dia:02d}" #le da el mismo formato
    return f"{cuota.num_cuot};{cuota.socio_docu};{fecha_venc};{cuota.monto};{cuota.estado};{fecha_pag}" #devolución de los campos

def linea_a_cuota(linea): #tranformacion de txt a datos funcionales, lo mismo que el otro
    try:
        campos = linea.strip().split(';')
        if len(campos) != 6: #checkea cant de campos
            return None
        
        año_v, mes_v, dia_v = map(int, campos[2].split('-')) #separa los datos y los vuelve enteros
        fecha_venc = Fecha_venc(año_v, mes_v, dia_v) #forma el subreg
        
        fecha_pag = None
        if campos[5] and campos[5] != "None": 
            año_p, mes_p, dia_p = map(int, campos[5].split('-'))
            fecha_pag = Fecha_pag(año_p, mes_p, dia_p) #en caso de que todos los campos esten completados, se completa la fecha de pago
        
        return control_cuot( #completa el registro con sus contenidos
            num_cuot=int(campos[0]),
            socio_docu=int(campos[1]),
            Fecha_venc=fecha_venc,
            monto=float(campos[3]),
            estado=campos[4],
            Fecha_pag=fecha_pag
        )
    except:
        return None

def actividad_a_linea(act):
    return f"{act.cod_activ};{act.nomb};{act.descrip};{act.horario.hora_ini};{act.horario.hora_fin};{act.horario.dia_semana};{act.cupo_actu};{act.estado}"
#lo mismo que los otros, este es para pasar a txt y el otro de txt a datos utiles
def linea_a_actividad(linea):
    try:
        campos = linea.strip().split(';')
        if len(campos) != 8:
            return None
        
        hor = horario(hora_ini=campos[3], hora_fin=campos[4], dia_semana=campos[5])
        
        return actividad(
            cod_activ=int(campos[0]),
            nomb=campos[1],
            descrip=campos[2],
            horario=hor,
            cupo_actu=int(campos[6]),
            estado=campos[7]
        )
    except:
        return None

def inscripcion_a_linea(insc):
    fecha = f"{insc.Fecha_inscrip.año}-{insc.Fecha_inscrip.mes:02d}-{insc.Fecha_inscrip.dia:02d}"
    return f"{insc.numb_inscrip};{insc.socio_docu};{insc.cod_activ};{fecha};{insc.estado}"

def linea_a_inscripcion(linea):
    try:
        campos = linea.strip().split(';')
        if len(campos) != 5:
            return None
        
        año, mes, dia = map(int, campos[3].split('-'))
        fecha_insc = Fecha_inscrip(año, mes, dia)
        
        return inscripcion(
            numb_inscrip=int(campos[0]),
            socio_docu=int(campos[1]),
            cod_activ=int(campos[2]),
            Fecha_inscrip=fecha_insc,
            estado=campos[4]
        )
    except:
        return None

def membresia_a_linea(memb):
    return f"{memb.cod_tip};{memb.descrip};{memb.dura_dias};{memb.monto};{memb.descuen};{memb.estado}"

def linea_a_membresia(linea):
    try:
        campos = linea.strip().split(';')
        if len(campos) != 6:
            return None
        
        return tipo_membre(
            cod_tip=int(campos[0]),
            descrip=campos[1],
            dura_dias=int(campos[2]),
            monto=float(campos[3]),
            descuen=int(campos[4]),
            estado=int(campos[5])
        )
    except:
        return None

def asistencia_a_linea(asis):
    fecha = f"{asis.Fecha.año}-{asis.Fecha.mes:02d}-{asis.Fecha.dia:02d}"
    egre = asis.hora_egre if asis.hora_egre else ""
    return f"{asis.num_asis};{asis.socio_docu};{fecha};{asis.hora_ing};{egre};{asis.tipo}"

def linea_a_asistencia(linea):
    try:
        campos = linea.strip().split(';')
        if len(campos) != 6:
            return None
        año, mes, dia = map(int, campos[2].split('-'))
        fecha = Fecha_asistencia(año, mes, dia)
        return control_asis(
            num_asis=int(campos[0]),
            socio_docu=int(campos[1]),
            Fecha=fecha,
            hora_ing=campos[3],
            hora_egre=campos[4] if campos[4] else None,
            tipo=campos[5]
        )
    except:
        return None
    
# MANEJO DE ARCHIVOS
#es "crear" lo que usamos nosotros en la catedra con archivos

def crearARCH(ruta, encabezado): 
    #crea archivo txt con encabezado (o sea una fila invisible que reconoce los campos) si no existe
    if not os.path.exists(ruta): #pregunta si no existe ya un archivo en donde se esté ejecutando el programa, si hay no hace nada
        with open(ruta, 'w', encoding='utf-8') as f: #accede a la ruta del archivo en modo escritura (w), la f funciona como un cerrar arch para cuando se cierre automaticamente. lo de utf8 es para que la ñ y tildes no se corrompan
            f.write(encabezado + "\n") #escribe los nombres de los campos y agrega un salto de linea
        return True #si lo tuvo que crear
    return False #si ya existia

def leerARCH(ruta, funcion_conversion): #permite leer el archivo completo desde el disco, saltarse la primera línea (porque es el encabezado, no datos reales) y transformar cada línea de texto en un objeto registro para poder usarlo 
    if not os.path.exists(ruta): #si el archivo no existe, devuelve una lista vacía
        return []
    
    registros = [] #lista vacia, para leer
    try:
        with open(ruta, 'r', encoding='utf-8') as f: #abro la ruta del archivo existente en modo lectura (r), utf8 para lo ya mencionado
            for linea in f.readlines()[1:]:  # lee todas las líneas del archivo y las mete en la lista, el [1] es para ignorar los encabezados
                linea = linea.strip() #elimina el salto de línea (\n) y los espacios en blanco que estén al principio o al final del texto
                if linea:
                    registro = funcion_conversion(linea) #obtiene los datos con la funcion previa (linea_a_socio)
                    if registro:
                        registros.append(registro) #se agrega el socio a la lista
    except Exception as e:
        print(f"Error al leer {ruta}: {e}") #avisa el error
    
    return registros #devuelve la lista de objetos para ser procesada

def escribirARCH(ruta, registros, encabezado, funcion_conversion): #trae la ubicación del archivo, el registro correspondiente, sus campos y la funcion a utilizar
    try:
        with open(ruta, 'w', encoding='utf-8') as f: #abre el archivo en modo de escritura (w)
            f.write(encabezado + "\n")
            for reg in registros:
                f.write(funcion_conversion(reg) + "\n") #Llama a funcion_conversion(reg) (por ejemplo, socio_a_linea) para convertir el objeto a texto, escribe esa linea en el archivo y da un salto
        return True
    except Exception as e:
        print(f"Error al escribir {ruta}: {e}") #muestra el error si hubo
        return False

def agregarREG(ruta, registro, funcion_conversion):
    #agrega un registro al final del archivo
    try:
        with open(ruta, 'a', encoding='utf-8') as f: #a seria agregar/append, se posiciona al final de todos los reg
            f.write(funcion_conversion(registro) + "\n") #incorpora la info
        return True
    except Exception as e:
        print(f"Error al agregar registro: {e}")
        return False

def buscarREG(ruta, funcion_conversion, campo, valor):
    #busca registros por campo
    registros = leerARCH(ruta, funcion_conversion)
    return [reg for reg in registros if getattr(reg, campo, None) == valor]

def contarREG(ruta):
    #cuenta registros en el archivo
    if not os.path.exists(ruta):
        return 0
    with open(ruta, 'r', encoding='utf-8') as f:
        return len(f.readlines()) - 1  # resta encabezado

# utilidades

def generar_id(ruta):
    #id autoincremental
    return contarREG(ruta) + 1

def obtener_fecha_actual():
    #retorna fecha actual como objeto Fecha
    ahora = datetime.now()
    return Fecha(ahora.year, ahora.month, ahora.day)

def obtener_hora_actual():
    #Retorna hora actual hh:mm
    return datetime.now().strftime("%H:%M")

def inicializar_sistema():
    #inicializa el sistema creando carpeta y archivos
    print("  SISTEMA DE GESTION DE GIMNASIO")
    
    if not os.path.exists(carpetadatos):
        os.makedirs(carpetadatos)
        print(f" Carpeta creada: {carpetadatos}/")
    
    archivos_creados = 0
    for archivo, encabezado in encabezados.items():
        ruta = os.path.join(carpetadatos, archivo)
        if crearARCH(ruta, encabezado):
            archivos_creados += 1
    
    if archivos_creados > 0:
        print(f"{archivos_creados} archivo(s) creado(s)")
    
    return True

def corte_de_control(registros, campo_agrupacion):
    #agrupa registros por campo para reportes
    grupos = {}
    for registro in registros:
        clave = getattr(registro, campo_agrupacion, "SIN_CLASE")
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(registro)
    return grupos