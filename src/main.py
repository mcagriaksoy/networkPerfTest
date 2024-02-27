# -*- coding: utf-8 -*-
"""
Network Performance Test Tool with GUI written by mcagriaksoy
- NetIO 1.33 is used in background!
Usage: python main.py
"""
__author__ = "Mehmet Cagri Aksoy - github.com/mcagriaksoy"
__credits__ = ["Mehmet Cagri Aksoy"]
__version__ = "0.0.1"
__maintainer__ = "Mehmet Cagri Aksoy"
__status__ = "Test"

import sys
import ctypes

from ui import start_ui


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    if is_admin():
        start_ui()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
