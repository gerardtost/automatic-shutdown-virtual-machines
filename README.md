[Lea esto en **castellano**](README.es.md) · [Llegiu això en **català**](README.ca.md)

# Automatic shutdown of KVM virtual machines
## Facilitates the orderly shutdown of machines managed with the libvirt library.

This simple Python 3 program allows you to do an automatic shutdown of all virtual machines on a host system. It will work with all Linux systems that use KVM, with the ```libvirt``` virtualization library.

After having several complications working with ```libvirt-python```, I decided to write an application that would shut down the virtual machines and the host. It avoids the need to install the libvirt-python module and frees us from shutting down the virtual machines one by one.

Closing can be automated by programming it with Cron or systemd (Linux). The program will wait a predetermined time after sending the shutdown order to each machine, and will repeat the attempts as many times as we want. Finally, you can also shut down the host system.

Configurable options:

- Number of attempted shutdown cycles, before forcing it.
- Time to wait for each machine to turn off.
- Shut down the host machine when the virtual machines have been shut down.
- Write an activity log.


Requirements:

- GNU/Linux operating system with systemd (does not work with the classic SysV Init).
- Python 3 installed with ```psutil``` and ```regex``` modules. Tested with Python 3.8.3 and QEMU 2.12.0 on CentOS 8 and QEMU 1.5.3 on CentOS 7.

Instructions:

- Download these files to your host by cloning the git project or as a compressed zip.
- Open the file ```vmshutdown.py``` with any plain text editor, and modify the following variables in the ```Configuration``` section:

    - ```waiting_minutes```: Time in minutes to shut down each machine. Default ```5``` minutes.
    - ```max_graceful_times```: How many times will a full cycle of shutdown attempts be made before a forced shutdown. Default ```3``` times.
    - ```shutdown_option```: If you want to shutdown the host set ```True```. Default is ```False```.
    - If you want to log actions, set the ```log_active``` variable to ```True```. Then you will have to configure the ```log_path``` and the log file name ```log_name```.

- Run the ```vmshutdown.py``` file by calling the Python interpreter (```python3 vmshutdown.py```). You can also give it command line permissions to run without calling the interpreter: ```chmod + x vmshutdown.py```. The file must be run as a user with permission to manage virtual machines with the ```virsh``` command. 

