# MKU, template based rootfs builder for Ubuntu.
# This file is the template for the beaglebone board.
# Copyright (C) 2013 Angelo Compagnucci <angelo.compagnucci@gmail.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

CONSOLE = """
start on stopped rc RUNLEVEL=[2345]
stop on runlevel [!2345]
 
respawn
exec /sbin/getty 115200 ttyO0
"""

import subprocess
import os


def board_prepare():

    # Setting up console
    console_path = os.path.join(os.getcwd(), "tmp", "console.conf")
    console = open(console_path, "w")
    console.write(CONSOLE)
    console.close()
    ret = subprocess.call(["sudo", "cp", console_path, "rootfs/etc/init/"])

    print("Please use BSP from TI, no binary BSP/Kernel for this board!")


def prepare_kernel_devenv():
    import os
    DEPS = ["git", "arm-linux-gnueabihf-gcc"]
    DEPS_PACKAGES = ["git", "gcc-arm-linux-gnueabihf"]
    try:
        for dep in DEPS:
            output = subprocess.check_output(["which", dep])
    except:
        print("""
    Missing dependencies, you can install them with:
    sudo apt-get install %s""" % " ".join(DEPS_PACKAGES))
        exit(1)
    print("This process may take a while, please wait ...")
    ret = subprocess.call(
        ["git", "clone", "git://github.com/beagleboard/kernel.git"])
    os.chdir("kernel")
    ret = subprocess.call(["git", "checkout", "origin/3.8", "-b", "3.8"])
    ret = subprocess.call(["./patch.sh"])
