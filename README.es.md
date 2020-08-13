[Read this in **English**](README.md) · [Llegiu això en **català**](README.ca.md)

# Apagado automático de máquinas virtuales KVM
## Facilita el cierre ordenado de máquinas gestionadas con la librería libvirt.

Este sencillo programa en Python 3 permite hacer una apagado automático de todas las máquinas virtuales que haya en un sistema anfitrión. Funcionará con todos los sistemas Linux que utilicen KVM, con la librería de virtualización ```libvirt```.

Después de tener varias complicaciones para trabajar con ```libvirt-python```, decidí escribirme una aplicación que cerrase las máquinas virtuales y el anfitrión. Nos evita la necesidad de instalar el módulo libvirt-python y nos libera de ir apagando las máquinas virtuales una por una.

Se puede automatizar el cierren programándolo con Cron o systemd (Linux). El programa esperará un rato predeterminado después de enviar la orden de apagado a cada máquina, y repetirá los intentos las veces que queramos. Finalmente, también puede apagar el sistema anfitrión (host).

Opciones configurables:

- Número de ciclos de intento de apagado, antes de forzarlo.
- Tiempo de espera para que se apague cada máquina.
- Apagar la máquina anfitriona cuando se hayan apagado las máquinas virtuales.
- Escribir un registro de actividad (log).

Requisitos:

- Sistema operativo GNU/Linux con systemd (no funciona con el clásico SysV Init).
- Python 3 instalado con los módulos ```psutil``` y ```regex```. Probado con Python 3.8.

Instrucciones:

- Descargue estos archivos a su host clonando el proyecto git o como zip comprimido.
- Abra el archivo vmshutdown.py con cualquier editor de texto plano, y modifíquele estas variables que hay en el apartado ```Configuration```:

    - ```waiting_minutes```: Tiempo en minutos para apagar cada máquina. Predeterminado ```5``` minutos.
    - ```max_graceful_times```: Cuántas veces se hará un ciclo completo de intentos de apagado antes de hacer un cierre forzado. Predeterminado ```3``` veces.
    - ```shutdown_option```: Si desea apagar el host anfitrión ponga ```True```. Predeterminado a ```False```.
    - Si desea registrar las acciones en el log, establezca a ```True``` la variable ```log_active```. Después tendrá que configurar la ruta ```log_path``` y el nombre del fichero de log ```log_name```.

- Ejecute el archivo ```vmshutdown.py``` llamando al intérprete Python (```python3 vmshutdown.py```). También puede darle permisos en línea de comandos para que se ejecute sin llamar al intérprete: ```chmod + x vmshutdown.py```. El archivo se debe ejecutar como un usuario con permiso para gestionar máquinas virtuales con el comando ```virsh```.
