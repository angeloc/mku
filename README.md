MKU
===

Making an Ubuntu rootfs for embedded platforms is easy with MKU!

About
-----

MKU is born with a strong focus on easily building rootfs for the embedded world.
With MKU you can generate and deploy a custom boot and rootfs to your embedded platform built against ubuntu core.

Everything is handled automatically by the software: it downloads boot files, kernels and ubuntu core, it sets up directory layout, and extract all files necessaries to build a complete boot and rootfs for your board.

Install
-------

* Clone the repository:
  
`git clone https://github.com/angeloc/mku.git`

* Append the folder you cloned to the $PATH in bashrc:

`echo PATH=$PATH:~/mku >> ~/.bashrc`

* Create a folder for the new rootfs:

* Enter the folder and prepare the environment with:

`mku prepare`

