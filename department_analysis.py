#!/usr/bin/env python3
"""
Детальный анализ влияния AI на различные HR-отделы
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Настройка для корректного отображения русского текста
plt.rcParams['font.family'] = 'DejaVu Sans'

class DepartmentAnalysis:
    def __init__(self):
        # Базовые данные по отделам
        self.departments = {
            'Рекрутинг': {
                'staff_count': 2,
                'avg_salary': 130000,
                'routine_tasks_ratio': 0.7,
                'ai_impact_ratio': 0.75,
                'tasks': [
                    'Создание и публикация вакансий',
                    'Первичная сортировка резюме',
                    'Планирование интервью',
                    'Коммуникация с кандидатами',
                    'Подготовка отчетов по рекрутингу'
                ]
            },
            'Кадровый учет': {
                'staff_count': 2,
                'avg_salary': 100000,
                'routine_tasks_ratio': 0.8,
                'ai_impact_ratio': 0.8,
                'tasks': [
                    'Обработка трудовых договоров',
                    'Ведение личных дел',
                    'Расчет отпусков и больничных',
                    'Подготовка справок',
                    'Ведение табелей учета рабочего времени'
                ]
            },
            'Обучение и развитие': {
                'staff_count': 1,
                'avg_salary': 110000,
                'routine_tasks_ratio': 0.4,
                'ai_impact_ratio': 0.6,
                'tasks': [
                    'Планирование обучения',
                    'Создание учебных материалов',
                    'Отслеживание прогресса',
                    'Оценка эффективности программ',
                    'Координация с внешними провайдерами'
                ]
            },
            'Компенсации и льготы': {
                'staff_count': 1,
                'avg_salary': 115000,
                'routine_tasks_ratio': 0.6,
                'ai_impact_ratio': 0.7,
                'tasks': [
                    'Расчет зарплат и премий',
                    'Обработка заявлений на льготы',
                    'Анализ рыночных зарплат',
                    'Подготовка бюджетов',
                    'Коммуникация по вопросам оплаты'
                ]
            },
            'HR-аналитика': {
                'staff_count': 1,
                'avg_salary': 140000,
                'routine_tasks_ratio': 0.3,
                'ai_impact_ratio': 0.9,
                'tasks': [
                    'Сбор и обработка данных',
                    'Создание отчетов и дашбордов',
                    'Анализ трендов',
                    'Прогнозирование потребностей',
                    'Подготовка презентаций'
                ]
            },
            'Корпоративная культура': {
                'staff_count': 1,
                'avg_salary': 120000,
                'routine_tasks_ratio': 0.5,
                'ai_impact_ratio': 0.5,
                'tasks': [
                    'Организация мероприятий',
                    'Внутренние коммуникации',
                    'Управление корпоративными каналами',
                    'Сбор обратной связи',
                    'Разработка политик'
                ]
            }
        }
        
        # Параметры AI-внедрения
        self.ai_license_cost = 30000  # стоимость лицензии на пользователя в год
        self.implementation_cost_per_dept = 100000  # стоимость внедрения на отдел
        
    def calculate_department_metrics(self):
        """Расчет метрик по каждому отделу"""
        results = []
        
        for dept_name, dept_data in self.departments.items():
            # Текущие затраты
            annual_salary_cost = dept_data['staff_count'] * dept_data['avg_salary']
            routine_tasks_cost = annual_salary_cost * dept_data['routine_tasks_ratio']
            strategic_tasks_cost = annual_salary_cost * (1 - dept_data['routine_tasks_ratio'])
            
            # Экономия от AI
            ai_savings = routine_tasks_cost * dept_data['ai_impact_ratio']
            
            # Затраты на AI
            ai_license_cost = dept_data['staff_count'] * self.ai_license_cost
            ai_implementation_cost = self.implementation_cost_per_dept
            
            # Чистая экономия
            net_savings = ai_savings - ai_license_cost
            
            # ROI
            roi = (net_savings / (ai_license_cost + ai_implementation_cost)) * 100 if (ai_license_cost + ai_implementation_cost) > 0 else 0
            
            # Время на окупаемость
            payback_period = ai_implementation_cost / net_savings if net_savings > 0 else float('inf')
            
            results.append({
                'Отдел': dept_name,
                'Сотрудников': dept_data['staff_count'],
                'Средняя зарплата': dept_data['avg_salary'],
                'Годовые затраты': annual_salary_cost,
                'Рутинные задачи (%)': dept_data['routine_tasks_ratio'] * 100,
                'Экономия от AI': ai_savings,
                'Затраты на AI': ai_license_cost,
                'Чистая экономия': net_savings,
                'ROI (%)': roi,
                'Окупаемость (лет)': payback_period,
                'Эффективность AI (%)': dept_data['ai_impact_ratio'] * 100
            })
        
        return pd.DataFrame(results)
    
    def create_productivity_analysis(self):
        """Анализ влияния на продуктивность по отделам"""
        productivity_data = []
        
        for dept_name, dept_data in self.departments.items():
            # Базовые показатели продуктивности
            base_productivity = 100  # базовый уровень 100%
            
            # Увеличение продуктивности от автоматизации рутинных задач
            routine_improvement = dept_data['routine_tasks_ratio'] * dept_data['ai_impact_ratio'] * 60  # до 60% улучшения
            
            # Дополнительное улучшение от освобождения времени для стратегических задач
            strategic_improvement = (1 - dept_data['routine_tasks_ratio']) * 25  # до 25% улучшения
            
            # Общее улучшение продуктивности
            total_improvement = routine_improvement + strategic_improvement
            new_productivity = base_productivity + total_improvement
            
            productivity_data.append({
                'Отдел': dept_name,
                'Текущая продуктивность (%)': base_productivity,
                'Улучшение от автоматизации (%)': routine_improvement,
                'Улучшение от стратегических задач (%)': strategic_improvement,
                'Общее улучшение (%)': total_improvement,
                'Новая продуктивность (%)': new_productivity
            })
        
        return pd.DataFrame(productivity_data)
    
    def create_task_automation_matrix(self):
        """Матрица автоматизации задач по отделам"""
        task_matrix = []
        
        for dept_name, dept_data in self.departments.items():
            for task in dept_data['tasks']:
                # Определение уровня автоматизации на основе типа задачи
                if 'создание' in task.lower() or 'подготовка' in task.lower() or 'обработка' in task.lower():
                    automation_level = 0.9
                elif 'планирование' in task.lower() or 'координация' in task.lower():
                    automation_level = 0.7
                elif 'коммуникация' in task.lower() or 'организация' in task.lower():
                    automation_level = 0.5
                else:
                    automation_level = 0.6
                
                task_matrix.append({
                    'Отдел': dept_name,
                    'Задача': task,
                    'Уровень автоматизации (%)': automation_level * 100,
                    'Время экономии (%)': automation_level * 80,  # до 80% экономии времени
                    'Качество улучшения (%)': automation_level * 30  # до 30% улучшения качества
                })
        
        return pd.DataFrame(task_matrix)
    
    def create_visualizations(self):
        """Создание визуализаций"""
        # 1. Экономия по отделам
        metrics_df = self.calculate_department_metrics()
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # График экономии по отделам
        ax1 = axes[0, 0]
        dept_names = metrics_df['Отдел']
        savings = metrics_df['Чистая экономия']
        colors = plt.cm.Set3(np.linspace(0, 1, len(dept_names)))
        
        bars = ax1.bar(dept_names, savings, color=colors)
        ax1.set_title('Чистая экономия по отделам (руб/год)', fontweight='bold')
        ax1.set_ylabel('Экономия (руб)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Добавление значений на столбцы
        for bar, saving in zip(bars, savings):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{saving:,.0f}', ha='center', va='bottom', fontsize=9)
        
        # График ROI по отделам
        ax2 = axes[0, 1]
        roi_values = metrics_df['ROI (%)']
        bars2 = ax2.bar(dept_names, roi_values, color=colors)
        ax2.set_title('ROI по отделам (%)', fontweight='bold')
        ax2.set_ylabel('ROI (%)')
        ax2.tick_params(axis='x', rotation=45)
        
        for bar, roi in zip(bars2, roi_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{roi:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # График улучшения продуктивности
        ax3 = axes[1, 0]
        productivity_df = self.create_productivity_analysis()
        improvement = productivity_df['Общее улучшение (%)']
        
        bars3 = ax3.bar(dept_names, improvement, color=colors)
        ax3.set_title('Улучшение продуктивности по отделам (%)', fontweight='bold')
        ax3.set_ylabel('Улучшение (%)')
        ax3.tick_params(axis='x', rotation=45)
        
        for bar, imp in zip(bars3, improvement):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{imp:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # График времени окупаемости
        ax4 = axes[1, 1]
        payback = metrics_df['Окупаемость (лет)']
        # Ограничиваем максимальное значение для лучшей визуализации
        payback_limited = [min(p, 5) for p in payback]
        
        bars4 = ax4.bar(dept_names, payback_limited, color=colors)
        ax4.set_title('Время окупаемости по отделам (лет)', fontweight='bold')
        ax4.set_ylabel('Годы')
        ax4.tick_params(axis='x', rotation=45)
        
        for bar, pb in zip(bars4, payback_limited):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{pb:.1f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('/workspace/department_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Матрица автоматизации задач
        task_matrix_df = self.create_task_automation_matrix()
        
        plt.figure(figsize=(14, 10))
        pivot_table = task_matrix_df.pivot_table(
            index='Отдел', 
            columns='Задача', 
            values='Уровень автоматизации (%)',
            fill_value=0
        )
        
        sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Уровень автоматизации (%)'})
        plt.title('Матрица автоматизации задач по отделам', fontweight='bold', fontsize=16)
        plt.xlabel('Задачи')
        plt.ylabel('Отделы')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        plt.savefig('/workspace/task_automation_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()

# Запуск анализа
if __name__ == "__main__":
    analysis = DepartmentAnalysis()
    
    print("=== АНАЛИЗ ПО ОТДЕЛАМ ===\n")
    
    # Расчет метрик
    metrics_df = analysis.calculate_department_metrics()
    print("МЕТРИКИ ПО ОТДЕЛАМ:")
    print(metrics_df.to_string(index=False, float_format='%.0f'))
    
    print("\nАНАЛИЗ ПРОДУКТИВНОСТИ:")
    productivity_df = analysis.create_productivity_analysis()
    print(productivity_df.to_string(index=False, float_format='%.1f'))
    
    print("\nМАТРИЦА АВТОМАТИЗАЦИИ ЗАДАЧ:")
    task_matrix_df = analysis.create_task_automation_matrix()
    print(task_matrix_df.to_string(index=False, float_format='%.0f'))
    
    print("\nСоздание визуализаций...")
    analysis.create_visualizations()
    
    print("\nГрафики сохранены:")
    print("- department_analysis.png")
    print("- task_automation_matrix.png")