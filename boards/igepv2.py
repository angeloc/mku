#MKU, template based rootfs builder for Ubuntu.
#This file is the template for the IGEPv2 board.
#Copyright (C) 2013 Angelo Compagnucci <angelo.compagnucci@gmail.com>

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

CONSOLE="""
start on stopped rc RUNLEVEL=[2345]
stop on runlevel [!2345]
 
respawn
exec /sbin/getty 115200 ttyO2
"""

BIN_URL = "http://labs.isee.biz/images/7/79/Igep-x-loader-2.5.0-2.tar.bz2"
KERNEL_URL = "http://downloads.isee.biz/pub/releases/linux_kernel/v2.6.37-5/zImage-2.6.37-5.bin"
MODULES_URL = "http://downloads.isee.biz/pub/releases/linux_kernel/v2.6.37-5/modules-2.6.37-5.tgz"
KERNEL_SRC_URL = "http://downloads.isee.biz/pub/releases/linux_kernel/v2.6.37-5/linux-omap-2.6.37-5.tar.gz"
KERNEL_SUFFIX = "-2.6.37-5"

import subprocess
import os

def board_prepare():
  
  #Getting BOOT binaries
  bin_path = os.path.join(os.getcwd(), "tmp", "igep-x-loader.tar.bz2")
  print(BIN_URL)
  ret = subprocess.call(["curl" , "-#", "-o", bin_path, "-C", "-", BIN_URL])
  ret = subprocess.call(["tar", "xzfv", bin_path, "-C", "tmp"])
  ret = subprocess.call(" ".join(["cp", "-uav", "tmp/binaries/*", "boot"]), shell=True)
  
  #Getting KERNEL
  kernel_name = KERNEL_SUFFIX + "-kernel.deb"
  kernel_path = os.path.join(os.getcwd(), "tmp", kernel_name)
  print(KERNEL_URL)
  ret = subprocess.call(["curl" , "-#", "-o", kernel_path, "-C", "-", KERNEL_URL])
  
  #Installing KERNEL
  ret = subprocess.call(["cp" , kernel_path, "boot/zImage"])
  
  #Getting MODULES
  modules_path = os.path.join(os.getcwd(),  "modules" + KERNEL_SUFFIX + ".tar.gz")
  print(MODULES_URL)
  ret = subprocess.call(["curl" , "-#", "-o", modules_path, "-C", "-", MODULES_URL])
  ret = subprocess.call(["sudo", "tar", "xzfv", modules_path, "-C", "rootfs"])
  
  #Setting up console
  console_path = os.path.join(os.getcwd(), "tmp", "console.conf")
  console = open(console_path,"w")
  console.write(CONSOLE)
  console.close()
  ret = subprocess.call(["sudo", "cp" , console_path, "rootfs/etc/init/"])
  
  #cleaning
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
  kernel_src_name = "kernel" + KERNEL_SUFFIX + ".tar.gz"
  kernel_src_path = os.path.join(os.getcwd(), "tmp", kernel_src_name)
  ret = subprocess.call(["curl" , "-#", "-o", kernel_src_path, "-C", "-", KERNEL_SRC_URL])
  ret = subprocess.call(["tar", "xzf", kernel_src_path])
