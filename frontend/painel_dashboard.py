import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QFrame, QLabel, 
                             QPushButton, QComboBox, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal, Slot

# Integração com Matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# Importações locais
from frontend.estilos_visuais import QSS_STYLE
from frontend.componentes_interface import KPICard
from frontend.janela_edicao import DialogEdicao
from backend.db_manager import DBManager
from backend.analytics import CRMAnalytics
from backend.graficos import CRMVisualizer # Mudamos para o Visualizer Estático
from backend.funcoes import lento

class DataLoadWorker(QThread):
    data_loaded = Signal(object)
    error_signal = Signal(str)

    def __init__(self, db_manager, agente="Todos", periodo="Todos"):
        super().__init__()
        self.db = db_manager
        self.agente = agente
        self.periodo = periodo

    def run(self):
        try:
            df = self.db.get_dados_completos(agente=self.agente, periodo=self.periodo)
            self.data_loaded.emit(df)
        except Exception as e:
            self.error_signal.emit(str(e))

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM Cloud Dashboard - Business Intelligence")
        self.resize(1300, 850)
        self.setStyleSheet(QSS_STYLE)

        # Instanciar Backend
        self.db = DBManager()
        self.viz = CRMVisualizer() # Agora usamos Matplotlib
        self.df = None
        
        self.init_ui()
        self.solicitar_dados()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- SIDEBAR ---
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(15)

        lbl_logo = QLabel("CLOUD BI")
        lbl_logo.setObjectName("SidebarTitle")
        sidebar_layout.addWidget(lbl_logo)

        sidebar_layout.addWidget(QLabel("PERÍODO"))
        self.cb_periodo = QComboBox()
        self.cb_periodo.addItems(["Todos", "Último Mês", "Último Trimestre", "Este Ano"])
        sidebar_layout.addWidget(self.cb_periodo)

        sidebar_layout.addWidget(QLabel("AGENTE"))
        self.cb_agente = QComboBox()
        sidebar_layout.addWidget(self.cb_agente)

        sidebar_layout.addSpacing(20)
        self.btn_filtrar = QPushButton("APLICAR FILTROS")
        self.btn_filtrar.setObjectName("PrimaryBtn")
        sidebar_layout.addWidget(self.btn_filtrar)

        sidebar_layout.addStretch()
        self.btn_edit = QPushButton("📝 EDITAR")
        sidebar_layout.addWidget(self.btn_edit)
        self.btn_export = QPushButton("📄 PDF")
        sidebar_layout.addWidget(self.btn_export)

        main_layout.addWidget(sidebar)

        # --- ÁREA DE CONTEÚDO ---
        content_area = QWidget()
        content_area.setObjectName("ContentArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(20)

        # KPIs
        kpi_layout = QHBoxLayout()
        self.card_faturamento = KPICard("FATURAMENTO", "$ 0.00")
        self.card_conversao = KPICard("CONVERSÃO", "0.0%")
        self.card_abertas = KPICard("ABERTAS", "0")
        kpi_layout.addWidget(self.card_faturamento)
        kpi_layout.addWidget(self.card_conversao)
        kpi_layout.addWidget(self.card_abertas)
        content_layout.addLayout(kpi_layout)

        # Gráficos (Usando Matplotlib Canvas)
        self.charts_grid = QGridLayout()
        
        # Criamos os containers para os gráficos
        self.canvas0 = None
        self.canvas1 = None
        self.canvas2 = None
        
        # Layout principal de gráficos
        self.chart_frame0 = QFrame() # Tendência (Linha)
        self.chart_frame1 = QFrame() # Agentes (Barra)
        self.chart_frame2 = QFrame() # Pipeline (Rosca)
        
        self.charts_grid.addWidget(self.chart_frame0, 0, 0, 1, 2)
        self.charts_grid.addWidget(self.chart_frame1, 1, 0)
        self.charts_grid.addWidget(self.chart_frame2, 1, 1)

        content_layout.addLayout(self.charts_grid)
        main_layout.addWidget(content_area)

        # Eventos
        self.btn_filtrar.clicked.connect(self.solicitar_dados)
        self.btn_export.clicked.connect(self.exportar_pdf)
        self.btn_edit.clicked.connect(self.abrir_edicao)

    def solicitar_dados(self):
        self.btn_filtrar.setEnabled(False)
        self.btn_filtrar.setText("BUSCANDO...")
        agente = self.cb_agente.currentText() if self.cb_agente.count() > 0 else "Todos"
        periodo = self.cb_periodo.currentText()
        self.worker = DataLoadWorker(self.db, agente, periodo)
        self.worker.data_loaded.connect(self.finalizar_carregamento)
        self.worker.error_signal.connect(self.tratar_erro)
        self.worker.start()

    @Slot(object)
    def finalizar_carregamento(self, df):
        self.df = df
        self.btn_filtrar.setEnabled(True)
        self.btn_filtrar.setText("APLICAR FILTROS")

        if self.df.empty:
            QMessageBox.warning(self, "Aviso", "Sem dados na nuvem.")
            return

        if self.cb_agente.count() == 0:
            agentes = sorted(self.df['vendedor'].dropna().unique().tolist())
            self.cb_agente.addItems(["Todos"] + agentes)

        analytics = CRMAnalytics(self.df)
        kpis = analytics.get_summary_kpis()
        self.card_faturamento.lbl_value.setText(f"$ {kpis['faturamento']:,.2f}")
        self.card_conversao.lbl_value.setText(f"{kpis['taxa_conversao']:.1f}%")
        self.card_abertas.lbl_value.setText(f"{kpis['oportunidades_abertas']}")

        self.atualizar_graficos()

    def limpar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget: widget.deleteLater()

    def atualizar_graficos(self):
        """Renderiza os gráficos Matplotlib dentro dos frames da GUI."""
        # Limpar layouts anteriores se existirem
        for frame in [self.chart_frame0, self.chart_frame1, self.chart_frame2]:
            if frame.layout():
                self.limpar_layout(frame.layout())
            else:
                frame.setLayout(QVBoxLayout())

        # Gerar figuras
        fig0 = self.viz.plot_tendencia_receita(self.df)
        fig1 = self.viz.plot_top_performers(self.df)
        fig2 = self.viz.plot_distribuicao_fases(self.df)

        # Adicionar aos frames
        self.chart_frame0.layout().addWidget(FigureCanvas(fig0))
        self.chart_frame1.layout().addWidget(FigureCanvas(fig1))
        self.chart_frame2.layout().addWidget(FigureCanvas(fig2))

    def tratar_erro(self, msg):
        self.btn_filtrar.setEnabled(True)
        QMessageBox.critical(self, "Erro", msg)

    def abrir_edicao(self):
        dialog = DialogEdicao(self)
        if dialog.exec(): self.solicitar_dados()

    def exportar_pdf(self):
        from backend.gerador_pdf import gerar_relatorio_pdf
        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar PDF", "", "PDF (*.pdf)")
        if caminho:
            analytics = CRMAnalytics(self.df)
            kpis = analytics.get_summary_kpis()
            figs = [
                self.viz.plot_tendencia_receita(self.df),
                self.viz.plot_top_performers(self.df),
                self.viz.plot_distribuicao_fases(self.df)
            ]
            if gerar_relatorio_pdf(caminho, kpis, figs, "Relatório Cloud BI"):
                QMessageBox.information(self, "Sucesso", "PDF Exportado!")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())
