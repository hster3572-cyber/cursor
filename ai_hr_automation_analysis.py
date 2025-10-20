#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Анализ внедрения AI-ассистента для автоматизации административных задач в HR
Моделирование снижения расходов и роста продуктивности по отделам
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Настройка для русского языка
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

class AIHRAutomationAnalyzer:
    """Класс для анализа внедрения AI в HR-автоматизацию"""
    
    def __init__(self):
        self.departments = {
            'Канцелярия': {
                'employees': 15,
                'avg_salary': 45000,  # руб/месяц
                'admin_tasks_hours': 6,  # часов в день на админ задачи
                'automation_potential': 0.75  # 75% задач можно автоматизировать
            },
            'Офис (HR отдел)': {
                'employees': 8,
                'avg_salary': 65000,
                'admin_tasks_hours': 5,
                'automation_potential': 0.60
            },
            'Бэк-офис': {
                'employees': 12,
                'avg_salary': 55000,
                'admin_tasks_hours': 4,
                'automation_potential': 0.70
            }
        }
        
        self.ai_costs = {
            'initial_setup': 500000,  # руб
            'monthly_license': 25000,  # руб/месяц
            'training_costs': 200000,  # руб
            'maintenance_monthly': 15000  # руб/месяц
        }
        
        self.productivity_metrics = {
            'error_reduction': 0.85,  # снижение ошибок на 85%
            'speed_increase': 2.5,    # увеличение скорости в 2.5 раза
            'quality_improvement': 0.40  # улучшение качества на 40%
        }

    def calculate_current_costs(self):
        """Расчет текущих расходов по отделам"""
        current_costs = {}
        
        for dept_name, dept_data in self.departments.items():
            monthly_salary_cost = dept_data['employees'] * dept_data['avg_salary']
            
            # Расчет стоимости времени на админ задачи
            working_hours_per_month = 22 * 8  # 22 рабочих дня по 8 часов
            hourly_rate = dept_data['avg_salary'] / working_hours_per_month
            admin_cost_per_month = (dept_data['employees'] * 
                                  dept_data['admin_tasks_hours'] * 22 * 
                                  hourly_rate)
            
            current_costs[dept_name] = {
                'total_salary': monthly_salary_cost,
                'admin_tasks_cost': admin_cost_per_month,
                'hourly_rate': hourly_rate
            }
        
        return current_costs

    def calculate_ai_benefits(self):
        """Расчет выгод от внедрения AI"""
        current_costs = self.calculate_current_costs()
        ai_benefits = {}
        
        for dept_name, dept_data in self.departments.items():
            current_admin_cost = current_costs[dept_name]['admin_tasks_cost']
            
            # Экономия от автоматизации
            automation_savings = (current_admin_cost * 
                                dept_data['automation_potential'])
            
            # Дополнительная продуктивность
            productivity_gain = (automation_savings * 
                               (self.productivity_metrics['speed_increase'] - 1))
            
            # Снижение ошибок (экономия на исправлениях)
            error_cost_reduction = current_admin_cost * 0.15 * self.productivity_metrics['error_reduction']
            
            ai_benefits[dept_name] = {
                'automation_savings': automation_savings,
                'productivity_gain': productivity_gain,
                'error_reduction_savings': error_cost_reduction,
                'total_monthly_benefit': automation_savings + productivity_gain + error_cost_reduction
            }
        
        return ai_benefits

    def create_financial_model(self, years=3):
        """Создание финансовой модели на несколько лет"""
        current_costs = self.calculate_current_costs()
        ai_benefits = self.calculate_ai_benefits()
        
        # Общие выгоды по всем отделам
        total_monthly_benefits = sum([benefits['total_monthly_benefit'] 
                                    for benefits in ai_benefits.values()])
        
        # Создание временного ряда
        months = list(range(1, years * 12 + 1))
        
        # Расчет ROI
        financial_data = []
        cumulative_investment = 0
        cumulative_savings = 0
        
        for month in months:
            if month == 1:
                # Первоначальные инвестиции
                monthly_investment = (self.ai_costs['initial_setup'] + 
                                    self.ai_costs['training_costs'] +
                                    self.ai_costs['monthly_license'] +
                                    self.ai_costs['maintenance_monthly'])
            else:
                monthly_investment = (self.ai_costs['monthly_license'] + 
                                    self.ai_costs['maintenance_monthly'])
            
            cumulative_investment += monthly_investment
            cumulative_savings += total_monthly_benefits
            
            net_benefit = cumulative_savings - cumulative_investment
            roi = (net_benefit / cumulative_investment * 100) if cumulative_investment > 0 else 0
            
            financial_data.append({
                'month': month,
                'monthly_investment': monthly_investment,
                'monthly_savings': total_monthly_benefits,
                'cumulative_investment': cumulative_investment,
                'cumulative_savings': cumulative_savings,
                'net_benefit': net_benefit,
                'roi_percent': roi
            })
        
        return pd.DataFrame(financial_data), current_costs, ai_benefits

    def create_department_comparison(self):
        """Создание сравнения по отделам"""
        current_costs = self.calculate_current_costs()
        ai_benefits = self.calculate_ai_benefits()
        
        comparison_data = []
        
        for dept_name in self.departments.keys():
            dept_data = self.departments[dept_name]
            current = current_costs[dept_name]
            benefits = ai_benefits[dept_name]
            
            comparison_data.append({
                'Отдел': dept_name,
                'Сотрудники': dept_data['employees'],
                'Текущие расходы на админ задачи (руб/мес)': current['admin_tasks_cost'],
                'Экономия от автоматизации (руб/мес)': benefits['automation_savings'],
                'Прирост продуктивности (руб/мес)': benefits['productivity_gain'],
                'Экономия от снижения ошибок (руб/мес)': benefits['error_reduction_savings'],
                'Общая выгода (руб/мес)': benefits['total_monthly_benefit'],
                'Потенциал автоматизации (%)': dept_data['automation_potential'] * 100
            })
        
        return pd.DataFrame(comparison_data)

if __name__ == "__main__":
    analyzer = AIHRAutomationAnalyzer()
    
    # Создание финансовой модели
    financial_df, current_costs, ai_benefits = analyzer.create_financial_model()
    
    # Создание сравнения по отделам
    dept_comparison = analyzer.create_department_comparison()
    
    print("=== ФИНАНСОВАЯ МОДЕЛЬ ВНЕДРЕНИЯ AI-АССИСТЕНТА ===")
    print(f"Точка безубыточности: {financial_df[financial_df['net_benefit'] >= 0]['month'].iloc[0]} месяц")
    print(f"ROI через 12 месяцев: {financial_df[financial_df['month'] == 12]['roi_percent'].iloc[0]:.1f}%")
    print(f"ROI через 36 месяцев: {financial_df[financial_df['month'] == 36]['roi_percent'].iloc[0]:.1f}%")
    
    print("\n=== СРАВНЕНИЕ ПО ОТДЕЛАМ ===")
    print(dept_comparison.to_string(index=False))