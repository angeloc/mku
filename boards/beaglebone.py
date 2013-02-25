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

UENV = """kernel_file=zImage
initrd_file=initrd.img

console=ttyO0,115200n8

mmcroot=/dev/mmcblk0p2 ro
mmcrootfstype=ext4 rootwait fixrtc

boot_fstype=fat
xyz_load_image=${boot_fstype}load mmc 0:1 0x80300000 ${kernel_file}
xyz_load_initrd=${boot_fstype}load mmc 0:1 0x81600000 ${initrd_file}; setenv initrd_size ${filesize}
xyz_load_dtb=${boot_fstype}load mmc 0:1 0x815f0000 /dtbs/${dtb_file}

xyz_mmcboot=run xyz_load_image; run xyz_load_initrd; echo Booting from mmc ...

video_args=setenv video 
device_args=run video_args; run expansion_args; run mmcargs
mmcargs=setenv bootargs console=${console} ${optargs} ${video} root=${mmcroot} rootfstype=${mmcrootfstype} ${expansion}

optargs=
expansion_args=setenv expansion ip=${ip_method}
loaduimage=run xyz_mmcboot; run device_args; bootz 0x80300000 0x81600000:${initrd_size}
"""

MLO_URL = "http://rcn-ee.net/deb/tools/beaglebone/MLO-beaglebone-v2013.01.01-r1"
UBOOT_URL = "http://rcn-ee.net/deb/tools/beaglebone/u-boot-beaglebone-v2013.01.01-r1.img"
PRECISE_KERNEL_URL = "http://rcn-ee.net/deb/precise-armhf/v3.2.33-psp26/linux-image-3.2.33-psp26_1.0precise_armhf.deb"
QUANTAL_KERNEL_URL = "http://rcn-ee.net/deb/quantal-armhf/v3.2.33-psp26/linux-image-3.2.33-psp26_1.0quantal_armhf.deb"
PRECISE_KERNEL_SUFFIX = "-3.2.33-psp26"
QUANTAL_KERNEL_SUFFIX = "-3.2.33-psp26"

import subprocess
import os

def board_prepare(os_version):
  KERNEL_URL    = eval(os_version + "_KERNEL_URL")
  KERNEL_SUFFIX = eval(os_version + "_KERNEL_SUFFIX")
  
  #Getting MLO
  mlo_path = os.path.join(os.getcwd(), "tmp", "MLO")
  print(MLO_URL)
  ret = subprocess.call(["curl" , "-#", "-o", mlo_path, "-C", "-", MLO_URL])
  
  #Getting UBOOT
  uboot_path = os.path.join(os.getcwd(), "tmp", "u-boot.img")
  print(UBOOT_URL)
  ret = subprocess.call(["curl" , "-#", "-o", uboot_path, "-C", "-", UBOOT_URL])
  
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
  
  #installing kernel
  ret = subprocess.call(["cp" , kernel_path, "rootfs/tmp"])
  rootfs_path = os.path.join(os.getcwd(), "rootfs")
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "dpkg", "-i", "/tmp/" + kernel_name])
  ret = subprocess.call(["cp" , "rootfs/boot/initrd.img" + KERNEL_SUFFIX, "boot/initrd.img"])
  ret = subprocess.call(["cp" , "rootfs/boot/vmlinuz" + KERNEL_SUFFIX, "boot/zImage"])
  
  #cleaning
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "rm", "/tmp/" + kernel_name])
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "rm", "-rf", "/boot/"])
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "mkdir", "/boot/"])
