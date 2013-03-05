Update check
------------

Links from which system parts are downloaded changes often, so we should keep ours updated to. Updating links means updating also MKU, so the user should have the opportunity to check if it's software is updated.

We could relay on git for the first time, the we could switch to something tagged.

To check for updates, MKU should get the revision form filesystem and compare to the repo's one. If it's different, should prompt the user for the update. The update should be a simple:

	git reset --hard
	git pull

IGEP support
------------

* [kernel](http://downloads.isee.biz/pub/releases/linux_kernel/v2.6.37-5/zImage-2.6.37-5.bin)

* [modules]( http://downloads.isee.biz/pub/releases/linux_kernel/v2.6.37-5/modules-2.6.37-5.tgz)

* [MLO](it's inside this archive http://labs.isee.biz/images/7/79/Igep-x-loader-2.5.0-2.tar.bz2). Follow the guide to understand how to use [here](http://labs.isee.biz/index.php/How_to_boot_from_MicroSD_Card#X-Loader_.28MLO.29)

* kernel and module should be used as described [here](http://labs.isee.biz/index.php/How_to_boot_from_MicroSD_Card#Install_the_kernel_modules) using modules and kernel files previously downloaded.

* latest kernel sources are [here](http://downloads.isee.biz/pub/releases/linux_kernel/v2.6.37-5/linux-omap-2.6.37-5.tar.gz)
