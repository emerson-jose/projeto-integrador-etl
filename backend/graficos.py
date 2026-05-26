import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.figure import Figure

class CRMVisualizer:
    """Classe responsável pela geração de gráficos com estética Dark Premium."""

    def __init__(self):
        # Configurações globais de estilo
        plt.style.use('dark_background')
        self.primary_color = '#00E5FF'  # Ciano Neon
        self.bg_color = '#121212'       # Cinza muito escuro (ajustado para bater com a GUI)
        self.text_color = '#E0E0E0'
        
        # Parâmetros customizados do Matplotlib
        plt.rcParams.update({
            'figure.facecolor': self.bg_color,
            'axes.facecolor': self.bg_color,
            'axes.edgecolor': '#333333',
            'axes.labelcolor': self.text_color,
            'xtick.color': self.text_color,
            'ytick.color': self.text_color,
            'grid.color': '#252525',
            'font.family': 'sans-serif'
        })

    def plot_tendencia_receita(self, df: pd.DataFrame) -> Figure:
        """Gráfico de Linha com área preenchida: Ajustes Manuais Extremos de Coordenadas."""
        import matplotlib.dates as mdates
        
        # Cria a figura e garante integração total com o fundo Dark do dashboard
        fig, ax = plt.subplots(figsize=(12, 4))
        fig.patch.set_facecolor(self.bg_color)
        ax.set_facecolor(self.bg_color)
        
        # Usamos uma data consolidada conforme novo mapeamento Cloud
        df_temp = df.copy()
        df_temp['data_grafico'] = df_temp['data_encerramento'].fillna(df_temp['data_proposta'])
        
        df_temp = df_temp[df_temp['data_grafico'].notna()]
        df_temp.set_index('data_grafico', inplace=True)
        
        # Agrupamos por mês e somamos o valor_acordado
        evolucao = df_temp['valor_acordado'].resample('ME').sum()

        ax.plot(evolucao.index, evolucao.values, color=self.primary_color, linewidth=2, marker='o', markersize=4)
        ax.fill_between(evolucao.index, evolucao.values, color=self.primary_color, alpha=0.2)
        
        # 1. TÍTULO: Fontsize 10 e Pad 25 para evitar corte no topo
        ax.set_title('TENDÊNCIA DE RECEITA E FLUXO MENSAL', fontsize=10, pad=25, color=self.primary_color, fontweight='bold')
        
        # 2. EIXO X: Redução de densidade para 5 pontos (máxima legibilidade)
        ax.xaxis.set_major_locator(plt.MaxNLocator(8)) 
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
        
        # 3. FORMATAÇÃO DE DATAS: Rotação e alinhamento profissional
        fig.autofmt_xdate(rotation=45, ha='right')
        
        # 4. MARGENS EXTREMAS (Ajuste Final):
        fig.subplots_adjust(bottom=0.45, top=0.82, left=0.10, right=0.95)
        
        ax.grid(True, axis='y', linestyle='--', alpha=0.1)
        sns.despine(left=True, bottom=True)
        
        return fig

    def plot_top_performers(self, df: pd.DataFrame) -> Figure:
        """Gráfico de Barras Empilhadas (Stacked) para os Top 6 Agentes."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        tops = df['vendedor'].value_counts().head(6).index
        q2 = df[df['vendedor'].isin(tops)].groupby(['vendedor', 'status_negocio']).size().unstack()
        q2 = q2.loc[q2.sum(axis=1).sort_values(ascending=False).index]
        
        q2.plot(kind='bar', stacked=True, ax=ax)
        
        ax.set_title('TOP 6 AGENTES COM MAIS OPORTUNIDADES', color=self.primary_color, fontsize=12, fontweight='bold')
        ax.set_ylabel('QUANTIDADE', fontsize=9)
        ax.grid(alpha=0.2, color='GREEN', axis='y')
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        fig.subplots_adjust(bottom=0.35, left=0.1, right=0.95, top=0.9)
        
        return fig

    def plot_distribuicao_fases(self, df: pd.DataFrame) -> Figure:
        """Gráfico de Rosca (Donut) para Fases de Negociação."""
        fig, ax = plt.subplots(figsize=(6, 6))
        dist = df['status_negocio'].value_counts()
        colors = ['#00E5FF', '#00B8D4', '#00838F', '#006064', '#26C6DA']
        
        wedges, texts, autotexts = ax.pie(
            dist, labels=dist.index, autopct='%1.1f%%', 
            colors=colors, startangle=140, 
            pctdistance=0.75, labeldistance=1.1,
            radius=0.85,
            textprops={'color': self.text_color, 'fontsize': 8},
            wedgeprops=dict(width=0.4, edgecolor='none')
        )
        
        centre_circle = plt.Circle((0,0), 0.45, fc=self.bg_color)
        fig.gca().add_artist(centre_circle)
        
        ax.set_title("DISTRIBUIÇÃO DO PIPELINE", color=self.primary_color, fontsize=12, fontweight='bold')
        plt.setp(autotexts, size=8, weight="bold")
        fig.subplots_adjust(top=0.85)
        
        return fig

    def plot_boxplot_tamanho_negocio(self, df: pd.DataFrame) -> Figure:
        """Boxplot estatístico do valor de fechamento por Produto."""
        fig, ax = plt.subplots(figsize=(8, 4))
        top_produtos = df['produto'].value_counts().head(5).index
        df_plot = df[df['produto'].isin(top_produtos)]
        
        sns.boxplot(
            data=df_plot, x='produto', y='valor_acordado', 
            ax=ax, color=self.primary_color,
            boxprops=dict(alpha=0.3),
            medianprops=dict(color=self.primary_color, linewidth=2)
        )
        
        ax.set_title("Distribuição de Valores por Produto", color=self.primary_color, pad=20)
        ax.set_ylabel("Valor Acordado ($)")
        ax.grid(True, axis='y', linestyle='--', alpha=0.1)
        sns.despine()
        
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        fig.subplots_adjust(bottom=0.25, left=0.1, right=0.95, top=0.9)
        
        return fig

if __name__ == "__main__":
    # Teste rápido com dados fictícios
    df_mock = pd.DataFrame({
        'data_fechamento': pd.date_range(start='1/1/2023', periods=100, freq='D'),
        'valor_fechamento': np.random.randint(1000, 10000, 100),
        'agente_vendas': np.random.choice(['Ana', 'Bruno', 'Carla'], 100),
        'fase_negociacao': np.random.choice(['Won', 'Lost', 'Open'], 100),
        'produto': np.random.choice(['SaaS', 'Hardware', 'Service'], 100)
    })
    
    viz = CRMVisualizer()
    f1 = viz.plot_tendencia_receita(df_mock)
    plt.show()
