# Калкулятор Основных Показателей Деятельности
# Расчет KPI для деловой аналитики

import pandas as pd
import numpy as np

class KPICalculator:
    """
    Класс для расчета KPI основных метрик
    """
    
    def __init__(self, df):
        """
        Инициализация калкулятора
        """
        self.df = df
    
    def calculate_total_orders(self):
        """
        Общее количество заказов
        """
        return len(self.df)
    
    def calculate_avg_processing_time(self):
        """
        Среднее время обработки в часах
        """
        if 'processing_time_hours' in self.df.columns:
            return self.df['processing_time_hours'].mean()
        return 0
    
    def calculate_on_time_delivery_rate(self):
        """
        Процент доставок в срок
        """
        if 'is_on_time' in self.df.columns:
            on_time_count = self.df['is_on_time'].sum()
            total_count = len(self.df)
            return (on_time_count / total_count * 100) if total_count > 0 else 0
        return 0
    
    def calculate_avg_order_value(self):
        """
        Средняя стоимость заказа в рублях
        """
        if 'order_value' in self.df.columns:
            return self.df['order_value'].mean()
        return 0
    
    def calculate_total_revenue(self):
        """
        Общая выручка от доставок
        """
        if 'order_value' in self.df.columns:
            return self.df['order_value'].sum()
        return 0
    
    def calculate_avg_weight_per_order(self):
        """
        Средний вес заказа в кг
        """
        if 'weight_kg' in self.df.columns:
            return self.df['weight_kg'].mean()
        return 0
    
    def get_all_kpi(self):
        """
        Получить все KPI значения
        """
        return {
            'total_orders': self.calculate_total_orders(),
            'avg_processing_time': round(self.calculate_avg_processing_time(), 1),
            'on_time_delivery_rate': round(self.calculate_on_time_delivery_rate(), 1),
            'avg_order_value': round(self.calculate_avg_order_value(), 2),
            'total_revenue': round(self.calculate_total_revenue(), 2),
            'avg_weight_per_order': round(self.calculate_avg_weight_per_order(), 2)
        }
