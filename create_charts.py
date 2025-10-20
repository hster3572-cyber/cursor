#!/usr/bin/env python3
"""
Создание дополнительных диаграмм и визуализаций
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Настройка для корректного отображения русского текста
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (12, 8)

def create_roi_comparison_chart():
    """Создание диаграммы сравнения ROI по отделам"""
    departments = ['Канцелярия', 'Офис', 'Бэк-офис']
    roi_values = [15.7, 15.3, 21.9]
    savings = [1.59, 3.48, 4.63]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Диаграмма ROI
    bars1 = ax1.bar(departments, roi_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax1.set_title('ROI по отделам (%)', fontsize=14, weight='bold')
    ax1.set_ylabel('ROI (%)')
    ax1.grid(True, alpha=0.3)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars1, roi_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{value}%', ha='center', va='bottom', weight='bold')
    
    # Диаграмма экономии
    bars2 = ax2.bar(departments, savings, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax2.set_title('Годовая экономия по отделам (млн руб)', fontsize=14, weight='bold')
    ax2.set_ylabel('Экономия (млн руб)')
    ax2.grid(True, alpha=0.3)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars2, savings):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{value} млн', ha='center', va='bottom', weight='bold')
    
    plt.tight_layout()
    plt.savefig('/workspace/roi_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_cost_breakdown_chart():
    """Создание диаграммы разбивки затрат на внедрение"""
    categories = ['Лицензии', 'Интеграция', 'Консультации', 'Обучение', 'Оборудование']
    costs = [500, 300, 400, 200, 150]  # в тысячах рублей
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(costs, labels=categories, colors=colors, autopct='%1.1f%%',
                                     startangle=90, textprops={'fontsize': 12})
    
    ax.set_title('Разбивка затрат на внедрение ИИ\n(1,550,000 руб)', fontsize=14, weight='bold')
    
    # Добавление абсолютных значений
    for i, (wedge, cost) in enumerate(zip(wedges, costs)):
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = 1.3 * np.cos(np.radians(angle))
        y = 1.3 * np.sin(np.radians(angle))
        ax.text(x, y, f'{cost}K руб', ha='center', va='center', 
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('/workspace/cost_breakdown.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_timeline_chart():
    """Создание временной шкалы внедрения"""
    tasks = [
        'Подготовка и планирование',
        'Выбор ИИ-платформы',
        'Интеграция с системами',
        'Обучение персонала',
        'Пилот (Канцелярия)',
        'Внедрение в Офис',
        'Внедрение в Бэк-офис',
        'Оптимизация'
    ]
    
    starts = [0, 2, 4, 6, 8, 10, 12, 14]
    durations = [2, 3, 4, 2, 2, 2, 2, 2]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for i, (task, start, duration, color) in enumerate(zip(tasks, starts, durations, colors)):
        ax.barh(i, duration, left=start, height=0.6, color=color, alpha=0.8, edgecolor='black')
        ax.text(start + duration/2, i, f'{task}\n{duration} мес', 
               ha='center', va='center', fontsize=9, weight='bold')
    
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels(tasks)
    ax.set_xlabel('Месяцы с начала проекта')
    ax.set_title('Временная шкала внедрения ИИ-решений', fontsize=14, weight='bold')
    ax.grid(True, alpha=0.3)
    
    # Добавление общей стоимости
    total_cost = 1550
    ax.text(0.02, 0.98, f'Общая стоимость: {total_cost:,}K руб', 
           transform=ax.transAxes, fontsize=12, weight='bold',
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('/workspace/timeline_chart.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_savings_projection():
    """Создание прогноза экономии на 5 лет"""
    years = [1, 2, 3, 4, 5]
    cumulative_savings = [9.7, 19.4, 29.1, 38.8, 48.5]  # в млн рублей
    annual_savings = [9.7, 9.7, 9.7, 9.7, 9.7]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Кумулятивная экономия
    ax1.plot(years, cumulative_savings, marker='o', linewidth=3, markersize=8, color='#2ECC71')
    ax1.fill_between(years, cumulative_savings, alpha=0.3, color='#2ECC71')
    ax1.set_title('Кумулятивная экономия за 5 лет', fontsize=14, weight='bold')
    ax1.set_xlabel('Годы')
    ax1.set_ylabel('Экономия (млн руб)')
    ax1.grid(True, alpha=0.3)
    
    # Добавление значений на точки
    for x, y in zip(years, cumulative_savings):
        ax1.annotate(f'{y} млн', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', weight='bold')
    
    # Годовая экономия
    bars = ax2.bar(years, annual_savings, color='#3498DB', alpha=0.7)
    ax2.set_title('Годовая экономия', fontsize=14, weight='bold')
    ax2.set_xlabel('Годы')
    ax2.set_ylabel('Экономия (млн руб)')
    ax2.grid(True, alpha=0.3)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars, annual_savings):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{value} млн', ha='center', va='bottom', weight='bold')
    
    plt.tight_layout()
    plt.savefig('/workspace/savings_projection.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_department_analysis():
    """Создание детального анализа по отделам"""
    departments = ['Канцелярия', 'Офис', 'Бэк-офис']
    employees = [15, 25, 20]
    staff_reduction = [2, 3, 3]
    time_savings = [231, 472, 630]  # часов в месяц
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Количество сотрудников
    ax1.bar(departments, employees, color='#3498DB', alpha=0.7, label='Всего сотрудников')
    ax1.bar(departments, staff_reduction, color='#E74C3C', alpha=0.7, label='Сокращение')
    ax1.set_title('Сотрудники по отделам', fontsize=12, weight='bold')
    ax1.set_ylabel('Количество человек')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Экономия времени
    bars = ax2.bar(departments, time_savings, color='#2ECC71', alpha=0.7)
    ax2.set_title('Экономия времени (часов/месяц)', fontsize=12, weight='bold')
    ax2.set_ylabel('Часы')
    ax2.grid(True, alpha=0.3)
    
    for bar, value in zip(bars, time_savings):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'{value} ч', ha='center', va='bottom', weight='bold')
    
    # ROI по отделам
    roi_values = [15.7, 15.3, 21.9]
    bars = ax3.bar(departments, roi_values, color='#F39C12', alpha=0.7)
    ax3.set_title('ROI по отделам (%)', fontsize=12, weight='bold')
    ax3.set_ylabel('ROI (%)')
    ax3.grid(True, alpha=0.3)
    
    for bar, value in zip(bars, roi_values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{value}%', ha='center', va='bottom', weight='bold')
    
    # Экономия в рублях
    savings = [1.59, 3.48, 4.63]
    bars = ax4.bar(departments, savings, color='#9B59B6', alpha=0.7)
    ax4.set_title('Годовая экономия (млн руб)', fontsize=12, weight='bold')
    ax4.set_ylabel('Экономия (млн руб)')
    ax4.grid(True, alpha=0.3)
    
    for bar, value in zip(bars, savings):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{value} млн', ha='center', va='bottom', weight='bold')
    
    plt.tight_layout()
    plt.savefig('/workspace/department_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("Создание диаграмм...")
    
    print("1. Диаграмма сравнения ROI...")
    create_roi_comparison_chart()
    
    print("2. Диаграмма разбивки затрат...")
    create_cost_breakdown_chart()
    
    print("3. Временная шкала внедрения...")
    create_timeline_chart()
    
    print("4. Прогноз экономии...")
    create_savings_projection()
    
    print("5. Анализ по отделам...")
    create_department_analysis()
    
    print("Все диаграммы созданы!")