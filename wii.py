import cwiid             # Import WiiMote code


def setupwii():
    # Connect Wiimote
    print '\nPress & hold 1 + 2 on your Wii Remote now ...\n\n'
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string("1+2")

    # Connect to the Wii Remote. If it times out then quit.
    
    global wii

    try:
        wii=cwiid.Wiimote()
    except RuntimeError:
        print 'Error opening wiimote connection'
        scrollphat.clear()         # Shutdown Scroll pHat
        scrollphat.write_string("Err")
        time.sleep(0.5)
        return False

    print 'Wii Remote connected...\n'
    wii.rumble = 1
    time.sleep(0.1)
    wii.rumble = 0
    
    wii.led = 1
    time.sleep(0.75) 
    wii.led = 2
    time.sleep(0.75)
    wii.led = 4
    time.sleep(0.75)
    wii.led = 8
    time.sleep(0.75)
    battery = int(wii.state['battery']/25)
    
    if battery == 4:
        wii.led = 8
    elif battery == 3:
        wii.led = 4
    elif battery == 2:
        wii.led = 2
    else: 
        wii.led = 1
    
    wii.rumble = 1
    time.sleep(0.1)
    wii.rumble = 0
    
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string("Gd")

    print '\nPress some buttons!\n'
    print 'Press PLUS and MINUS together to disconnect and quit.\n'
    
    return True
  
