#MKU, template based rootfs builder for Ubuntu.
#This file is the template for the beaglebone board.
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

UENV = """
kernel_file=zImage
initrd_file=initrd.img
dtb_file=am335x-boneblack.dtb

initrd_high=0xffffffff
fdt_high=0xffffffff

console=ttyO0,115200n8

mmcroot=/dev/mmcblk0p2 ro
mmcrootfstype=ext4 rootwait fixrtc

boot_fstype=fat
xyz_load_image=${boot_fstype}load mmc 0:1 0x80300000 ${kernel_file}
xyz_load_initrd=${boot_fstype}load mmc 0:1 0x81600000 ${initrd_file}; setenv initrd_size ${filesize}
xyz_load_dtb=${boot_fstype}load mmc 0:1 0x815f0000 ${dtb_file}

xyz_mmcboot=run xyz_load_image; run xyz_load_initrd; run xyz_load_dtb; echo Booting from mmc ...

video_args=setenv video 
device_args=run video_args; run expansion_args; run mmcargs
mmcargs=setenv bootargs console=${console} ${optargs} ${video} root=${mmcroot} rootfstype=${mmcrootfstype} ${expansion}

optargs=
expansion_args=setenv expansion ip=${ip_method}
loaduimage=run xyz_mmcboot; run device_args; bootz 0x80300000 0x81600000:${initrd_size} 0x815f0000
"""

CONSOLE="""
start on stopped rc RUNLEVEL=[2345]
stop on runlevel [!2345]
 
respawn
exec /sbin/getty 115200 ttyO0
"""

MLO_URL = "http://rcn-ee.net/deb/tools/beaglebone/MLO-beaglebone-v2013.07-rc2-r0"
UBOOT_URL = "http://rcn-ee.net/deb/tools/beaglebone/u-boot-beaglebone-v2013.07-rc2-r0.img"
PRECISE_KERNEL_URL = "http://rcn-ee.net/deb/precise-armhf/v3.8.13-bone24/linux-image-3.8.13-bone24_1.0precise_armhf.deb"
PRECISE_FIRMWARE_URL = "http://rcn-ee.net/deb/precise-armhf/v3.8.13-bone24/linux-firmware-image_1.0precise_all.deb"
PRECISE_DTBS_URL = "http://rcn-ee.net/deb/precise-armhf/v3.8.13-bone24/3.8.13-bone24-dtbs.tar.gz"
QUANTAL_KERNEL_URL = "http://rcn-ee.net/deb/quantal-armhf/v3.8.13-bone24/linux-image-3.8.13-bone24_1.0quantal_armhf.deb"
QUANTAL_FIRMWARE_URL = "http://rcn-ee.net/deb/quantal-armhf/v3.8.13-bone24/linux-firmware-image_1.0quantal_all.deb"
QUANTAL_DTBS_URL = "http://rcn-ee.net/deb/quantal-armhf/v3.8.13-bone24/3.8.13-bone24-dtbs.tar.gz"
RARING_KERNEL_URL = "http://rcn-ee.net/deb/raring-armhf/v3.13.1-bone5/linux-image-3.13.1-bone5_1.0raring_armhf.deb"
RARING_FIRMWARE_URL = "http://rcn-ee.net/deb/raring-armhf/v3.13.1-bone5/linux-firmware-image-3.13.1-bone5_1.0raring_all.deb"
RARING_DTBS_URL = "http://rcn-ee.net/deb/raring-armhf/v3.13.1-bone5/3.13.1-bone5-dtbs.tar.gz"
SAUCY_KERNEL_URL = "http://rcn-ee.net/deb/saucy-armhf/v3.13.1-bone5/linux-image-3.13.1-bone5_1.0saucy_armhf.deb"
SAUCY_FIRMWARE_URL = "http://rcn-ee.net/deb/saucy-armhf/v3.13.1-bone5/linux-firmware-image-3.13.1-bone5_1.0saucy_all.deb"
SAUCY_DTBS_URL = "http://rcn-ee.net/deb/saucy-armhf/v3.13.1-bone5/3.13.1-bone5-dtbs.tar.gz"

PRECISE_KERNEL_SUFFIX = "-3.8.13-bone24"
QUANTAL_KERNEL_SUFFIX = "-3.8.13-bone24"
RARING_KERNEL_SUFFIX  = "-3.13.1-bone5"
SAUCY_KERNEL_SUFFIX  = "-3.13.1-bone5"

import subprocess
import os

def board_prepare():
  KERNEL_URL    = eval(os_version + "_KERNEL_URL")
  DTBS_URL      = eval(os_version + "_DTBS_URL")
  FIRMWARE_URL  = eval(os_version + "_FIRMWARE_URL")
  KERNEL_SUFFIX = eval(os_version + "_KERNEL_SUFFIX")
  
  #Getting MLO
  mlo_path = os.path.join(os.getcwd(), "tmp", "MLO")
  print(MLO_URL)
  ret = subprocess.call(["curl" , "-#", "-o", mlo_path, "-C", "-", MLO_URL])
  
  #Getting UBOOT
  uboot_path = os.path.join(os.getcwd(), "tmp", "u-boot.img")
  print(UBOOT_URL)
  ret = subprocess.call(["curl" , "-#", "-o", uboot_path, "-C", "-", UBOOT_URL])
  
  #Getting DTBS
  dtbs_name = os_version + KERNEL_SUFFIX + "-dtbs.tar.gz"
  dtbs_path = os.path.join(os.getcwd(), "tmp", dtbs_name)
  print(DTBS_URL)
  ret = subprocess.call(["curl" , "-#", "-o", dtbs_path, "-C", "-", DTBS_URL])
  
  #Getting FIRMWARE
  firmware_name = os_version + KERNEL_SUFFIX + "-firmware.deb"
  firmware_path = os.path.join(os.getcwd(), "tmp", firmware_name)
  print(FIRMWARE_URL)
  ret = subprocess.call(["curl" , "-#", "-o", firmware_path, "-C", "-", FIRMWARE_URL])
  
  #Getting KERNEL
  kernel_name = os_version + KERNEL_SUFFIX + "-kernel.deb"
  kernel_path = os.path.join(os.getcwd(), "tmp", kernel_name)
  print(KERNEL_URL)
  ret = subprocess.call(["curl" , "-#", "-o", kernel_path, "-C", "-", KERNEL_URL])
  
  #Setting up uEnv.txt
  ret = subprocess.call(["cp", "-v", mlo_path, "boot"])
  ret = subprocess.call(["cp", "-v", uboot_path, "boot"])
  uenv_path = os.path.join(os.getcwd(), "boot", "uEnv.txt")
  uenv = open(uenv_path,"w")
  uenv.write(UENV)
  uenv.close()
  
  #Setting up console
  console_path = os.path.join(os.getcwd(), "tmp", "console.conf")
  console = open(console_path,"w")
  console.write(CONSOLE)
  console.close()
  ret = subprocess.call(["sudo", "cp" , console_path, "rootfs/etc/init/"])
  
  #installing kernel
  ret = subprocess.call(["cp" , kernel_path, "rootfs/tmp"])
  rootfs_path = os.path.join(os.getcwd(), "rootfs")
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "dpkg", "-i", "/tmp/" + kernel_name])
  ret = subprocess.call(["cp", "-v" , "rootfs/boot/initrd.img" + KERNEL_SUFFIX, "boot/initrd.img"])
  ret = subprocess.call(["cp", "-v" , "rootfs/boot/vmlinuz" + KERNEL_SUFFIX, "boot/zImage"])
  
  #installing firmware
  ret = subprocess.call(["cp" , firmware_path, "rootfs/tmp"])
  rootfs_path = os.path.join(os.getcwd(), "rootfs")
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "dpkg", "-i", "/tmp/" + firmware_name])
  
  #installing dtbs
  ret = subprocess.call(["tar", "zxvf", dtbs_path, "-C", "boot", "am335x-boneblack.dtb"])
  
  #cleaning
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "rm", "/tmp/" + kernel_name])
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "rm", "-rf", "/boot/"])
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "mkdir", "/boot/"])

def prepare_kernel_devenv():
  import os
  DEPS = ["git", "arm-linux-gnueabihf-gcc"]
  DEPS_PACKAGES = ["git", "gcc-arm-linux-gnueabihf"]
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
  ret = subprocess.call(["git", "checkout", "origin/3.8", "-b", "3.8"])
  ret = subprocess.call(["./patch.sh"])
