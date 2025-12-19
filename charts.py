# Графики и диаграммы для анализа данных
# Диаграммы для визуализации данных о заказах

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_trend_chart(df, period):
    """
    График тренда заказов по времени
    """
    orders_by_period = df.groupby('period').size().reset_index(name='order_count')
    orders_by_period['period'] = orders_by_period['period'].astype(str)
    
    trend_fig = px.line(
        orders_by_period,
        x='period',
        y='order_count',
        title=' Динамика количества заказов',
        labels={'order_count': 'Количество заказов', 'period': 'Период'},
        markers=True
    )
    trend_fig.update_traces(line=dict(width=3))
    return trend_fig

def create_status_chart(df):
    """
    Круговая диаграмма распределения по статусам
    """
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    
    status_fig = px.pie(
        status_counts,
        values='count',
        names='status',
        title=' Распределение заказов по статусам',
        hole=0.3
    )
    return status_fig

def create_city_chart(df):
    """
    График времени обработки по городам
    """
    city_processing = df.groupby('city_from').agg({
        'processing_time_hours': 'mean',
        'order_id': 'count'
    }).reset_index()
    city_processing.columns = ['city', 'avg_processing_hours', 'order_count']
    
    city_fig = px.bar(
        city_processing.sort_values('avg_processing_hours', ascending=False).head(10),
        x='city',
        y='avg_processing_hours',
        title=' Время обработки по городам (10)',
        labels={'avg_processing_hours': 'Часы', 'city': 'Город'},
        color='order_count'
    )
    return city_fig

def create_scatter_chart(df):
    """
    График рассеяния - зависимость стоимости от веса
    """
    scatter_fig = px.scatter(
        df,
        x='weight_kg',
        y='delivery_cost',
        color='city_to',
        title=' Зависимость стоимости от веса',
        labels={'weight_kg': 'Вес (кг)', 'delivery_cost': 'Стоимость (руб)'},
        trendline='ols'
    )
    return scatter_fig
