import sys
import os

# Adiciona a raiz do projeto ao path para facilitar os imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from frontend.app_gui import QApplication, ModernETLWindow
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = ModernETLWindow()
        window.show()
        sys.exit(app.exec())
except ImportError as e:
    print(f"❌ Erro ao iniciar a aplicação: {e}")
    print("Verifique se os módulos do backend e frontend estão acessíveis.")