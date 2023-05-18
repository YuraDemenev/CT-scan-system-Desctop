import sys
import os
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QTableWidgetItem,
    QTableWidget,
)
from UI_main import Ui_MainWindow

# Для копирования
import shutil

import glob
from DicomOpen import DicomOpenClass
import pymysql


# pyside6-uic UI_main.ui -o UI_main.py
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.DeleleteImages()

        # Add Entry
        addEntryButton = self.ui.AddEntryButton
        addEntryButton.clicked.connect(self.AddEntry)

        # hide ui
        global hideList
        hideList = [
            self.ui.tableDidcom,
            addEntryButton,
            self.ui.DirectionLine,
            self.ui.FullNametLine,
            self.ui.TreatmentLine,
            self.ui.ScanObjectLine,
            self.ui.ReccomendationLine,
            self.ui.FullNameLabel,
            self.ui.DirectionLabel,
            self.ui.TreatmentLabel,
            self.ui.ScanObjectLabel,
            self.ui.ReccomendationLabel,
        ]

        for item in hideList:
            item.setVisible(False)

        # File Dialog
        download_button = self.ui.DownloadButton
        open_dicom_button = self.ui.OpenDicomButton

        download_button.clicked.connect(self.FileDialog)
        open_dicom_button.clicked.connect(self.OpenDicom)

        # Sliders
        self.ui.AxialSlider.valueChanged.connect(self.AxialSlider)
        self.ui.SagitalSlider.valueChanged.connect(self.SagitalSlider)
        self.ui.CoronalSlider.valueChanged.connect(self.CoronalSlider)

        # DataBase
        self.ui.OpenDataBaseButton.clicked.connect(self.OpenDataBase)
        self.ui.DataBaseTable.setVisible(False)
        self.ui.BackTableButton.setVisible(False)
        self.ui.DeleteTableButton.setVisible(False)
        self.ui.DeleteTableLine.setVisible(False)
        self.ui.DataBaseTable.cellDoubleClicked.connect(self.ClickDataBase)
        self.ui.DeleteTableButton.clicked.connect(self.DeleteRow)
        self.ui.BackTableButton.clicked.connect(self.BackTable)

    def FileDialog(self):
        file_filter = "Dicom file (*.dcm)"
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a file",
            dir=os.getcwd(),
            filter=file_filter,
        )
        shutil.copy2(response[0], os.getcwd() + "\\WorkFiles\\dicom.dcm")
        self.ui.OpenDicomButton.setEnabled(True)
        self.ui.InfoTable.setText("File Dicom Dowload")

    def OpenDicom(self):
        self.ui.OpenDicomButton.setEnabled(False)
        DicomOpenClass.OpenDicom()
        self.ui.AxialImage.setPixmap(QPixmap("./Images/Axial/axial256.jpg"))
        self.ui.SagitalImage.setPixmap(QPixmap("./Images/Sagital/sagital256.jpg"))
        self.ui.CoronalImage.setPixmap(QPixmap("./Images/Coronal/coronal256.jpg"))

        self.ui.AxialCount.setText("256")
        self.ui.SagitalCount.setText("256")
        self.ui.CoronalCount.setText("256")

        self.ui.AxialSlider.setValue(256)
        self.ui.SagitalSlider.setValue(256)
        self.ui.CoronalSlider.setValue(256)

        # Table
        table = DicomOpenClass.create_a_table_array()
        self.ui.tableDidcom.setRowCount(len(table))
        for i in range(len(table)):
            column = table[i]
            self.ui.tableDidcom.setItem(i, 0, QTableWidgetItem(str(column[0])))
            self.ui.tableDidcom.setItem(i, 1, QTableWidgetItem(column[1]))

        # Add entry
        for item in hideList:
            item.setVisible(True)

    def DeleleteImages(self):
        list_files = [
            "./Images/Axial/*",
            "./Images/Coronal/*",
            "./Images/Sagital/*",
        ]
        for i in range(3):
            files = glob.glob(list_files[i])
            for f in files:
                os.remove(f)

    def AxialSlider(self):
        count = self.ui.AxialSlider.value()
        self.ui.AxialImage.setPixmap(QPixmap(f"./Images/Axial/axial{count}.jpg"))
        self.ui.AxialCount.setText(str(count))

    def CoronalSlider(self):
        count = self.ui.CoronalSlider.value()
        self.ui.CoronalImage.setPixmap(QPixmap(f"./Images/Coronal/coronal{count}.jpg"))
        self.ui.CoronalCount.setText(str(count))

    def SagitalSlider(self):
        count = self.ui.SagitalSlider.value()
        self.ui.SagitalImage.setPixmap(QPixmap(f"./Images/Sagital/Sagital{count}.jpg"))
        self.ui.SagitalCount.setText(str(count))

    def AddEntry(self):
        if self.ui.ScanObjectLine.text() == "":
            self.ui.ScanObjectLine.setText("Fill this Field")

        elif self.ui.FullNametLine.text() == "":
            self.ui.FullNametLine.setText("Fill this Field")

        elif self.ui.TreatmentLine.text() == "":
            self.ui.TreatmentLine.setText("Fill this Field")

        elif self.ui.DirectionLine.text() == "":
            self.ui.DirectionLine.setText("Fill this Field")

        elif self.ui.ReccomendationLine.text() == "":
            self.ui.ReccomendationLine.setText("Fill this Field")

        else:
            # SQl Add request
            # self.ui.tableDidcom.setItem(i, 0, QTableWidgetItem(str(column[0])))
            dic = {
                "Study_date": self.ui.tableDidcom.item(0, 1).text(),
                "Modality": self.ui.tableDidcom.item(1, 1).text(),
                "Patient_ID": self.ui.tableDidcom.item(2, 1).text(),
                "Patient_position": self.ui.tableDidcom.item(3, 1).text(),
                "Patient_sex": self.ui.tableDidcom.item(4, 1).text(),
                "Object": self.ui.ScanObjectLine.text(),
            }

            config = {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "260203",
                "db_name": "test",
            }
            try:
                connection = pymysql.connect(
                    host=config.get("host"),
                    port=config.get("port"),
                    user=config.get("user"),
                    password=config.get("password"),
                    database=config.get("db_name"),
                )

            except:
                self.ui.InfoTable.setText("server connection error")

            with connection.cursor() as cursor:
                query = f"SELECT Patient_ID,Count(*) FROM global Where Patient_ID={dic.get('Patient_ID')}"
                cursor.execute(query)
                loc_check = list(cursor.fetchone())

                if loc_check[0] == None:
                    add_info = "INSERT INTO global (Patient_ID) VALUES (%(Patient_ID)s)"
                    cursor.execute(add_info, dic)
                    connection.commit()

                else:
                    count = loc_check[1]
                    count += 1
                    # dic['Count'] = count+1
                    update_info = f"UPDATE global set Count={count} WHERE Patient_ID={dic.get('Patient_ID')}"
                    cursor.execute(update_info)
                    connection.commit()

                try:
                    # with connection.cursor() as cursor:
                    add_info = (
                        "INSERT INTO patient_info "
                        "(Study_date,Modality,Patient_ID,Patient_position,Patient_sex,Object) "
                        "VALUES (%(Study_date)s,%(Modality)s,%(Patient_ID)s,%(Patient_position)s,%(Patient_sex)s,%(Object)s)"
                    )
                    cursor.execute(add_info, dic)
                    connection.commit()

                    dic["Treatment"] = (self.ui.TreatmentLine.text(),)
                    dic["Direction"] = (self.ui.DirectionLine.text(),)
                    dic["Full_name"] = (self.ui.FullNametLine.text(),)
                    dic["Recomendation"] = self.ui.ReccomendationLine.text()

                    add_info = (
                        "INSERT INTO rec_dir (Patient_ID,Treatment,Direction,Recommendation,Full_name,Study_date,Object) "
                        "VALUES (%(Patient_ID)s,%(Treatment)s,%(Direction)s,%(Recomendation)s,%(Full_name)s,%(Study_date)s,%(Object)s)"
                    )
                    cursor.execute(add_info, dic)
                    connection.commit()

                    self.ui.InfoTable.setText("Success ADD")
                    connection.close()

                except:
                    connection.close()
                    self.ui.InfoTable.setText("This entry exists")

    def OpenDataBase(self):
        if self.ui.OpenDataBaseButton.text() == "Open DataBase":
            config = {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "260203",
                "db_name": "test",
            }
            connection = pymysql.connect(
                host=config.get("host"),
                port=config.get("port"),
                user=config.get("user"),
                password=config.get("password"),
                database=config.get("db_name"),
            )
            self.ui.DataBaseTable.setVisible(True)
            self.ui.DeleteTableButton.setVisible(True)
            self.ui.DeleteTableLine.setVisible(True)
            self.ui.BackTableButton.setVisible(True)

            self.ui.DataBaseTable.setColumnCount(3)
            self.ui.DataBaseTable.setHorizontalHeaderLabels(
                ["Number", "Patiend Id", "Count"]
            )
            with connection.cursor() as cursor:
                query = "SELECT * FROM global"
                cursor.execute(query)
                rows = list(cursor.fetchall())
                cursor.close()
            self.ui.DataBaseTable.setRowCount(len(rows))

            for i in range(len(rows)):
                column = rows[i]
                self.ui.DataBaseTable.setItem(i, 0, QTableWidgetItem(str(column[0])))
                self.ui.DataBaseTable.setItem(i, 1, QTableWidgetItem(str(column[1])))
                self.ui.DataBaseTable.setItem(i, 2, QTableWidgetItem(str(column[2])))
        else:
            self.ui.DataBaseTable.setVisible(False)

    def ClickDataBase(self, row, column):
        config = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "260203",
            "db_name": "test",
        }
        try:
            connection = pymysql.connect(
                host=config.get("host"),
                port=config.get("port"),
                user=config.get("user"),
                password=config.get("password"),
                database=config.get("db_name"),
            )

        except:
            self.ui.InfoTable.setText("Connection error")

        count = self.ui.DataBaseTable.columnCount()
        if count == 3:
            id = self.ui.DataBaseTable.item(row, 1).text()
            with connection.cursor() as cursor:
                query = (
                    "SELECT global.Patient_ID,Study_date,Modality,Patient_position,Patient_sex,Object,patient_info.Number FROM "
                    f"global, patient_info WHERE global.Patient_ID=patient_info.Patient_ID AND patient_info.Patient_ID={id}"
                )

                cursor.execute(query)
                rows = list(cursor.fetchall())

                td = [
                    "Patient_ID",
                    "Study_date",
                    "Modality",
                    "Patient_position",
                    "Patient_sex",
                    "Object",
                    "Number",
                ]
                self.ui.DataBaseTable.clear()
                self.ui.DataBaseTable.setColumnCount(len(td))
                self.ui.DataBaseTable.setHorizontalHeaderLabels(td)
                self.ui.DataBaseTable.setRowCount(len(rows))

                for i in range(len(rows)):
                    column = rows[i]
                    for j in range(len(column)):
                        self.ui.DataBaseTable.setItem(
                            i, j, QTableWidgetItem(str(column[j]))
                        )

                cursor.close()

    def DeleteRow(self):
        config = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "260203",
            "db_name": "test",
        }
        try:
            connection = pymysql.connect(
                host=config.get("host"),
                port=config.get("port"),
                user=config.get("user"),
                password=config.get("password"),
                database=config.get("db_name"),
            )

        except:
            self.ui.InfoTable.setText("Connection error")

        count = self.ui.DataBaseTable.columnCount()
        if count == 3:
            num = int(self.ui.DeleteTableLine.text())
            id = self.ui.DataBaseTable.item(num - 1, 1).text()
            print(id)
            if id == "":
                self.ui.DeleteTableLine.setText("Write row number")
                return
            with connection.cursor() as cursor:
                query = f"DELETE FROM test.rec_dir WHERE (Patient_ID = '{id}');"
                cursor.execute(query)
                connection.commit()

                query = f"DELETE FROM test.patient_info WHERE (Patient_ID = '{id}');"
                cursor.execute(query)
                connection.commit()

                query = f"DELETE FROM test.global WHERE (Patient_ID = '{id}');"
                cursor.execute(query)
                connection.commit()

                query = "SELECT * FROM global"
                cursor.execute(query)
                rows = list(cursor.fetchall())

                table = []
                for item in rows:
                    for i in range(len(item)):
                        table.append(item[i])

                td = [
                    "Number",
                    "Patient ID",
                    "Count",
                ]

                cursor.close()
        elif count == 7:
            num = int(self.ui.DeleteTableLine.text())
            id = self.ui.DataBaseTable.item(num - 1, 0).text()
            study_date = self.ui.DataBaseTable.item(num - 1, 1).text()
            object_ = self.ui.DataBaseTable.item(num - 1, 5).text()
            if id == "":
                self.ui.DeleteTableLine.setText("Write line number")
                return

            with connection.cursor() as cursor:
                query = f"SELECT Patient_ID,Count(*) FROM global Where Patient_ID={id}"
                cursor.execute(query)
                loc_check = list(cursor.fetchone())

                if loc_check[0] == None:
                    return

                elif loc_check[1] != 1:
                    count = loc_check[1]
                    count -= 1
                    update_info = (
                        f"UPDATE global set Count={count} WHERE Patient_ID={id}"
                    )
                    cursor.execute(update_info)
                    connection.commit()

                query = f"DELETE FROM test.rec_dir WHERE (Patient_ID = '{id}') AND (Study_date='{study_date}') AND (Object='{object_}');"
                cursor.execute(query)
                connection.commit()

                query = f"DELETE FROM test.patient_info WHERE (Patient_ID = '{id}') AND (Study_date='{study_date}') AND (Object='{object_}');"
                cursor.execute(query)
                connection.commit()

                if loc_check[1] == 1:
                    query = f"DELETE FROM test.global WHERE (Patient_ID = '{id}');"
                    cursor.execute(query)
                    connection.commit()

                query = (
                    "SELECT * FROM patient_info WHERE (Patient_ID = '{patient_id}');"
                )
                cursor.execute(query)
                rows = list(cursor.fetchall())

                table = []
                for item in rows:
                    for i in range(len(item)):
                        table.append(item[i])

                td = [
                    "Patient ID",
                    "Study date",
                    "Modality",
                    "Patient sex",
                    "Object",
                    "Number",
                ]

                cursor.close()

    def BackTable(self):
        config = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "260203",
            "db_name": "test",
        }
        connection = pymysql.connect(
            host=config.get("host"),
            port=config.get("port"),
            user=config.get("user"),
            password=config.get("password"),
            database=config.get("db_name"),
        )
        self.ui.DataBaseTable.setVisible(True)
        self.ui.DeleteTableButton.setVisible(True)
        self.ui.DeleteTableLine.setVisible(True)
        self.ui.BackTableButton.setVisible(True)

        self.ui.DataBaseTable.setColumnCount(3)
        self.ui.DataBaseTable.setHorizontalHeaderLabels(
            ["Number", "Patiend Id", "Count"]
        )
        with connection.cursor() as cursor:
            query = "SELECT * FROM global"
            cursor.execute(query)
            rows = list(cursor.fetchall())
            cursor.close()
        self.ui.DataBaseTable.setRowCount(len(rows))

        for i in range(len(rows)):
            column = rows[i]
            self.ui.DataBaseTable.setItem(i, 0, QTableWidgetItem(str(column[0])))
            self.ui.DataBaseTable.setItem(i, 1, QTableWidgetItem(str(column[1])))
            self.ui.DataBaseTable.setItem(i, 2, QTableWidgetItem(str(column[2])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
