import sys, os, ctypes, platform, shutil
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QCheckBox, QMessageBox, QFrame, 
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class OlimpusGuard(QWidget):
    def __init__(self):
        super().__init__()
        # Dosya yollarını kesinleştir
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if platform.system() == "Windows" else "/etc/hosts"
        self.backup_path = self.hosts_path + ".bak"
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(450, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Ana Arka Plan Kartı (CustomTkinter Stilinde)
        self.container = QFrame(self)
        self.container.setGeometry(10, 10, 430, 580)
        self.container.setStyleSheet("""
            QFrame {
                background-color: #0d1117;
                border-radius: 20px;
                border: 2px solid #30363d;
            }
        """)

        # Gölge Efekti (Derinlik hissi için)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(40, 40, 40, 40)

        # Kapatma Butonu
        close_btn = QPushButton("✕", self.container)
        close_btn.setGeometry(390, 15, 25, 25)
        close_btn.setStyleSheet("color: #8b949e; border: none; font-size: 16px; font-weight: bold;")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.close)

        # Logo
        self.logo = QLabel("OLIMPUS")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setStyleSheet("color: #ffffff; font-size: 32px; font-weight: 900; letter-spacing: 5px;")
        layout.addWidget(self.logo)

        self.brand = QLabel("GUARD")
        self.brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.brand.setStyleSheet("color: #58a6ff; font-size: 12px; font-weight: bold; letter-spacing: 10px; margin-bottom: 20px;")
        layout.addWidget(self.brand)

        # Yasal Onay Metni
        self.info = QLabel("YASAL NOT: OlimpusGuard, kullanıcı onayıyla sistem DNS ayarlarını değiştirir. Yapımcı hiçbir sorumluluk kabul etmez.")
        self.info.setWordWrap(True)
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info.setStyleSheet("background-color: #161b22; color: #8b949e; padding: 15px; border-radius: 10px; font-size: 10px;")
        layout.addWidget(self.info)

        # Onay Checkbox
        self.check = QCheckBox("Tüm sorumluluğu kabul ediyorum.")
        self.check.setStyleSheet("""
            QCheckBox { color: #c9d1d9; font-size: 11px; margin-top: 20px; }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 2px solid #30363d; }
            QCheckBox::indicator:checked { background-color: #238636; border: 2px solid #238636; }
        """)
        layout.addWidget(self.check)

        # Aksiyon Butonları
        self.btn_start = self.create_btn("KORUMAYI ETKİNLEŞTİR", "#238636", "#ffffff")
        self.btn_start.clicked.connect(self.run_shield)
        layout.addWidget(self.btn_start)

        self.btn_reset = self.create_btn("SİSTEMİ RESTORE ET", "#21262d", "#c9d1d9")
        self.btn_reset.clicked.connect(self.restore)
        layout.addWidget(self.btn_reset)

        self.status = QLabel("SYSTEM: STANDBY")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("color: #484f58; font-size: 9px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(self.status)

    def create_btn(self, text, bg, fg):
        btn = QPushButton(text)
        btn.setFixedHeight(50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg}; color: {fg};
                border-radius: 10px; font-weight: bold; font-size: 11px;
            }}
            QPushButton:hover {{ background-color: #ffffff; color: #000000; }}
        """)
        return btn

    def run_shield(self):
        if not self.check.isChecked():
            QMessageBox.warning(self, "OlimpusGuard", "Lütfen yasal onayı işaretleyin.")
            return
        try:
            if not os.path.exists(self.backup_path):
                shutil.copy(self.hosts_path, self.backup_path)
            
            with open(self.hosts_path, "a") as f:
                f.write("\n127.0.0.1 www.doubleclick.net\n127.0.0.1 ads.youtube.com")
            
            self.status.setText("SYSTEM: PROTECTED")
            self.status.setStyleSheet("color: #238636; font-size: 9px; font-weight: bold;")
            QMessageBox.information(self, "OlimpusGuard", "Koruma aktif edildi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya hatası: {e}")

    def restore(self):
        if os.path.exists(self.backup_path):
            shutil.copy(self.backup_path, self.hosts_path)
            self.status.setText("SYSTEM: STANDBY")
            QMessageBox.information(self, "OlimpusGuard", "Sistem geri yüklendi.")
        else:
            QMessageBox.warning(self, "Hata", "Yedek bulunamadı.")

    # Pencere Sürükleme Mantığı
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            diff = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.x() + diff.x(), self.y() + diff.y())
            self.drag_pos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
    
    window = OlimpusGuard()
    window.show()
    sys.exit(app.exec())