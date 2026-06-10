import plotly.express as px
import plotly.graph_objects as op

def plot_spending_pie(df):
    """Generates a pie chart of spending by category."""
    expenses = df[df['amount'] < 0].copy()
    expenses['amount'] = expenses['amount'].abs()
    
    summary = expenses.groupby('category', as_index=False)['amount'].sum()
    
    fig = px.pie(summary, values='amount', names='category', 
                 title="Spending Breakdown by Category",
                 hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Safe)
    return fig

def plot_spending_trend(df):
    """Generates a historical time-series chart of transactions."""
    df_sorted = df.sort_values('date')
    fig = px.line(df_sorted, x='date', y='amount', 
                  title="Daily Financial Activity Trend",
                  labels={'amount': 'Amount ($)', 'date': 'Date'},
                  markers=True)
    fig.update_traces(line_color='#2ca02c')
    return fig