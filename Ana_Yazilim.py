import sys, sqlite3
from Dizayn_modul import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.nesnemiz = Ui_MainWindow()        
        self.nesnemiz.setupUi(self)

        self.veritabanı = sqlite3.connect("Planlama_Sistemi_Database.sqlite")
        self.islem1 = self.veritabanı.cursor()
        self.islem1.execute("CREATE TABLE IF NOT EXISTS Hedef (Veri)")
        self.islem1.execute("CREATE TABLE IF NOT EXISTS Bitirilen (Veri)")
        self.islem1.execute("CREATE TABLE IF NOT EXISTS Profil (ad, soyad, sifre)")
        self.islem1.execute("CREATE TABLE IF NOT EXISTS Proje (Açıklama, Alan, Tarih)")

        self.nesnemiz.labelVersion.setText("version 2.0")

        self.nesnemiz.stackedWidget.setCurrentIndex(0)

        self.anahtar = "off"

        self.nesnemiz.actionAna_Sayfa.triggered.connect(self.Anasayfa_task)
        self.nesnemiz.actionHedefler.triggered.connect(self.Hedefler_task)
        self.nesnemiz.actionBitirilen.triggered.connect(self.Bitirilen_task)
        self.nesnemiz.actionProjeler.triggered.connect(self.Projeler_task)
        self.nesnemiz.actionProfilim.triggered.connect(self.Profil_task)

        self.parola = QtWidgets.QLineEdit.Password
        self.nesnemiz.lineEdit_a1.setEchoMode(self.parola)

        self.nesnemiz.buton_a1.clicked.connect(self.buton_a1_task)
        self.nesnemiz.buton_kaydet1.clicked.connect(self.kaydet1_task)
        self.nesnemiz.buton_b1.clicked.connect(self.buton_b1_task)
        self.nesnemiz.buton_b2.clicked.connect(self.buton_b2_task)
        self.nesnemiz.buton_b3.clicked.connect(self.buton_b3_task)
        self.nesnemiz.buton_b4.clicked.connect(self.buton_b4_task)
        self.nesnemiz.buton_b5.clicked.connect(self.buton_b5_task)
        self.nesnemiz.buton_kaydet2.clicked.connect(self.kaydet2_task)
        self.nesnemiz.buton_c1.clicked.connect(self.buton_c1_task)
        self.nesnemiz.buton_c2.clicked.connect(self.buton_c2_task)
        self.nesnemiz.buton_c3.clicked.connect(self.buton_c3_task)
        self.nesnemiz.buton_c4.clicked.connect(self.buton_c4_task)
        self.nesnemiz.buton_c5.clicked.connect(self.buton_c5_task)
        self.nesnemiz.buton_profilKaydet.clicked.connect(self.buton_Profilsave_task)
        self.nesnemiz.butonEkle_pr.clicked.connect(self.proje_ekle)
        self.nesnemiz.butonTamam.clicked.connect(self.Tamamlandi_task1)
        self.nesnemiz.butonKaydet_pr.clicked.connect(self.kaydet_project)

    def Anasayfa_task(self):
        self.nesnemiz.actionAna_Sayfa.setChecked(False)
        self.nesnemiz.stackedWidget.setCurrentIndex(0)

    def buton_a1_task(self):
        self.girilen = self.nesnemiz.lineEdit_a1.text()
        self.nesnemiz.lineEdit_a1.clear()

        self.islem1.execute("SELECT sifre FROM Profil")
        data = self.islem1.fetchall()

        if self.girilen == data[0][0]:
            self.anahtar = "on"
            message = QMessageBox()
            message.setWindowTitle("Giriş")    
            message.setText("Giriş Başarıyla Yapıldı.")
            message.setIcon(QMessageBox.Information)
            x = message.exec()
        else:
            message = QMessageBox()
            message.setWindowTitle("Uyarı")    
            message.setText("Girilen Şifre Hatalı!")
            message.setIcon(QMessageBox.Critical)                      
            x = message.exec()

    def Hedefler_task(self):
        liste_1 = []
        self.nesnemiz.actionHedefler.setChecked(False)
        
        if self.anahtar == "on":
            self.nesnemiz.stackedWidget.setCurrentIndex(1)

            self.nesnemiz.listWidget_1.clear()
            
            self.islem1.execute("SELECT * FROM Hedef")
            data = self.islem1.fetchall()
            karar = bool(data)
            if karar == True:
                for i in data:
                    liste_1.append(i[0])
                self.nesnemiz.listWidget_1.addItems(liste_1)
                self.nesnemiz.listWidget_1.setCurrentRow(0)

    def kaydet1_task(self):
        sayı = self.nesnemiz.listWidget_1.count()
        liste = []
        
        self.islem1.execute("SELECT * FROM Hedef")
        data = self.islem1.fetchall()
        karar = bool(data)
        if karar == True:
            count = 0
            for i in data:
                count = count + 1

            for i in range(1,count+1):
                self.islem1.execute("DELETE FROM Hedef WHERE rowid = {}".format(i))
                self.veritabanı.commit()
                
        for i in range(0,sayı):
            isim = self.nesnemiz.listWidget_1.item(i).text()
            liste.append(isim)

        for i in liste:
            self.islem1.execute("INSERT INTO Hedef VALUES ('{}')".format(i))
            self.veritabanı.commit()

        self.nesnemiz.listWidget_1.setCurrentRow(0)

        
    def buton_b1_task(self): 
        diyalog = QtWidgets.QInputDialog()
        veri = diyalog.getText(self, "Yeni", "Veri:")
        if veri[1] == True:
            check = veri[0].find("'")
            if check == -1:
                self.nesnemiz.listWidget_1.addItem(veri[0])
                sayı = self.nesnemiz.listWidget_2.count()
                self.nesnemiz.listWidget_1.setCurrentRow(sayı-1)
            else:
                message = QMessageBox()
                message.setWindowTitle("Uyarı")    
                message.setText("Karakter hatası!")
                message.setIcon(QMessageBox.Information)
                x = message.exec()
            

    def buton_b2_task(self):
        varolan_toplam = self.nesnemiz.listWidget_1.count()
        if varolan_toplam > 0:
            a = self.nesnemiz.listWidget_1.currentRow()
            if a > -1:
                seçili_sıra = self.nesnemiz.listWidget_1.currentRow()
                seçili_isim = self.nesnemiz.listWidget_1.item(seçili_sıra).text()
                self.nesnemiz.listWidget_1.takeItem(seçili_sıra)
                self.nesnemiz.listWidget_1.setCurrentRow(0)
        

    def buton_b3_task(self):
        varolan_toplam = self.nesnemiz.listWidget_1.count()
        if varolan_toplam > 0:
            a = self.nesnemiz.listWidget_1.currentRow()
            if a > -1:
                seçili_sıra = self.nesnemiz.listWidget_1.currentRow()
                seçili_isim = self.nesnemiz.listWidget_1.item(seçili_sıra).text()
                if varolan_toplam -1 > seçili_sıra:    
                    self.nesnemiz.listWidget_1.takeItem(seçili_sıra)
                    self.nesnemiz.listWidget_1.insertItem(seçili_sıra+1, seçili_isim)
                    self.nesnemiz.listWidget_1.setCurrentRow(seçili_sıra+1)


    def buton_b4_task(self):
        varolan_toplam = self.nesnemiz.listWidget_1.count()
        if varolan_toplam > 0:
            a = self.nesnemiz.listWidget_1.currentRow()
            if a > -1:
                seçili_sıra = self.nesnemiz.listWidget_1.currentRow()
                seçili_isim = self.nesnemiz.listWidget_1.item(seçili_sıra).text()
                if seçili_sıra > 0:    
                    self.nesnemiz.listWidget_1.takeItem(seçili_sıra)
                    self.nesnemiz.listWidget_1.insertItem(seçili_sıra-1, seçili_isim)
                    self.nesnemiz.listWidget_1.setCurrentRow(seçili_sıra-1)


    def buton_b5_task(self):
        varolan_toplam = self.nesnemiz.listWidget_1.count()
        if varolan_toplam > 0:
            a = self.nesnemiz.listWidget_1.currentRow()
            if a > -1:
                seçili_sıra = self.nesnemiz.listWidget_1.currentRow()
                seçili_isim = self.nesnemiz.listWidget_1.item(seçili_sıra).text()

                diyalog = QtWidgets.QInputDialog()
                veri = diyalog.getText(self, "Güncelle", "Veri:")

                if veri[1] == True:
                    check = veri[0].find("'")
                    if check == -1:
                        self.nesnemiz.listWidget_1.takeItem(seçili_sıra)
                        self.nesnemiz.listWidget_1.insertItem(seçili_sıra, veri[0])
                        self.nesnemiz.listWidget_1.setCurrentRow(seçili_sıra)
                    else:
                        message = QMessageBox()
                        message.setWindowTitle("Uyarı")    
                        message.setText("Karakter hatası!")
                        message.setIcon(QMessageBox.Information)
                        x = message.exec()

    def Bitirilen_task(self):
        liste_2 = []
        self.nesnemiz.actionBitirilen.setChecked(False)
        
        if self.anahtar == "on":
            self.nesnemiz.stackedWidget.setCurrentIndex(3)

            self.nesnemiz.listWidget_2.clear()
            
            self.islem1.execute("SELECT * FROM Bitirilen")
            data = self.islem1.fetchall()
            karar = bool(data)
            if karar == True:
                for i in data:
                    liste_2.append(i[0])
                self.nesnemiz.listWidget_2.addItems(liste_2)
                self.nesnemiz.listWidget_2.setCurrentRow(0)


    def kaydet2_task(self):
        sayı = self.nesnemiz.listWidget_2.count()
        liste = []
        
        self.islem1.execute("SELECT * FROM Bitirilen")
        data = self.islem1.fetchall()
        karar = bool(data)
        if karar == True:
            count = 0
            for i in data:
                count = count + 1

            for i in range(1,count+1):
                self.islem1.execute("DELETE FROM Bitirilen WHERE rowid = {}".format(i))
                self.veritabanı.commit()
                
        for i in range(0,sayı):
            isim = self.nesnemiz.listWidget_2.item(i).text()
            liste.append(isim)

        for i in liste:
            self.islem1.execute("INSERT INTO Bitirilen VALUES ('{}')".format(i))
            self.veritabanı.commit()

        self.nesnemiz.listWidget_2.setCurrentRow(0)

    
    def buton_c1_task(self): 
        diyalog = QtWidgets.QInputDialog()
        veri = diyalog.getText(self, "Yeni", "Veri:")
        if veri[1] == True:
            check = veri[0].find("'")
            if check == -1:
                self.nesnemiz.listWidget_2.addItem(veri[0])
                sayı = self.nesnemiz.listWidget_2.count()
                self.nesnemiz.listWidget_2.setCurrentRow(sayı-1)
            else:
                message = QMessageBox()
                message.setWindowTitle("Uyarı")    
                message.setText("Karakter hatası!")
                message.setIcon(QMessageBox.Information)
                x = message.exec()

                
    def buton_c2_task(self):
        varolan_toplam = self.nesnemiz.listWidget_2.count()
        if varolan_toplam > 0:
            a = self.nesnemiz.listWidget_2.currentRow()
            if a > -1:
                seçili_sıra = self.nesnemiz.listWidget_2.currentRow()
                seçili_isim = self.nesnemiz.listWidget_2.item(seçili_sıra).text()
                self.nesnemiz.listWidget_2.takeItem(seçili_sıra)
                self.nesnemiz.listWidget_2.setCurrentRow(0)

                
    def buton_c3_task(self):
        varolan_toplam = self.nesnemiz.listWidget_2.count()
        if varolan_toplam > 0:
            a = self.nesnemiz.listWidget_2.currentRow()
            if a > -1:
                seçili_sıra = self.nesnemiz.listWidget_2.currentRow()
                seçili_isim = self.nesnemiz.listWidget_2.item(seçili_sıra).text()
                if varolan_toplam -1 > seçili_sıra:    
                    self.nesnemiz.listWidget_2.takeItem(seçili_sıra)
                    self.nesnemiz.listWidget_2.insertItem(seçili_sıra+1, seçili_isim)
                    self.nesnemiz.listWidget_2.setCurrentRow(seçili_sıra+1)
            

    def buton_c4_task(self):
        varolan_toplam = self.nesnemiz.listWidget_2.count()
        if varolan_toplam > 0:
            a = self.nesnemiz.listWidget_2.currentRow()
            if a > -1:
                seçili_sıra = self.nesnemiz.listWidget_2.currentRow()
                seçili_isim = self.nesnemiz.listWidget_2.item(seçili_sıra).text()
                if seçili_sıra > 0:    
                    self.nesnemiz.listWidget_2.takeItem(seçili_sıra)
                    self.nesnemiz.listWidget_2.insertItem(seçili_sıra-1, seçili_isim)
                    self.nesnemiz.listWidget_2.setCurrentRow(seçili_sıra-1)
    

    def buton_c5_task(self):
        varolan_toplam = self.nesnemiz.listWidget_2.count()
        if varolan_toplam > 0:
            a = self.nesnemiz.listWidget_2.currentRow()
            if a > -1:
                seçili_sıra = self.nesnemiz.listWidget_2.currentRow()
                seçili_isim = self.nesnemiz.listWidget_2.item(seçili_sıra).text()

                diyalog = QtWidgets.QInputDialog()
                veri = diyalog.getText(self, "Güncelle", "Veri:")
                if veri[1] == True:
                    check = veri[0].find("'")
                    if check == -1:
                        self.nesnemiz.listWidget_2.takeItem(seçili_sıra)
                        self.nesnemiz.listWidget_2.insertItem(seçili_sıra, veri[0])
                        self.nesnemiz.listWidget_2.setCurrentRow(seçili_sıra)
                    else:
                        message = QMessageBox()
                        message.setWindowTitle("Uyarı")    
                        message.setText("Karakter hatası!")
                        message.setIcon(QMessageBox.Information)
                        x = message.exec()


    def Profil_task(self):
        self.nesnemiz.actionProfilim.setChecked(False)
        
        if self.anahtar == "on":
            self.nesnemiz.stackedWidget.setCurrentIndex(4)

            self.islem1.execute("SELECT ad FROM Profil")
            data = self.islem1.fetchall()
            karar = bool(data)
            if karar == True:
                self.nesnemiz.lineEdit_profisim.setText(data[0][0])

            self.islem1.execute("SELECT soyad FROM Profil")
            data = self.islem1.fetchall()
            karar = bool(data)
            if karar == True:
                self.nesnemiz.lineEdit_profsoyisim.setText(data[0][0])
                    
            self.islem1.execute("SELECT sifre FROM Profil")
            data = self.islem1.fetchall()
            karar = bool(data)
            if karar == True:
                self.nesnemiz.lineEdit_sifre.setText(data[0][0])


    def buton_Profilsave_task(self):
        name = self.nesnemiz.lineEdit_profisim.text()
        surname = self.nesnemiz.lineEdit_profsoyisim.text()
        passw = self.nesnemiz.lineEdit_sifre.text()

        if (bool(name) == False) or (bool(surname) == False) or (bool(passw) == False):
            message = QMessageBox()
            message.setWindowTitle("Uyarı")    
            message.setText("Girilen Değerler minimum 3 karakter olmalı!")
            message.setIcon(QMessageBox.Critical)                      
            x = message.exec()

            self.nesnemiz.lineEdit_profisim.clear()
            self.nesnemiz.lineEdit_profsoyisim.clear()
            self.nesnemiz.lineEdit_sifre.clear()

        else:
            self.islem1.execute("UPDATE Profil SET ad = '{}' WHERE rowid = 1".format(name))
            self.islem1.execute("UPDATE Profil SET soyad = '{}' WHERE rowid = 1".format(surname))
            self.islem1.execute("UPDATE Profil SET sifre = '{}' WHERE rowid = 1".format(passw))
            self.veritabanı.commit()        

    
    def Projeler_task(self):
        self.nesnemiz.actionProjeler.setChecked(False)
        
        if self.anahtar == "on":
            self.nesnemiz.stackedWidget.setCurrentIndex(2)                  

            self.nesnemiz.tableWidget.horizontalHeader().setStretchLastSection(True)     #sütun aralıklarını eşitleme (kaldırılabilir)
            self.nesnemiz.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            
            self.islem1.execute("SELECT * FROM Proje")
            data = self.islem1.fetchall()
            karar = bool(data)
            if karar == True:
                row_count = 0
                for i in data:
                    row_count = row_count + 1

                self.nesnemiz.tableWidget.setRowCount(row_count)

                sıra = 0  #row_sırası

                for i in data:
                    self.nesnemiz.tableWidget.setItem(sıra,0, QtWidgets.QTableWidgetItem(i[0]))
                    self.nesnemiz.tableWidget.setItem(sıra,1, QtWidgets.QTableWidgetItem(i[1]))
                    self.nesnemiz.tableWidget.setItem(sıra,2, QtWidgets.QTableWidgetItem(i[2]))
                    sıra = sıra + 1


    def proje_ekle(self):
        anahtar = True
        diyalog = QtWidgets.QInputDialog()
        veri = diyalog.getText(self, "Yeni Proje", "Açıklama:")
        if veri[1] == True:
            check = veri[0].find("'")
            if check == -1:
                aciklama = veri[0]
            else:
                message = QMessageBox()
                message.setWindowTitle("Uyarı")    
                message.setText("Karakter hatası!")
                message.setIcon(QMessageBox.Information)
                x = message.exec()
                anahtar = False
        else:
            anahtar = False

        diyalog = QtWidgets.QInputDialog()
        veri = diyalog.getText(self, "Yeni Proje", "Alan:")
        if veri[1] == True:
            check = veri[0].find("'")
            if check == -1:
                alan = veri[0]
            else:
                message = QMessageBox()
                message.setWindowTitle("Uyarı")    
                message.setText("Karakter hatası!")
                message.setIcon(QMessageBox.Information)
                x = message.exec()
                anahtar = False
        else:
            anahtar = False

        diyalog = QtWidgets.QInputDialog()
        veri = diyalog.getText(self, "Yeni Proje", "Tarih:")
        if veri[1] == True:
            check = veri[0].find("'")
            if check == -1:
                tarih = veri[0]
            else:
                message = QMessageBox()
                message.setWindowTitle("Uyarı")    
                message.setText("Karakter hatası!")
                message.setIcon(QMessageBox.Information)
                x = message.exec()
                anahtar = False
        else:
            anahtar = False

        if(anahtar == True):
            RowSayisi = self.nesnemiz.tableWidget.rowCount()
            self.nesnemiz.tableWidget.setRowCount(RowSayisi+1)
            self.nesnemiz.tableWidget.setItem(RowSayisi,0, QtWidgets.QTableWidgetItem(aciklama))
            self.nesnemiz.tableWidget.setItem(RowSayisi,1, QtWidgets.QTableWidgetItem(alan))
            self.nesnemiz.tableWidget.setItem(RowSayisi,2, QtWidgets.QTableWidgetItem(tarih))

    def Tamamlandi_task1(self):
        delRow = self.nesnemiz.tableWidget.currentRow()
        
        if(delRow == -1):
            message = QMessageBox()
            message.setWindowTitle("Uyarı")    
            message.setText("Tamamlanabilmesi için bir proje seçili olmalı!")
            message.setIcon(QMessageBox.Critical)                      
            x = message.exec()
        else:
            self.nesnemiz.tableWidget.removeRow(delRow)

    def kaydet_project(self):
        self.islem1.execute("SELECT * FROM Proje")
        data = self.islem1.fetchall()
        karar = bool(data)
        if karar == True:
            count = 0
            for i in data:
                count = count + 1

            for i in range(1,count+1):
                self.islem1.execute("DELETE FROM Proje WHERE rowid = {}".format(i))
                self.veritabanı.commit()

        RowSayisi = self.nesnemiz.tableWidget.rowCount()

        for i in range(0, RowSayisi):
            v1 = self.nesnemiz.tableWidget.item(i, 0).text()
            v2 = self.nesnemiz.tableWidget.item(i, 1).text()
            v3 = self.nesnemiz.tableWidget.item(i, 2).text()
            self.islem1.execute("INSERT INTO Proje VALUES ('{}', '{}', '{}')".format(v1,v2,v3))
            self.veritabanı.commit()
        


app = QApplication(sys.argv)
pencerem = MyWindow()
pencerem.show()
sys.exit(app.exec())