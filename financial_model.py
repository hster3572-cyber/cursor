#!/usr/bin/env python3
"""
Финансовая модель внедрения ИИ-решений в HR-процессы
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Настройка для корректного отображения русского текста
plt.rcParams['font.family'] = 'DejaVu Sans'

class HR_AIAnalysis:
    def __init__(self):
        # Базовые данные по отделам (в рублях)
        self.departments = {
            'Канцелярия': {
                'employees': 15,
                'avg_salary': 45000,
                'monthly_operations': 1200,
                'avg_time_per_task': 0.5,  # часа
                'automation_potential': 0.55  # 55% задач можно автоматизировать
            },
            'Офис': {
                'employees': 25,
                'avg_salary': 55000,
                'monthly_operations': 2000,
                'avg_time_per_task': 0.75,
                'automation_potential': 0.45  # 45% задач можно автоматизировать
            },
            'Бэк-офис': {
                'employees': 20,
                'avg_salary': 60000,
                'monthly_operations': 1500,
                'avg_time_per_task': 1.0,
                'automation_potential': 0.60  # 60% задач можно автоматизировать
            }
        }
        
        # Стоимость внедрения ИИ
        self.ai_implementation_costs = {
            'software_licenses': 500000,  # Лицензии на ИИ-платформы
            'integration': 300000,       # Интеграция с существующими системами
            'training': 200000,          # Обучение персонала
            'consulting': 400000,        # Консультационные услуги
            'hardware': 150000,          # Дополнительное оборудование
            'total': 1550000
        }
        
        # Ежемесячные операционные расходы на ИИ
        self.monthly_ai_costs = {
            'licenses': 50000,
            'maintenance': 25000,
            'support': 15000,
            'total': 90000
        }
    
    def calculate_baseline_costs(self):
        """Расчет базовых расходов до внедрения ИИ"""
        baseline = {}
        
        for dept, data in self.departments.items():
            # Зарплатный фонд
            salary_fund = data['employees'] * data['avg_salary'] * 12
            
            # Стоимость рутинных операций
            operations_cost = (data['monthly_operations'] * 
                             data['avg_time_per_task'] * 
                             data['avg_salary'] / 160 * 12)  # 160 часов в месяц
            
            # Общие расходы
            total_cost = salary_fund + operations_cost
            
            baseline[dept] = {
                'salary_fund': salary_fund,
                'operations_cost': operations_cost,
                'total_cost': total_cost,
                'cost_per_employee': total_cost / data['employees']
            }
        
        return baseline
    
    def calculate_ai_impact(self):
        """Расчет влияния внедрения ИИ"""
        baseline = self.calculate_baseline_costs()
        ai_impact = {}
        
        for dept, data in self.departments.items():
            # Экономия на автоматизированных операциях
            automated_operations = data['monthly_operations'] * data['automation_potential']
            time_savings = automated_operations * data['avg_time_per_task'] * 0.7  # 70% экономии времени
            
            # Экономия в рублях
            cost_savings = time_savings * data['avg_salary'] / 160 * 12
            
            # Сокращение персонала (частичное)
            staff_reduction = int(data['employees'] * 0.15)  # 15% сокращение
            staff_savings = staff_reduction * data['avg_salary'] * 12
            
            # Новые расходы на ИИ (пропорционально размеру отдела)
            total_employees = sum(d['employees'] for d in self.departments.values())
            ai_cost_share = (data['employees'] / total_employees) * self.monthly_ai_costs['total'] * 12
            
            # Чистая экономия
            net_savings = cost_savings + staff_savings - ai_cost_share
            
            ai_impact[dept] = {
                'automated_operations': automated_operations,
                'time_savings_hours': time_savings,
                'cost_savings': cost_savings,
                'staff_reduction': staff_reduction,
                'staff_savings': staff_savings,
                'ai_costs': ai_cost_share,
                'net_savings': net_savings,
                'roi_percentage': (net_savings / baseline[dept]['total_cost']) * 100
            }
        
        return ai_impact
    
    def create_financial_summary(self):
        """Создание сводной финансовой таблицы"""
        baseline = self.calculate_baseline_costs()
        ai_impact = self.calculate_ai_impact()
        
        summary_data = []
        
        for dept in self.departments.keys():
            summary_data.append({
                'Отдел': dept,
                'Сотрудников': self.departments[dept]['employees'],
                'Расходы_до_ИИ_млн_руб': round(baseline[dept]['total_cost'] / 1_000_000, 2),
                'Экономия_млн_руб': round(ai_impact[dept]['net_savings'] / 1_000_000, 2),
                'ROI_%': round(ai_impact[dept]['roi_percentage'], 1),
                'Сокращение_персонала': ai_impact[dept]['staff_reduction'],
                'Экономия_времени_часов_месяц': round(ai_impact[dept]['time_savings_hours'], 0)
            })
        
        return pd.DataFrame(summary_data)
    
    def calculate_implementation_timeline(self):
        """Расчет временной шкалы внедрения"""
        timeline = {
            'Подготовка и планирование': {'start': 0, 'duration': 2, 'cost': 200000},
            'Выбор и настройка ИИ-платформы': {'start': 2, 'duration': 3, 'cost': 400000},
            'Интеграция с существующими системами': {'start': 4, 'duration': 4, 'cost': 300000},
            'Обучение персонала': {'start': 6, 'duration': 2, 'cost': 200000},
            'Пилотное внедрение (Канцелярия)': {'start': 8, 'duration': 2, 'cost': 150000},
            'Внедрение в Офис': {'start': 10, 'duration': 2, 'cost': 200000},
            'Внедрение в Бэк-офис': {'start': 12, 'duration': 2, 'cost': 200000},
            'Оптимизация и масштабирование': {'start': 14, 'duration': 2, 'cost': 100000}
        }
        
        return timeline
    
    def create_gantt_chart(self):
        """Создание диаграммы Ганта"""
        timeline = self.calculate_implementation_timeline()
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(timeline)))
        
        for i, (task, data) in enumerate(timeline.items()):
            start = data['start']
            duration = data['duration']
            
            ax.barh(i, duration, left=start, height=0.6, 
                   color=colors[i], alpha=0.8, edgecolor='black')
            
            # Добавляем стоимость в скобках
            ax.text(start + duration/2, i, f'{task}\n({data["cost"]//1000}K руб)', 
                   ha='center', va='center', fontsize=9, weight='bold')
        
        ax.set_yticks(range(len(timeline)))
        ax.set_yticklabels(list(timeline.keys()))
        ax.set_xlabel('Месяцы с начала проекта')
        ax.set_title('Диаграмма Ганта: Внедрение ИИ-решений в HR-процессы', 
                    fontsize=14, weight='bold')
        ax.grid(True, alpha=0.3)
        
        # Добавляем общую стоимость
        total_cost = sum(data['cost'] for data in timeline.values())
        ax.text(0.02, 0.98, f'Общая стоимость внедрения: {total_cost:,} руб', 
               transform=ax.transAxes, fontsize=12, weight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        
        plt.tight_layout()
        plt.savefig('/workspace/gantt_chart.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return timeline
    
    def create_roi_analysis(self):
        """Анализ окупаемости инвестиций"""
        baseline = self.calculate_baseline_costs()
        ai_impact = self.calculate_ai_impact()
        
        # Общие расходы на внедрение
        total_implementation_cost = self.ai_implementation_costs['total']
        
        # Общая годовая экономия
        total_annual_savings = sum(ai_impact[dept]['net_savings'] for dept in self.departments.keys())
        
        # Окупаемость
        payback_period = total_implementation_cost / total_annual_savings
        
        # 5-летний ROI
        five_year_savings = total_annual_savings * 5
        five_year_roi = ((five_year_savings - total_implementation_cost) / total_implementation_cost) * 100
        
        roi_data = {
            'Стоимость внедрения (руб)': total_implementation_cost,
            'Годовая экономия (руб)': total_annual_savings,
            'Период окупаемости (месяцы)': round(payback_period * 12, 1),
            '5-летний ROI (%)': round(five_year_roi, 1),
            'Общая экономия за 5 лет (руб)': five_year_savings
        }
        
        return roi_data

# Создание и запуск анализа
if __name__ == "__main__":
    analysis = HR_AIAnalysis()
    
    # Создание финансовой сводки
    financial_summary = analysis.create_financial_summary()
    print("=== ФИНАНСОВАЯ СВОДКА ===")
    print(financial_summary.to_string(index=False))
    
    # Анализ ROI
    roi_analysis = analysis.create_roi_analysis()
    print("\n=== АНАЛИЗ ОКУПАЕМОСТИ ===")
    for key, value in roi_analysis.items():
        print(f"{key}: {value:,}" if isinstance(value, (int, float)) and value > 1000 else f"{key}: {value}")
    
    # Создание диаграммы Ганта
    print("\n=== СОЗДАНИЕ ДИАГРАММЫ ГАНТА ===")
    gantt_data = analysis.create_gantt_chart()
    
    # Сохранение данных в CSV
    financial_summary.to_csv('/workspace/financial_summary.csv', index=False, encoding='utf-8')
    
    print("\nАнализ завершен! Результаты сохранены в файлы.")