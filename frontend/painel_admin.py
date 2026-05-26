from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem, QLineEdit, 
                             QHeaderView, QMessageBox, QFrame, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from backend.db_admin import DBAdmin

class PainelAdmin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DB Admin - Painel de Controle CRM")
        self.setMinimumSize(1100, 700)
        self.admin_backend = DBAdmin()
        
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: #E0E0E0;
            }
            QLabel {
                color: #00E5FF;
                font-weight: bold;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                background-color: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
            QTableWidget {
                background-color: #1E1E1E;
                alternate-background-color: #252525;
                gridline-color: #2A2A2A;
                color: #E0E0E0;
                border: none;
                selection-background-color: #005BB7;
            }
            QHeaderView::section {
                background-color: #252525;
                color: #00E5FF;
                padding: 5px;
                border: 1px solid #2A2A2A;
                font-weight: bold;
            }
            QPushButton {
                background-color: #2D2D2D;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3D3D3D;
            }
            #BtnSearch {
                background-color: #005BB7;
            }
            #BtnSearch:hover {
                background-color: #0078D7;
            }
            #BtnDelete {
                background-color: #550000;
            }
            #BtnDelete:hover {
                background-color: #770000;
            }
            #BtnDanger {
                background-color: #8B0000;
                color: white;
                font-weight: bold;
            }
            #BtnDanger:hover {
                background-color: #FF3333;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header / Filtros
        header_layout = QHBoxLayout()
        
        self.lbl_tabela = QLabel("Tabela:")
        header_layout.addWidget(self.lbl_tabela)
        
        self.combo_tabelas = QComboBox()
        self.combo_tabelas.addItems(['contas', 'equipes_vendas', 'metadados', 'pipeline_vendas', 'produtos'])
        self.combo_tabelas.setFixedWidth(200)
        header_layout.addWidget(self.combo_tabelas)

        self.txt_busca = QLineEdit()
        self.txt_busca.setPlaceholderText("Pesquisar termo...")
        header_layout.addWidget(self.txt_busca)

        self.btn_search = QPushButton("🔍 PESQUISAR")
        self.btn_search.setObjectName("BtnSearch")
        self.btn_search.clicked.connect(self.atualizar_tabela)
        header_layout.addWidget(self.btn_search)

        layout.addLayout(header_layout)

        # Tabela
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Rodapé de Ações
        footer_layout = QHBoxLayout()
        
        self.btn_delete = QPushButton("🗑️ DELETAR SELECIONADO")
        self.btn_delete.setObjectName("BtnDelete")
        self.btn_delete.clicked.connect(self.confirmar_delecao)
        footer_layout.addWidget(self.btn_delete)
        
        footer_layout.addStretch()

        self.btn_truncate = QPushButton("🧨 LIMPAR TODO O BANCO")
        self.btn_truncate.setObjectName("BtnDanger")
        self.btn_truncate.clicked.connect(self.confirmar_truncar)
        footer_layout.addWidget(self.btn_truncate)

        layout.addLayout(footer_layout)

        # Carregamento inicial
        self.atualizar_tabela()

    def atualizar_tabela(self):
        tabela = self.combo_tabelas.currentText()
        busca = self.txt_busca.text()
        
        colunas, dados = self.admin_backend.buscar_registros(tabela, termo_busca=busca)
        
        self.table.setColumnCount(len(colunas))
        self.table.setHorizontalHeaderLabels(colunas)
        self.table.setRowCount(len(dados))

        for row_idx, row_data in enumerate(dados):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.table.setItem(row_idx, col_idx, item)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def confirmar_delecao(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Aviso", "Selecione uma linha para deletar.")
            return

        row = selected_rows[0].row()
        # Assume que a primeira coluna é sempre o ID
        col_id = self.table.horizontalHeaderItem(0).text()
        val_id = self.table.item(row, 0).text()
        tabela = self.combo_tabelas.currentText()

        resposta = QMessageBox.warning(
            self, "Confirmação", 
            f"Tem certeza que deseja deletar o registro {val_id} da tabela '{tabela}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            sucesso = self.admin_backend.deletar_registro(tabela, col_id, val_id)
            if sucesso:
                QMessageBox.information(self, "Sucesso", "Registro removido.")
                self.atualizar_tabela()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível deletar o registro.")

    def confirmar_truncar(self):
        resposta = QMessageBox.critical(
            self, "ALERTA CRÍTICO", 
            "VOCÊ ESTÁ PRESTES A APAGAR TODOS OS DADOS DO BANCO!\n\nEssa ação é irreversível. Deseja continuar?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            # Segunda confirmação para segurança extrema
            segunda_resposta = QMessageBox.question(
                self, "Última Chance", 
                "TEM CERTEZA ABSOLUTA?", 
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if segunda_resposta == QMessageBox.Yes:
                sucesso, mensagem = self.admin_backend.truncar_todas_tabelas()
                if sucesso:
                    QMessageBox.information(self, "Sucesso", mensagem)
                    self.atualizar_tabela()
                else:
                    QMessageBox.critical(self, "Erro SQL", mensagem)
