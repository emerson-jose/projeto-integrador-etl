# --- ESTILO QSS PREMIUM ---
QSS_STYLE = """
QMainWindow {
    background-color: #0A0A0A;
}

#Sidebar {
    background-color: #121212;
    border-right: 1px solid #333333;
    min-width: 260px;
}

#ContentArea {
    background-color: #0A0A0A;
}

#KPICard {
    background-color: #181818;
    border: 1px solid #2A2A2A;
    border-radius: 12px;
    padding: 15px;
}

#ChartFrame {
    background-color: #121212;
    border: 1px solid #222222;
    border-radius: 10px;
}

QLabel {
    color: #E0E0E0;
    font-family: 'Segoe UI', sans-serif;
}

QLabel#KPITitle {
    color: #888888;
    font-size: 13px;
    font-weight: bold;
    text-transform: uppercase;
}

QLabel#KPIValue {
    color: #00E5FF;
    font-size: 24px;
    font-weight: bold;
}

QLabel#SidebarTitle {
    color: #00E5FF;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 20px;
}

QComboBox {
    background-color: #1E1E1E;
    color: white;
    border: 1px solid #333333;
    border-radius: 5px;
    padding: 8px;
    min-width: 200px;
}

QPushButton {
    background-color: #1A1A1A;
    color: white;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 10px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #252525;
}

QPushButton#PrimaryBtn {
    background-color: #005BB7;
    border: 1px solid #00E5FF;
    color: white;
}

QPushButton#PrimaryBtn:hover {
    background-color: #0078D7;
}

QTableWidget {
    background-color: #181818;
    color: white;
    gridline-color: #333333;
    border: 1px solid #333333;
}

QHeaderView::section {
    background-color: #252525;
    color: #00E5FF;
    padding: 5px;
    border: 1px solid #333333;
}
"""
