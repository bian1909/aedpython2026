# primer archivo, aca vamos a definir los registros y campos con los que vamos a trabajar

from dataclasses import dataclass, field, asdict # trabajaremos con clases de datos, field nos permite personalizar los atributos individualmente, asdict nos sirve para transformar tambien en un diccionario, otra forma de representar registros, para facilitar su uso
from typing import Literal #para verificacion de datos especificos x = Literal["op1", "op2"], admite valores por lista
from datetime import date # para poder trabajar con las fechas automatixadas del sistema 

#subregistros

@dataclass
class Fecha:
    # sub-registro para fechas (año, mes, día)
    año: int
    mes: int
    dia: int
    
    def __str__(self):
        return f"{self.dia:02d}/{self.mes:02d}/{self.año}" #muestra fecha por consola con print
    
    def to_iso(self):
        # convierte a formato año-mes-dia para archivos
        return f"{self.año:04d}-{self.mes:02d}-{self.dia:02d}"
    
    @classmethod
    def from_iso(cls, fecha_str):
        # crea Fecha desde formato año-mes-dia.
        if not fecha_str or fecha_str == "None":
            return None
        año, mes, dia = map(int, fecha_str.split('-'))
        return cls(año, mes, dia)

#subreg de socio

@dataclass
class Fecha_nac:
    año: int
    mes: int
    dia: int
    
#reg socio

@dataclass
class Socio:
    apeynom: str
    docu_identi: int
    num_tele: str
    correo_elec: str
    Fecha_nac: Fecha_nac = None
    membresia_act: int = 1
    estado: Literal["Activo", "Inactivo", "Baja"] = "Activo" #dafault
    
#subreg control de cuotas
@dataclass
class Fecha_venc:
    año: int
    mes: int
    dia: int

@dataclass
class Fecha_pag:
    año: int
    mes: int
    dia: int
    
#reg control de cuotas
@dataclass
class control_cuot:
    num_cuot: int
    socio_docu: int
    Fecha_venc: Fecha_venc
    monto: float
    estado: Literal["Pagada", "Impagada", "Vencida"] = "Impagada" #estado default
    Fecha_pag: Fecha_pag = None
    
    
#subregistros de actividad
@dataclass
class horario:
    hora_ini: str  # formato hora:minutos
    hora_fin: str  # mismo formato
    dia_semana: str  # "Lunes", "Martes", etc.

#reg actividad
@dataclass
class actividad:
    cod_activ: int
    nomb: str
    descrip: str
    horario: horario
    cupo_actu: int = 0
    estado: Literal["Activa", "Inactiva"] = "Activa" #default
    
#subreg inscripcion
@dataclass
class Fecha_inscrip:
    año: int
    mes: int
    dia: int


 #reg inscripcion
@dataclass
class inscripcion:
    numb_inscrip: int
    socio_docu: int
    cod_activ: int
    Fecha_inscrip: Fecha_inscrip
    estado: Literal["Baja", "Activa", "Pendiente"] = "Activa" #default

#subreg membrexia
@dataclass
class fecha_ini:
    año: int
    mes: int
    dia: int

@dataclass
class fecha_fin:
    año: int
    mes: int
    dia: int

@dataclass
class membre_socio:
    num_membre: int
    socio_docu: int
    cod_tipo: int
    fecha_ini: fecha_ini
    fecha_fin: fecha_fin

#membresia
@dataclass
class tipo_membre:
    cod_tip: int
    descrip: str
    dura_dias: int
    monto: float
    descuen: int = 0  # porcentaje de descuento
    estado: int = 1  # 1=activo, 0=inactivo



