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
console=ttyO2,115200n8
 
#Camera: Uncomment to enable:
#http://shop.leopardimaging.com/product.sc?productId=17
#camera=li5m03
 
#SPI: enable for userspace spi access on expansion header
#buddy=spidev
 
#LSR COM6L Adapter Board
#http://eewiki.net/display/linuxonarm/LSR+COM6L+Adapter+Board
#First production run has unprogramed eeprom:
#buddy=lsr-com6l-adpt
 
#LSR COM6L Adapter Board + TiWi5
#wl12xx_clk=wl12xx_26mhz
 
#These are now set by default: uncomment/change if you need something else
vram=16MB
#defaultdisplay=dvi
#dvimode=1280x720MR-16@60
 
mmcroot=/dev/mmcblk0p2 ro
mmcrootfstype=ext4 rootwait fixrtc
 
optargs=console=tty0
 
mmc_load_image=fatload mmc 0:1 0x80300000 zImage
mmc_load_initrd=fatload mmc 0:1 0x81600000 initrd.img; setenv initrd_size ${filesize}
mmc_load_dtb=fatload mmc 0:1 0x815f0000 /dtbs/${dtb_file}
 
deviceargs=setenv device_args buddy=${buddy} buddy2=${buddy2} wl12xx_clk=${wl12xx_clk}
mmcargs=setenv bootargs console=${console} ${optargs} vram=${vram} omapfb.mode=${defaultdisplay}:${dvimode} omapdss.def_disp=${defaultdisplay} root=${mmcroot} rootfstype=${mmcrootfstype} ${device_args}
 
#Just: zImage
xyz_mmcboot=run mmc_load_image; echo Booting from mmc ...
loaduimage=run xyz_mmcboot; run deviceargs; run mmcargs; bootz 0x80300000
 
#zImage and initrd
#xyz_mmcboot=run mmc_load_image; run mmc_load_initrd; echo Booting from mmc ...
#loaduimage=run xyz_mmcboot; run deviceargs; run mmcargs; bootz 0x80300000 0x81600000:${initrd_size}"""

CONSOLE="""
start on stopped rc RUNLEVEL=[2345]
stop on runlevel [!2345]
 
respawn
exec /sbin/getty 115200 ttyO2
"""

MLO_URL = "http://rcn-ee.net/deb/tools/beagleboard/MLO-beagleboard-v2013.01.01-r1"
UBOOT_URL = "http://rcn-ee.net/deb/tools/beagleboard/u-boot-beagleboard-v2013.01.01-r1.img"
PRECISE_KERNEL_URL = "http://rcn-ee.net/deb/precise-armhf/v3.7.10-x9/linux-image-3.7.10-x9_1.0precise_armhf.deb"
QUANTAL_KERNEL_URL = "http://rcn-ee.net/deb/quantal-armhf/v3.7.10-x9/linux-image-3.7.10-x9_1.0quantal_armhf.deb"
PRECISE_DTBS_URL      = "http://rcn-ee.net/deb/precise-armhf/v3.7.10-x9/3.7.10-x9-dtbs.tar.gz"
QUANTAL_DTBS_URL      = "http://rcn-ee.net/deb/quantal-armhf/v3.7.10-x9/3.7.10-x9-dtbs.tar.gz"
PRECISE_FIRMWARE_URL  = "http://rcn-ee.net/deb/precise-armhf/v3.7.10-x9/linux-firmware-image_1.0precise_all.deb"
QUANTAL_FIRMWARE_URL  = "http://rcn-ee.net/deb/quantal-armhf/v3.7.10-x9/linux-firmware-image_1.0quantal_all.deb"
PRECISE_KERNEL_SUFFIX = "-3.7.10-x9"
QUANTAL_KERNEL_SUFFIX = "-3.7.10-x9"

import subprocess
import os

def board_prepare():
  KERNEL_URL    = eval(os_version + "_KERNEL_URL")
  KERNEL_SUFFIX = eval(os_version + "_KERNEL_SUFFIX")
  FIRMWARE_URL  = eval(os_version + "_FIRMWARE_URL")
  DTBS_URL      = eval(os_version + "_DTBS_URL")
  
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
  
  #Getting FIRMWARE
  firmware_name = os_version + KERNEL_SUFFIX + "-firmware.deb"
  firmware_path = os.path.join(os.getcwd(), "tmp", firmware_name)
  print(FIRMWARE_URL)
  ret = subprocess.call(["curl" , "-#", "-o", firmware_path, "-C", "-", FIRMWARE_URL])
  
  #Getting DTB
  dtbs_name = os_version + KERNEL_SUFFIX + "-dtbs.tar.gz"
  dtbs_path = os.path.join(os.getcwd(), "tmp", dtbs_name)
  print(DTBS_URL)
  ret = subprocess.call(["curl" , "-#", "-o", dtbs_path, "-C", "-", DTBS_URL])
  ret = subprocess.call(["tar", "zxf", dtbs_path, "-C", "tmp/"])
  ret = subprocess.call(["sudo", "cp" , dtbs_path, "boot/"])
  
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
  ret = subprocess.call(["sudo", "chroot", rootfs_path, "dpkg", "-i", "/tmp/" + firmware_name])
  ret = subprocess.call(["cp" , "rootfs/boot/initrd.img" + KERNEL_SUFFIX, "boot/initrd.img"])
  ret = subprocess.call(["cp" , "rootfs/boot/vmlinuz" + KERNEL_SUFFIX, "boot/zImage"])
  
  #cleaning
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
  ret = subprocess.call(["git", "checkout", "origin/beagleboard-3.6", "-b", "beagleboard-3.6"])
  ret = subprocess.call(["./patch.sh"])
  print("Done!")
