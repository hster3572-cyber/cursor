#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главный скрипт для комплексного анализа внедрения AI-ассистента в HR
Автор: AI Assistant
Дата: 2024
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Импорт наших модулей
from ai_hr_automation_analysis import AIHRAutomationAnalyzer
from gantt_chart_generator import GanttChartGenerator
from presentation_generator import create_full_presentation

# Настройка для русского языка
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def create_visualizations(analyzer, financial_df, dept_comparison):
    """Создание визуализаций для анализа"""
    
    # 1. График ROI по времени
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(financial_df['month'], financial_df['roi_percent'], 'b-', linewidth=2, marker='o')
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.7)
    plt.title('ROI проекта по месяцам', fontsize=14, fontweight='bold')
    plt.xlabel('Месяц')
    plt.ylabel('ROI (%)')
    plt.grid(True, alpha=0.3)
    
    # 2. Кумулятивные инвестиции vs экономия
    plt.subplot(2, 2, 2)
    plt.plot(financial_df['month'], financial_df['cumulative_investment']/1000, 'r-', 
             label='Инвестиции', linewidth=2)
    plt.plot(financial_df['month'], financial_df['cumulative_savings']/1000, 'g-', 
             label='Экономия', linewidth=2)
    plt.title('Кумулятивные показатели (тыс. руб)', fontsize=14, fontweight='bold')
    plt.xlabel('Месяц')
    plt.ylabel('Сумма (тыс. руб)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 3. Сравнение выгод по отделам
    plt.subplot(2, 2, 3)
    dept_benefits = dept_comparison['Общая выгода (руб/мес)'] / 1000
    bars = plt.bar(range(len(dept_benefits)), dept_benefits, 
                   color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    plt.title('Выгода по отделам (тыс. руб/мес)', fontsize=14, fontweight='bold')
    plt.ylabel('Выгода (тыс. руб/мес)')
    plt.xticks(range(len(dept_comparison)), dept_comparison['Отдел'], rotation=45)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars, dept_benefits):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{value:.0f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Потенциал автоматизации
    plt.subplot(2, 2, 4)
    automation_potential = dept_comparison['Потенциал автоматизации (%)']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    plt.pie(automation_potential, labels=dept_comparison['Отдел'], 
            autopct='%1.0f%%', colors=colors, startangle=90)
    plt.title('Потенциал автоматизации по отделам', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('ai_hr_analysis_charts.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✓ Графики созданы и сохранены в 'ai_hr_analysis_charts.png'")

def create_detailed_reports(analyzer, financial_df, dept_comparison):
    """Создание детальных отчетов"""
    
    # Создание Excel-файла с результатами
    with pd.ExcelWriter('AI_HR_Analysis_Results.xlsx', engine='openpyxl') as writer:
        
        # Лист 1: Финансовая модель
        financial_df.to_excel(writer, sheet_name='Финансовая модель', index=False)
        
        # Лист 2: Сравнение по отделам
        dept_comparison.to_excel(writer, sheet_name='Анализ по отделам', index=False)
        
        # Лист 3: Сводка проекта
        summary_data = {
            'Показатель': [
                'Общая продолжительность проекта (месяцев)',
                'Первоначальные инвестиции (руб)',
                'Ежемесячные расходы (руб)',
                'Ежемесячная экономия (руб)',
                'Точка безубыточности (месяц)',
                'ROI через 12 месяцев (%)',
                'ROI через 36 месяцев (%)',
                'Общее количество сотрудников',
                'Средний потенциал автоматизации (%)'
            ],
            'Значение': [
                9,
                700000,
                40000,
                financial_df['monthly_savings'].iloc[0],
                financial_df[financial_df['net_benefit'] >= 0]['month'].iloc[0],
                financial_df[financial_df['month'] == 12]['roi_percent'].iloc[0],
                financial_df[financial_df['month'] == 36]['roi_percent'].iloc[0],
                dept_comparison['Сотрудники'].sum(),
                dept_comparison['Потенциал автоматизации (%)'].mean()
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Сводка проекта', index=False)
    
    print("✓ Детальный Excel-отчет создан: 'AI_HR_Analysis_Results.xlsx'")

def print_executive_summary(financial_df, dept_comparison):
    """Вывод краткого резюме для руководства"""
    
    print("\n" + "="*80)
    print("ИСПОЛНИТЕЛЬНОЕ РЕЗЮМЕ: ВНЕДРЕНИЕ AI-АССИСТЕНТА В HR")
    print("="*80)
    
    print(f"\n📊 КЛЮЧЕВЫЕ ФИНАНСОВЫЕ ПОКАЗАТЕЛИ:")
    print(f"   • Первоначальные инвестиции: 700,000 руб")
    print(f"   • Ежемесячная экономия: {financial_df['monthly_savings'].iloc[0]:,.0f} руб")
    print(f"   • Точка безубыточности: {financial_df[financial_df['net_benefit'] >= 0]['month'].iloc[0]} месяц")
    print(f"   • ROI через 12 месяцев: {financial_df[financial_df['month'] == 12]['roi_percent'].iloc[0]:.1f}%")
    print(f"   • ROI через 36 месяцев: {financial_df[financial_df['month'] == 36]['roi_percent'].iloc[0]:.1f}%")
    
    print(f"\n🏢 ВОЗДЕЙСТВИЕ ПО ОТДЕЛАМ:")
    for _, row in dept_comparison.iterrows():
        print(f"   • {row['Отдел']}: {row['Общая выгода (руб/мес)']:,.0f} руб/мес экономии")
    
    total_monthly_benefit = dept_comparison['Общая выгода (руб/мес)'].sum()
    annual_benefit = total_monthly_benefit * 12
    
    print(f"\n💰 ОБЩИЕ РЕЗУЛЬТАТЫ:")
    print(f"   • Общая ежемесячная экономия: {total_monthly_benefit:,.0f} руб")
    print(f"   • Годовая экономия: {annual_benefit:,.0f} руб")
    print(f"   • Охват сотрудников: {dept_comparison['Сотрудники'].sum()} человек")
    print(f"   • Средний потенциал автоматизации: {dept_comparison['Потенциал автоматизации (%)'].mean():.0f}%")
    
    print(f"\n✅ РЕКОМЕНДАЦИЯ: ПРОЕКТ РЕКОМЕНДУЕТСЯ К РЕАЛИЗАЦИИ")
    print(f"   Высокая экономическая эффективность и быстрая окупаемость")
    
    print("="*80)

def main():
    """Главная функция для запуска полного анализа"""
    
    print("🚀 Запуск комплексного анализа внедрения AI-ассистента в HR...")
    print("="*60)
    
    # Обновляем статус задачи
    # from TodoWrite import TodoWrite
    
    try:
        # 1. Создание анализатора и расчет данных
        print("\n📈 Этап 1: Создание финансовой модели...")
        analyzer = AIHRAutomationAnalyzer()
        financial_df, current_costs, ai_benefits = analyzer.create_financial_model()
        dept_comparison = analyzer.create_department_comparison()
        
        print("✓ Финансовая модель создана")
        print("✓ Анализ по отделам завершен")
        
        # 2. Создание диаграммы Ганта
        print("\n📅 Этап 2: Создание диаграммы Ганта...")
        gantt_generator = GanttChartGenerator()
        gantt_fig = gantt_generator.create_gantt_chart()
        gantt_fig.write_html("gantt_chart.html")
        
        project_summary = gantt_generator.get_project_summary()
        print("✓ Диаграмма Ганта создана и сохранена в 'gantt_chart.html'")
        
        # 3. Создание визуализаций
        print("\n📊 Этап 3: Создание графиков и визуализаций...")
        create_visualizations(analyzer, financial_df, dept_comparison)
        
        # 4. Создание детальных отчетов
        print("\n📋 Этап 4: Создание детальных отчетов...")
        create_detailed_reports(analyzer, financial_df, dept_comparison)
        
        # 5. Создание презентации
        print("\n🎯 Этап 5: Создание презентации...")
        presentation_file = create_full_presentation(dept_comparison, financial_df)
        print(f"✓ Презентация создана: '{presentation_file}'")
        
        # 6. Вывод исполнительного резюме
        print_executive_summary(financial_df, dept_comparison)
        
        # 7. Итоговая информация о файлах
        print(f"\n📁 СОЗДАННЫЕ ФАЙЛЫ:")
        print(f"   • {presentation_file} - Основная презентация")
        print(f"   • AI_HR_Analysis_Results.xlsx - Детальные расчеты")
        print(f"   • gantt_chart.html - Интерактивная диаграмма Ганта")
        print(f"   • ai_hr_analysis_charts.png - Графики анализа")
        
        print(f"\n🎉 АНАЛИЗ ЗАВЕРШЕН УСПЕШНО!")
        print(f"Все файлы готовы для презентации руководству.")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении анализа: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Программа завершена успешно!")
    else:
        print("\n❌ Программа завершена с ошибками!")
        sys.exit(1)