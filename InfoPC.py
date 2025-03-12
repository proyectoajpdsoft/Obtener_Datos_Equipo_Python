# Importamos los módulos requeridos
import platform
from datetime import datetime
import psutil
import os

# Información básica del equipo
print("\n---Información básica---")
print("* Arquitectura: {0}".format(platform.architecture()[0]))
print("* Versión {0}, Release: {1}".format(platform.version(), platform.release()))
print("* Sistema: {0}, plataforma: {1}".format(platform.system(), platform.platform()))
print("* Nombre: {0}".format(platform.node()))
# print("* Procesador:",platform.processor())

# De la librería psutil obtenemos la fecha y hora de arranque del equipo
if platform.system() == "Linux":
    fecha_arranque = datetime.fromtimestamp(psutil.boot_time())
    with open("/proc/uptime", "r") as f:
        uptime = f.read().split(" ")[0].strip()
    uptime = int(float(uptime))
    uptime_hours = uptime // 3600
    uptime_minutes = (uptime % 3600) // 60
    print("* Fecha arranque: {0}, horas arrancado: {1}".format(fecha_arranque, str(uptime_hours) + ":" + str(uptime_minutes)))

# Número de procesos en ejecución
if platform.system() == "Linux":
    numProcesos = []
    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            numProcesos.append(subdir)
    print("* Número de procesos: {0}".format(len(numProcesos)))

# Información de CPU
print("\n---CPU---")
print("* Cores físicos: {0}, cores totales {1}".format(psutil.cpu_count(logical=False), psutil.cpu_count(logical=True)))
# Frecuenca CPU en Mhz
frecuenciaCPU = psutil.cpu_freq()
print("* Frecuencia: {0} MHZ".format(frecuenciaCPU.current))

# Modelo de procesador
if platform.system() == "Linux":
    with open("/proc/cpuinfo", "r") as f:
        file_info = f.readlines()
    cpuinfo = [x.strip().split(":")[1] for x in file_info if "model name" in x]
    for index, item in enumerate(cpuinfo):
        print("* Procesador " + str(index) + " : " + item)

# Para convertir bytes en Gigabytes
def bytes_to_GB(bytes):
    gb = bytes/(1024*1024*1024)
    gb = round(gb, 2)
    return gb

# Memoria RAM
virtual_memory = psutil.virtual_memory()
print("\n---RAM total:", bytes_to_GB(virtual_memory.total), "Gb")

# Discos duros
particionesDisco = psutil.disk_partitions()
print("\n---HD---")
# Información de cada partición
for partition in particionesDisco:
    disk_usage = psutil.disk_usage(partition.mountpoint)
    print("* {0}, total espacio: {1}".format(partition.device, bytes_to_GB(disk_usage.total), "GB"))
    # print("* Sistema de ficheros: ", partition.fstype)
    # print("Montaje: ", partition.mountpoint)

# Interfaces de red
interfacesRed = psutil.net_if_addrs()
print("\n---Interfaces de red---")
for interface_name, interface_addresses in interfacesRed.items():
    for address in interface_addresses:
        if interface_name != "lo" and address.address != "":                
                if str(address.family) == 'AddressFamily.AF_INET':
                        print("Interfaz:", interface_name)
                        print("IP:", address.address)
                        # print("* Subred: ", address.netmask)
                        # print("* Broadcast: ", address.broadcast)
                # elif str(address.family) == 'AddressFamily.AF_PACKET':
                        #print("MAC:", address.address)
                        # print("* Subred: ", address.netmask)
                        # print("* Broadcast: ",address.broadcast)