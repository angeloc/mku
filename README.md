MKU
===

Making an Ubuntu rootfs is easy with MKU!

About
-----

MKU was born with a strong focus on easy rootfs building for the embedded world.
With MKU you can generate and deploy a custom boot and rootfs, built against ubuntu core, to your embedded platform.

Everything is handled automatically by the software: it downloads boot files, kernels, ubuntu core, it sets up directory layout, and extract all the necessary files to build a complete boot and rootfs for your board.

Install
-------

* Clone the repository:
  
`git clone https://github.com/angeloc/mku.git`

* Append the folder you cloned to the $PATH in bashrc:

`echo "PATH=$PATH:~/mku" >> ~/.bashrc`

* Create a folder for the new rootfs like `mkurootfs`

* Copy `project-sample.mku` to `mkurootfs/project.mku`

* Change the default values into `project.mku` to suite your needs

* Enter the folder and prepare the environment with:

`mku prepare`

