"""
Usage:
  arduCryoFridgeCLI.py configure [--ontime=<ontime>] [--offtime=<offtime>]
  arduCryoFridgeCLI.py switch [--on | --off] [--now | --delay=<delay>]
  arduCryoFridgeCLI.py -s | --status
  arduCryoFridgeCLI.py -h | --help
  arduCryoFridgeCLI.py -q
  arduCryoFridgeCLI.py [--port=<USBportname> | --autoport]
  
Options:
  --ontime=<ontime>     duration of ontime minutes.
  --offtime=<offtime>   duration of offtime minutes.
  --delay=<delay>       start on/off cycle in delay [default: 0] minutes.
  -s --status           Read out and report PT410 status
  -h --help             Show this screen.
  -q                    Query program version + version run on the arduino
  --port=<USBportname>  Specify USB port: must be done before running any other commands
  --autoport            automatically detect USB port: alternative that must be done before running other commands

"""

from docopt import docopt
import serial
import serial.tools.list_ports
# from gi.repository import Gtk

baud = 9600
programVersion = 1.0


if __name__ == "__main__":
    args = docopt(__doc__)  # docopt saves arguments and options as key:value pairs in a dictionary
    print(args)


# NOTE: MUST SPECIFY OR AUTODETECT PORT BEFORE RUNNING ANY OTHER COMMANNDS, OTHERWISE NOTHING WORKS
if args['--port'] != None:
    usbPort = args['--port']
    try:
        ser = serial.Serial(usbPort, baud)
    except:
        print("\nCouldn't find port: " + str(usbPort) + " Recheck your port or try '--autoport' to autodetect the port.")
        ser = None
elif args['--autoport'] != False:
    # doesn't work with third-party Arduino knockoffs (in which case, user specifies port)
    ports = serial.tools.list_ports.comports()
    connected = False
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        if desc == "USB2.0-Serial":
            try:
                ser = serial.Serial(port, baud, timeout = 0.05)
                # textbuff.insert_at_cursor("Connected to: " + port + '\n', -1)
                print("Connected to: " + port + '\n')
                connected = True
                break
            except Exception as e:
                # textbuff.insert_at_cursor("\nCouldn't open port: " + str(e), -1)
                print("\nCouldn't open port: " + str(e))
                ser = None
    if not(connected):
        # textbuff.insert_at_cursor("No likely serial port found\n", -1)
        print("No likely serial port found. Use command '--port=<USBportname>' to manually specify port")


if args['configure'] == True:
    if args['--ontime'] != None:
        ontime = args['--ontime']
        print("Ontime = " + ontime)
        ser.write(('A'+ str(ontime)).encode())
    elif args['--offtime'] != None:
        offtime = args['--offtime']
        print("Offtime = " + offtime)
        ser.write(('B'+ str(offtime)).encode())
        
elif args['switch'] == True:
    if args['--on'] == True:
        if args['--now'] == True:
            print("switch compressor on NOW")
            ser.write('G'.encode())
        else:
            delay = args['--delay']
            print("delay turning on by " + str(delay) + " minutes")
            ser.write(('Z'+str(delay)).encode())
    elif args['--off'] == True:
        if args['--now'] == True:
            print("switch compressor off NOW")
            ser.write('X'.encode())
        else:
            delay = args['--delay']
            print("delay turning off by " + str(delay) + " minutes")
            ser.write(('Z'+str(delay)).encode())
            
elif args['--status'] != False:
    print("PT410 status: ")
    ser.write('S'.encode())
    ser.readline()
    arduinoStatus = ser.readline()
    print(arduinoStatus)
    
elif args['-q'] != False:
    print("Python program version: " + str(programVersion))
    ser.write('Q'.encode())
    arduinoProgramVersion = ser.readline()
    print("Arduino program version: " + str(arduinoProgramVersion))
            
        
