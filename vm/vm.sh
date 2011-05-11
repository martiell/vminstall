#!/bin/sh -e
#wget -N http://ftp.uk.debian.org/debian/dists/squeeze/main/installer-amd64/current/images/netboot/mini.iso
#wget -N http://ftp.uk.debian.org/debian/dists/squeeze/main/installer-amd64/current/images/netboot/netboot.tar.gz

config() {
  for d in vboxmanage VBoxManage ; do
    which $d > /dev/null && VBOXMANAGE=$d && break
  done
}

config
$VBOXMANAGE createvm --name martin --ostype "Debian_64" --register
$VBOXMANAGE storagectl martin --name "SATA Controller" --add sata
$VBOXMANAGE createhd --filename martin-sda --size 500
$VBOXMANAGE storageattach martin --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium martin-sda.vdi
$VBOXMANAGE storageattach martin --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium cd.iso
$VBOXMANAGE modifyvm martin --keyboard usb
#VBoxManage unregistervm --delete martin
#VBoxManage startvm martin --type headless
