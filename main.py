"""
PumpR
Centrifugal Pump Simulator

This program simulates the performance of a centrifugal pump.

Author: Faiq Raedaya
Date: 24/06/2026
Version: 1.1.0

Changelog:
- 1.0.0: 
    - Initial release
- 1.1.0: 
    - Fixed NPSH-required physics and added NPSH available/margin with cavitation warning
    - Corrected performance curves (now pass through the design point), affinity-law performance maps, and mass-fraction mixture mixing 
    - Added CSV export
    - Refactored into src/core (calculations) and src/ui (GUI) packages.
"""

import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import PumpSimulatorGUI

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationName("PumpR")
    app.setApplicationVersion("1.1.0")
    window = PumpSimulatorGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()