import dash
from dash import dcc, html, dash_table, Input, Output, State, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import base64
import io
from datetime import datetime, timedelta

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Полномасштабные Аналитики для Транспортной Компании', 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
    
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Перетащите или ',
                html.A('выберите CSV файл')
            ]),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center', 'margin': '10px'
            },
            multiple=False
        ),
    ], style={'width': '50%', 'margin': 'auto'}),
    
    html.Div([
        html.Label('Выберите период:', style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='period-selector',
            options=[
                {'label': 'Неделя', 'value': 'week'},
                {'label': 'Месяц', 'value': 'month'},
                {'label': 'Квартал', 'value': 'quarter'}
            ],
            value='week',
            style={'width': '200px', 'margin': '10px'}
        )
    ], style={'margin': '20px'}),
    
    html.Div([
        html.Div([html.H4(id='total-orders'), html.P('Всего заказов')], 
                 style={'padding': '20px', 'background': '#f8f9fa', 'borderRadius': '10px', 'textAlign': 'center'}),
        html.Div([html.H4(id='avg-processing-time'), html.P('Среднее время (ч)')], 
                 style={'padding': '20px', 'background': '#f8f9fa', 'borderRadius': '10px', 'textAlign': 'center'}),
        html.Div([html.H4(id='on-time-delivery'), html.P('Вовремя')], 
                 style={'padding': '20px', 'background': '#f8f9fa', 'borderRadius': '10px', 'textAlign': 'center'}),
        html.Div([html.H4(id='avg-order-value'), html.P('Средняя стоимость')], 
                 style={'padding': '20px', 'background': '#f8f9fa', 'borderRadius': '10px', 'textAlign': 'center'})
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px', 'margin': '20px'}),
    
    html.Div([
        dcc.Graph(id='orders-trend'),
        dcc.Graph(id='status-distribution'),
        dcc.Graph(id='processing-time-by-city'),
        dcc.Graph(id='weight-vs-cost')
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '20px', 'margin': '20px'}),
    
    html.Div([
        html.H3('Детали заказов'),
        dash_table.DataTable(
            id='orders-table',
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': '#2c3e50', 'color': 'white', 'fontWeight': 'bold'}
        )
    ], style={'margin': '20px'})
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'})

@app.callback(
    [Output('orders-trend', 'figure'),
     Output('status-distribution', 'figure'),
     Output('processing-time-by-city', 'figure'),
     Output('weight-vs-cost', 'figure'),
     Output('orders-table', 'data'),
     Output('orders-table', 'columns'),
     Output('total-orders', 'children'),
     Output('avg-processing-time', 'children'),
     Output('on-time-delivery', 'children'),
     Output('avg-order-value', 'children')],
    [Input('upload-data', 'contents'),
     Input('period-selector', 'value')],
    [State('upload-data', 'filename')],
    prevent_initial_call=True
)
def update_dashboard(contents, period, filename):
    if contents is None:
        empty_fig = go.Figure()
        return [empty_fig, empty_fig, empty_fig, empty_fig, [], [], '0', '0 ч', '0%', '0 р']
    
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    except:
        return [go.Figure() for _ in range(4)] + [[], [], '0', '0 ч', '0%', '0 р']
    
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    if period == 'week':
        df['period'] = df['order_date'].dt.to_period('W')
    elif period == 'month':
        df['period'] = df['order_date'].dt.to_period('M')
    else:
        df['period'] = df['order_date'].dt.to_period('Q')
    
    orders_by_period = df.groupby('period').size().reset_index(name='order_count')
    orders_by_period['period'] = orders_by_period['period'].astype(str)
    trend_fig = px.line(orders_by_period, x='period', y='order_count',
                       title='График тренда', markers=True)
    
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    status_fig = px.pie(status_counts, values='count', names='status',
                       title='НА графики статусов', hole=0.3)
    
    city_processing = df.groupby('city_from').agg(
        {'processing_time_hours': 'mean', 'order_id': 'count'}).reset_index()
    city_processing.columns = ['city', 'avg_hours', 'count']
    city_fig = px.bar(city_processing.head(10), x='city', y='avg_hours',
                     title='Время обработки по городам')
    
    scatter_fig = px.scatter(df, x='weight_kg', y='delivery_cost', color='city_to',
                            title='Корреляция веса и стоимости')
    
    table_data = df.to_dict('records')
    table_columns = [{'name': col, 'id': col} for col in df.columns]
    
    total = len(df)
    avg_time = f"{df['processing_time_hours'].mean():.1f} ч"
    on_time = f"{(df['is_on_time'].sum() / len(df) * 100):.1f}%"
    avg_value = f"{df['order_value'].mean():,.0f} р"
    
    return trend_fig, status_fig, city_fig, scatter_fig, table_data, table_columns, str(total), avg_time, on_time, avg_value

if __name__ == '__main__':
    app.run_server(debug=True)
