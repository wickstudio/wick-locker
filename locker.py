import json
import os
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QLineEdit

class Locker:
    def __init__(self, parent=None):
        self.parent = parent
        self.data_file = "data.json"
        self.lock_file = "locker.lock"
        self.locked_items = self.load_data()
    
    def load_data(self):
        try:
            with open(self.data_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump(self.locked_items, file)
    
    def get_locked_items(self):
        return list(self.locked_items.keys())
    
    def add_passcode(self, item, passcode):
        self.locked_items[item] = passcode
        self.lock_item(item)
        self.save_data()
    
    def remove_passcode(self, item):
        if item in self.locked_items:
            passcode, ok = QInputDialog.getText(self.parent, "Enter Passcode", "Please enter the passcode to remove:", QLineEdit.Password)
            if ok and self.check_passcode(item, passcode):
                del self.locked_items[item]
                self.unlock_item(item, True)
                self.save_data()
            else:
                QMessageBox.warning(self.parent, "Invalid Passcode", "Access denied. Invalid passcode.")
    
    def check_passcode(self, item, passcode):
        if item in self.locked_items:
            return self.locked_items[item] == passcode
        return True
    
    def is_locked(self, item):
        lock_file = item + ".lock"
        return os.path.exists(lock_file)
    
    def lock_item(self, item):
        if os.path.exists(item):
            lock_file = item + ".lock"
            open(lock_file, "w").close()
            os.system(f'attrib +h "{item}"')
    
    def unlock_item(self, item, force=False):
        if self.is_locked(item) and not force:
            passcode, ok = QInputDialog.getText(self.parent, "Enter Passcode", "Please enter the passcode to unlock:", QLineEdit.Password)
            if ok and self.check_passcode(item, passcode):
                self._unlock_item(item)
            else:
                QMessageBox.warning(self.parent, "Invalid Passcode", "Access denied. Invalid passcode.")
        else:
            self._unlock_item(item)
    
    def _unlock_item(self, item):
        lock_file = item + ".lock"
        if os.path.exists(lock_file):
            os.remove(lock_file)
        os.system(f'attrib -h "{item}"')
    
    def reset_passcode(self, item):
        if item in self.locked_items:
            password, ok = QInputDialog.getText(self.parent, "Reset Passcode", "Enter the password to reset the passcode:", QLineEdit.Password)
            if ok and password == "WickLocker":
                new_passcode, ok = QInputDialog.getText(self.parent, "Reset Passcode", "Enter the new passcode:", QLineEdit.Password)
                if ok and new_passcode:
                    self.locked_items[item] = new_passcode
                    self.save_data()
                    QMessageBox.information(self.parent, "Passcode Reset", "The passcode has been reset successfully.")
            else:
                QMessageBox.warning(self.parent, "Invalid Password", "Access denied. Invalid password.")
        else:
            QMessageBox.warning(self.parent, "Invalid Item", "The selected item is not locked.")