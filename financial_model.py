#!/usr/bin/env python3
"""
Финансовая модель внедрения AI-ассистента для HR-процессов
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Настройка для корректного отображения русского текста
plt.rcParams['font.family'] = 'DejaVu Sans'

class HR_AI_Financial_Model:
    def __init__(self):
        # Базовые параметры компании (средняя компания 500-1000 сотрудников)
        self.company_size = 750  # количество сотрудников
        self.hr_team_size = 8    # размер HR-команды
        self.avg_hr_salary = 120000  # средняя зарплата HR-специалиста в год (руб)
        self.working_hours_per_year = 2000  # рабочих часов в год
        
        # Стоимость внедрения AI
        self.ai_license_cost_per_user = 30000  # стоимость лицензии на пользователя в год
        self.implementation_cost = 500000  # стоимость внедрения (консультации, настройка)
        self.training_cost = 200000  # стоимость обучения команды
        
        # Параметры эффективности
        self.time_savings_percentage = 0.65  # 65% экономии времени на рутинных задачах
        self.routine_tasks_percentage = 0.6  # 60% времени тратится на рутинные задачи
        self.productivity_increase = 0.25  # 25% увеличение продуктивности
        
    def calculate_current_costs(self):
        """Расчет текущих затрат на HR"""
        annual_hr_salary_costs = self.hr_team_size * self.avg_hr_salary
        routine_tasks_cost = annual_hr_salary_costs * self.routine_tasks_percentage
        
        return {
            'total_hr_costs': annual_hr_salary_costs,
            'routine_tasks_cost': routine_tasks_cost,
            'strategic_tasks_cost': annual_hr_salary_costs * (1 - self.routine_tasks_percentage)
        }
    
    def calculate_ai_costs(self):
        """Расчет затрат на внедрение AI"""
        annual_ai_license = self.hr_team_size * self.ai_license_cost_per_user
        total_implementation = self.implementation_cost + self.training_cost
        
        return {
            'annual_license_cost': annual_ai_license,
            'one_time_implementation': total_implementation,
            'total_first_year': annual_ai_license + total_implementation
        }
    
    def calculate_savings(self):
        """Расчет экономии от внедрения AI"""
        current_costs = self.calculate_current_costs()
        ai_costs = self.calculate_ai_costs()
        
        # Экономия от сокращения времени на рутинные задачи
        routine_savings = current_costs['routine_tasks_cost'] * self.time_savings_percentage
        
        # Дополнительная экономия от повышения продуктивности
        productivity_savings = current_costs['strategic_tasks_cost'] * self.productivity_increase
        
        # Общая экономия
        total_annual_savings = routine_savings + productivity_savings
        
        # Чистая экономия (за вычетом стоимости AI)
        net_annual_savings = total_annual_savings - ai_costs['annual_license_cost']
        
        return {
            'routine_savings': routine_savings,
            'productivity_savings': productivity_savings,
            'total_annual_savings': total_annual_savings,
            'net_annual_savings': net_annual_savings,
            'ai_annual_cost': ai_costs['annual_license_cost']
        }
    
    def calculate_roi(self, years=3):
        """Расчет ROI за указанное количество лет"""
        savings = self.calculate_savings()
        ai_costs = self.calculate_ai_costs()
        
        # Общие затраты на AI за период
        total_ai_costs = ai_costs['one_time_implementation'] + (ai_costs['annual_license_cost'] * years)
        
        # Общая экономия за период
        total_savings = savings['net_annual_savings'] * years
        
        # ROI в процентах
        roi_percentage = ((total_savings - total_ai_costs) / total_ai_costs) * 100
        
        # Срок окупаемости
        payback_period = ai_costs['one_time_implementation'] / savings['net_annual_savings']
        
        return {
            'total_ai_costs': total_ai_costs,
            'total_savings': total_savings,
            'net_benefit': total_savings - total_ai_costs,
            'roi_percentage': roi_percentage,
            'payback_period_years': payback_period
        }
    
    def create_detailed_breakdown(self):
        """Создание детальной разбивки по отделам"""
        departments = {
            'Рекрутинг': {'hr_ratio': 0.3, 'routine_ratio': 0.7},
            'Кадровый учет': {'hr_ratio': 0.25, 'routine_ratio': 0.8},
            'Обучение и развитие': {'hr_ratio': 0.2, 'routine_ratio': 0.4},
            'Компенсации и льготы': {'hr_ratio': 0.15, 'routine_ratio': 0.6},
            'HR-аналитика': {'hr_ratio': 0.1, 'routine_ratio': 0.3}
        }
        
        current_costs = self.calculate_current_costs()
        savings = self.calculate_savings()
        
        breakdown = []
        for dept, params in departments.items():
            dept_hr_costs = current_costs['total_hr_costs'] * params['hr_ratio']
            dept_routine_costs = dept_hr_costs * params['routine_ratio']
            dept_savings = dept_routine_costs * self.time_savings_percentage
            
            breakdown.append({
                'Отдел': dept,
                'Текущие затраты (руб/год)': dept_hr_costs,
                'Рутинные задачи (руб/год)': dept_routine_costs,
                'Экономия (руб/год)': dept_savings,
                'Экономия (%)': (dept_savings / dept_hr_costs) * 100
            })
        
        return pd.DataFrame(breakdown)
    
    def generate_5_year_projection(self):
        """Генерация 5-летней проекции"""
        years = list(range(1, 6))
        projections = []
        
        current_costs = self.calculate_current_costs()
        savings = self.calculate_savings()
        ai_costs = self.calculate_ai_costs()
        
        cumulative_ai_cost = ai_costs['one_time_implementation']
        cumulative_savings = 0
        
        for year in years:
            if year == 1:
                annual_ai_cost = ai_costs['total_first_year']
            else:
                annual_ai_cost = ai_costs['annual_license_cost']
            
            cumulative_ai_cost += annual_ai_cost
            cumulative_savings += savings['net_annual_savings']
            net_benefit = cumulative_savings - cumulative_ai_cost
            
            projections.append({
                'Год': year,
                'Затраты на AI (руб)': annual_ai_cost,
                'Накопленные затраты (руб)': cumulative_ai_cost,
                'Годовая экономия (руб)': savings['net_annual_savings'],
                'Накопленная экономия (руб)': cumulative_savings,
                'Чистая выгода (руб)': net_benefit,
                'ROI (%)': (net_benefit / cumulative_ai_cost) * 100 if cumulative_ai_cost > 0 else 0
            })
        
        return pd.DataFrame(projections)

# Создание экземпляра модели
model = HR_AI_Financial_Model()

# Вывод результатов
print("=== ФИНАНСОВАЯ МОДЕЛЬ ВНЕДРЕНИЯ AI-АССИСТЕНТА ДЛЯ HR ===\n")

# Текущие затраты
current_costs = model.calculate_current_costs()
print("ТЕКУЩИЕ ЗАТРАТЫ НА HR:")
print(f"Общие затраты на HR-команду: {current_costs['total_hr_costs']:,.0f} руб/год")
print(f"Затраты на рутинные задачи: {current_costs['routine_tasks_cost']:,.0f} руб/год")
print(f"Затраты на стратегические задачи: {current_costs['strategic_tasks_cost']:,.0f} руб/год\n")

# Затраты на AI
ai_costs = model.calculate_ai_costs()
print("ЗАТРАТЫ НА ВНЕДРЕНИЕ AI:")
print(f"Стоимость лицензий (год): {ai_costs['annual_license_cost']:,.0f} руб")
print(f"Разовые затраты на внедрение: {ai_costs['one_time_implementation']:,.0f} руб")
print(f"Общие затраты в первый год: {ai_costs['total_first_year']:,.0f} руб\n")

# Экономия
savings = model.calculate_savings()
print("ЭКОНОМИЯ ОТ ВНЕДРЕНИЯ AI:")
print(f"Экономия на рутинных задачах: {savings['routine_savings']:,.0f} руб/год")
print(f"Экономия от повышения продуктивности: {savings['productivity_savings']:,.0f} руб/год")
print(f"Общая годовая экономия: {savings['total_annual_savings']:,.0f} руб/год")
print(f"Чистая годовая экономия: {savings['net_annual_savings']:,.0f} руб/год\n")

# ROI
roi = model.calculate_roi(3)
print("ПОКАЗАТЕЛИ ЭФФЕКТИВНОСТИ (3 года):")
print(f"ROI: {roi['roi_percentage']:.1f}%")
print(f"Срок окупаемости: {roi['payback_period_years']:.1f} лет")
print(f"Чистая выгода за 3 года: {roi['net_benefit']:,.0f} руб\n")

# Детальная разбивка по отделам
print("ДЕТАЛЬНАЯ РАЗБИВКА ПО ОТДЕЛАМ:")
breakdown_df = model.create_detailed_breakdown()
print(breakdown_df.to_string(index=False, float_format='%.0f'))

# 5-летняя проекция
print("\n5-ЛЕТНЯЯ ПРОЕКЦИЯ:")
projection_df = model.generate_5_year_projection()
print(projection_df.to_string(index=False, float_format='%.0f'))