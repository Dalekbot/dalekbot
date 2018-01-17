# Build raspberry Pi with strech on 32GB card
## 5/01/2018


download from https://www.raspberrypi.org/downloads/raspbian/
write disk with win32 Disk Imager

Boot the Raspberry Pi

goto Raspberry Pi Config

Change password and Hostname

Enable interfaces: Camera, SSH, SPI ,I2C, 1-Wire
```
sudo apt-get update
sudo apt-get upgrade
```
Now get remote desktop working

http://www.raspberrypiblog.com/2012/10/how-to-setup-remote-desktop-from.html

```
sudo apt-get install xrdp
```
Start the opencv install

Make Space  if needed and get rid of unneeded stuff
``` 
$ sudo apt-get purge wolfram-engine
$ sudo apt-get purge libreoffice*
$ sudo apt-get clean
$ sudo apt-get autoremove
```

expand file system
``` 
sudo raspi-config
```
check disk 

```
> df -h
```
install samba for file sharing
```
sudo apt-get install samba
sudo smbpasswd -a pi // set password for user
```
edit samba conf.
```B8:27:EB:4E:3F:9E 
sudo nano /etc/samba/smb.conf
```
```
[share]
  Comment = Pi shared folder
  Path =/home/pi/share
  Browseable = Yes
  Writeable = Yes
  only guest = no
  create mask = 0777
  directory mask = 0777
  Public = no
  Guest ok = no
```

restart samba
```
sudo /etc/init.d/samba restart
```

## Install OpenCv
https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/


```
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python2.7-dev python3-dev
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.0.zip
unzip opencv.zip
 
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.0.zip
unzip opencv_contrib.zip
 
wget https://bootstrap.pypa.io/get-pip.py  - you should already be upto date
sudo python get-pip.py
sudo python3 get-pip.py
```

install numpy
```
pip install numpy
```


```
cd ~/opencv-3.4.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.0/modules \
    -D BUILD_EXAMPLES=ON ..
```

change swap file size
```
sudo nano /etc/dphys-swapfile
```
change to:
```
# CONF_SWAPSIZE=100
CONF_SWAPSIZE=1024
```
save ane exit

flush swapfile

```
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
```

while the make is processing use this to monitor the temp of the cpu
```
 /opt/vc/bin/vcgencmd measure_temp
```

make the prog
```
make -j4
```

save to pc G:\Dev\RasPi\
```
sudo make install
sudo ldconfig
```
test to see it worked
```
python
>> import cv2
>> cv2.__version__
```
### >>> IMPORTANT <<<
change swap file size back 
```
sudo nano /etc/dphys-swapfile
```
change to:
```
CONF_SWAPSIZE=100
# CONF_SWAPSIZE=1024
```

```
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
```



app dependencies.
```
pip3 install picamera
pip3 install spidev
pip3 install termcolor
```
Setup ps3 controller

https://www.piborg.org/blog/rpi-ps3-help
```
sudo apt-get -y install libusb-dev joystick python-pygame
cd ~
wget http://www.pabr.org/sixlinux/sixpair.c
gcc -o sixpair sixpair.c -lusb

sudo shutdown -h now
```
### Save to pc again 
If we get any errors or need to install a different controller we can re-image the disk.