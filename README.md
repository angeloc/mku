MKU
===

Making an Ubuntu rootfs is easy with MKU!

About
-----

MKU was born with a strong focus on easy rootfs building for the embedded world.
With MKU you can generate and deploy a custom boot and rootfs, built against Ubuntu core, to your embedded platform.

Everything is handled automatically by the software: it downloads boot files, kernels, Ubuntu core, it sets up directory layout, and extract all the necessary files to build a complete boot and rootfs for your board.

MKU keeps every file it download in a temporary folder so you do not have to redownload files over and over again.

Install
-------

* Clone the repository:
  
		git clone https://github.com/angeloc/mku.git

* Append the folder you cloned to the $PATH variable in bashrc:

		echo "PATH=$PATH:~/mku" >> ~/.bashrc

How to use
----------

* Create a folder for the new rootfs like `mkurootfs`.

* Copy `project-sample.mku` to `mkurootfs/project.mku`.

* Change `project.mku` default values to suite your needs.

* Enter the folder and prepare the environment with:

		mku prepare

* Please wait until it completes, it may take a while due to file downloading the first time.

* When done, you can add your files to the rootfs folder.

* Your rootfs is now done. To use it, copy boot folder and rootfs folder to your embedded board. You can install them with:

		mku install_boot -d /media/boot
		mku install_rootfs -d /media/rootfs

* If you want you can `pack` your boot and rootfs with:

		mku pack
	they will be packed in `dist` folder in tar.gz format.

Development support
-------------------

With MKU you can also prepare a kernel development environment. MKU knows your board so it can download and set up a properly configured environment for your kernel development needs.

You can prepare your kernel development environment with:

	mku prepare_kernel

You can also prepare a scratchbox2 environment with:

	mku scratchboxit

Acknowledgments
---------------

Many thanks to Robert Nelson (http://www.rcn-ee.com/) for keep running his wonderful infrastructure on which some parts of this software are based.

