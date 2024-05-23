from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class TableWidgetConfig:
    @staticmethod 
    def setDimensions(table_widget: QTableWidget, width: int, height: int):
        """
        Set cell dimensions for a QTableWidget.
        """
        width = int(width)
        height = int(height)

        for col in range(table_widget.columnCount()):
            table_widget.setColumnWidth(col, width)

        for row in range(table_widget.rowCount()):
            table_widget.setRowHeight(row, height)

    @staticmethod
    def setSize(table_widget: QTableWidget, column_count: int, row_count: int):
        """
        set column and row count for a QTableWidget.
        """

        column_count = int(column_count)
        row_count = int(row_count)

        table_widget.setColumnCount(column_count)
        table_widget.setRowCount(row_count)

    @staticmethod
    def setDataDicts(table_widget: QTableWidget, data: list, adjust_size: bool = False, use_keys: bool = False):
        """
        Set data for a QTableWidget from a list of dictionaries.
        """        
        if adjust_size:
            TableWidgetConfig.setSize(table_widget, len(max(data, key=len)), len(data))

        if use_keys:
            table_widget.setHorizontalHeaderLabels(list(max(data, key=len).keys()) if data else [])

        for row, row_data in enumerate(data):
            for col, (key, value) in enumerate(row_data.items()):
                item = QTableWidgetItem(str(value))
                table_widget.setItem(row, col, item)
