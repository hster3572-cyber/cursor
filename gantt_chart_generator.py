#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор диаграммы Ганта для проекта внедрения AI-ассистента
"""

import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

class GanttChartGenerator:
    """Класс для создания диаграммы Ганта проекта внедрения AI"""
    
    def __init__(self, start_date='2024-01-01'):
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.project_phases = self._define_project_phases()
    
    def _define_project_phases(self):
        """Определение фаз проекта внедрения AI-ассистента"""
        phases = [
            {
                'Task': 'Анализ и планирование',
                'Start': self.start_date,
                'Duration': 30,  # дни
                'Resource': 'Аналитики',
                'Description': 'Анализ текущих процессов, определение требований'
            },
            {
                'Task': 'Выбор AI-платформы',
                'Start': self.start_date + timedelta(days=20),
                'Duration': 20,
                'Resource': 'IT-команда',
                'Description': 'Оценка и выбор подходящей AI-платформы'
            },
            {
                'Task': 'Закупка лицензий',
                'Start': self.start_date + timedelta(days=35),
                'Duration': 15,
                'Resource': 'Закупки',
                'Description': 'Приобретение необходимых лицензий и подписок'
            },
            {
                'Task': 'Настройка инфраструктуры',
                'Start': self.start_date + timedelta(days=45),
                'Duration': 25,
                'Resource': 'IT-команда',
                'Description': 'Развертывание и настройка технической инфраструктуры'
            },
            {
                'Task': 'Интеграция с существующими системами',
                'Start': self.start_date + timedelta(days=60),
                'Duration': 35,
                'Resource': 'Разработчики',
                'Description': 'Интеграция AI-ассистента с HR-системами'
            },
            {
                'Task': 'Разработка процедур и регламентов',
                'Start': self.start_date + timedelta(days=50),
                'Duration': 30,
                'Resource': 'HR-команда',
                'Description': 'Создание новых рабочих процедур'
            },
            {
                'Task': 'Обучение персонала (Канцелярия)',
                'Start': self.start_date + timedelta(days=85),
                'Duration': 20,
                'Resource': 'Тренеры',
                'Description': 'Обучение сотрудников канцелярии работе с AI'
            },
            {
                'Task': 'Обучение персонала (HR отдел)',
                'Start': self.start_date + timedelta(days=90),
                'Duration': 15,
                'Resource': 'Тренеры',
                'Description': 'Обучение HR-специалистов'
            },
            {
                'Task': 'Обучение персонала (Бэк-офис)',
                'Start': self.start_date + timedelta(days=95),
                'Duration': 18,
                'Resource': 'Тренеры',
                'Description': 'Обучение сотрудников бэк-офиса'
            },
            {
                'Task': 'Пилотное внедрение (Канцелярия)',
                'Start': self.start_date + timedelta(days=105),
                'Duration': 30,
                'Resource': 'Канцелярия',
                'Description': 'Тестовое внедрение в канцелярии'
            },
            {
                'Task': 'Пилотное внедрение (HR отдел)',
                'Start': self.start_date + timedelta(days=110),
                'Duration': 25,
                'Resource': 'HR-команда',
                'Description': 'Тестовое внедрение в HR отделе'
            },
            {
                'Task': 'Пилотное внедрение (Бэк-офис)',
                'Start': self.start_date + timedelta(days=115),
                'Duration': 28,
                'Resource': 'Бэк-офис',
                'Description': 'Тестовое внедрение в бэк-офисе'
            },
            {
                'Task': 'Анализ результатов пилота',
                'Start': self.start_date + timedelta(days=135),
                'Duration': 15,
                'Resource': 'Аналитики',
                'Description': 'Оценка эффективности пилотного внедрения'
            },
            {
                'Task': 'Корректировка и оптимизация',
                'Start': self.start_date + timedelta(days=145),
                'Duration': 20,
                'Resource': 'IT-команда',
                'Description': 'Внесение улучшений по результатам пилота'
            },
            {
                'Task': 'Полное внедрение',
                'Start': self.start_date + timedelta(days=160),
                'Duration': 30,
                'Resource': 'Все команды',
                'Description': 'Развертывание на всех отделах'
            },
            {
                'Task': 'Мониторинг и поддержка',
                'Start': self.start_date + timedelta(days=180),
                'Duration': 90,
                'Resource': 'IT-поддержка',
                'Description': 'Постоянный мониторинг и техподдержка'
            }
        ]
        
        # Добавляем вычисляемые поля
        for phase in phases:
            phase['Finish'] = phase['Start'] + timedelta(days=phase['Duration'])
            phase['Start_str'] = phase['Start'].strftime('%Y-%m-%d')
            phase['Finish_str'] = phase['Finish'].strftime('%Y-%m-%d')
        
        return phases
    
    def create_gantt_dataframe(self):
        """Создание DataFrame для диаграммы Ганта"""
        gantt_data = []
        
        for phase in self.project_phases:
            gantt_data.append({
                'Task': phase['Task'],
                'Start': phase['Start_str'],
                'Finish': phase['Finish_str'],
                'Resource': phase['Resource'],
                'Description': phase['Description'],
                'Duration': phase['Duration']
            })
        
        return pd.DataFrame(gantt_data)
    
    def create_gantt_chart(self):
        """Создание интерактивной диаграммы Ганта"""
        df = self.create_gantt_dataframe()
        
        # Цветовая схема для ресурсов
        colors = {
            'Аналитики': '#FF6B6B',
            'IT-команда': '#4ECDC4',
            'Закупки': '#45B7D1',
            'Разработчики': '#96CEB4',
            'HR-команда': '#FFEAA7',
            'Тренеры': '#DDA0DD',
            'Канцелярия': '#98D8C8',
            'Бэк-офис': '#F7DC6F',
            'Все команды': '#BB8FCE',
            'IT-поддержка': '#85C1E9'
        }
        
        fig = ff.create_gantt(
            df, 
            colors=colors,
            index_col='Resource',
            show_colorbar=True,
            group_tasks=True,
            showgrid_x=True,
            showgrid_y=True,
            title="Диаграмма Ганта: Внедрение AI-ассистента для автоматизации HR-задач"
        )
        
        # Настройка макета
        fig.update_layout(
            title={
                'text': "Диаграмма Ганта: Внедрение AI-ассистента для автоматизации HR-задач",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            xaxis_title="Временная шкала",
            yaxis_title="Задачи проекта",
            height=800,
            font=dict(size=10),
            showlegend=True
        )
        
        return fig
    
    def get_project_summary(self):
        """Получение сводки по проекту"""
        total_duration = max([phase['Finish'] for phase in self.project_phases]) - self.start_date
        
        resource_workload = {}
        for phase in self.project_phases:
            resource = phase['Resource']
            if resource not in resource_workload:
                resource_workload[resource] = 0
            resource_workload[resource] += phase['Duration']
        
        summary = {
            'total_duration_days': total_duration.days,
            'total_phases': len(self.project_phases),
            'resource_workload': resource_workload,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': max([phase['Finish'] for phase in self.project_phases]).strftime('%Y-%m-%d')
        }
        
        return summary

if __name__ == "__main__":
    generator = GanttChartGenerator()
    
    # Создание диаграммы Ганта
    fig = generator.create_gantt_chart()
    
    # Сохранение диаграммы
    fig.write_html("gantt_chart.html")
    fig.write_image("gantt_chart.png", width=1200, height=800)
    
    # Получение сводки
    summary = generator.get_project_summary()
    
    print("=== СВОДКА ПО ПРОЕКТУ ===")
    print(f"Общая продолжительность: {summary['total_duration_days']} дней")
    print(f"Количество фаз: {summary['total_phases']}")
    print(f"Дата начала: {summary['start_date']}")
    print(f"Дата окончания: {summary['end_date']}")
    print("\nНагрузка по ресурсам:")
    for resource, days in summary['resource_workload'].items():
        print(f"  {resource}: {days} дней")