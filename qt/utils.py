from PyQt5.QtWidgets import QLabel


def clearLayout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().deleteLater()


class BuddyLabel(QLabel):
    def __init__(self, buddy, parent=None):
        super(BuddyLabel, self).__init__(parent)
        self.buddy = buddy
        self.buddy.hide()

    # When it's clicked, hide itself and show its buddy
    def mousePressEvent(self, event):
        self.hide()
        self.buddy.show()
        self.buddy.setFocus()  # Set focus on buddy so user doesn't have to click again


def textEdited(label, edit):
    def func():
        if edit.text():
            label.setText(str(edit.text()))
            edit.hide()
            label.show()
        else:
            # If the input is left empty, revert back to the label showing
            edit.hide()
            label.show()

    return func
