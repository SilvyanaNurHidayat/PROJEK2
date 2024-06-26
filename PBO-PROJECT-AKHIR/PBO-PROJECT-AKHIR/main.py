from PyQt5 import QtCore, QtGui, QtWidgets
from ticket_booking_ui import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Hapus item yang ada dan tambahkan tujuan yang unik
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(["Pilih Tujuan", "Jakarta", "Bandung", "Surabaya", "Yogyakarta"])

        # Set initial state for comboBox_2 (waktu)
        self.ui.comboBox_2.addItem("Pilih Waktu")

        # Set initial state for price display
        self.ui.lineEdit_2.setText("Rp.0")

        # Connect signals to slots
        self.ui.comboBox.currentIndexChanged.connect(self.update_times_and_price)
        self.ui.comboBox_2.currentIndexChanged.connect(self.update_price)
        self.ui.radioButton.clicked.connect(self.reset_destination_and_time)
        self.ui.radioButton_2.clicked.connect(self.reset_destination_and_time)
        self.ui.radioButton_3.clicked.connect(self.reset_destination_and_time)
        self.ui.pushButton.clicked.connect(self.clear_fields)
        self.ui.pushButton_2.clicked.connect(self.book_ticket)
        self.ui.pushButton_3.clicked.connect(self.delete_order)

        # Initialize order list
        self.orders = []

        # Prices based on destination, time, and class
        self.prices = {
            "Jakarta": {
                "06.00": {"VIP": 500000, "BISNIS": 350000, "EKONOMI": 200000},
                "08.00": {"VIP": 450000, "BISNIS": 300000, "EKONOMI": 150000},
                "10.00": {"VIP": 400000, "BISNIS": 250000, "EKONOMI": 100000},
                "12.00": {"VIP": 550000, "BISNIS": 400000, "EKONOMI": 250000},
                "14.00": {"VIP": 500000, "BISNIS": 350000, "EKONOMI": 200000},
                "16.00": {"VIP": 450000, "BISNIS": 300000, "EKONOMI": 150000}
            },
            "Bandung": {
                "06.30": {"VIP": 450000, "BISNIS": 300000, "EKONOMI": 150000},
                "08.30": {"VIP": 400000, "BISNIS": 250000, "EKONOMI": 100000},
                "10.30": {"VIP": 350000, "BISNIS": 200000, "EKONOMI": 50000},
                "12.30": {"VIP": 500000, "BISNIS": 350000, "EKONOMI": 250000},
                "14.30": {"VIP": 450000, "BISNIS": 300000, "EKONOMI": 200000},
                "16.30": {"VIP": 400000, "BISNIS": 250000, "EKONOMI": 150000}
            },
            "Surabaya": {
                "07.00": {"VIP": 600000, "BISNIS": 400000, "EKONOMI": 250000},
                "09.00": {"VIP": 550000, "BISNIS": 375000, "EKONOMI": 225000},
                "11.00": {"VIP": 500000, "BISNIS": 350000, "EKONOMI": 200000},
                "13.00": {"VIP": 650000, "BISNIS": 450000, "EKONOMI": 300000},
                "15.00": {"VIP": 600000, "BISNIS": 400000, "EKONOMI": 250000},
                "17.00": {"VIP": 550000, "BISNIS": 375000, "EKONOMI": 225000}
            },
            "Yogyakarta": {
                "07.30": {"VIP": 550000, "BISNIS": 375000, "EKONOMI": 225000},
                "09.30": {"VIP": 500000, "BISNIS": 350000, "EKONOMI": 200000},
                "11.30": {"VIP": 450000, "BISNIS": 300000, "EKONOMI": 150000},
                "13.30": {"VIP": 600000, "BISNIS": 400000, "EKONOMI": 250000},
                "15.30": {"VIP": 550000, "BISNIS": 375000, "EKONOMI": 225000},
                "17.30": {"VIP": 500000, "BISNIS": 350000, "EKONOMI": 200000}
            }
        }

    def clear_fields(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.setText("Rp.0")
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItem("Pilih Waktu")
        self.reset_destination_and_time()

    def book_ticket(self):
        name = self.ui.lineEdit.text()
        destination = self.ui.comboBox.currentText()
        time = self.ui.comboBox_2.currentText()

        if self.ui.radioButton.isChecked():
            kelas = "VIP"
        elif self.ui.radioButton_2.isChecked():
            kelas = "BISNIS"
        else:
            kelas = "EKONOMI"

        try:
            price = self.prices[destination][time][kelas]
            self.ui.lineEdit_2.setText(f"Rp.{price:,}")
            order = {
                "name": name,
                "kelas": kelas,
                "destination": destination,
                "time": time,
                "harga": f"Rp.{price:,}"
            }
            self.orders.append(order)
            self.display_orders()
        except KeyError:
            self.ui.lineEdit_2.setText("N/A")

    def display_orders(self):
        self.ui.tableWidget.setRowCount(len(self.orders))
        for i, order in enumerate(self.orders):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i+1)))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(order["name"]))
            self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(order["kelas"]))
            self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(order["destination"]))
            self.ui.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(order["time"]))
            self.ui.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(order["harga"]))

    def delete_order(self):
        if self.orders:
            self.orders.pop()
            self.display_orders()
        else:
            self.ui.tableWidget.setRowCount(0)

    def update_times_and_price(self):
        # Update comboBox_2 (time) based on comboBox (destination)
        destination = self.ui.comboBox.currentText()

        if destination == "Pilih Tujuan":
            times = []
        elif destination == "Jakarta":
            times = ["06.00", "08.00", "10.00", "12.00", "14.00", "16.00"]
        elif destination == "Bandung":
            times = ["06.30", "08.30", "10.30", "12.30", "14.30", "16.30"]
        elif destination == "Surabaya":
            times = ["07.00", "09.00", "11.00", "13.00", "15.00", "17.00"]
        elif destination == "Yogyakarta":
            times = ["07.30", "09.30", "11.30", "13.30", "15.30", "17.30"]
        else:
            times = []

        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItem("Pilih Waktu")
        self.ui.comboBox_2.addItems(times)

        # Update price when class (kelas) changes
        self.update_price()

    def update_price(self):
        destination = self.ui.comboBox.currentText()
        time = self.ui.comboBox_2.currentText()

        if destination and time:
            kelas = "VIP" if self.ui.radioButton.isChecked() else "BISNIS" if self.ui.radioButton_2.isChecked() else "EKONOMI"

            try:
                price = self.prices[destination][time][kelas]
                self.ui.lineEdit_2.setText(f"Rp.{price:,}")
            except KeyError:
                self.ui.lineEdit_2.setText("N/A")

    def reset_destination_and_time(self):
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItem("Pilih Waktu")
        self.ui.lineEdit_2.setText("Rp.0")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
