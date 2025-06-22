import sys
import sqlite3
import csv
import random
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *

class giziBalita(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("test gizi")
            self.setGeometry(100, 100, 1480, 1300)
            self.conn = sqlite3.connect("D:/KULIAH/6 ipi/pemvis/final/pv25-finalproject-nyetelLagu/data.db")
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #FFE6F0;  /* pink pastel */
                }
            """)

            menubar = self.menuBar()
            menu_menu = menubar.addMenu("menu")
            option_menu = menubar.addMenu("option")
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

            option_menu.addAction(cari_action)
            option_menu.addAction(hapus_action)
            option_menu.addAction(auto_fill_action)

            auto_fill_action.triggered.connect(self.auto_fill)
            hapus_action.triggered.connect(self.delete_data)

            nama_action = QAction("Baiq Luthfida Khairunnisa", self)
            nim_action = QAction("NIM F1D022037", self)
            kelas_action = QAction("Kelas C", self)

            profil_menu.addAction(nama_action)
            profil_menu.addAction(nim_action)
            profil_menu.addAction(kelas_action)

            self.tabs = QTabWidget()
            self.setCentralWidget(self.tabs)

            self.tab1 = QWidget()
            self.tabs.addTab(self.tab1, "hitung gizi")
            self.init_ui_tab1()
            self.tab1.setStyleSheet("""                 
                QLineEdit, QComboBox {
                    background-color: #FFFFFF;
                    border: 2px solid #E8BFD6;
                    border-radius: 10px;
                    padding: 6px 10px;
                    font-family: 'Poppins';
                    font-size: 20px;
                    color: #5D3A7A;
                }
                QLabel {
                    color: #5D3A7A;                
                    font-family: 'Poppins';
                    font-size: 20px;
                    font-weight: bold;
                }

                QTableWidget {
                    background-color: #FFF8FC;
                    font-family: 'Poppins';
                    font-size: 18px;
                    color: #5D3A7A;
                    border: 2px solid #E8BFD6;
                    border-radius: 10px;
                    gridline-color: #E8BFD6;
                }

                QHeaderView::section {
                    background-color: #E8BFD6;
                    color: #5D3A7A;
                    font-weight: bold;
                    font-size: 13px;
                    padding: 6px;
                }
                
                """)


            self.tab2 = QWidget()
            self.tabs.addTab(self.tab2, "grafik gizi")
            self.init_ui_tab2()

            self.tabs.setStyleSheet("""
                QTabBar::tab {
                    min-width: 150px;
                    padding: 10px;
                    margin: 2px;
                }
                QTabBar::tab:selected {
                    background-color: #F8A5C2;  /* Hijau pastel tua */
                    font-weight: bold;
                }
                QTabBar::tab:!selected {
                    background-color: #FDAEAE;  /* Hijau pastel lebih muda */
                }
                QTabWidget::pane {
                    border: none;
                }
            """)

        def init_ui_tab1(self):
            layout = QVBoxLayout()

            # Membuat layout horizontal
            judul_layout = QHBoxLayout()

            # Gambar icon (ganti path dengan gambar kamu)
            icon_label = QLabel()
            icon_pixmap = QPixmap("bear.png") 
            icon_pixmap = icon_pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)

            icon_label2 = QLabel()
            icon_pixmap2 = QPixmap("bear.png") 
            icon_pixmap2 = icon_pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label2.setPixmap(icon_pixmap)

            # Teks judul
            self.judul = QLabel("Yuk Hitung Gizi Balita")
            self.judul.setStyleSheet("""
                color: #5D3A7A;
                font-family: 'Comic Sans MS';
                font-size: 42px;
                font-weight: bold;
                letter-spacing: 1px;
                padding-top: 12px;
                padding-bottom: 42px;
            """)
            self.judul.setAlignment(Qt.AlignVCenter)

            # Tambahkan icon dan teks ke layout horizontal
            judul_layout.addWidget(icon_label)
            judul_layout.addWidget(self.judul)
            judul_layout.addWidget(icon_label2)
            judul_layout.setAlignment(Qt.AlignHCenter)

            # Tambahkan layout ini ke layout utama
            layout.addLayout(judul_layout)



            self.name_input = QLineEdit()
            self.name_input.setPlaceholderText("nama")
            self.gender_input = QComboBox()
            self.gender_input.addItems(["Laki-laki", "Perempuan"])
            self.umur_input = QLineEdit()
            self.umur_input.setPlaceholderText("Umur (bulan)")
            self.tb_input = QLineEdit()
            self.tb_input.setPlaceholderText("Tinggi Badan (cm)")
            self.bb_input = QLineEdit()
            self.bb_input.setPlaceholderText("Berat Badan (kg)")

            form_layout = QFormLayout()

            form_layout.addRow(QLabel("Nama:"), self.name_input)
            form_layout.addRow(QLabel("Jenis Kelamin:"), self.gender_input)
            form_layout.addRow(QLabel("Umur (bulan):"), self.umur_input)
            form_layout.addRow(QLabel("Tinggi Badan (cm):"), self.tb_input)
            form_layout.addRow(QLabel("Berat Badan (kg):"), self.bb_input)

            layout.addLayout(form_layout)


            self.save_btn = QPushButton("Simpan dan Check Gizi")
            self.save_btn.clicked.connect(self.save_data)
            self.save_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFB6C1;     /* Pink pastel */
                    color: #6A0572;                /* Ungu untuk teks */
                    font-family: 'Comic Sans MS';  /* Font lucu */
                    font-size: 20px;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 10px;
                    border: 2px solid #FF69B4;
                }
                QPushButton:hover {
                    background-color: #FF99CC;     /* Saat hover */
                }
            """)

            self.export_btn = QPushButton("Ekspor ke CSV")
            self.export_btn.clicked.connect(self.export_to_csv)
            self.export_btn.setStyleSheet("""
                QPushButton {
                    background-color: #B4F8C8;         /* hijau pastel lembut */
                    color: #1C6E5E;                     /* Ungu untuk teks */
                    font-family: 'Comic Sans MS';  /* Font lucu */
                    font-size: 20px;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 10px;
                    border: 2px solid #99E2B4;
                }
                QPushButton:hover {
                    background-color: #FF99CC;     /* Saat hover */
                }
            """)


            btn_layout = QHBoxLayout()
            btn_layout.addWidget(self.export_btn)   # kiri
            btn_layout.addWidget(self.save_btn)     # kanan

            # Tambahkan ke layout utama
            layout.addLayout(btn_layout)


            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("Cari anak...")
            self.search_input.textChanged.connect(self.load_data)
            layout.addWidget(self.search_input)

            self.table = QTableWidget()
            self.table.setColumnCount(7)
            self.table.setHorizontalHeaderLabels(["ID", "Nama", "Kelamin", "umur", "TB", "BB", "Status"])
            self.table.cellChanged.connect(self.update_data)
            layout.addWidget(self.table)

            self.delete_btn = QPushButton("Hapus Data")
            self.delete_btn.setStyleSheet("background-color: orange;")
            self.delete_btn.clicked.connect(self.delete_data)
            layout.addWidget(self.delete_btn)

            self.tab1.setLayout(layout)
            self.load_data()

        def init_ui_tab2(self):
            layout = QVBoxLayout()

            figure = Figure(figsize=(4, 3))
            self.canvas = FigureCanvas(figure)
            layout.addWidget(self.canvas)
            self.ax = figure.add_subplot(111)

            self.plot_gizi_data()

            self.tab2.setLayout(layout)

        def plot_gizi_data(self):

            cur = self.conn.cursor()
            cur.execute("SELECT status_gizi, COUNT(*) FROM gizi GROUP BY status_gizi")
            data = cur.fetchall()
            labels = [row[0] for row in data]
            counts = [row[1] for row in data]

            self.ax.clear()
            colors = ['#FFC0CB', '#FF69B4', '#DB7093', '#FFB6C1', '#FF85A2']  # variasi pink
            self.ax.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
            self.ax.set_title("Distribusi Status Gizi Anak")
            self.canvas.draw()

        def cek_gizi_manual(self, umur, tb, bb):
            try:
                umur = int(umur)
                tb = float(tb)
                bb = float(bb)

                # Contoh aturan gizi berdasarkan rentang nilai manual
                if umur <= 12:
                    if tb < 65 or bb < 6:
                        return "Gizi Buruk"
                    elif 65 <= tb <= 75 and 6 <= bb <= 9:
                        return "Gizi Normal"
                    else:
                        return "Gizi Lebih"

                elif 13 <= umur <= 24:
                    if tb < 75 or bb < 8:
                        return "Gizi Buruk"
                    elif 75 <= tb <= 85 and 8 <= bb <= 11:
                        return "Gizi Normal"
                    else:
                        return "Gizi Lebih"

                elif 25 <= umur <= 36:
                    if tb < 85 or bb < 10:
                        return "Gizi Buruk"
                    elif 85 <= tb <= 95 and 10 <= bb <= 13:
                        return "Gizi Normal"
                    else:
                        return "Gizi Lebih"

                elif 37 <= umur <= 60:
                    if tb < 95 or bb < 12:
                        return "Gizi Buruk"
                    elif 95 <= tb <= 110 and 12 <= bb <= 17:
                        return "Gizi Normal"
                    else:
                        return "Gizi Lebih"

                else:
                    return "Data luar rentang balita (0–60 bulan)"
            
            except:
                return "Input tidak valid"

        def save_data(self):
            nama = self.name_input.text()
            jenis_kelamin = self.gender_input.currentText()
            umur = self.umur_input.text()
            tb = self.tb_input.text()
            bb = self.bb_input.text()
            status = self.cek_gizi_manual(umur, tb, bb)
            if not nama or not jenis_kelamin or not umur or not tb or not bb:
                QMessageBox.warning(self, "Input Kosong", "Semua kolom harus diisi sebelum menyimpan.")
                return
            cur = self.conn.cursor()
            cur.execute("INSERT INTO gizi (nama, kelamin, umur, tb, bb, status_gizi) VALUES (?, ?, ?, ?, ?, ?)", (nama, jenis_kelamin, umur, tb, bb, status))
            self.conn.commit()
            self.name_input.clear()
            self.gender_input.setCurrentIndex(0)
            self.umur_input.clear()
            self.tb_input.clear()
            self.bb_input.clear()
            self.load_data()

        def load_data(self, text=None):
            # Pastikan text adalah string, kalau None jadi string kosong
            if text is None:
                text = self.search_input.text()
            search = text.strip()  # bersihkan spasi

            query = "SELECT * FROM gizi WHERE nama LIKE ?" if search else "SELECT * FROM gizi"
            cur = self.conn.cursor()
            if search:
                cur.execute(query, ('%' + search + '%',))
            else:
                cur.execute(query)

            records = cur.fetchall()
            self.table.blockSignals(True)
            self.table.setRowCount(0)
            for row_data in records:
                row_number = self.table.rowCount()
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_number, column_number, item)
            self.table.blockSignals(False)


        def update_data(self, row, col):
            id_item = self.table.item(row, 0)
            new_value = self.table.item(row, col).text()
            field = ['id', 'nama', 'kelamin', 'umur', 'tb', 'bb'][col]
            cur = self.conn.cursor()
            cur.execute(f"UPDATE gizi SET {field} = ? WHERE id = ?", (new_value, id_item.text()))
            self.conn.commit()

        def delete_data(self):
            selected = self.table.currentRow()
            if selected < 0:
                QMessageBox.warning(self, "Tidak Ada Data", "Pilih satu buku terlebih dahulu untuk dihapus.")
                return

            judul = self.table.item(selected, 1).text()
            reply = QMessageBox.question(
                self, "Konfirmasi Hapus", f"Apakah yakin ingin menghapus buku berjudul '{judul}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                id_item = self.table.item(selected, 0)
                cur = self.conn.cursor()
                cur.execute("DELETE FROM gizi WHERE id = ?", (id_item.text(),))
                self.conn.commit()
                self.load_data()

        def export_to_csv(self):
            path, _ = QFileDialog.getSaveFileName(self, "Simpan File", "", "CSV Files (*.csv)")
            if path:
                cur = self.conn.cursor()
                cur.execute("SELECT * FROM gizi")
                records = cur.fetchall()
                with open(path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Nama", "Kelamin", "Umur", "Tinggi Badan", "Berat Badan", "Status Gizi"])
                    writer.writerows(records)

        def auto_fill(self):
            self.name_input.setText("fulan")
            self.gender_input.setCurrentIndex(0)
            self.umur_input.setText("41")
            self.tb_input.setText("100")
            self.bb_input.setText("15")
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = giziBalita()
    window.show()
    sys.exit(app.exec_())