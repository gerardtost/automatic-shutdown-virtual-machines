[Read this in **English**](README.md) · [Lea esto en **castellano**](README.es.md)

# Apagada automàtica de màquines virtuals KVM
## Facilita el tancament ordenat de màquines gestionades amb la llibreria libvirt.

Aquest senzill programa en Python 3 permet fer una apagada automàtica de totes les màquines virtuals que hi hagi en un sistema amfitrió. Funcionarà amb tots els sistemes Linux que utilitzin KVM, amb la llibreria de virtualització ```libvirt```.

Després de tenir diverses complicacions per a treballar amb ```libvirt-python```, vaig decidir escriure'm una aplicació que tanqués les màquines virtuals i l'amfitrió. Ens evita la necessitat d'instal·lar el mòdul libvirt-python i ens allibera d'anar apagant les màquines virtuals una per una.

Es pot automatitzar l'apagada programant-la amb Cron o Systemd (Linux). El programa esperarà una estona predeterminada després d'enviar l'ordre d'apagat a cada màquina, i repetirà els intents les vegades que vulguem. Finalment, també pot apagar el sistema amfitrió (host).

Opcions configurables:

- Nombre de cicles d'intent d'apagada, abans de forçar-ho.
- Temps d'espera per tal que s'apagui cada màquina.
- Apagar la màquina amfitriona quan s'hagin apagat les màquines virtuals.
- Escriure un registre d'activitat (log).

Requisits:

- Sistema operatiu GNU/Linux.
- Python 3 instal·lat amb els mòduls ```psutil``` i ```regex```. Provat amb Python 3.8.3 i QEMU 2.12.0 en CentOS 8 i QEMU 1.5.3 en CentOS 7.

Instruccions:

- Descarregueu aquests fitxers al vostre host clonant el projecte git o com a zip comprimit.
- Obriu el fitxer ```vmshutdown.py``` amb qualsevol editor de text pla, i modifiqueu-le aquestes variables que hi ha a l'apartat ```Configuration```: 

    - ```waiting_minutes```: Temps en minuts per a apagar cada màquina. Predeterminat ```5``` minuts.
    - ```max_graceful_times```: Quantes vegades es farà un cicle complet d'intents d'apagat abans de fer una apagada forçada. Predeterminat ```3``` vegades.
    - ```shutdown_option```: Si voleu apagar el host amfitrió poseu ```True```. Predeterminat a ```False```.
    - Si voleu registrar les accions al log, poseu a ```True``` la variable ```log_active```. Després haureu de configurar la ruta ```log_path``` i el nom del fitxer de log ```log_name```.

- Executeu el fitxer ```vmshutdown.py``` cridant l'intèrpret Python (```python3 vmshutdown.py```). També podeu donar-li permisos en línia de comandes per tal que s'executi sense cridar l'intèrpret: ```chmod +x vmshutdown.py```. El fitxer s'ha d'executar com a un usuari amb permís per a gestionar màquines virtuals amb la comanda ```virsh```.

