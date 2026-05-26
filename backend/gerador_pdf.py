import io
import datetime
from typing import Dict, List, Any
from fpdf import FPDF
from matplotlib.figure import Figure

# Força o uso de fpdf2 se disponível (mais estável)
try:
    from fpdf import FPDF
except ImportError:
    import fpdf

class RelatorioPDF(FPDF):
    """Subclasse de FPDF para personalizar cabeçalhos e rodapés do relatório CRM."""
    
    def __init__(self):
        super().__init__()
        self.bg_color = (18, 18, 18)  # #121212 em RGB
        self.primary_color = (0, 229, 255) # Ciano Neon
        self.text_color = (224, 224, 224) # Cinza claro
        
    def add_page(self, orientation='', format='', same=False):
        super().add_page(orientation, format, same)
        # Pintar o fundo da página de Dark
        self.set_fill_color(*self.bg_color)
        self.rect(0, 0, 210, 297, 'F')

    def header(self):
        # Título do Relatório
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(*self.primary_color)
        self.cell(0, 15, 'CRM ANALYTICS - RELATÓRIO PREMIUM', border=False, ln=True, align='C')
        
        # Data e Hora da Geração
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(150, 150, 150)
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cell(0, 5, f'Gerado em: {data_hora}', border=False, ln=True, align='C')
        self.ln(5)
        
        # Linha separadora Neon
        self.set_draw_color(*self.primary_color)
        self.set_line_width(0.5)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(10)

    def footer(self):
        # Footer removido conforme solicitado para uma aparência mais limpa
        pass

def figure_to_buffer(fig: Figure) -> io.BytesIO:
    """ Converte um objeto Figure do Matplotlib em um buffer de memória PNG. """
    buf = io.BytesIO()
    # Para o PDF Dark, NÃO usamos transparente, mantemos o fundo original do gráfico
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf

def gerar_relatorio_pdf(caminho_salvamento: str, kpis: Dict[str, Any], graficos: List[Figure], analise_texto: str) -> bool:
    """
    Função principal para orquestrar a geração do PDF Dark Premium.
    """
    try:
        pdf = RelatorioPDF()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()
        
        # --- SEÇÃO 1: KPIs ---
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(*pdf.primary_color)
        pdf.cell(0, 10, 'INDICADORES CHAVE (KPIs)', ln=True)
        pdf.ln(5)
        
        # Moldura para KPIs
        pdf.set_fill_color(30, 30, 30) # Cinza um pouco mais claro que o fundo
        pdf.set_draw_color(50, 50, 50)
        
        for label, valor in kpis.items():
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(180, 180, 180)
            pdf.cell(55, 10, f" {label.upper()}: ", border=0, ln=0)
            
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(255, 255, 255)
            
            if 'faturamento' in label.lower() or 'valor' in label.lower():
                valor_str = f"$ {valor:,.2f}"
            elif 'taxa' in label.lower():
                valor_str = f"{valor:.2f}%"
            else:
                valor_str = str(valor)
                
            pdf.cell(0, 10, valor_str, border=0, ln=True)
        
        pdf.ln(10)
        
        # --- SEÇÃO 2: GRÁFICOS ---
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(*pdf.primary_color)
        pdf.cell(0, 10, 'ANÁLISE VISUAL DE PERFORMANCE', ln=True)
        pdf.ln(5)
        
        for i, fig in enumerate(graficos):
            img_buf = figure_to_buffer(fig)
            
            # Gráfico de tendência (o primeiro) ocupa a largura toda
            if i == 0:
                pdf.image(img_buf, x=15, w=180)
                pdf.ln(5)
            else:
                # Os outros dividem a linha se couberem, ou um por linha para ficar grande
                pdf.image(img_buf, x=15, w=180)
                pdf.ln(5)
            
            # Evita quebras de página no meio de um gráfico
            if i == 1:
                pdf.add_page()

        # --- SEÇÃO 3: ANÁLISE E CONCLUSÕES ---
        pdf.ln(10)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(*pdf.primary_color)
        pdf.cell(0, 10, 'CONCLUSÕES E INSIGHTS', ln=True)
        pdf.ln(5)
        
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(200, 200, 200)
        pdf.multi_cell(0, 7, analise_texto, align='J')
        
        # Finalização
        pdf.output(caminho_salvamento)
        return True

    except PermissionError:
        print(f"❌ Erro: Sem permissão para salvar em '{caminho_salvamento}'. Verifique se o arquivo está aberto.")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado ao gerar PDF: {e}")
        return False

if __name__ == "__main__":
    # Teste rápido de sanidade
    import matplotlib.pyplot as plt
    import numpy as np
    
    test_fig, ax = plt.subplots()
    ax.plot(np.random.rand(10))
    
    kpis_mock = {"Faturamento": 500000.0, "Taxa de Conversão": 15.5, "Oportunidades": 42}
    texto_mock = "A análise demonstra um crescimento sustentável no último trimestre, com destaque para a performance dos agentes seniores."
    
    if gerar_relatorio_pdf("teste_relatorio.pdf", kpis_mock, [test_fig]*4, texto_mock):
        print("✅ Relatório de teste gerado com sucesso!")
