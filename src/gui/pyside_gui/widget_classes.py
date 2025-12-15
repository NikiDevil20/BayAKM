# python
from PySide6.QtWidgets import (QWidget, QHBoxLayout,
                               QPushButton, QLineEdit,
                               QVBoxLayout, QTableWidget,
                               QCheckBox, QTableWidgetItem,
                               QSizePolicy)
from PySide6.QtCore import Signal, Qt

class CounterWidget(QWidget):
    value_changed = Signal(int)

    def __init__(self, parent=None, minimum: int = 1, maximum: int = 10, value: int | None = None):
        super().__init__(parent)
        self._min = minimum
        self._max = maximum
        self._value = (value if value is not None else self._min)

        self.dec_btn = QPushButton("-")
        self.inc_btn = QPushButton("+")
        self.display = QLineEdit(str(self._value))
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setFrame(False)
        self.display.setStyleSheet("border: none, background: transparent")
        self.display.setFixedWidth(60)

        hl = QHBoxLayout(self)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.addWidget(self.dec_btn)
        hl.addWidget(self.display)
        hl.addWidget(self.inc_btn)

        self.dec_btn.clicked.connect(self._decrease)
        self.inc_btn.clicked.connect(self._increase)

        self._update_buttons()

    def _decrease(self):
        self.set_value(self._value - 1)

    def _increase(self):
        self.set_value(self._value + 1)

    def set_value(self, val: int):
        val = max(self._min, min(self._max, int(val)))
        if val == self._value:
            return
        self._value = val
        self.display.setText(str(self._value))
        self._update_buttons()
        self.value_changed.emit(self._value)

    def _update_buttons(self):
        self.dec_btn.setEnabled(self._value > self._min)
        self.inc_btn.setEnabled(self._value < self._max)

    def value(self) -> int:
        return self._value


class CreateChoiceTable(QWidget):
    def __init__(self, data: list[str]):
        super().__init__()

        self.data: list[str] = data

        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["", "Name"])

        self.populate_table()

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

    def populate_table(self):
        self.table.setRowCount(len(self.data))

        for row, name in enumerate(self.data):
            checkbox = QCheckBox()
            checkbox.setChecked(False)

            cell_widget = QWidget()
            hlayout = QHBoxLayout(cell_widget)
            hlayout.setContentsMargins(0, 0, 0, 0)
            hlayout.addWidget(checkbox, 0, Qt.AlignCenter)

            self.table.setCellWidget(row, 0, cell_widget)

            name_item = QTableWidgetItem(name)
            name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 1, name_item)

    def get_selected(self) -> list[str]:
        selected = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0).findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                name = self.table.item(row, 1).text()
                selected.append(name)
        return selected
