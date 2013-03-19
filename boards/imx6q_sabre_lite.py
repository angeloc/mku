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

KERNEL_SUFFIX    = "-boundary-imx_3.0.35_1.1.1"

import subprocess
import os

def board_prepare():
  KERNEL_PATH = os.path.join(BOARD_CONFIGS_PATH, "support", "imx6q_sabre_lite")
  
  print ("""
  ************************************************************************
  *                                                                      *
  * To boot this board, please update the on-board uboot to the          *
  * latest version as described here:                                    *
  *                                                                      *
  * http://boundarydevices.com/i-mx-6dq-u-boot-updates/                  *
  *                                                                      *
  ************************************************************************
  """)
  
  #Getting KERNEL
  kernel_path = os.path.join(KERNEL_PATH, "uImage" + KERNEL_SUFFIX)
  print(kernel_path)
  ret = subprocess.call(["sudo", "cp", "-av" , kernel_path, "boot"])
  
  #Getting MODULES
  modules_path = os.path.join(KERNEL_PATH,  "modules" + KERNEL_SUFFIX + ".tar.gz")
  print(modules_path)
  ret = subprocess.call(["sudo", "tar", "xzfv", modules_path, "-C", "rootfs"])
  
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
