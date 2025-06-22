from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys
import sqlite3
import csv
from PyQt5.QtWidgets import QMessageBox

class NutriCheck(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gizi.ui", self)
        self.setWindowTitle("pipi musik")
        self.conn = sqlite3.connect("D:/KULIAH/6 ipi/pemvis/final/pv25-finalproject-nyetelLagu/data.db")

        menubar = self.menuBar()
        menu_menu = menubar.addMenu("menu")
        option_menu = menubar.addMenu("Option")
        profil_menu = menubar.addMenu("Profil")

        save_action = QAction("Simpan", self)
        export_action = QAction("Ekspor ke CSV", self)
        exit_action = QAction("Keluar", self)

        menu_menu.addAction(save_action)
        menu_menu.addAction(export_action)
        menu_menu.addAction(exit_action)

        save_action.triggered.connect(self.save_data)  
        export_action.triggered.connect(self.export_to_csv)
        exit_action.triggered.connect(self.close)

        cari_action = QAction("Cari anak", self)
        hapus_action = QAction("Hapus anak", self)
        auto_fill_action = QAction("Auto Fill", self)

        option_menu = menubar.addMenu("option")
        option_menu.addAction(cari_action)
        option_menu.addAction(hapus_action)
        option_menu.addAction(auto_fill_action)

        cari_action.triggered.connect(self.cari_anak)
        hapus_action.triggered.connect(self.hapus_anak)
        auto_fill_action.triggered.connect(self.auto_fill)

        nama_action = QAction("Baiq Luthfida Khairunnisa", self)
        nim_action = QAction("NIM F1D022037", self)
        kelas_action = QAction("Kelas C", self)

        profil_menu.addAction(nama_action)
        profil_menu.addAction(nim_action)
        profil_menu.addAction(kelas_action)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.form_ui = uic.loadUi("gizi.ui")  # ganti dengan nama file .ui kamu
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(self.form_ui)
        self.tab1.setLayout(tab1_layout)
        self.tabs.addTab(self.tab1, "hitung gizi")

        # TAB 2: Manual Statistik
        self.tab2 = QWidget()
        self.stat_label = QLabel("Statistik akan muncul di sini")
        self.stat_btn = QPushButton("Lihat Statistik")
        self.stat_btn.clicked.connect(self.show_stats)

        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(self.stat_label)
        tab2_layout.addWidget(self.stat_btn)
        self.tab2.setLayout(tab2_layout)
        self.tabs.addTab(self.tab2, "Statistik")

    def show_stats(self):
        cur = self.conn.cursor()
        cur.execute("SELECT status, COUNT(*) FROM anak GROUP BY status")
        rows = cur.fetchall()
        teks = "Statistik Gizi:<br>"
        for s, jml in rows:
            teks += f"{s}: {jml} anak<br>"
        self.stat_label.setText(teks)

    def export_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan CSV", "", "CSV Files (*.csv)")
        if path:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM anak")
            rows = cur.fetchall()
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nama", "Umur", "JK", "BB", "TB", "Status"])
                writer.writerows(rows)

    def save_data(self):
            nama = self.title_input.text()
            kelamin = self.author_input.text()
            umur = self.year_input.text()
            tb = self.album_input.text()
            bb = self.genre_input.text()

            if not title or not author or not year or not album or not genre or not song:
                QMessageBox.warning(self, "Input Kosong", "Semua kolom harus diisi sebelum menyimpan.")
                return
            cur = self.conn.cursor()
            cur.execute("INSERT INTO song (judul, pengarang, tahun, album, genre, lagu) VALUES (?, ?, ?, ?, ?, ?)", (title, author, year, album, genre, song))
            self.conn.commit()
            self.title_input.clear()
            self.author_input.clear()
            self.year_input.clear()
            self.album_input.clear()
            self.genre_input.clear()
            self.song_input.clear()
            self.load_data()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = NutriCheck()
    window.show()
    sys.exit(app.exec_())
