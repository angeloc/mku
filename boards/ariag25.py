# MKU, template based rootfs builder for Ubuntu.
# This file is the template for the IGEPv2 board.
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

BIN_URLS = ("http://www.acmesystems.it/download/microsd/A4/kernel/boot128.bin",
            "http://www.acmesystems.it/download/microsd/A4/kernel/boot256.bin")
KERNEL_URL = "http://www.acmesystems.it/download/microsd/A4/kernel/image.bin"
KERNEL_SRC_URL = "https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.13.tar.xz"

import subprocess
import os


def board_prepare():

    # Getting BOOT binaries
    print(BIN_URLS)
    os.chdir(os.path.join(os.getcwd(), "tmp/"))
    for url in BIN_URLS:
        ret = subprocess.call(["curl", "-#", "-C", "-J", "-O", url])

    # Getting KERNEL
    print(KERNEL_URL)
    ret = subprocess.call(
        ["curl", "-#", "-C", "-J", "-O", KERNEL_URL])
    
    os.chdir(os.path.join(os.getcwd(), ".."))

    # Installing KERNEL AND BINARIES
    ret = subprocess.call(
        " ".join(["cp", "-uav", "tmp/*.bin", "boot"]), shell=True)


def prepare_kernel_devenv():
    import os
    DEPS = ["arm-linux-gnueabi-gcc"]
    DEPS_PACKAGES = ["gcc-arm-linux-gnueabi"]
    try:
        for dep in DEPS:
            output = subprocess.check_output(["which", dep])
    except:
        print("""
    Missing dependencies, you can install them with:
    sudo apt-get install %s\n""" % " ".join(DEPS_PACKAGES))
        exit(1)
    print(KERNEL_SRC_URL)
    kernel_src_name = "kernel" + KERNEL_SUFFIX + ".tar.gz"
    kernel_src_path = os.path.join(os.getcwd(), "tmp", kernel_src_name)
    ret = subprocess.call(
        ["curl", "-#", "-o", kernel_src_path, "-C", "-", KERNEL_SRC_URL])
    ret = subprocess.call(["tar", "azf", kernel_src_path])
