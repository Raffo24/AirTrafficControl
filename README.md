# Air Traffic Control
Air Traffic Control is a visualization software that, paired with Dump1090, identifies and calculate the coordinates of the aircraft
# System requirements
* Operating system: Windows 7 or newer
* Anaconda(recommended spyder IDE) with python 3.7
* A Dongle rtl-sdr with chip realtek RTL2832U, specific to 1090mHz and ADS-B Standard
* An antenna compatible with 1090mHz
* Dump1090 + Driver + dll
# How To Download And Install Dependences
* Install Anaconda following the official documentation https://docs.anaconda.com/anaconda/
* To get dump1090 up and running you should first install RTL1090. The two apps use many of the same dynamic link library (dll) files. So download the Installer from this link http://globe-s.eu/download/rtl1090imu.exe. Plug in your USB dongle and then install RTL1090. The IMU version will download and install all of the necessary dll’s and drivers in c:\RTL1090. You may have to run the Zadig setup, which you will find in the RTL1090 folder. In Zadig(driver installer) under "options" select "list all devices", then choose “Bulk-In, Interface (Interface 0)” and click install driver.
* Once that’s done, download dump1090 from the github repository of Antirez https://github.com/antirez/dump1090/archive/master.zip, and unzip the contents of the file to the same directory as RTL1090. Don’t overwrite any existing files. You should now have dump1090.exe and dump1090.bat among your RTL1090 files.
* Download the zip file of this github repository and extract the python script "ATC.py"
# Execute The Software
* Now in the command prompt window, type "C:\rtl1090\dump1090.exe --interactive --net" and press Enter.
* Run Spyder IDE(Integrated Development Environment), that is included with Anaconda
* So use the keyboard shortcut "CTRL + O" to open python script in the Spyder IDE
* Run it using keybord shortcut "F5"
* If there aren't troubles, open browser and type on andress bar "localhost:1000"
