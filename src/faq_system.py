import sys
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QTableView, QPushButton, QDialog, QFormLayout,
                            QLineEdit, QComboBox, QDialogButtonBox, QFileDialog,
                            QAction, QHeaderView, QAbstractScrollArea, QAbstractItemView,
                            QTextEdit, QMenu)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class FAQViewDialog(QDialog):
    def __init__(self, parent=None, faq_data=None):
        super().__init__(parent)
        self.setWindowTitle('查看FAQ')
        self.resize(800, 600)
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setVerticalSpacing(15)
        
        self.app_name = QLineEdit()
        self.question = QLineEdit()
        self.solution = QTextEdit()
        self.notes = QTextEdit()
        
        # 设置为只读
        self.app_name.setReadOnly(True)
        self.question.setReadOnly(True)
        self.solution.setReadOnly(True)
        self.notes.setReadOnly(True)
        
        # 设置最小尺寸
        self.solution.setMinimumHeight(150)
        self.notes.setMinimumHeight(80)
        
        form_layout.addRow('所属应用:', self.app_name)
        form_layout.addRow('问题:', self.question)
        form_layout.addRow('解决方法:', self.solution)
        form_layout.addRow('备注:', self.notes)
        
        main_layout.addLayout(form_layout)
        
        if faq_data:
            self.app_name.setText(faq_data[2])
            self.question.setText(faq_data[3])
            self.solution.setPlainText(faq_data[4])
            self.notes.setPlainText(faq_data[5] if faq_data[5] else '')

class FAQDialog(QDialog):
    def __init__(self, parent=None, faq_data=None):
        super().__init__(parent)
        self.setWindowTitle('添加FAQ' if not faq_data else '编辑FAQ')
        self.resize(800, 600)
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setVerticalSpacing(15)
        
        self.app_name = QLineEdit()
        self.question = QLineEdit()
        self.solution = QTextEdit()
        self.notes = QTextEdit()
        
        # 设置自动补全
        completer = QComboBox()
        completer.addItems(self.get_existing_app_names())
        completer.setEditable(True)
        self.app_name.setCompleter(completer.completer())
        
        # 设置最小尺寸
        self.solution.setMinimumHeight(150)
        self.notes.setMinimumHeight(80)
        
        form_layout.addRow('所属应用:', self.app_name)
        form_layout.addRow('问题:', self.question)
        form_layout.addRow('解决方法:', self.solution)
        form_layout.addRow('备注:', self.notes)
        
        main_layout.addLayout(form_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(buttons)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        if faq_data:
            self.app_name.setText(faq_data[2])
            self.question.setText(faq_data[3])
            self.solution.setText(faq_data[4])
            self.notes.setText(faq_data[5] if faq_data[5] else '')

    def get_existing_app_names(self):
        self.parent().cursor.execute("SELECT DISTINCT app_name FROM faqs")
        return [row[0] for row in self.parent().cursor.fetchall()]

class FAQSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_excel_path = None
        self.data_modified = False
        self.initUI()
        self.initDB()
        
    def sync_to_excel(self):
        if self.current_excel_path:
            try:
                self.cursor.execute('''
            SELECT original_id, app_name, question, solution, notes 
            FROM faqs 
            ORDER BY CAST(original_id AS INTEGER) ASC
                ''')
                data = self.cursor.fetchall()
                df = pd.DataFrame(data, columns=['序号', '所属应用', '问题', '解决方法', '备注'])
                # 确保按照original_id升序排列后写入Excel
                df = df.sort_values('序号', ascending=True).reset_index(drop=True)
                df.to_excel(self.current_excel_path, index=False)
                self.data_modified = False
                print(f"数据已同步到 {self.current_excel_path}")
            except Exception as e:
                print(f"同步到Excel失败: {str(e)}")
        
    def initUI(self):
        self.setWindowTitle('FAQ知识库系统')
        self.setGeometry(100, 100, 1600, 1066)
        
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('文件')
        
        import_action = QAction('导入', self)
        import_action.triggered.connect(self.import_excel)
        file_menu.addAction(import_action)
        
        export_action = QAction('导出', self)
        export_action.triggered.connect(self.export_excel)
        file_menu.addAction(export_action)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        btn_layout = QWidget()
        btn_box = QHBoxLayout()
        btn_layout.setLayout(btn_box)
        
        self.add_btn = QPushButton('添加')
        self.edit_btn = QPushButton('编辑')
        self.del_btn = QPushButton('删除')
        self.view_btn = QPushButton('查看')
        self.refresh_btn = QPushButton('刷新')
        
        btn_box.addWidget(self.add_btn)
        btn_box.addWidget(self.edit_btn)
        btn_box.addWidget(self.del_btn)
        btn_box.addWidget(self.view_btn)
        btn_box.addWidget(self.refresh_btn)
        btn_box.addSpacing(20)

        # 新增搜索组件
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入关键字")
        self.search_btn = QPushButton('查询')
        btn_box.addWidget(self.search_input)
        btn_box.addWidget(self.search_btn)
        
        # 连接按钮信号
        self.add_btn.clicked.connect(self.add_faq)
        self.edit_btn.clicked.connect(self.edit_faq)
        self.del_btn.clicked.connect(self.delete_faq)
        self.view_btn.clicked.connect(self.view_faq)
        self.refresh_btn.clicked.connect(self.load_data)
        self.search_btn.clicked.connect(self.search_faq)
        
        layout.addWidget(btn_layout)
        
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        layout.addWidget(self.table_view)
        
        self.refresh_btn.clicked.connect(self.load_data)
        self.search_btn.clicked.connect(self.search_faq)
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.create_context_menu)
        self.table_view.doubleClicked.connect(lambda: self.view_faq(by_index=True))
        
    def search_faq(self):
        keyword = self.search_input.text().strip()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['所属应用', '问题', '解决方法', '备注'])
        
        if keyword:
            self.cursor.execute('''
                SELECT app_name, question, solution, notes 
                FROM faqs 
                WHERE question LIKE ? OR solution LIKE ?
            ''', (f'%{keyword}%', f'%{keyword}%'))
        else:
            self.cursor.execute('SELECT app_name, question, solution, notes FROM faqs')
            
        for row in self.cursor.fetchall():
            items = [QStandardItem(str(field)) for field in row]
            model.appendRow(items)
        
        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setSortingEnabled(False)
        self.table_view.doubleClicked.connect(self.view_faq)

    def import_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel文件 (*.xlsx *.xls)"
        )
        if not file_path:
            return
        
        try:
            # 尝试读取Excel文件
            print(f"尝试读取Excel文件: {file_path}")
            df = pd.read_excel(file_path, engine='openpyxl')
            print("Excel文件读取成功")
            df.columns = df.columns.str.strip()
            
            valid_rows = []
            for index, row in df.iterrows():
                if pd.isna(row.get('序号')):
                    continue
                
                original_id = int(row['序号']) if not pd.isna(row['序号']) else 0
                app_name = str(row['所属应用']).strip() if '所属应用' in row and not pd.isna(row['所属应用']) else ''
                question = str(row['问题']).strip() if '问题' in row and not pd.isna(row['问题']) else ''
                solution = str(row['解决方法']).strip() if '解决方法' in row and not pd.isna(row['解决方法']) else ''
                notes = str(row['备注']).strip() if '备注' in row and not pd.isna(row['备注']) else ''
                
                valid_rows.append((original_id, app_name, question, solution, notes))
            
            if valid_rows:
                self.current_excel_path = file_path
                self.cursor.execute('BEGIN TRANSACTION')
                try:
                    self.cursor.execute('DELETE FROM faqs')
                    for data in valid_rows:
                        self.cursor.execute('''
                            INSERT INTO faqs (original_id, app_name, question, solution, notes)
                            VALUES (?, ?, ?, ?, ?)
                        ''', data)
                    self.conn.commit()
                    self.data_modified = True
                    self.sync_to_excel()
                except Exception as e:
                    self.conn.rollback()
                    raise
            self.load_data()
            self.table_view.reset()
        except Exception as e:
            self.conn.rollback()
            print(f"导入失败: {str(e)}")
            import traceback
            traceback.print_exc()
            # 显示错误对话框
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "导入错误", 
                f"导入Excel文件失败:\n\n{str(e)}\n\n详细信息请查看控制台输出")

    def export_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存Excel文件", "", "Excel文件 (*.xlsx)"
        )
        if not file_path:
            return
        
        try:
            self.cursor.execute('SELECT original_id, app_name, question, solution, notes FROM faqs ORDER BY CAST(original_id AS INTEGER) ASC')
            data = self.cursor.fetchall()
            df = pd.DataFrame(data, columns=['序号', '所属应用', '问题', '解决方法', '备注'])
            df.to_excel(file_path, index=False)
        except Exception as e:
            print(f"导出失败: {str(e)}")
        
    def get_selected_faq_id(self, by_index=False):
        if by_index:
            index = self.table_view.currentIndex()
            if not index.isValid():
                return None
            row = index.row()
        else:
            selected = self.table_view.selectionModel().selectedRows()
            if not selected:
                return None
            row = selected[0].row()
        
        model = self.table_view.model()
        app_name = model.index(row, 0).data()
        question = model.index(row, 1).data()
        self.cursor.execute('SELECT id FROM faqs WHERE app_name=? AND question=?',
                          (app_name, question))
        result = self.cursor.fetchone()
        return result[0] if result else None
        
    def get_max_original_id(self):
        self.cursor.execute('SELECT original_id FROM faqs ORDER BY CAST(original_id AS INTEGER) DESC LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def add_faq(self):
        dialog = FAQDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            max_id = self.get_max_original_id()
            new_id = max_id + 1 if max_id else 1
            self.cursor.execute('''
                INSERT INTO faqs (original_id, app_name, question, solution, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                new_id,
                dialog.app_name.text(),
                dialog.question.text(),
                dialog.solution.toPlainText(),
                dialog.notes.toPlainText()
            ))
            self.conn.commit()
            self.data_modified = True
            self.sync_to_excel()
            self.load_data()
            
    def edit_faq(self):
        faq_id = self.get_selected_faq_id()
        if faq_id is None:
            return
        
        self.cursor.execute('SELECT * FROM faqs WHERE id = ?', (faq_id,))
        faq_data = self.cursor.fetchone()
        
        dialog = FAQDialog(self, faq_data)
        if dialog.exec_() == QDialog.Accepted:
            self.cursor.execute('''
                UPDATE faqs SET
                    app_name = ?,
                    question = ?,
                    solution = ?,
                    notes = ?
                WHERE id = ?
            ''', (
                dialog.app_name.text(),
                dialog.question.text(),
                dialog.solution.toPlainText(),
                dialog.notes.toPlainText(),
                faq_id
            ))
            self.conn.commit()
            self.data_modified = True
            self.sync_to_excel()
            self.load_data()
            
    def view_faq(self):
        faq_id = self.get_selected_faq_id()
        if faq_id is None:
            print("请先选择要查看的行")
            return
        
        try:
            self.cursor.execute('SELECT * FROM faqs WHERE id = ?', (faq_id,))
            faq_data = self.cursor.fetchone()
            if not faq_data:
                print("未找到对应的FAQ记录")
                return
            
            dialog = FAQViewDialog(self, faq_data)
            dialog.exec_()
        except Exception as e:
            print(f"查看FAQ时发生错误: {str(e)}")

    def delete_faq(self):
        faq_id = self.get_selected_faq_id()
        if faq_id is None:
            return
        
        self.cursor.execute('DELETE FROM faqs WHERE id = ?', (faq_id,))
        self.conn.commit()
        self.data_modified = True
        self.sync_to_excel()
        self.load_data()

    def initDB(self):
        self.conn = sqlite3.connect('faq_database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''\
            CREATE TABLE IF NOT EXISTS faqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_id INTEGER,
                app_name TEXT,
                question TEXT,
                solution TEXT,
                notes TEXT
            )''')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_app_name ON faqs(app_name)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_question ON faqs(question)')
        self.conn.commit()
        self.load_data()

    def create_context_menu(self, position):
        menu = QMenu()
        
        add_action = menu.addAction("添加")
        add_action.triggered.connect(self.add_faq)
        
        edit_action = menu.addAction("编辑")
        edit_action.triggered.connect(self.edit_faq)
        
        delete_action = menu.addAction("删除")
        delete_action.triggered.connect(self.delete_faq)
        
        view_action = menu.addAction("查看")
        view_action.triggered.connect(self.view_faq)
        
        menu.exec_(self.table_view.viewport().mapToGlobal(position))

    def load_data(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['所属应用', '问题', '解决方法', '备注'])
        self.cursor.execute('''
            SELECT app_name, question, solution, notes 
            FROM faqs
        ''')
        for row in self.cursor.fetchall():
            items = [QStandardItem(str(field)) for field in row]
            model.appendRow(items)
        self.table_view.setModel(model)
        self.table_view.setColumnHidden(0, False)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setSortingEnabled(False)
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.create_context_menu)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FAQSystem()
    window.show()
    sys.exit(app.exec_())
