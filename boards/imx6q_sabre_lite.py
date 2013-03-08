#MKU, template based rootfs builder for Ubuntu.
#This file is the template for the beaglebone board.
#Copyright (C) Angelo Compagnucci <angelo.compagnucci@gmail.com> 2013

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


UBOOTSCRIPT_URL = "http://commondatastorage.googleapis.com/boundarydevices.com/6x_bootscript-20121110"
PRECISE_KERNEL_URL = "http://rcn-ee.net/deb/precise-armhf/v3.8.2-imx4/linux-image-3.8.2-imx4_1.0precise_armhf.deb"
QUANTAL_KERNEL_URL = "http://rcn-ee.net/deb/quantal-armhf/v3.8.2-imx4/linux-image-3.8.2-imx4_1.0quantal_armhf.deb"
DTBS_URL = "http://rcn-ee.net/deb/precise-armhf/v3.8.2-imx4/3.8.2-imx4-dtbs.tar.gz"
PRECISE_KERNEL_SUFFIX = "-3.8.2-imx4"
QUANTAL_KERNEL_SUFFIX = "-3.8.2-imx4"

import subprocess
import os

def board_prepare(os_version):
  KERNEL_URL    = eval(os_version + "_KERNEL_URL")
  KERNEL_SUFFIX = eval(os_version + "_KERNEL_SUFFIX")
  
  #Getting bootscript
  ubootscript_path = os.path.join(os.getcwd(), "tmp", "6x_bootscript")
  print(ubootscript_path)
  print(UBOOTSCRIPT_URL)
  ret = subprocess.call(["curl" , "-#", "-o", ubootscript_path, "-C", "-", UBOOTSCRIPT_URL])
  
  #Getting KERNEL
  kernel_name = os_version + KERNEL_SUFFIX + "-kernel.deb"
  kernel_path = os.path.join(os.getcwd(), "tmp", kernel_name)
  print(KERNEL_URL)
  ret = subprocess.call(["curl" , "-#", "-o", kernel_path, "-C", "-", KERNEL_URL])
  
  #Copy bootscript
  ret = subprocess.call(["cp", "-v", "tmp/6x_bootscript" , "boot/6x_bootscript"])
  
  #installing kernel
  ret = subprocess.call(["cp" , kernel_path, "rootfs/tmp"])
  rootfs_path = os.path.join(os.getcwd(), "rootfs")
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "dpkg", "-i", "/tmp/" + kernel_name])
  ret = subprocess.call(["cp", "-v", "rootfs/boot/initrd.img" + KERNEL_SUFFIX, "boot/initrd.img"])
  ret = subprocess.call(["cp", "-v", "rootfs/boot/vmlinuz" + KERNEL_SUFFIX, "boot/zImage"])
  ret = subprocess.call(["mkimage", "-A", "arm", "-O", "linux", 
                          "-T", "kernel", "-C", "none", "-a", "0x10008000", "-e", "0x10008000",
                          "-n", '"Linux"', "-d", "boot/zImage", "boot/uImage"])
  
  #cleaning
  ret = subprocess.call(["rm", "boot/zImage"])
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "rm", "/tmp/" + kernel_name])
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "rm", "-rf", "/boot/"])
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "mkdir", "/boot/"])

def prepare_kernel_devenv():
  import os
  DEPS = ["git", "arm-linux-gnueabihf-gcc", "arm-linux-gnueabi-gcc"]
  DEPS_PACKAGES = ["git", "gcc-arm-linux-gnueabi", "gcc-arm-linux-gnueabihf"]
  try:
    for dep in DEPS:
      output = subprocess.check_output(["which" , dep])
  except:
    print("""
    Missing dependencies, you can install them with:
    sudo apt-get install %s""" % " ".join(DEPS_PACKAGES))
    exit(1)
  print("This process may take a while, please wait ...")
  ret = subprocess.call(["git", "clone", "git://github.com/beagleboard/kernel.git"])
  os.chdir("kernel")
  ret = subprocess.call(["git", "checkout", "origin/beaglebone-3.2", "-b", "beaglebone-3.2"])
  ret = subprocess.call(["./patch.sh"])
  print("Done!")
