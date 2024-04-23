from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QWidget, QInputDialog, QMessageBox, QLabel, QLineEdit, QFileDialog
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
from locker import Locker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wick Locker")
        self.setGeometry(100, 100, 500, 550)
        
        self.setWindowIcon(QIcon("logo.png"))
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(38, 38, 38))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(38, 38, 38))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(38, 85, 231))
        palette.setColor(QPalette.Highlight, QColor(38, 85, 231))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
            }
            QListWidget {
                background-color: #191919;
                border: 1px solid #2655E7;
                border-radius: 5px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #2655E7;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #2655E7;
                color: #FFFFFF;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1E439C;
            }
            QLineEdit {
                background-color: #191919;
                color: #FFFFFF;
                border: 1px solid #2655E7;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        
        self.locker = Locker(self)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png")
        logo_pixmap = logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        title_label = QLabel("Wick Locker")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        self.locked_list = QListWidget()
        self.locked_list.setFont(QFont("Arial", 12))
        layout.addWidget(self.locked_list)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        add_button = QPushButton("Add Passcode")
        add_button.clicked.connect(self.add_passcode)
        buttons_layout.addWidget(add_button)
        
        remove_button = QPushButton("Remove Passcode")
        remove_button.clicked.connect(self.remove_passcode)
        buttons_layout.addWidget(remove_button)
        
        reset_button = QPushButton("Reset Passcode")
        reset_button.clicked.connect(self.reset_passcode)
        buttons_layout.addWidget(reset_button)
        
        layout.addLayout(buttons_layout)
        
        copyright_label = QLabel("© 2023 Wick Locker. All rights reserved.")
        copyright_label.setFont(QFont("Arial", 10))
        copyright_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(copyright_label)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.load_locked_items()
    
    def load_locked_items(self):
        locked_items = self.locker.get_locked_items()
        self.locked_list.clear()
        self.locked_list.addItems(locked_items)
        
        self.locked_list.itemDoubleClicked.connect(self.unlock_item)
    
    def add_passcode(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        
        item_type, ok = QInputDialog.getItem(self, "Select Item Type", "Choose the type of item to lock:", ["File", "Folder/App"], 0, False)
        if ok:
            if item_type == "File":
                item, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
            else:
                item = QFileDialog.getExistingDirectory(self, "Select Folder/App", options=options)
            
            if item:
                passcode, ok = QInputDialog.getText(self, "Add Passcode", "Enter the passcode:", QLineEdit.Password)
                if ok and passcode:
                    self.locker.add_passcode(item, passcode)
                    self.load_locked_items()
    
    def remove_passcode(self):
        item = self.locked_list.currentItem()
        if item:
            self.locker.remove_passcode(item.text())
            self.load_locked_items()
        else:
            QMessageBox.warning(self, "Remove Passcode", "Please select an item from the list.")
    
    def unlock_item(self, item):
        self.locker.unlock_item(item.text())
    
    def reset_passcode(self):
        item = self.locked_list.currentItem()
        if item:
            self.locker.reset_passcode(item.text())
        else:
            QMessageBox.warning(self, "Reset Passcode", "Please select an item from the list.")