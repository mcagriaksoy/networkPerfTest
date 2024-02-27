# Written by: Mehmet Cagri Aksoy - 2024

import sys
import os
import io
import subprocess

try:
    from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
    from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
    from PyQt6.uic import loadUi
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'PyQt6'])
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", 'PyQt6-tools'])
    from PyQt6.QtCore import QThread, pyqtSignal
    from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
    from PyQt6.uic import loadUi


class IperfThread(QThread):
    """ Iperf Thread Class """
    iperf_log = pyqtSignal(str)
    iperf_started = pyqtSignal()
    iperf_finished = pyqtSignal()

    @pyqtSlot()
    def __init__(self, mode, protocol, ip):
        super(IperfThread, self).__init__()
        self.mode = mode
        self.protocol = protocol
        self.ip = ip

    def run(self):
        """ Run the iperf command """
        self.iperf_started.emit()
        # Get the current working directory
        cwd = os.getcwd()
        if self.mode == "-s":
            iperf = cwd + "/../tools/iperf3.exe" + " " + self.mode
        else:
            if self.protocol == "-u":
                iperf = cwd + "/../tools/iperf3.exe" + " -c " + self.ip + " -u"
            else:
                iperf = cwd + "/../tools/iperf3.exe" + " -c " + self.ip
        self.iperf_log.emit(iperf)
        result = subprocess.run(iperf, capture_output=True, text=True)
        self.iperf_log.emit(result.stdout)
        # self.iperf_finished.emit()


class NetIOThread(QThread):
    """ NetIO Thread Class """
    netio_log = pyqtSignal(str)
    netio_started = pyqtSignal()
    netio_finished = pyqtSignal()

    @pyqtSlot()
    def __init__(self, mode, protocol, ip):
        super(NetIOThread, self).__init__()
        self.mode = mode
        self.protocol = protocol
        self.ip = ip

    def run(self):
        """ Run the netio command """
        self.netio_started.emit()
        # Get the current working directory
        cwd = os.getcwd()
        if self.mode == "-s":
            netio = cwd + "/../tools/netio123.exe" + " " + self.mode + " " + self.protocol
        else:
            netio = cwd + "/../tools/netio123.exe" + " " + self.protocol + " " + self.ip
        self.netio_log.emit(netio)
        # command = [netio, self.mode, self.protocol, self.ip]
        # self.netio_log.emit(command)
        result = subprocess.run(netio, capture_output=True, text=True)
        self.netio_log.emit(result.stdout)
        # self.netio_finished.emit()


class MainWindow(QMainWindow):
    """ Main Window Class """

    def __init__(self):
        # Call the inherited classes __init__ method
        super(MainWindow, self).__init__()
        loadUi('ui.ui', self)  # Load the .ui file
        self.show()  # Show the GUI
        self.msg = None

        self.start_button.clicked.connect(self.start_test)
        self.stop_button.clicked.connect(self.stop_test)

    def start_test(self):
        """ Start the test """
        # Read the tool selection:

        # Read the radio button values
        if self.server_radio.isChecked():
            mode = "-s"
        else:
            mode = "-c"

        if self.tcp_radio.isChecked():
            protocol = "-t"
        else:
            protocol = "-u"

        # If we are client Get the IP address from user
        if mode == "-c":
            ip, ok = QInputDialog.getText(
                self, "IP Address", "Enter the Server IP Address:")
            if ok:
                ip = ip
                mode = ""
            else:
                return
        else:
            ip = ""

        if self.netio_button.isChecked():
            # Start the test
            self.worker = NetIOThread(mode, protocol, ip)
            self.worker.netio_started.connect(self.test_start_info)
            self.worker.netio_finished.connect(self.test_finish_info)
            self.worker.netio_log.connect(self.log_output)
            self.worker.start()
        else:
            self.worker2 = IperfThread(mode, protocol, ip)
            self.worker2.iperf_started.connect(self.test_start_info)
            self.worker2.iperf_finished.connect(self.test_finish_info)
            self.worker2.iperf_log.connect(self.log_output)
            self.worker2.start()

    def log_output(self, output):
        """ Log the output """
        self.textEdit.insertPlainText("{}".format(output))

    def test_start_info(self):
        """ Show the test start information """
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Icon.Information)
        self.msg.setText("Test Started!")
        self.msg.setWindowTitle("Test Started")
        self.msg.show()

    def test_stop_info(self):
        """ Show the test stop information """
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Icon.Information)
        self.msg.setText("Test Stopped!")
        self.msg.setWindowTitle("Test Stopped")
        self.msg.show()

    def test_finish_info(self):
        """ Show the test finish information """
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Icon.Information)
        self.msg.setText("Test Finished!")
        self.msg.setWindowTitle("Test Finished")
        self.msg.show()

    def stop_test(self):
        """ Stop the test """
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Icon.Warning)
        self.msg.setText("Are you sure to stop the test?")
        self.msg.setWindowTitle("Stop Test")
        ret = self.msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.msg.show()
        if ret == QMessageBox.StandardButton.Yes:
            self.worker.quit()
            self.worker2.quit()
            self.test_stop_info()


def start_ui():
    """ Start the UI Design """
    app = QApplication(sys.argv)  # Create an instance
    window_object = MainWindow()  # Create an instance of our class

    app.exec()  # Start the application
