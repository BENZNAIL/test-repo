# Upload компонент для загружения CSV файла с данными заказов
# Компонент позволяет пользователю загружать файлы через web интерфейс

from dash import dcc, html

def create_upload_component():
    """
    Создает компонент для загружения файлов
    Returns:
        dcc.Upload: Компонент загрузки файлов
    """
    upload_component = dcc.Upload(
        id='upload-data',
        children=html.Div([
            ' Перетащите или ',
            html.A('выберите CSV файл с данными заказов')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    )
    
    return upload_component
