"""
Centrifugal Pump Simulator

This program simulates the performance of a centrifugal pump.

Author: Faiq Raedaya
Date: 30/05/2025
Version: 1.0.0

Changelog:
- 1.0.0: Initial release

"""

import sys
from PyQt5.QtWidgets import QApplication
from src.gui import PumpSimulatorGUI

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    app.setApplicationName("Centrifugal Pump Simulator")
    app.setApplicationVersion("1.0")
    window = PumpSimulatorGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()