# Minatsuki-Pro-Drums-Plus
This is an update for the Minatsuki python script that allows the PS4 Rock Band 4 drums to work with the pro cymbals. 

This update allows for the pro drums to work natively in emulators as and xinput (xbox 360) controller. It also allows for the drums to be used as a midi controller for prgrams that accept the velocity control of the pads and cymbals (such as DAW like Ableton, Pro Tools, Waveform, etc.)

The majority of the credit for this should go to yanagiragi who made the original python script that allows for keyboard input, as well as to 
yannbouteiller who made the vgamepad library for python and rdoursenaud who made the midi library mido for python.

Install Instructions (these can also be found in the Python Installer Options text file)


**Python install scripts**

For all options you will need to install Minatsuki's required python libraries, open the folder containing these files in a python script (or alternatively drop all files into c:\users\(your computers user name) or whatever the default location is in your terminal)

pip install -r requirements.txt

I also highly recommend updating your drums firmware. If you have the MadCatz drum, feel free to DM me on reddit @ u/cumbandicoot (I know it's a ridiculous name, but it's the only account I have that I haven't lost access to and actually use) If you have the PDP kit (I think that's the other company that made them?) you may still be able to find the firmware using the Internet Archive's Wayback Machine.


**Keyboard**

This will allow you to use the keyboard inputs by running the main.py script, which will work with clone hero and many other rhythm games

For the keyboard input you will run the main.py in terminal and you can find all of these files on the Minatsuki gihub page here:


**Gamepad**

For gamepad use run this in your python terminal (recommended for programs like RPCS3 and Xenia, but can also be used with Clone Hero)

pip install vgamepad

There are two options for running the script with gamepad inputs. main_xinput.py emulates the Xbox360 pad setup where the cymbals are picked up using a combination of buttons (this is necessary for RPCS3 pro drums on Rock Band 3) The other option, main_xinputcs.py, splits the cymbals into different individual outputs just like the keyboard version, but this will output as buttons on an xinput controller instead.


**Midi**

For Midi use the setup is significantly more involved, but it does allow for the velocity of the instruments to be used which opens it up to more applications (I mostly made this for me to play around with using the drum kit in Ableton, but it could have several applications as Midi is a much more widely accepted format and it allows for velocity). You will need to run this in your python terminal:

pip install mido python-rtmidi

(I want to note here that I also had to install Microsoft Visual Studio C++ for desktop development in order to get this install to work. Those can be found on Microsoft's website: https://visualstudio.microsoft.com/visual-cpp-build-tools/)

You will also need to install a virtual midi device, which I set this up using loopmidi. You will need to need to name the device Virtual Drum Kit and press the plus button in the softwatre. Be sure that you open this application before running your python script. You can find loopmidi here:

https://www.tobias-erichsen.de/software/loopmidi.html
