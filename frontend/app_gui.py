import sys
import time
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                             QProgressBar, QFrame)
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor

# Importando as funções do seu backend
from backend.extracao_dados_web import extracao
from backend.extracao_teste import extracao_playwright
from backend.converter_parquet import convertidos
from backend.tratando import tratados
from backend.funcoes import lento

# --- ESTILIZAÇÃO QSS (DARK PREMIUM) ---
QSS_STYLE = """
QMainWindow {
    background-color: #0F0F0F;
}

#Sidebar {
    background-color: #1A1A1A;
    border-right: 1px solid #333333;
    min-width: 250px;
    max-width: 250px;
}

#MainArea {
    background-color: #121212;
}

#VirtualTerminal {
    background-color: #0A0A0A;
    color: #E0E0E0;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 13px;
    border: 1px solid #333333;
    border-radius: 8px;
    padding: 10px;
}

#StatusFrame, #SummaryFrame {
    background-color: #1E1E1E;
    border: 1px solid #333333;
    border-radius: 10px;
    padding: 15px;
}

QLabel#TitleLabel {
    color: #00D1FF;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
}

QLabel#SectionTitle {
    color: #AAAAAA;
    font-size: 14px;
    font-weight: bold;
    text-transform: uppercase;
}

QPushButton {
    background-color: #2D2D2D;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #3D3D3D;
}

QPushButton#StartButton {
    background-color: #005BB7;
    border: 1px solid #00D1FF;
}

QPushButton#StartButton:hover {
    background-color: #0078D7;
}

QPushButton#ExitButton {
    background-color: #B70000;
}

QPushButton#ExitButton:hover {
    background-color: #D70000;
}

QProgressBar {
    border: 1px solid #333333;
    border-radius: 5px;
    text-align: center;
    background-color: #1A1A1A;
    color: white;
}

QProgressBar::chunk {
    background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, 
                        stop:0 #005BB7, stop:1 #00D1FF);
    border-radius: 4px;
}
"""

# --- REDIRECIONADOR DE STDOUT PARA SINAL ---
class StreamProxy:
    def __init__(self, signal):
        self.signal = signal

    def write(self, text):
        if text:
            self.signal.emit(text)

    def flush(self):
        pass

# --- THREAD DE PROCESSAMENTO ETL ---
class ETLWorker(QThread):
    progress_signal = Signal(int)
    log_signal = Signal(str)
    summary_signal = Signal(dict)
    finished_signal = Signal()

    def run(self):
        try:
            inicio_total = time.time()
            
            # 1. Extração
            self.log_signal.emit("[INFO] EXTRAÇÃO: Buscando dados externos...")
            self.progress_signal.emit(15)
            start = time.time()
            extracao()           
            extracao_playwright() 
            t_ext = time.time() - start

            # 2. Processamento Local (Polars/Parquet)
            self.log_signal.emit("[INFO] PROCESSAMENTO: Otimizando arquivos Parquet...")
            self.progress_signal.emit(40)
            start = time.time()
            convertidos()
            tratados()
            t_proc = time.time() - start

            # 3. Carga Direta na Nuvem (Supabase)
            self.log_signal.emit("[INFO] CARGA: Sincronizando com Supabase Cloud...")
            self.progress_signal.emit(70)
            start = time.time()
            from backend.inserir_dados import inserir_no_banco
            inserir_no_banco()
            t_carga = time.time() - start
            
            self.progress_signal.emit(100)
            tempo_total = time.time() - inicio_total
            
            resumo = {
                "extracao": t_ext,
                "conversao": t_proc / 2, # Estimativa para manter compatibilidade com resumo antigo
                "tratamento": t_proc / 2,
                "carga": t_carga,
                "total": tempo_total
            }
            self.summary_signal.emit(resumo)
            self.log_signal.emit("✨ [SUCCESS] Pipeline Cloud-Native Finalizado!")
            
        except Exception as e:
            self.log_signal.emit(f"❌ [FAIL] Erro no Pipeline Cloud: {str(e)}")
        
        self.finished_signal.emit()

# --- JANELA PRINCIPAL ---
class ModernETLWindow(QMainWindow):
    stdout_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini ETL Orchestrator - Cloud Edition")
        self.resize(1100, 750)
        self.setStyleSheet(QSS_STYLE)

        self.init_ui()
        
        self.stdout_signal.connect(self.append_log)
        sys.stdout = StreamProxy(self.stdout_signal)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 40, 20, 40)
        sidebar_layout.setSpacing(15)

        title = QLabel("CLOUD PANEL")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title)
        sidebar_layout.addStretch()

        self.btn_start = QPushButton("🚀 EXECUTAR PIPELINE")
        self.btn_start.setObjectName("StartButton")
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.clicked.connect(self.start_etl)
        sidebar_layout.addWidget(self.btn_start)

        self.btn_dashboard = QPushButton("📊 DASHBOARD CLOUD")
        self.btn_dashboard.setCursor(Qt.PointingHandCursor)
        self.btn_dashboard.setStyleSheet("background-color: #1E1E1E; border: 1px solid #00E5FF; color: #00E5FF;")
        self.btn_dashboard.clicked.connect(self.open_dashboard)
        sidebar_layout.addWidget(self.btn_dashboard)

        # --- BOTÃO: ADMIN CLOUD ---
        self.btn_admin = QPushButton("⚙️ ADMIN CLOUD")
        self.btn_admin.setCursor(Qt.PointingHandCursor)
        self.btn_admin.setStyleSheet("background-color: #1E1E1E; border: 1px solid #FF4500; color: #FF4500;")
        self.btn_admin.clicked.connect(self.open_admin_panel)
        sidebar_layout.addWidget(self.btn_admin)

        btn_exit = QPushButton("✖ SAIR")
        btn_exit.setObjectName("ExitButton")
        btn_exit.setCursor(Qt.PointingHandCursor)
        btn_exit.clicked.connect(self.close)
        sidebar_layout.addWidget(btn_exit)

        main_layout.addWidget(sidebar)

        # Área Principal
        content_area = QWidget()
        content_area.setObjectName("MainArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Progresso
        status_frame = QFrame()
        status_frame.setObjectName("StatusFrame")
        status_layout = QVBoxLayout(status_frame)
        status_layout.addWidget(QLabel("PROGRESSO DO PIPELINE CLOUD", objectName="SectionTitle"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(25)
        status_layout.addWidget(self.progress_bar)
        content_layout.addWidget(status_frame)

        # Terminal
        content_layout.addWidget(QLabel("LOGS DE OPERAÇÃO NA NUVEM", objectName="SectionTitle"))
        self.terminal = QTextEdit()
        self.terminal.setObjectName("VirtualTerminal")
        self.terminal.setReadOnly(True)
        content_layout.addWidget(self.terminal)

        # Resumo
        self.summary_frame = QFrame()
        self.summary_frame.setObjectName("SummaryFrame")
        self.summary_layout = QHBoxLayout(self.summary_frame)
        self.lbl_total = QLabel("Aguardando comando...")
        self.lbl_total.setStyleSheet("color: #00D1FF; font-size: 16px; font-weight: bold;")
        self.summary_layout.addWidget(self.lbl_total)
        content_layout.addWidget(self.summary_frame)

        main_layout.addWidget(content_area)

    @Slot(str)
    def append_log(self, text):
        color = QColor("#FFFFFF")
        if "[OK]" in text or "SUCESSO" in text or "✔️" in text or "✅" in text:
            color = QColor("#00FF00")
        elif "AVISO" in text or "WARN" in text or "⚠️" in text or "⌛" in text:
            color = QColor("#FFD700")
        elif "[FAIL]" in text or "ERRO" in text or "❌" in text or "Ops" in text:
            color = QColor("#FF3333")
        elif "[INFO]" in text or "⏳" in text or "🚀" in text or "✨" in text:
            color = QColor("#00D1FF")

        fmt = QTextCharFormat()
        fmt.setForeground(color)
        
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text, fmt)
        
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()

    def set_buttons_enabled(self, enabled):
        """Habilita ou desabilita os botões de ação principal."""
        self.btn_start.setEnabled(enabled)
        self.btn_admin.setEnabled(enabled)

    def start_etl(self):
        self.set_buttons_enabled(False)
        self.btn_start.setText("⏳ PROCESSANDO...")
        
        self.terminal.clear()
        self.progress_bar.setValue(0)
        self.lbl_total.setText("Executando pipeline CLOUD-ONLY...")

        self.worker = ETLWorker()
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.log_signal.connect(self.append_log)
        self.worker.summary_signal.connect(self.show_summary)
        self.worker.finished_signal.connect(self.on_etl_finished)
        self.worker.start()

    def show_summary(self, data):
        resumo_texto = (f"RESULTADO CLOUD: Total {data['total']:.2f}s | "
                       f"E: {data['extracao']:.2f}s | C: {data['conversao']:.2f}s | "
                       f"T: {data['tratamento']:.2f}s | L: {data['carga']:.2f}s")
        self.lbl_total.setText(resumo_texto)

    def on_etl_finished(self):
        self.set_buttons_enabled(True)
        self.btn_start.setText("🚀 REINICIAR PIPELINE")

    def open_dashboard(self):
        """Abre a janela do Dashboard Analítico sem fechar a atual."""
        from frontend.painel_dashboard import DashboardWindow
        self.dash_window = DashboardWindow()
        self.dash_window.show()

    def open_admin_panel(self):
        """Abre o Painel de Administração de Banco de Dados."""
        from frontend.painel_admin import PainelAdmin
        self.admin_panel = PainelAdmin(self)
        self.admin_panel.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernETLWindow()
    window.show()
    sys.exit(app.exec())
