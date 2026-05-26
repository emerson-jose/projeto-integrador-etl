import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class CRMInteractiveVisualizer:
    """Classe responsável pela geração de gráficos INTERATIVOS com Plotly."""

    def __init__(self):
        self.primary_color = '#00E5FF'
        self.bg_color = '#121212'
        self.text_color = '#E0E0E0'
        self.template = "plotly_dark"

    def _format_layout(self, fig, title):
        fig.update_layout(
            title={'text': title, 'font': {'color': self.primary_color, 'size': 18}, 'x': 0.5},
            paper_bgcolor=self.bg_color,
            plot_bgcolor=self.bg_color,
            font={'color': self.text_color},
            margin=dict(l=50, r=50, t=80, b=50),
            template=self.template,
            dragmode=False,
            autosize=True
        )
        return fig

    def _to_html(self, fig):
        """Converte a figura para HTML embutindo o JS para máxima compatibilidade."""
        return fig.to_html(
            include_plotlyjs=True, # Embutir JS para funcionar sem internet/firewall
            full_html=False, 
            config={'responsive': True, 'displayModeBar': False}
        )

    def plot_tendencia_receita(self, df: pd.DataFrame) -> str:
        if df.empty: return "<h3 style='color:white; text-align:center;'>Aguardando dados...</h3>"
        
        df_temp = df.copy()
        df_temp['data_grafico'] = df_temp['data_encerramento'].fillna(df_temp['data_proposta'])
        df_temp = df_temp[df_temp['data_grafico'].notna()]
        
        if df_temp.empty: return "<h3 style='color:white; text-align:center;'>Sem histórico de datas</h3>"
        
        # Agrupamento mensal
        evolucao = df_temp.set_index('data_grafico')['valor_acordado'].resample('ME').sum().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=evolucao['data_grafico'], 
            y=evolucao['valor_acordado'],
            mode='lines+markers',
            name='Receita',
            line=dict(color=self.primary_color, width=4),
            fill='tozeroy',
            fillcolor='rgba(0, 229, 255, 0.1)'
        ))
        
        self._format_layout(fig, 'TENDÊNCIA DE RECEITA MENSAL')
        return self._to_html(fig)

    def plot_top_performers(self, df: pd.DataFrame) -> str:
        if df.empty or 'vendedor' not in df.columns: 
            return "<h3 style='color:white; text-align:center;'>Sem dados de vendedores</h3>"
        
        tops = df['vendedor'].value_counts().head(6).index
        df_plot = df[df['vendedor'].isin(tops)].groupby(['vendedor', 'status_negocio']).size().reset_index(name='Quantidade')
        
        fig = px.bar(
            df_plot, x='vendedor', y='Quantidade', color='status_negocio',
            color_discrete_sequence=['#00E5FF', '#00B8D4', '#00838F', '#006064', '#004D40']
        )
        
        self._format_layout(fig, 'TOP 6 AGENTES POR STATUS')
        fig.update_layout(barmode='stack', xaxis_title="", yaxis_title="Qtd")
        return self._to_html(fig)

    def plot_distribuicao_fases(self, df: pd.DataFrame) -> str:
        if df.empty or 'status_negocio' not in df.columns:
            return "<h3 style='color:white; text-align:center;'>Sem dados de status</h3>"
            
        dist = df['status_negocio'].value_counts().reset_index()
        dist.columns = ['Status', 'Quantidade']
        
        fig = px.pie(
            dist, values='Quantidade', names='Status', hole=0.4,
            color_discrete_sequence=['#00E5FF', '#00B8D4', '#00838F', '#006064', '#004D40']
        )
        
        self._format_layout(fig, 'DISTRIBUIÇÃO DO PIPELINE')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return self._to_html(fig)
