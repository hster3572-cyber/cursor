#!/usr/bin/env python3
"""
Создание диаграммы Ганта для плана внедрения AI-ассистента в HR
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

# Настройка для корректного отображения русского текста
plt.rcParams['font.family'] = 'DejaVu Sans'

def create_gantt_chart():
    # Определение задач и их временных рамок
    tasks = [
        {
            'name': 'Анализ текущих процессов',
            'start': datetime(2024, 1, 1),
            'duration': 30,
            'color': '#FF6B6B'
        },
        {
            'name': 'Выбор AI-платформы',
            'start': datetime(2024, 1, 15),
            'duration': 21,
            'color': '#4ECDC4'
        },
        {
            'name': 'Настройка инфраструктуры',
            'start': datetime(2024, 2, 5),
            'duration': 45,
            'color': '#45B7D1'
        },
        {
            'name': 'Обучение HR-команды',
            'start': datetime(2024, 2, 20),
            'duration': 30,
            'color': '#96CEB4'
        },
        {
            'name': 'Пилотное внедрение',
            'start': datetime(2024, 3, 1),
            'duration': 60,
            'color': '#FFEAA7'
        },
        {
            'name': 'Анализ результатов пилота',
            'start': datetime(2024, 4, 15),
            'duration': 15,
            'color': '#DDA0DD'
        },
        {
            'name': 'Полномасштабное внедрение',
            'start': datetime(2024, 5, 1),
            'duration': 45,
            'color': '#98D8C8'
        },
        {
            'name': 'Оптимизация процессов',
            'start': datetime(2024, 6, 1),
            'duration': 30,
            'color': '#F7DC6F'
        },
        {
            'name': 'Мониторинг и поддержка',
            'start': datetime(2024, 6, 15),
            'duration': 365,
            'color': '#BB8FCE'
        }
    ]
    
    # Создание фигуры
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Настройка осей
    y_pos = np.arange(len(tasks))
    
    # Создание горизонтальных полос для каждой задачи
    for i, task in enumerate(tasks):
        start_date = task['start']
        end_date = start_date + timedelta(days=task['duration'])
        
        ax.barh(i, task['duration'], left=start_date, 
                color=task['color'], alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Добавление названия задачи
        ax.text(start_date - timedelta(days=5), i, task['name'], 
                va='center', ha='right', fontsize=10, fontweight='bold')
    
    # Настройка внешнего вида
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f'Задача {i+1}' for i in range(len(tasks))])
    ax.set_xlabel('Дата', fontsize=12, fontweight='bold')
    ax.set_title('Диаграмма Ганта: План внедрения AI-ассистента в HR-процессы', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Форматирование оси X для отображения дат
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.xticks(rotation=45)
    
    # Настройка сетки
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_axisbelow(True)
    
    # Настройка границ
    ax.set_xlim(datetime(2023, 12, 15), datetime(2025, 1, 15))
    
    # Добавление легенды с этапами
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor='#FF6B6B', alpha=0.7, label='Планирование'),
        plt.Rectangle((0,0),1,1, facecolor='#4ECDC4', alpha=0.7, label='Выбор решения'),
        plt.Rectangle((0,0),1,1, facecolor='#45B7D1', alpha=0.7, label='Техническая подготовка'),
        plt.Rectangle((0,0),1,1, facecolor='#96CEB4', alpha=0.7, label='Обучение'),
        plt.Rectangle((0,0),1,1, facecolor='#FFEAA7', alpha=0.7, label='Пилотное внедрение'),
        plt.Rectangle((0,0),1,1, facecolor='#DDA0DD', alpha=0.7, label='Анализ'),
        plt.Rectangle((0,0),1,1, facecolor='#98D8C8', alpha=0.7, label='Полное внедрение'),
        plt.Rectangle((0,0),1,1, facecolor='#F7DC6F', alpha=0.7, label='Оптимизация'),
        plt.Rectangle((0,0),1,1, facecolor='#BB8FCE', alpha=0.7, label='Поддержка')
    ]
    
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
    
    # Настройка макета
    plt.tight_layout()
    
    # Сохранение диаграммы
    plt.savefig('/workspace/gantt_chart.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return tasks

def create_milestone_timeline():
    """Создание временной шкалы с ключевыми вехами"""
    milestones = [
        {'date': datetime(2024, 1, 30), 'name': 'Завершение анализа процессов', 'type': 'analysis'},
        {'date': datetime(2024, 2, 5), 'name': 'Выбор AI-платформы', 'type': 'decision'},
        {'date': datetime(2024, 3, 20), 'name': 'Готовность инфраструктуры', 'type': 'technical'},
        {'date': datetime(2024, 3, 20), 'name': 'Завершение обучения команды', 'type': 'training'},
        {'date': datetime(2024, 5, 1), 'name': 'Запуск пилотного проекта', 'type': 'pilot'},
        {'date': datetime(2024, 4, 30), 'name': 'Анализ результатов пилота', 'type': 'analysis'},
        {'date': datetime(2024, 6, 15), 'name': 'Полное внедрение', 'type': 'deployment'},
        {'date': datetime(2024, 7, 1), 'name': 'Начало оптимизации', 'type': 'optimization'}
    ]
    
    # Создание временной шкалы
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Цвета для разных типов вех
    colors = {
        'analysis': '#FF6B6B',
        'decision': '#4ECDC4', 
        'technical': '#45B7D1',
        'training': '#96CEB4',
        'pilot': '#FFEAA7',
        'deployment': '#98D8C8',
        'optimization': '#F7DC6F'
    }
    
    # Отображение вех
    for i, milestone in enumerate(milestones):
        color = colors.get(milestone['type'], '#BB8FCE')
        ax.scatter(milestone['date'], i, s=200, c=color, alpha=0.8, edgecolors='black')
        ax.text(milestone['date'] + timedelta(days=10), i, milestone['name'], 
                va='center', fontsize=10, fontweight='bold')
    
    # Настройка осей
    ax.set_yticks(range(len(milestones)))
    ax.set_yticklabels([f'Веха {i+1}' for i in range(len(milestones))])
    ax.set_xlabel('Дата', fontsize=12, fontweight='bold')
    ax.set_title('Ключевые вехи внедрения AI-ассистента', fontsize=16, fontweight='bold')
    
    # Форматирование дат
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.xticks(rotation=45)
    
    # Настройка сетки
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('/workspace/milestone_timeline.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("Создание диаграммы Ганта...")
    tasks = create_gantt_chart()
    
    print("\nСоздание временной шкалы с вехами...")
    create_milestone_timeline()
    
    print("\nДиаграммы сохранены:")
    print("- gantt_chart.png")
    print("- milestone_timeline.png")