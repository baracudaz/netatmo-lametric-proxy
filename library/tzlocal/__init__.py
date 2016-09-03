import sys
if sys.platform == 'win32':
    from library.tzlocal.win32 import get_localzone, reload_localzone
elif 'darwin' in sys.platform:
    from library.tzlocal.darwin import get_localzone, reload_localzone
else:
    from library.tzlocal.unix import get_localzone, reload_localzone
