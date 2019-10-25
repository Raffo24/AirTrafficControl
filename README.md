# Air Traffic Control
Air Traffic Control is a visualization software that, paired with Dump1090, identifies and calculate the coordinates of the aircraft
# System requirements
Operating system: Windows 7 or newer or LinuxA
A Dongle rtl-sdr with chip realtek RTL2832 or RTL2832U, specific to 1090mHz and Standard ADS-B
An antenna compatible with 1090mHz
Dump1090
# how to execute
1)Install Anaconda following the official documentation https://docs.anaconda.com/anaconda/
3)To get dump1090 up and running you should first install RTL1090. The two apps use many of the same dynamic link library (dll) files. So download the "Installer and Maintenance Utility" from this link http://globe-s.eu/download/rtl1090imu.exe. Plug in your USB dongle and then install RTL1090. The IMU version will download and install all of the necessary dll’s and drivers in c:\RTL1090. You may have to run the Zadig setup, which you will find in the RTL1090 folder.
Once that’s done, download dump1090 for Windows, from the github repository of Antirez https://github.com/antirez/dump1090/archive/master.zip, and unzip the contents of the file to the same directory as RTL1090. Don’t overwrite any existing files. You should now have dump1090.exe and dump1090.bat among your RTL1090 files.
Now in the command prompt window, type "C:\rtl1090\dump1090.exe --interactive --net" and press Enter.

2)Run Spyder IDE(Integrated Development Environment) that is included with Anaconda
3)So use the keyboard shortcut "CTRL + O" to open python script
4)Run it using keybord shortcut "F5"
