import pandas as pd
from typing import Dict, Any

class CRMAnalytics:
    """Classe responsável pelo cálculo de KPIs e métricas de negócio."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calc_faturamento_total(self) -> float:
        """Soma de 'valor_acordado' onde o status é 'Won' ou 'Ganho'."""
        if 'status_negocio' not in self.df.columns:
            return 0.0
        ganhos = self.df[self.df['status_negocio'].str.lower().isin(['won', 'ganho'])]
        return float(pd.to_numeric(ganhos['valor_acordado'], errors='coerce').sum())

    def calc_taxa_conversao(self) -> float:
        """Porcentagem de negócios ganhos em relação ao total de negócios finalizados."""
        if 'status_negocio' not in self.df.columns:
            return 0.0
        total_finalizado = self.df[self.df['status_negocio'].str.lower().isin(['won', 'ganho', 'lost', 'perdido'])]
        
        if len(total_finalizado) == 0:
            return 0.0
            
        ganhos = total_finalizado[total_finalizado['status_negocio'].str.lower().isin(['won', 'ganho'])]
        return (len(ganhos) / len(total_finalizado)) * 100

    def calc_oportunidades_abertas(self) -> int:
        """Contagem de negócios que não estão finalizados."""
        if 'status_negocio' not in self.df.columns:
            return 0
        finalizados = ['won', 'ganho', 'lost', 'perdido']
        abertas = self.df[~self.df['status_negocio'].str.lower().isin(finalizados)]
        return int(len(abertas))

    def get_summary_kpis(self) -> Dict[str, Any]:
        """Retorna um dicionário com os principais indicadores para a UI."""
        val_fechamento = pd.to_numeric(self.df['valor_acordado'], errors='coerce') if not self.df.empty else pd.Series([])
        return {
            "faturamento": self.calc_faturamento_total(),
            "taxa_conversao": self.calc_taxa_conversao(),
            "oportunidades_abertas": self.calc_oportunidades_abertas(),
            "ticket_medio": val_fechamento.mean() if not self.df.empty else 0.0
        }

if __name__ == "__main__":
    # Exemplo de uso (simulado)
    data = {
        'fase_negociacao': ['Won', 'Lost', 'Prospecting', 'Won'],
        'valor_fechamento': [1000, 0, 500, 2000]
    }
    df_test = pd.DataFrame(data)
    analytics = CRMAnalytics(df_test)
    print(analytics.get_summary_kpis())
