#!/usr/bin/env python3
# -*- coding: utf-8  -*-

#
# Easy KVM VMs shutdown
#
# GNU General Public License (GPL) 3.0
#
# Gerard Tost (recull@digipime.com)
# https://github.com/gerardtost/
#

import os
import sys
import time
import datetime
import subprocess

import psutil
import regex as re


# Configuration section

waiting_minutes = 5
max_graceful_times = 3
shutdown_option = True
log_active = False
log_name = "vmshutdown.log"
log_path = "/home/base"


# Please do not edit anything below this line.

attempt = 0
process_dict = {}
list_of_process_names = []
list_of_virtual_machines = []
waiting = int(waiting_minutes * 60)
dir_log = "{}/{}".format(log_path, log_name)


try:
    subprocess.run(["command", "-v", "virsh"], shell=True,
                   check=True, capture_output=True)
except subprocess.CalledProcessError:
    print("libvirt has not been installed: exiting")
    sys.exit(1)

if log_active:
    if not log_name:
        print("Please, verify set your log file name or disable log in the config section.")
        sys.exit(1)
    elif not os.path.exists(log_path):
        print(
            "Wrong path: Please, verify your log path or disable log in the config section.")
        sys.exit(1)


def write_log(line):
    """Simple log """
    with open(dir_log, "a") as log:
        log.write("{} {}{}".format(datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), line, "\n"))


def get_machines():
    """This function gets a list of processes and detects 
       the libvirt virtual machines that are running now.

    """
    for proc in psutil.process_iter():
        process_dict = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
        list_of_process_names.append(process_dict)

    count = 0
    for proc_select in list_of_process_names:
        if proc_select["name"] == "qemu-kvm":

            vm_name = ""
            index_label = proc_select["cmdline"].index("-name")
            isolate = re.search(r"guest=([a-z0-9A-Z_-]+),",
                                proc_select["cmdline"][index_label+1])

            if isolate:
                vm_name = isolate[1]
            else:
                vm_name = proc_select["cmdline"][index_label+1]

            list_of_virtual_machines.append({"pid":
                                             proc_select["pid"], "name": vm_name})
            count += 1

            print("Virtual machine {}: {}".format(count, vm_name))
            if log_active:
                write_log("Virtual machine {}: {}".format(count, vm_name))

    print("Total virtual machines running: {}\n".format(count))
    if log_active:
        write_log("Total virtual machines running: {}".format(count))

    list_of_process_names.clear()
    return count


def shutdown_graceful(machine_dict):
    """Graceful shut down individual machine """
    verify = subprocess.run(["virsh", "shutdown", "{}".format(
        machine_dict["name"])], capture_output=True)
    if "error:" in str(verify.stderr):
        print("Error in trying shut down virtual machine {}. Please, verify the user permissions".format(
            machine_dict["name"]))
        if log_active:
            write_log("Error in trying shut down virtual machine {}. Please, verify the user permissions".format(
                machine_dict["name"]))
        return None

    print("Shut down machine {}".format(machine_dict['name']))
    print("Waiting {} minutes\n".format(waiting_minutes))
    if log_active:
        write_log("Shut down machine {}. Waiting {} minutes".format(
            machine_dict["name"], waiting_minutes))

    time.sleep(waiting)
    return True


def shutdown_forced(machine_dict):
    """Forced shut down individual machine """
    verify = subprocess.run(["virsh", "destroy", "{}".format(
        machine_dict["name"])], capture_output=True)
    if "error:" in str(verify.stderr):
        print("Error in trying forced shut down virtual machine {}. Please, verify the user permissions".format(
            machine_dict["name"]))
        if log_active:
            write_log("Error in trying forced shut down virtual machine {}. Please, verify the user permissions".format(
                machine_dict["name"]))
        return None

    print("Force shut down: machine '{}' with PID {}".format(
        machine_dict["name"], machine_dict["pid"]))
    if log_active:
        write_log("Force shut down: machine '{}' with PID {}".format(
            machine_dict["name"], machine_dict["pid"]))
    return True


def shutdown_host():
    """Shut down the host machine, if the user have permissions to do it.

    """
    print("Shut down host...")
    if log_active:
        write_log("Shut down host...")
    try:
        subprocess.run(["shutdown", "-h", "now"], check=True,
                       capture_output=True)
    except subprocess.CalledProcessError:
        print("Unable to shut down the host. Please, verify the user permissions.")
        if log_active:
            write_log("Unable to shut down the host")
        sys.exit(1)


# Graceful shutdown
for graceful in range(max_graceful_times):

    if not get_machines():
        print("No active virtual machines")
        if log_active:
            write_log("No active virtual machines")
        if shutdown_option:
            shutdown_host()

        sys.exit(0)

    attempt = graceful + 1
    print("Attempt {}\n".format(attempt))
    if log_active:
        write_log("Attempt {}".format(attempt))

    for machine in list_of_virtual_machines:
        shutdown_graceful(machine)

    list_of_virtual_machines.clear()


# Forced shutdown
get_machines()

for machine in list_of_virtual_machines:
    shutdown_forced(machine)
    time.sleep(2)

if get_machines():
    print("Cannot shut down virtual machines in current context")
    if log_active:
        write_log("Cannot shut down virtual machines in current context")
    else:
        print("No active virtual machines")
        if log_active:
            write_log("No active virtual machines")

if shutdown_option:
    shutdown_host()
