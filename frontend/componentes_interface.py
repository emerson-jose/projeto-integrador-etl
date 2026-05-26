from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel

class KPICard(QFrame):
    """Componente visual para exibição de indicadores (Cards)."""
    def __init__(self, title, value):
        super().__init__()
        self.setObjectName("KPICard")
        layout = QVBoxLayout(self)
        
        self.lbl_title = QLabel(title)
        self.lbl_title.setObjectName("KPITitle")
        
        self.lbl_value = QLabel(value)
        self.lbl_value.setObjectName("KPIValue")
        
        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_value)
