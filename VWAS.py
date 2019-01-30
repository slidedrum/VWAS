import subprocess
import os
import sys
import time

Default_Location = "C:\Program Files\VIVE Wireless\ConnectionUtility\\"
Location = Default_Location
#Make sure that they have vive wireless installed
try:
    with open('Location.txt', 'r') as text:
        Location = text.read()
        if not Location[len(Location)-1] == "\\":
            Location = Location + "\\"
        if not os.path.isfile(Location+"HtcConnectionUtility.exe"):
            print("Could not find new location.  Check that the path is correct in Location.txt Reverting to default")
            Location = Default_Location
            if not os.path.isfile(Location + "HtcConnectionUtility.exe"):
                print("Could not find HtcConnectionUtility.exe in default location.  Please install it or create a file called 'Location.txt' with the new path.")
                input("Press enter to exit.")
                sys.exit()
except Exception:
    if os.path.isfile("Location.txt"):
        print ("Could not read new location. Reverting to default")
        Location = Default_Location
        if not os.path.isfile(Location + "HtcConnectionUtility.exe"):
            print("Could not find HtcConnectionUtility.exe in default location.  Please install it or create a file called 'Location.txt' with the new path.")
            input("Press enter to exit.")
            sys.exit()
    elif not os.path.isfile(Location + "HtcConnectionUtility.exe"):
        print("Could not find HtcConnectionUtility.exe in default location.  Please install it or create a file called 'Location.txt' with the new path.")
        input("Press enter to exit.")
        sys.exit()
def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call)
    outputs = str(output).strip().split('\\r\\n')
    for i in outputs:
        if process_name in i:
            return True
    return False
#Check windows environment to see if bat files are present.
if os.path.isfile("start.bat"):
    pass
else:
    print ("Start.bat not found.  Creating.")
    startBat = open("start.bat", "w+")
    startBat.write("""Start ""  "%s"
exit"""%(Location+"HtcConnectionUtility.exe"))
    startBat.close()
if os.path.isfile("stop.bat"):
    pass
else:
    print ("Stop.bat not found.  Creating.")
    stopBat = open("stop.bat", "w+")
    stopBat.write("""taskkill /IM HtcConnectionUtility.exe
exit""")
    stopBat.close()
current = process_exists('vrserver.exe')
if current:
    if not process_exists('HtcConnectionUtility.exe'):
        print("Steam VR already started. Starting Vive Wireless.")
        subprocess.Popen("start.bat")
    else:
        print("Steam VR already started. Waiting for it to stop.")
else:
    print("Waiting for Steam VR to start.")

#Actually do the thing and listen for steam VR to start
while True:
    time.sleep(1)
    if process_exists('vrserver.exe') or process_exists('vrmonitor.exe'):
        if not current:
            print("Steam VR started!")
            if not process_exists('HtcConnectionUtility.exe'):
                print ("Starting Vive Wireless.")
                subprocess.Popen("start.bat")
                time.sleep(0.5)
                if not process_exists('HtcConnectionUtility.exe'):
                    print ("Vive wireless failed to start.  Did you modify the bat file?")
            else:
                print("Vive wireless already running.  Did you start it manually?")
        current = True
    else:
        if current:
            print ("Steam VR Stopped!")
            if process_exists('HtcConnectionUtility.exe'):
                print("Stopping Vive Wireless.")
                subprocess.Popen("stop.bat")
                time.sleep(0.5)
                if process_exists('HtcConnectionUtility.exe'):
                    print ("Failed to stop Vive Wireless. Did you modify the bat file?")
            else:
                print("Vive wireless not running.  Did you stop it manually?")
        current = False
#


