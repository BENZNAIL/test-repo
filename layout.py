from app import app
from dash import dcc, html, dash_table

# Макет приложения
app.layout = html.Div([
    # Заголовок
    html.H1("📋 Анализ обработки заказов транспортной компании", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
    
    # Загружение файла
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                '📄 Перетащите или ',
                html.A('выберите CSV файл с данными заказов')
            ]),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center', 'margin': '10px'
            },
            multiple=False
        ),
    ], style={'width': '50%', 'margin': 'auto'}),
    
    # Выбор периода
    html.Div([
        html.Label("📅 Выберите период анализа:", style={'fontWeight': 'bold'}),
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
    
    # KPI индикаторы
    html.Div([
        html.Div([html.H4(id='total-orders'), html.P("Всего заказов")], 
                 className='indicator', style={'padding': '20px', 'background': '#f8f9fa', 'borderRadius': '10px', 'textAlign': 'center'}),
        html.Div([html.H4(id='avg-processing-time'), html.P("Среднее время обработки (ч)")], 
                 className='indicator', style={'padding': '20px', 'background': '#f8f9fa', 'borderRadius': '10px', 'textAlign': 'center'}),
        html.Div([html.H4(id='on-time-delivery'), html.P("Доставлено вовремя")], 
                 className='indicator', style={'padding': '20px', 'background': '#f8f9fa', 'borderRadius': '10px', 'textAlign': 'center'}),
        html.Div([html.H4(id='avg-order-value'), html.P("Средняя стоимость заказа")], 
                 className='indicator', style={'padding': '20px', 'background': '#f8f9fa', 'borderRadius': '10px', 'textAlign': 'center'})
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px', 'margin': '20px'}),
    
    # Графики
    html.Div([
        dcc.Graph(id='orders-trend', style={'gridColumn': 'span 2'}),
        dcc.Graph(id='status-distribution'),
        dcc.Graph(id='processing-time-by-city', style={'gridColumn': 'span 2'}),
        dcc.Graph(id='weight-vs-cost')
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '20px', 'margin': '20px'}),
    
    # Таблица с деталями заказов
    html.Div([
        html.H3("📋 Детальная информация о заказах"),
        dash_table.DataTable(
            id='orders-table',
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': '#2c3e50', 'color': 'white', 'fontWeight': 'bold'}
        )
    ], style={'margin': '20px'})
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'})
