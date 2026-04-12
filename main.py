import sys
from PyQt6.QtWidgets import QApplication, QWidget
import controller, core, programs, tests, ui

def main():
    #core.cpu.run_cpu()
    #controller.cpu_controller.run_view_control()

    app = QApplication(sys.argv)

    window = QWidget()
    window.show()

    app.exec()



if __name__ == '__main__':
    sys.exit(main())