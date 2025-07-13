# Minatsuki-Pro-Drums-Plus
This is an add-on for the Minatsuki python script that allows the PS4 Rock Band 4 drums to work with the pro cymbals. 

This add-on allows for the pro drums to work natively in emulators as an xinput (xbox 360) controller. It also allows for the drums to be used as a midi controller for prgrams that accept the velocity control of the pads and cymbals (such as DAWs like Ableton, Pro Tools, Waveform, etc.)

The majority of the credit for this should go to yanagiragi who made the original python script that allows for keyboard input, as well as to yannbouteiller who made the vgamepad library for python and rdoursenaud who made the midi library mido for python.

**Install Instructions** (these can also be found in the Python Installer Options text file)


**Download Original Minatsuki Files**

For any of this to work (except for the keyboard functions) you will need both the files from here and from the original Minatsuki module. You can find all of the other necessary files on the Minatsuki github page here: https://github.com/yanagiragi/Minatsuki


**Python install scripts**

For all options you will need to install Minatsuki's required python libraries, open the folder containing these files in a python terminal, such as the windows native terminal (or alternatively drop all files into c:\users\(your computers user name) or whatever the default location is in your terminal) You will also need the latest version of python installed on your computer. Once that is done run this in the terminal by right clicking in the folder and selecting open in terminal where the requirements.txt is:

`pip install -r requirements.txt`

I also highly recommend updating your drums firmware. If you have the MadCatz drum, feel free to DM me on reddit @ u/cumbandicoot (I know it's a ridiculous name, but it's the only account I have that I haven't lost access to and actually use) If you have the PDP kit (I think that's the other company that made them?) you may still be able to find the firmware using the Internet Archive's Wayback Machine.


**Keyboard**

This will allow you to use the drum kit as a keyboard output by running the main.py script, which will work with clone hero and many other rhythm games

In a terminal that is opened by right clicking in the folder containg the original Minatsuki files, or alternatively just the default location of your terminal if you dropped the files there, run this script to start the keyboard output:

`python main.py`

Then Select the last instance of your controller (mine says something like MadCatz Rock Band 4 Drums) by typing the corresponding number and press enter.


**Gamepad**

For gamepad use run this in your python terminal (recommended for programs like RPCS3 and Xenia, but can also be used with Clone Hero)

`pip install vgamepad`

There are two options for running the script with gamepad inputs. main_xinput.py emulates the Xbox360 pad setup where the cymbals are picked up using a combination of buttons (this is necessary for RPCS3 pro drums on Rock Band 3) unfortunately with this setup I am not currently able to get the green and blue cymbal working correctly with the toms, however that effects a very small number of songs. If you want better functionality with the drum and cymbals in Rock Band 3 on PC you can use the main_midi.py script. The other option, main_xinputcs.py, splits the cymbals into different individual outputs just like the keyboard version, but this will output as buttons on an xinput controller instead. This will not work with programs like RPCS3 or Xenia, but will work in Clone Hero and YARG. Make sure both of these files are in the same folder as the files from the Minatsuki github pages, or are all in your computers user folder. 

You may also need to install the ViGEm bus driver for the virtual controller output, but since that was already installed before I set this up, I'm not 100% certain wether you do or not. You can download the ViGEm bus driver here: https://vigembusdriver.com/

For combined cymbal modifier hits run this script in terminal by right clicking in the folder: 

`pthon main_xinput.py`

Then select the corresponding number for your drum controller

For the cymbals separated as individual xinput buttons run this script: 

`python main_xinputcs.py`

Then select the corresponding number for your drum controller


**Midi**

For Midi use the setup is a bit more For Midi use the setup is a bit more involved, but it does allow for the velocity of the instruments to be used which opens it up to more applications (I mostly made this for me to play around with using the drum kit in Ableton, but it could have several applications as Midi is a much more widely accepted format and it allows for velocity). This setup is also necessary for better input handling in RPCS3. There are two versions of the midi script as well. main_midi.py is setup how an e drum kit would be setup where the hi hat pedal plays a distinct note when opened or closed and main_midi-rpcs3.py os set up how it should be for Rock Band 3 where a closed hi hat plays a hi hat note (yellow) and an open one plays a ride (blue). You will need to run this in your python terminal once everything else is set up:

`pip install mido python-rtmidi`

(I want to note here that I also had to install Microsoft Visual Studio C++ for desktop development in order to get this install to work. Those can be found on Microsoft's website: https://visualstudio.microsoft.com/visual-cpp-build-tools/)

You will also need to install a virtual midi device, which I set this up using loopmidi. You will need to need to name the device Virtual Drum Kit and press the plus button in the softwatre. Be sure that you open this application before running your python script. You can find loopmidi here:
https://www.tobias-erichsen.de/software/loopmidi.html

Once everything is properly set up, and both the files from the original Minatsuki github and this page are in the same folder or all in your windows user folder, you can run this in the target folder opened in terminal:

`python main_midi.py`

or if you are playing Rock Band 3

`python main_midi_rpcs3.py`

Then select the corresponding number for your drum controller

If you would like to use this in RPCS3 to play Rock Band 3, I really reccomend installing Rock Band 3 Deluxe and following their guide for setting up a midi controller found here: https://rb3pc.milohax.org/ctrls_drums_midi
You will need to edit the rb3drums.yml and set the velocity detection lower, I am using 1 and that seems to work perfectly. I also had to change the combo triggers to three hi hat pressess to enable the start button, but if you do not have an additional pedal you can always use a controller plugged in as a microphone for navigation and control buttons you just have to drop ot out at the start of each song. 

One caveat to the midi implementation is that there is no way to use the face buttons without breaking the toms and cymbals. If you really want the face buttons to be functinal you can use either of the xinput modules. This setup is primarily intended for use with music production software and Rock Band 3, but can also be used in other rhythm games that allow for a midi controller setup.

If you have any questions feel free to ask them here, but given that I don't code that often I may not see it here. However, I am always availible by Reddit DM's at u/cumbandicoot
