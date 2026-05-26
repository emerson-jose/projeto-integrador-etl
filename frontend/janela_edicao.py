from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt
from backend.db_manager import DBManager

class DialogEdicao(QDialog):
    """Janela Pop-up para edição direta de registros do banco."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edição de Registros - CRM")
        self.resize(1100, 700)
        self.db = DBManager()
        self.init_ui()
        self.carregar_dados()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #121212; color: white;")

        self.table = QTableWidget()
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btn_salvar = QPushButton("💾 SALVAR ALTERAÇÕES")
        self.btn_salvar.setObjectName("PrimaryBtn")
        self.btn_salvar.clicked.connect(self.salvar_alteracoes)
        
        self.btn_cancelar = QPushButton("CANCELAR")
        self.btn_cancelar.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancelar)
        btn_layout.addWidget(self.btn_salvar)
        layout.addLayout(btn_layout)

    def carregar_dados(self):
        df = self.db.get_dados_completos().head(100) # Últimos 100 registros
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        for i, row in df.iterrows():
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                # Travar edição do ID
                if df.columns[j] == 'id_oportunidade':
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, j, item)

    def salvar_alteracoes(self):
        linhas_alteradas = 0
        for row in range(self.table.rowCount()):
            id_op = self.table.item(row, 0).text()
            # Mapeamento dinâmico para evitar erros de índice se a query mudar
            novos_dados = {
                'fase_negociacao': self.table.item(row, 4).text(),
                'valor_fechamento': float(self.table.item(row, 7).text().replace(',', ''))
            }
            if self.db.atualizar_oportunidade(id_op, novos_dados):
                linhas_alteradas += 1
        
        QMessageBox.information(self, "Sucesso", f"{linhas_alteradas} registros atualizados!")
        self.accept()
