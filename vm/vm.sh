#!/bin/sh -e
#wget -N http://ftp.uk.debian.org/debian/dists/squeeze/main/installer-amd64/current/images/netboot/mini.iso
#wget -N http://ftp.uk.debian.org/debian/dists/squeeze/main/installer-amd64/current/images/netboot/netboot.tar.gz
VBoxManage createvm --name martin --ostype "Debian_64" --register
VBoxManage storagectl martin --name "SATA Controller" --add sata
VBoxManage createhd --filename martin-sda --size 500
VBoxManage storageattach martin --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium martin-sda.vdi
VBoxManage storageattach martin --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium cd.iso
VBoxManage modifyvm martin --keyboard usb
#VBoxManage unregistervm --delete martin
#VBoxManage startvm martin --type headless
