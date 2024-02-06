# boot.py -- run on boot-up
import webrepl
import time
import ntptime
import connection
import ujson


# connection.do_connect("home.json")
connection.do_connect("hotspot.json")
try:
    from max30102 import MAX30102
except ImportError as e:
    # Module not available. Try to connect to Internet to download it.
    print(f"Import error: {e}")
    print("Trying to connect to the Internet to download the module.")
    try:
        # Try to leverage upip package manager to download the module.
        import upip
        upip.install("micropython-max30102")
    except ImportError:
        # upip not available. Try to leverage mip package manager to download the module.
        print("upip not available in this port. Trying with mip.")
        import mip
        mip.install("github:n-elia/MAX30102-MicroPython-driver")

#sync the time clock of the board
ntptime.settime()
#starting WebREPL
try: 
    webrepl.start()
except TypeError:
    import webrepl_setup
    webrepl.start()
