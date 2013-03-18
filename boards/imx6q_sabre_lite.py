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

import random

UENV = """initrd_high=0xffffffff
fdt_high=0xffffffff
 
console=ttymxc1,115200
 
mmcroot=/dev/mmcblk0p2
mmcrootfstype=ext4 rootwait fixrtc
 
mmc_load_image=${fs}load mmc ${disk}:1 0x10000000 uImage
mmc_load_initrd=${fs}load mmc ${disk}:1 0x12000000 uInitrd; setenv initrd_size ${filesize}
 
mmcargs=setenv bootargs $videoargs fec.macaddr=0x00,0x04,0x9f,0x11,0x22,0x33 console=tty0 console=${console} root=${mmcroot} rootfstype=${mmcrootfstype} consoleblank=0
 
#Just: uImage
xyz_mmcboot=run mmc_load_image; echo Booting from mmc ...
loaduimage=run xyz_mmcboot; run mmcargs; bootm 0x10000000
"""

BOOTCMD="""setenv videoargs
setenv nextcon 0;

if hdmidet ; then
	setenv videoargs $videoargs video=mxcfb${nextcon}:dev=hdmi,1280x720M@60,if=RGB24
	setenv fbmem "fbmem=28M";
	setexpr nextcon $nextcon + 1
else
	echo "------ no HDMI monitor";
fi

i2c dev 2
if i2c probe 0x04 ; then
	setenv videoargs $videoargs video=mxcfb${nextcon}:dev=ldb,LDB-XGA,if=RGB666
	if test "0" -eq $nextcon; then
		setenv fbmem "fbmem=10M";
	else
		setenv fbmem ${fbmem},10M
	fi
	setexpr nextcon $nextcon + 1
else
	echo "------ no Freescale display";
fi

if i2c probe 0x38 ; then
	setenv videoargs $videoargs video=mxcfb${nextcon}:dev=ldb,1024x600M@60,if=RGB666
	if test "0" -eq $nextcon; then
		setenv fbmem "fbmem=10M";
	else
		setenv fbmem ${fbmem},10M
	fi
	setexpr nextcon $nextcon + 1
else
	echo "------ no 1024x600 display";
fi

if i2c probe 0x48 ; then
	setenv videoargs $videoargs video=mxcfb${nextcon}:dev=lcd,CLAA-WVGA,if=RGB666
	if test "0" -eq $nextcon; then
		setenv fbmem "fbmem=10M";
	else
		setenv fbmem ${fbmem},10M
	fi
	setexpr nextcon $nextcon + 1
else
	echo "------ no 800x480 display";
fi

while test "3" -ne $nextcon ; do
	setenv videoargs $videoargs video=mxcfb${nextcon}:off ;
	setexpr nextcon $nextcon + 1 ;
done

setenv videoargs $videoargs $fbmem ;

${fs}load mmc ${disk}:1 ${loadaddr} uEnv.txt
env import -t ${loadaddr} ${filesize}
run loaduimage
"""

CONSOLE="""
start on stopped rc RUNLEVEL=[2345]
stop on runlevel [!2345]
 
respawn
exec /sbin/getty 115200 ttymxc1
"""

PRECISE_KERNEL_URL    = "http://rcn-ee.net/deb/precise-armhf/v3.7.5-imx6/linux-image-3.7.5-imx6_1.0precise_armhf.deb"
QUANTAL_KERNEL_URL    = "http://rcn-ee.net/deb/quantal-armhf/v3.7.5-imx6/linux-image-3.7.5-imx6_1.0quantal_armhf.deb"
PRECISE_FIRMWARE_URL  = "http://rcn-ee.net/deb/precise-armhf/v3.7.5-imx6/linux-firmware-image_1.0precise_armhf.deb"
QUANTAL_FIRMWARE_URL  = "http://rcn-ee.net/deb/quantal-armhf/v3.7.5-imx6/linux-firmware-image_1.0quantal_all.deb"
PRECISE_DTBS_URL      = "http://rcn-ee.net/deb/precise-armhf/v3.7.5-imx6/3.7.5-imx6-dtbs.tar.gz"
QUANTAL_DTBS_URL      = "http://rcn-ee.net/deb/quantal-armhf/v3.7.5-imx6/3.7.5-imx6-dtbs.tar.gz"
PRECISE_KERNEL_SUFFIX = "-3.7.5-imx6"
QUANTAL_KERNEL_SUFFIX = "-3.7.5-imx6"

import subprocess
import os

def board_prepare(os_version):
  KERNEL_URL    = eval(os_version + "_KERNEL_URL")
  KERNEL_SUFFIX = eval(os_version + "_KERNEL_SUFFIX")
  FIRMWARE_URL  = eval(os_version + "_FIRMWARE_URL")
  DTBS_URL      = eval(os_version + "_DTBS_URL")
  
  print ("""
  ************************************************************************
  *                                                                      *
  * For this board to boot, please update the on-board uboot to the      *
  * latest version as described here:                                    *
  *                                                                      *
  * http://boundarydevices.com/i-mx-6dq-u-boot-updates/                  *
  *                                                                      *
  * Also, you should really recompile your own kernel,                   *
  * cause there is not a precompiled version available.                  *
  *                                                                      *
  * Please run with "prepare_kernel" and then recompile your own kernel. *
  * Then copy uImage to boot/ and modules to rootfs/lib/modules/         *
  *                                                                      *
  ************************************************************************
  """)
  
  #Getting KERNEL
  #kernel_name = os_version + KERNEL_SUFFIX + "-kernel.deb"
  #kernel_path = os.path.join(os.getcwd(), "tmp", kernel_name)
  #print(KERNEL_URL)
  #ret = subprocess.call(["curl" , "-#", "-o", kernel_path, "-C", "-", KERNEL_URL])
  
  #Getting FIRMWARE
  #firmware_name = os_version + KERNEL_SUFFIX + "-firmware.deb"
  #firmware_path = os.path.join(os.getcwd(), "tmp", firmware_name)
  #print(FIRMWARE_URL)
  #ret = subprocess.call(["curl" , "-#", "-o", firmware_path, "-C", "-", FIRMWARE_URL])
  
  #Getting DTB
  #dtbs_name = os_version + KERNEL_SUFFIX + "-dtbs.tar.gz"
  #dtbs_path = os.path.join(os.getcwd(), "tmp", dtbs_name)
  #print(DTBS_URL)
  #ret = subprocess.call(["curl" , "-#", "-o", dtbs_path, "-C", "-", DTBS_URL])
  #ret = subprocess.call(["tar", "zxf", dtbs_path, "-C", "tmp/"])
  #ret = subprocess.call(["sudo", "cp" , dtbs_path, "boot/"])
  
  #Setting up bootscript
  bootcmd_path = os.path.join(os.getcwd(), "tmp", "boot.cmd")
  bootcmd = open(bootcmd_path,"w")
  bootcmd.write(BOOTCMD)
  bootcmd.close()
  ret = subprocess.call(["mkimage", "-A", "arm", "-O", "linux", "-T", 
                          "script", "-C", "none", "-a", "0", "-e", "0",
                          "-n", '"bootscript"', "-d", "tmp/boot.cmd" , "boot/6x_bootscript"])
                          
  #Setting up uEnv.txt
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
  
  #installing kernel and firmware
  #ret = subprocess.call(["cp" , kernel_path, "rootfs/tmp"])
  #ret = subprocess.call(["cp" , firmware_path, "rootfs/tmp"])
  #rootfs_path = os.path.join(os.getcwd(), "rootfs")
  #ret = subprocess.call(["sudo", "chroot", rootfs_path, "dpkg", "-i", "/tmp/" + kernel_name])
  #ret = subprocess.call(["sudo", "chroot", rootfs_path, "dpkg", "-i", "/tmp/" + firmware_name])
  #ret = subprocess.call(["cp", "-v", "rootfs/boot/initrd.img" + KERNEL_SUFFIX, "boot/initrd.img"])
  #ret = subprocess.call(["cp", "-v", "rootfs/boot/vmlinuz" + KERNEL_SUFFIX, "boot/zImage"])
  #ret = subprocess.call(["mkimage", "-A", "arm", "-O", "linux", 
  #                        "-T", "kernel", "-C", "none", "-a", "0x10008000", "-e", "0x10008000",
  #                        "-n", '"Linux"', "-d", "boot/zImage", "boot/uImage"])
  #ret = subprocess.call(["mkimage", "-A", "arm", "-O", "linux", "-a", "0", "-e", "0",
  #                        "-T", "ramdisk", "-C", "none",
  #                        "-n", '"Ramdisk"', "-d", "boot/initrd.img", "boot/uInitrd"])
  
  #cleaning
  #ret = subprocess.call(["rm", "boot/zImage"])
  #ret = subprocess.call(["rm", "boot/initrd.img"])
  #ret = subprocess.call(["sudo", "chroot", rootfs_path, "rm", "/tmp/" + kernel_name])
  #ret = subprocess.call(["sudo", "chroot", rootfs_path, "rm", "-rf", "/boot/"])
  #ret = subprocess.call(["sudo", "chroot", rootfs_path, "mkdir", "/boot/"])

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
  ret = subprocess.call(["git", "clone", "git://github.com/boundarydevices/linux-imx6.git", "--branch", "boundary-imx_3.0.35_1.1.1", "kernel"])
