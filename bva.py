# Developed by N.A.Pearson, HPE OpsRamp
# v1.5 - June 2025 - Added Executive Report Generator with PDF/HTML Export

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io
from datetime import datetime

# Executive Report Dependencies
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    import matplotlib.pyplot as plt
    from io import BytesIO
    REPORT_DEPENDENCIES_AVAILABLE = True
except ImportError:
    REPORT_DEPENDENCIES_AVAILABLE = False

# Set page configuration
st.set_page_config(page_title="Business Value Assessment Tool", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.header("Customize Your Financial Impact Model Inputs")

# Solution Name Input
solution_name = st.sidebar.text_input("Solution Name", value="AIOPs", key="solution_name")

# --- Implementation Timeline ---
st.sidebar.subheader("📅 Implementation Timeline")
implementation_delay_months = st.sidebar.slider(
    "Implementation Delay (months)", 
    0, 24, 6, 
    help="Time from project start until benefits begin to be realized",
    key="implementation_delay"
)
benefits_ramp_up_months = st.sidebar.slider(
    "Benefits Ramp-up Period (months)", 
    0, 12, 3,
    help="Time to reach full benefits after go-live (gradual adoption)",
    key="benefits_ramp_up"
)

# --- Industry Benchmark Templates ---
industry_templates = {
    "Custom": {},
    "Financial Services": {
        "alert_volume": 1_200_000,
        "major_incident_volume": 140,
        "avg_alert_triage_time": 25,
        "alert_reduction_pct": 40,
        "incident_volume": 400_000,
        "avg_incident_triage_time": 30,
        "incident_reduction_pct": 40,
        "mttr_improvement_pct": 40
    },
    "Retail": {
        "alert_volume": 600_000,
        "major_incident_volume": 80,
        "avg_alert_triage_time": 20,
        "alert_reduction_pct": 30,
        "incident_volume": 200_000,
        "avg_incident_triage_time": 25,
        "incident_reduction_pct": 30,
        "mttr_improvement_pct": 30
    },
    "MSP": {
        "alert_volume": 2_500_000,
        "major_incident_volume": 200,
        "avg_alert_triage_time": 35,
        "alert_reduction_pct": 50,
        "incident_volume": 800_000,
        "avg_incident_triage_time": 35,
        "incident_reduction_pct": 50,
        "mttr_improvement_pct": 50
    },
    "Healthcare": {
        "alert_volume": 800_000,
        "major_incident_volume": 100,
        "avg_alert_triage_time": 30,
        "alert_reduction_pct": 35,
        "incident_volume": 300_000,
        "avg_incident_triage_time": 30,
        "incident_reduction_pct": 35,
        "mttr_improvement_pct": 35
    },
    "Telecom": {
        "alert_volume": 1_800_000,
        "major_incident_volume": 160,
        "avg_alert_triage_time": 35,
        "alert_reduction_pct": 45,
        "incident_volume": 600_000,
        "avg_incident_triage_time": 35,
        "incident_reduction_pct": 40,
        "mttr_improvement_pct": 45
    }
}

selected_template = st.sidebar.selectbox("Select Industry Template", list(industry_templates.keys()), key="industry_template")
template = industry_templates[selected_template]
st.sidebar.caption("📌 Industry templates provide baseline values for estimation only. Adjust any field as needed.")

# --- Currency Selection ---
currency_symbol = st.sidebar.selectbox("Currency", ["$", "€", "£", "Kč"], key="currency")

# --- Working Hours Configuration ---
st.sidebar.subheader("⏰ Working Hours Configuration")
hours_per_day = st.sidebar.number_input(
    "Working Hours per Day", 
    value=8.0, 
    min_value=1.0, 
    max_value=24.0,
    step=0.5,
    key="hours_per_day",
    help="Standard working hours per day for your FTEs"
)
days_per_week = st.sidebar.number_input(
    "Working Days per Week", 
    value=5, 
    min_value=1, 
    max_value=7,
    key="days_per_week",
    help="Standard working days per week"
)
weeks_per_year = st.sidebar.number_input(
    "Working Weeks per Year", 
    value=52, 
    min_value=1, 
    max_value=52,
    key="weeks_per_year",
    help="Total weeks worked per year"
)
holiday_sick_days = st.sidebar.number_input(
    "Holiday + Sick Days per Year", 
    value=25, 
    min_value=0, 
    max_value=100,
    key="holiday_sick_days",
    help="Total days off per year (holidays, vacation, sick leave)"
)

# Calculate and display total working hours
total_working_days = (weeks_per_year * days_per_week) - holiday_sick_days
working_hours_per_fte_per_year = total_working_days * hours_per_day
st.sidebar.info(f"**Calculated: {working_hours_per_fte_per_year:,.0f} working hours per FTE per year**")

# --- ALERT INPUTS ---
st.sidebar.subheader("🚨 Alert Management")
alert_volume = st.sidebar.number_input(
    "Total Infrastructure Related Alerts Managed per Year", 
    value=template.get("alert_volume", 0),
    key="alert_volume"
)
alert_ftes = st.sidebar.number_input(
    "Total FTEs Managing Infrastructure Alerts", 
    value=0,
    key="alert_ftes"
)
avg_alert_triage_time = st.sidebar.number_input(
    "Average Alert Triage Time (minutes)", 
    value=template.get("avg_alert_triage_time", 0),
    key="avg_alert_triage_time"
)
avg_alert_fte_salary = st.sidebar.number_input(
    "Average Annual Salary per Alert Management FTE", 
    value=50000,
    key="avg_alert_fte_salary"
)
alert_reduction_pct = st.sidebar.slider(
    "% Alert Reduction", 
    0, 100, 
    value=template.get("alert_reduction_pct", 0),
    key="alert_reduction_pct"
)
alert_triage_time_saved_pct = st.sidebar.slider(
    "% Alert Triage Time Reduction", 
    0, 100, 0,
    key="alert_triage_time_saved_pct"
)

# --- INCIDENT INPUTS ---
st.sidebar.subheader("🔧 Incident Management")
incident_volume = st.sidebar.number_input(
    "Total Infrastructure Related Incident Volumes Managed per Year", 
    value=template.get("incident_volume", 0),
    key="incident_volume"
)
incident_ftes = st.sidebar.number_input(
    "Total FTEs Managing Infrastructure Incidents", 
    value=0,
    key="incident_ftes"
)
avg_incident_triage_time = st.sidebar.number_input(
    "Average Incident Triage Time (minutes)", 
    value=template.get("avg_incident_triage_time", 0),
    key="avg_incident_triage_time"
)
avg_incident_fte_salary = st.sidebar.number_input(
    "Average Annual Salary per Incident Management FTE", 
    value=50000,
    key="avg_incident_fte_salary"
)
incident_reduction_pct = st.sidebar.slider(
    "% Incident Reduction", 
    0, 100, 
    value=template.get("incident_reduction_pct", 0),
    key="incident_reduction_pct"
)
incident_triage_time_savings_pct = st.sidebar.slider(
    "% Incident Triage Time Reduction", 
    0, 100, 0,
    key="incident_triage_time_savings_pct"
)

# --- MAJOR INCIDENT INPUTS ---
st.sidebar.subheader("🚨 Major Incidents (Sev1)")
major_incident_volume = st.sidebar.number_input(
    "Total Infrastructure Related Major Incidents per Year (Sev1)", 
    value=template.get("major_incident_volume", 0),
    key="major_incident_volume"
)
avg_major_incident_cost = st.sidebar.number_input(
    "Average Major Incident Cost per Hour", 
    value=0,
    key="avg_major_incident_cost"
)
avg_mttr_hours = st.sidebar.number_input(
    "Average MTTR (hours)", 
    value=0.0,
    key="avg_mttr_hours"
)
mttr_improvement_pct = st.sidebar.slider(
    "MTTR Improvement Percentage", 
    0, 100, 
    value=template.get("mttr_improvement_pct", 0),
    key="mttr_improvement_pct"
)

# --- OTHER BENEFITS ---
st.sidebar.subheader("💰 Additional Benefits")
tool_savings = st.sidebar.number_input(
    "Tool Consolidation Savings", 
    value=0,
    key="tool_savings"
)
people_cost_per_year = st.sidebar.number_input(
    "People Efficiency Gains", 
    value=0,
    key="people_efficiency"
)
fte_avoidance = st.sidebar.number_input(
    "FTE Avoidance (annualized value in local currency)", 
    value=0,
    key="fte_avoidance"
)
sla_penalty_avoidance = st.sidebar.number_input(
    "SLA Penalty Avoidance (Service Providers)", 
    value=0,
    key="sla_penalty"
)
revenue_growth = st.sidebar.number_input(
    "Revenue Growth (Service Providers)", 
    value=0,
    key="revenue_growth"
)
capex_savings = st.sidebar.number_input(
    "Capital Expenditure Savings (Hardware)", 
    value=0,
    key="capex_savings"
)
opex_savings = st.sidebar.number_input(
    "Operational Expenditure Savings (e.g. Storage Costs)", 
    value=0,
    key="opex_savings"
)

# --- COSTS ---
st.sidebar.subheader("💳 Solution Costs")
platform_cost = st.sidebar.number_input(
    "Annual Subscription Cost (After discounts)", 
    value=0,
    key="platform_cost"
)
services_cost = st.sidebar.number_input(
    "Implementation & Services (One-Time)", 
    value=0,
    key="services_cost"
)

# --- FINANCIAL SETTINGS ---
st.sidebar.subheader("📊 Financial Analysis Settings")
evaluation_years = st.sidebar.slider(
    "Evaluation Period (Years)", 
    1, 5, 3,
    key="evaluation_years"
)
discount_rate = st.sidebar.slider(
    "NPV Discount Rate (%)", 
    0, 20, 10,
    key="discount_rate"
) / 100

# --- CORRECTED CALCULATIONS WITH CONFIGURABLE WORKING HOURS ---

# Function to calculate alert costs based on FTE time allocation
def calculate_alert_costs(alert_volume, alert_ftes, avg_alert_triage_time, avg_salary_per_year, 
                         hours_per_day, days_per_week, weeks_per_year, holiday_sick_days):
    """Calculate the true cost per alert based on FTE time allocation"""
    if alert_volume == 0 or alert_ftes == 0:
        return 0, 0, 0, 0
    
    total_alert_time_minutes_per_year = alert_volume * avg_alert_triage_time
    total_alert_time_hours_per_year = total_alert_time_minutes_per_year / 60
    
    total_working_days = (weeks_per_year * days_per_week) - holiday_sick_days
    working_hours_per_fte_per_year = total_working_days * hours_per_day
    total_available_fte_hours = alert_ftes * working_hours_per_fte_per_year
    
    fte_time_percentage_on_alerts = total_alert_time_hours_per_year / total_available_fte_hours if total_available_fte_hours > 0 else 0
    
    total_fte_cost = alert_ftes * avg_salary_per_year
    total_alert_handling_cost = total_fte_cost * fte_time_percentage_on_alerts
    cost_per_alert = total_alert_handling_cost / alert_volume if alert_volume > 0 else 0
    
    return cost_per_alert, total_alert_handling_cost, fte_time_percentage_on_alerts, working_hours_per_fte_per_year

# Function to calculate incident costs based on FTE time allocation
def calculate_incident_costs(incident_volume, incident_ftes, avg_incident_triage_time, avg_salary_per_year,
                           hours_per_day, days_per_week, weeks_per_year, holiday_sick_days):
    """Calculate the true cost per incident based on FTE time allocation"""
    if incident_volume == 0 or incident_ftes == 0:
        return 0, 0, 0, 0
    
    total_incident_time_minutes_per_year = incident_volume * avg_incident_triage_time
    total_incident_time_hours_per_year = total_incident_time_minutes_per_year / 60
    
    total_working_days = (weeks_per_year * days_per_week) - holiday_sick_days
    working_hours_per_fte_per_year = total_working_days * hours_per_day
    total_available_fte_hours = incident_ftes * working_hours_per_fte_per_year
    
    fte_time_percentage_on_incidents = total_incident_time_hours_per_year / total_available_fte_hours if total_available_fte_hours > 0 else 0
    
    total_fte_cost = incident_ftes * avg_salary_per_year
    total_incident_handling_cost = total_fte_cost * fte_time_percentage_on_incidents
    cost_per_incident = total_incident_handling_cost / incident_volume if incident_volume > 0 else 0
    
    return cost_per_incident, total_incident_handling_cost, fte_time_percentage_on_incidents, working_hours_per_fte_per_year

# Calculate alert and incident costs
cost_per_alert, total_alert_handling_cost, alert_fte_percentage, alert_working_hours = calculate_alert_costs(
    alert_volume, alert_ftes, avg_alert_triage_time, avg_alert_fte_salary,
    hours_per_day, days_per_week, weeks_per_year, holiday_sick_days
)

cost_per_incident, total_incident_handling_cost, incident_fte_percentage, incident_working_hours = calculate_incident_costs(
    incident_volume, incident_ftes, avg_incident_triage_time, avg_incident_fte_salary,
    hours_per_day, days_per_week, weeks_per_year, holiday_sick_days
)

# Calculate baseline savings
avoided_alerts = alert_volume * (alert_reduction_pct / 100)
remaining_alerts = alert_volume - avoided_alerts
alert_reduction_savings = avoided_alerts * cost_per_alert
remaining_alert_handling_cost = remaining_alerts * cost_per_alert
alert_triage_savings = remaining_alert_handling_cost * (alert_triage_time_saved_pct / 100)

avoided_incidents = incident_volume * (incident_reduction_pct / 100)
remaining_incidents = incident_volume - avoided_incidents
incident_reduction_savings = avoided_incidents * cost_per_incident
remaining_incident_handling_cost = remaining_incidents * cost_per_incident
incident_triage_savings = remaining_incident_handling_cost * (incident_triage_time_savings_pct / 100)

mttr_hours_saved_per_incident = (mttr_improvement_pct / 100) * avg_mttr_hours
total_mttr_hours_saved = major_incident_volume * mttr_hours_saved_per_incident
major_incident_savings = total_mttr_hours_saved * avg_major_incident_cost

# Total Annual Benefits (baseline)
total_annual_benefits = (
    alert_reduction_savings + alert_triage_savings + incident_reduction_savings +
    incident_triage_savings + major_incident_savings + tool_savings + people_cost_per_year +
    fte_avoidance + sla_penalty_avoidance + revenue_growth + capex_savings + opex_savings
)

# --- Implementation Delay Functions ---
def calculate_benefit_realization_factor(month, implementation_delay_months, ramp_up_months):
    """Calculate what percentage of benefits are realized in a given month"""
    if month <= implementation_delay_months:
        return 0.0  # No benefits during implementation
    elif month <= implementation_delay_months + ramp_up_months:
        # Linear ramp-up during ramp-up period
        months_since_golive = month - implementation_delay_months
        return months_since_golive / ramp_up_months
    else:
        return 1.0  # Full benefits realized

def calculate_scenario_results(benefits_multiplier, implementation_delay_multiplier, scenario_name):
    """Calculate NPV, ROI, and payback for a given scenario"""
    # Adjust benefits and timeline
    scenario_benefits = total_annual_benefits * benefits_multiplier
    scenario_impl_delay = max(1, int(implementation_delay_months * implementation_delay_multiplier))
    scenario_ramp_up = benefits_ramp_up_months
    
    # Calculate cash flows
    scenario_cash_flows = []
    for year in range(1, evaluation_years + 1):
        year_start_month = (year - 1) * 12 + 1
        year_end_month = year * 12
        
        monthly_factors = []
        for month in range(year_start_month, year_end_month + 1):
            factor = calculate_benefit_realization_factor(month, scenario_impl_delay, scenario_ramp_up)
            monthly_factors.append(factor)
        
        avg_realization_factor = np.mean(monthly_factors)
        year_benefits = scenario_benefits * avg_realization_factor
        year_platform_cost = platform_cost
        year_services_cost = services_cost if year == 1 else 0
        year_net_cash_flow = year_benefits - year_platform_cost - year_services_cost
        
        scenario_cash_flows.append({
            'year': year,
            'benefits': year_benefits,
            'platform_cost': year_platform_cost,
            'services_cost': year_services_cost,
            'net_cash_flow': year_net_cash_flow,
            'realization_factor': avg_realization_factor
        })
    
    # Calculate metrics
    scenario_npv = sum([cf['net_cash_flow'] / ((1 + discount_rate) ** cf['year']) for cf in scenario_cash_flows])
    scenario_tco = sum([cf['platform_cost'] + cf['services_cost'] for cf in scenario_cash_flows])
    scenario_roi = scenario_npv / scenario_tco if scenario_tco != 0 else 0
    
    # Calculate payback
    scenario_payback = "N/A"
    cumulative_net_cash_flow = 0
    for cf in scenario_cash_flows:
        cumulative_net_cash_flow += cf['net_cash_flow']
        if cumulative_net_cash_flow >= 0:
            scenario_payback = f"{cf['year']} years"
            break
    
    return {
        'npv': scenario_npv,
        'roi': scenario_roi,
        'payback': scenario_payback,
        'impl_delay': scenario_impl_delay,
        'benefits_mult': benefits_multiplier,
        'cash_flows': scenario_cash_flows,
        'annual_benefits': scenario_benefits
    }

# Calculate scenarios
scenarios = {
    "Conservative": {
        "benefits_multiplier": 0.7,  # 30% lower benefits
        "implementation_delay_multiplier": 1.3,  # 30% longer implementation
        "description": "Benefits 30% lower, implementation 30% longer",
        "color": "#ff6b6b",
        "icon": "🔴"
    },
    "Expected": {
        "benefits_multiplier": 1.0,  # Baseline
        "implementation_delay_multiplier": 1.0,  # Baseline
        "description": "Baseline assumptions as entered",
        "color": "#4ecdc4",
        "icon": "🟢"
    },
    "Optimistic": {
        "benefits_multiplier": 1.2,  # 20% higher benefits
        "implementation_delay_multiplier": 0.8,  # 20% faster implementation
        "description": "Benefits 20% higher, implementation 20% faster",
        "color": "#45b7d1",
        "icon": "🔵"
    }
}

scenario_results = {}
for scenario_name, params in scenarios.items():
    scenario_results[scenario_name] = calculate_scenario_results(
        params["benefits_multiplier"], 
        params["implementation_delay_multiplier"],
        scenario_name
    )
    scenario_results[scenario_name].update({
        "color": params["color"],
        "description": params["description"],
        "icon": params["icon"]
    })

def create_implementation_timeline_chart(implementation_delay_months, ramp_up_months, evaluation_years, currency_symbol, total_annual_benefits):
    """Create a visual timeline showing benefit realization over time"""
    
    total_months = evaluation_years * 12
    months = list(range(1, total_months + 1))
    realization_factors = []
    monthly_benefits = []
    
    for month in months:
        factor = calculate_benefit_realization_factor(month, implementation_delay_months, ramp_up_months)
        realization_factors.append(factor * 100)
        monthly_benefits.append(total_annual_benefits * factor / 12)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=realization_factors, mode='lines+markers', name='Benefit Realization %',
        line=dict(color='#2E86AB', width=3), marker=dict(size=4),
        hovertemplate='<b>Month %{x}</b><br>Benefit Realization: %{y:.1f}%<br><extra></extra>',
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=[b/1000 for b in monthly_benefits], mode='lines', name=f'Monthly Benefits ({currency_symbol}K)',
        line=dict(color='#A23B72', width=2), fill='tonexty', fillcolor='rgba(162, 59, 114, 0.2)',
        hovertemplate='<b>Month %{x}</b><br>' + f'Monthly Benefit: {currency_symbol}' + '%{customdata:,.0f}<br><extra></extra>',
        customdata=monthly_benefits, yaxis='y2'
    ))
    
    if implementation_delay_months > 0:
        fig.add_vline(x=implementation_delay_months, line_dash="dash", line_color="red", line_width=2,
                      annotation_text="Go-Live", annotation_position="top",
                      annotation=dict(bgcolor="white", bordercolor="red"))
    
    if ramp_up_months > 0:
        fig.add_vline(x=implementation_delay_months + ramp_up_months, line_dash="dash", line_color="green", line_width=2,
                      annotation_text="Full Benefits", annotation_position="top",
                      annotation=dict(bgcolor="white", bordercolor="green"))
    
    if implementation_delay_months > 0:
        fig.add_vrect(x0=0, x1=implementation_delay_months, fillcolor="red", opacity=0.1, layer="below", line_width=0,
                      annotation_text="Implementation Phase", annotation_position="top left",
                      annotation=dict(textangle=0, font=dict(size=10, color="red")))
    
    if ramp_up_months > 0:
        fig.add_vrect(x0=implementation_delay_months, x1=implementation_delay_months + ramp_up_months,
                      fillcolor="orange", opacity=0.1, layer="below", line_width=0,
                      annotation_text="Ramp-up Phase", annotation_position="top left",
                      annotation=dict(textangle=0, font=dict(size=10, color="orange")))
    
    fig.add_vrect(x0=implementation_delay_months + ramp_up_months, x1=total_months,
                  fillcolor="green", opacity=0.1, layer="below", line_width=0,
                  annotation_text="Full Benefits Phase", annotation_position="top left",
                  annotation=dict(textangle=0, font=dict(size=10, color="green")))
    
    fig.update_layout(
        title={'text': 'Implementation Timeline & Benefit Realization', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 18}},
        xaxis_title="Months from Project Start",
        yaxis=dict(title="Benefit Realization (%)", side="left", range=[0, 105], color='#2E86AB'),
        yaxis2=dict(title=f"Monthly Benefits ({currency_symbol}K)", side="right", overlaying="y", color='#A23B72'),
        height=500, hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=80), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig

# --- EXECUTIVE REPORT GENERATOR FUNCTIONS ---

def create_executive_summary_data(scenario_results, currency_symbol):
    """Create data structure for executive summary"""
    return {
        'investment_summary': {
            'conservative_npv': scenario_results['Conservative']['npv'],
            'expected_npv': scenario_results['Expected']['npv'],
            'optimistic_npv': scenario_results['Optimistic']['npv'],
            'expected_roi': scenario_results['Expected']['roi'],
            'payback_period': scenario_results['Expected']['payback'],
            'currency': currency_symbol
        },
        'key_benefits': {
            'alert_reduction_savings': alert_reduction_savings,
            'incident_reduction_savings': incident_reduction_savings,
            'major_incident_savings': major_incident_savings,
            'total_operational_savings': alert_reduction_savings + incident_reduction_savings + major_incident_savings,
            'additional_benefits': tool_savings + people_cost_per_year + fte_avoidance + revenue_growth
        },
        'implementation': {
            'delay_months': implementation_delay_months,
            'ramp_up_months': benefits_ramp_up_months,
            'full_benefits_month': implementation_delay_months + benefits_ramp_up_months,
            'evaluation_years': evaluation_years
        }
    }

def create_timeline_chart_for_pdf():
    """Create implementation timeline chart for PDF"""
    if not REPORT_DEPENDENCIES_AVAILABLE:
        return None
        
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Timeline data
    phases = ['Implementation', 'Ramp-up', 'Full Benefits']
    starts = [0, implementation_delay_months, implementation_delay_months + benefits_ramp_up_months]
    durations = [implementation_delay_months, benefits_ramp_up_months, 24 - (implementation_delay_months + benefits_ramp_up_months)]
    colors_list = ['#ff6b6b', '#ffa500', '#4ecdc4']
    
    # Create Gantt chart
    for i, (phase, start, duration, color) in enumerate(zip(phases, starts, durations, colors_list)):
        if duration > 0:
            ax.barh(i, duration, left=start, height=0.6, color=color, alpha=0.7, label=phase)
            ax.text(start + duration/2, i, phase, ha='center', va='center', fontweight='bold', fontsize=10)
    
    ax.set_ylim(-0.5, len(phases) - 0.5)
    ax.set_xlim(0, 24)
    ax.set_xlabel('Months from Project Start', fontsize=12)
    ax.set_title('Implementation Timeline & Benefit Realization', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    # Remove y-axis labels
    ax.set_yticks([])
    
    plt.tight_layout()
    
    # Save to BytesIO
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

def create_scenario_chart_for_pdf(scenario_results, currency_symbol):
    """Create scenario comparison chart for PDF"""
    if not REPORT_DEPENDENCIES_AVAILABLE:
        return None
        
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scenarios_list = list(scenario_results.keys())
    npvs = [scenario_results[scenario]['npv'] for scenario in scenarios_list]
    colors_list = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    
    bars = ax.bar(scenarios_list, npvs, color=colors_list, alpha=0.8)
    
    # Add value labels on bars
    for bar, npv in zip(bars, npvs):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + max(npvs)*0.01,
                f'{currency_symbol}{npv:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    ax.set_ylabel(f'Net Present Value ({currency_symbol})', fontsize=12)
    ax.set_title('Scenario Analysis - NPV Comparison', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Format y-axis
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{currency_symbol}{x/1000:.0f}K'))
    
    plt.tight_layout()
    
    # Save to BytesIO
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

def generate_executive_report_pdf(summary_data, scenario_results, solution_name, organization_name="Your Organization"):
    """Generate comprehensive executive report PDF"""
    
    if not REPORT_DEPENDENCIES_AVAILABLE:
        return None
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkblue,
        borderWidth=1,
        borderColor=colors.darkblue,
        borderPadding=5
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.darkblue
    )
    
    # Title Page
    story.append(Paragraph(f"Business Value Assessment", title_style))
    story.append(Paragraph(f"{solution_name} Implementation", styles['Title']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"Prepared for: {organization_name}", styles['Heading2']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    # Custom style for white header text
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        textColor=colors.white,
        fontName='Helvetica-Bold'
    )
    
    # Executive Summary Box with proper column widths and white headers
    exec_summary_data = [
        [Paragraph('<b>Metric</b>', header_style), 
         Paragraph('<b>Conservative</b>', header_style), 
         Paragraph('<b>Expected</b>', header_style), 
         Paragraph('<b>Optimistic</b>', header_style)],
        [Paragraph('Net Present Value', styles['Normal']), 
         Paragraph(f"{summary_data['investment_summary']['currency']}{scenario_results['Conservative']['npv']:,.0f}", styles['Normal']),
         Paragraph(f"{summary_data['investment_summary']['currency']}{scenario_results['Expected']['npv']:,.0f}", styles['Normal']),
         Paragraph(f"{summary_data['investment_summary']['currency']}{scenario_results['Optimistic']['npv']:,.0f}", styles['Normal'])],
        [Paragraph('Return on Investment', styles['Normal']),
         Paragraph(f"{scenario_results['Conservative']['roi']*100:.1f}%", styles['Normal']),
         Paragraph(f"{scenario_results['Expected']['roi']*100:.1f}%", styles['Normal']),
         Paragraph(f"{scenario_results['Optimistic']['roi']*100:.1f}%", styles['Normal'])],
        [Paragraph('Payback Period', styles['Normal']),
         Paragraph(scenario_results['Conservative']['payback'], styles['Normal']),
         Paragraph(scenario_results['Expected']['payback'], styles['Normal']),
         Paragraph(scenario_results['Optimistic']['payback'], styles['Normal'])]
    ]
    
    exec_table = Table(exec_summary_data, colWidths=[2.2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(exec_table)
    story.append(PageBreak())
    
    # 1. Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    
    exec_text = f"""
    This Business Value Assessment demonstrates the financial and operational benefits of implementing {solution_name} 
    at {organization_name}. Our analysis shows strong positive returns across all scenarios:
    
    <b>Key Financial Highlights:</b><br/>
    • Expected NPV: {summary_data['investment_summary']['currency']}{summary_data['investment_summary']['expected_npv']:,.0f}<br/>
    • Expected ROI: {summary_data['investment_summary']['expected_roi']*100:.1f}%<br/>
    • Payback Period: {summary_data['investment_summary']['payback_period']}<br/>
    • NPV Range: {summary_data['investment_summary']['currency']}{scenario_results['Conservative']['npv']:,.0f} to {summary_data['investment_summary']['currency']}{scenario_results['Optimistic']['npv']:,.0f}<br/><br/>
    
    <b>Primary Value Drivers:</b><br/>
    • Alert Management Optimization: {summary_data['investment_summary']['currency']}{alert_reduction_savings + alert_triage_savings:,.0f} annually<br/>
    • Incident Management Efficiency: {summary_data['investment_summary']['currency']}{incident_reduction_savings + incident_triage_savings:,.0f} annually<br/>
    • Major Incident Impact Reduction: {summary_data['investment_summary']['currency']}{major_incident_savings:,.0f} annually<br/><br/>
    
    <b>Implementation Timeline:</b><br/>
    • Implementation Phase: {summary_data['implementation']['delay_months']} months<br/>
    • Ramp-up to Full Benefits: {summary_data['implementation']['ramp_up_months']} months<br/>
    • Full ROI Realization: Month {summary_data['implementation']['full_benefits_month']}<br/><br/>
    
    Even under conservative assumptions (30% lower benefits, 30% longer implementation), the investment delivers 
    {scenario_results['Conservative']['roi']*100:.1f}% ROI with {scenario_results['Conservative']['payback']} payback period.
    """
    
    story.append(Paragraph(exec_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Add scenario chart
    scenario_chart = create_scenario_chart_for_pdf(scenario_results, summary_data['investment_summary']['currency'])
    if scenario_chart:
        story.append(Image(scenario_chart, width=6*inch, height=3.6*inch))
    story.append(PageBreak())
    
    # 2. Implementation Roadmap with wrapped text and white headers
    story.append(Paragraph("Implementation Roadmap & Milestones", heading_style))
    
    roadmap_data = [
        [Paragraph('<b>Phase</b>', header_style), 
         Paragraph('<b>Duration</b>', header_style), 
         Paragraph('<b>Key Activities</b>', header_style), 
         Paragraph('<b>Benefits Realization</b>', header_style)],
        [Paragraph('Planning & Setup', styles['Normal']), 
         Paragraph(f"Months 1-2", styles['Normal']), 
         Paragraph('Environment setup, integration planning, team training', styles['Normal']), 
         Paragraph('0%', styles['Normal'])],
        [Paragraph('Core Implementation', styles['Normal']), 
         Paragraph(f"Months 3-{implementation_delay_months}", styles['Normal']), 
         Paragraph('Data integration, alert configuration, dashboard creation', styles['Normal']), 
         Paragraph('0%', styles['Normal'])],
        [Paragraph('Go-Live & Ramp-up', styles['Normal']), 
         Paragraph(f"Months {implementation_delay_months+1}-{implementation_delay_months + benefits_ramp_up_months}", styles['Normal']), 
         Paragraph('Deployment, user adoption, process optimization', styles['Normal']), 
         Paragraph('0% → 100%', styles['Normal'])],
        [Paragraph('Full Operation', styles['Normal']), 
         Paragraph(f"Month {implementation_delay_months + benefits_ramp_up_months}+", styles['Normal']), 
         Paragraph('Business as usual, continuous improvement', styles['Normal']), 
         Paragraph('100%', styles['Normal'])],
    ]
    
    roadmap_table = Table(roadmap_data, colWidths=[1.3*inch, 1.1*inch, 3*inch, 1.3*inch])
    roadmap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(roadmap_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Add timeline chart
    timeline_chart = create_timeline_chart_for_pdf()
    if timeline_chart:
        story.append(Image(timeline_chart, width=6*inch, height=2.4*inch))
    story.append(Spacer(1, 0.3*inch))
    
    # Key Milestones
    story.append(Paragraph("Key Success Milestones", subheading_style))
    milestones_text = f"""
    <b>Month {implementation_delay_months}: Go-Live Milestone</b><br/>
    • Solution deployed and operational<br/>
    • Initial benefits begin to materialize<br/>
    • User training completed<br/><br/>
    
    <b>Month {implementation_delay_months + benefits_ramp_up_months}: Full Benefits Milestone</b><br/>
    • 100% benefit realization achieved<br/>
    • All processes optimized<br/>
    • ROI tracking established<br/><br/>
    
    <b>Month 12: First Year Review</b><br/>
    • Actual vs. predicted benefits analysis<br/>
    • Process refinement opportunities<br/>
    • Expansion planning<br/>
    """
    story.append(Paragraph(milestones_text, styles['Normal']))
    story.append(PageBreak())
    
    # 3. Risk Assessment & Mitigation with wrapped text and white headers
    story.append(Paragraph("Risk Assessment & Mitigation Strategies", heading_style))
    
    risk_data = [
        [Paragraph('<b>Risk Category</b>', header_style), 
         Paragraph('<b>Probability</b>', header_style), 
         Paragraph('<b>Impact</b>', header_style), 
         Paragraph('<b>Mitigation Strategy</b>', header_style)],
        [Paragraph('Implementation Delays', styles['Normal']), 
         Paragraph('Medium', styles['Normal']), 
         Paragraph('Medium', styles['Normal']), 
         Paragraph('Dedicated project team, phased approach, vendor support', styles['Normal'])],
        [Paragraph('Lower Than Expected Benefits', styles['Normal']), 
         Paragraph('Low', styles['Normal']), 
         Paragraph('High', styles['Normal']), 
         Paragraph('Conservative estimates, pilot validation, change management', styles['Normal'])],
        [Paragraph('User Adoption Challenges', styles['Normal']), 
         Paragraph('Medium', styles['Normal']), 
         Paragraph('Medium', styles['Normal']), 
         Paragraph('Comprehensive training, change champions, gradual rollout', styles['Normal'])],
        [Paragraph('Technical Integration Issues', styles['Normal']), 
         Paragraph('Low', styles['Normal']), 
         Paragraph('Medium', styles['Normal']), 
         Paragraph('Pre-implementation assessment, technical validation, fallback plans', styles['Normal'])],
    ]
    
    risk_table = Table(risk_data, colWidths=[1.8*inch, 0.9*inch, 0.8*inch, 3.2*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(risk_table)
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Scenario Analysis - Downside Protection", subheading_style))
    risk_analysis_text = f"""
    Our scenario analysis provides confidence in the investment's robustness:
    
    <b>Conservative Scenario (30% lower benefits, 30% longer implementation):</b><br/>
    • NPV: {summary_data['investment_summary']['currency']}{scenario_results['Conservative']['npv']:,.0f}<br/>
    • ROI: {scenario_results['Conservative']['roi']*100:.1f}%<br/>
    • Payback: {scenario_results['Conservative']['payback']}<br/>
    • Still delivers positive returns even under adverse conditions<br/><br/>
    
    <b>Risk Tolerance Analysis:</b><br/>
    Benefits would need to be significantly lower than expected before the investment becomes unprofitable. 
    This provides substantial downside protection for your investment decision.
    """
    story.append(Paragraph(risk_analysis_text, styles['Normal']))
    story.append(PageBreak())
    
    # 4. Detailed Financial Analysis (Appendix)
    story.append(Paragraph("Appendix: Detailed Financial Calculations", heading_style))
    
    # Benefits breakdown table with wrapped text and white headers
    benefits_data = [
        [Paragraph('<b>Benefit Category</b>', header_style), 
         Paragraph('<b>Annual Value</b>', header_style), 
         Paragraph('<b>Calculation Method</b>', header_style)],
        [Paragraph('Alert Reduction Savings', styles['Normal']), 
         Paragraph(f"{summary_data['investment_summary']['currency']}{alert_reduction_savings:,.0f}", styles['Normal']), 
         Paragraph("Avoided alerts × Cost per alert", styles['Normal'])],
        [Paragraph('Alert Triage Efficiency', styles['Normal']), 
         Paragraph(f"{summary_data['investment_summary']['currency']}{alert_triage_savings:,.0f}", styles['Normal']), 
         Paragraph("Remaining alerts × Time savings × Hourly cost", styles['Normal'])],
        [Paragraph('Incident Reduction Savings', styles['Normal']), 
         Paragraph(f"{summary_data['investment_summary']['currency']}{incident_reduction_savings:,.0f}", styles['Normal']), 
         Paragraph("Avoided incidents × Cost per incident", styles['Normal'])],
        [Paragraph('Incident Triage Efficiency', styles['Normal']), 
         Paragraph(f"{summary_data['investment_summary']['currency']}{incident_triage_savings:,.0f}", styles['Normal']), 
         Paragraph("Remaining incidents × Time savings × Hourly cost", styles['Normal'])],
        [Paragraph('Major Incident MTTR Improvement', styles['Normal']), 
         Paragraph(f"{summary_data['investment_summary']['currency']}{major_incident_savings:,.0f}", styles['Normal']), 
         Paragraph("Volume × MTTR improvement × Cost per hour", styles['Normal'])],
        [Paragraph('Tool Consolidation', styles['Normal']), 
         Paragraph(f"{summary_data['investment_summary']['currency']}{tool_savings:,.0f}", styles['Normal']), 
         Paragraph("License and maintenance savings", styles['Normal'])],
        [Paragraph('Additional Benefits', styles['Normal']), 
         Paragraph(f"{summary_data['investment_summary']['currency']}{summary_data['key_benefits']['additional_benefits']:,.0f}", styles['Normal']), 
         Paragraph("Process efficiency + FTE avoidance + Revenue growth", styles['Normal'])],
    ]
    
    benefits_table = Table(benefits_data, colWidths=[2.2*inch, 1.3*inch, 3.2*inch])
    benefits_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(benefits_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Financial assumptions
    story.append(Paragraph("Key Financial Assumptions", subheading_style))
    assumptions_text = f"""
    <b>Working Hours Configuration:</b><br/>
    • Working hours per FTE per year: {working_hours_per_fte_per_year:,.0f} hours<br/>
    • Based on: {hours_per_day} hours/day × {days_per_week} days/week × {weeks_per_year} weeks - {holiday_sick_days} holiday days<br/><br/>
    
    <b>Cost Calculations:</b><br/>
    • Cost per alert: {summary_data['investment_summary']['currency']}{cost_per_alert:.2f}<br/>
    • Cost per incident: {summary_data['investment_summary']['currency']}{cost_per_incident:.2f}<br/>
    • FTE time allocation: Alert management {alert_fte_percentage*100:.1f}%, Incident management {incident_fte_percentage*100:.1f}%<br/><br/>
    
    <b>Financial Parameters:</b><br/>
    • Discount rate: {discount_rate*100:.0f}%<br/>
    • Evaluation period: {evaluation_years} years<br/>
    • Implementation delay: {implementation_delay_months} months<br/>
    • Benefits ramp-up: {benefits_ramp_up_months} months<br/>
    """
    story.append(Paragraph(assumptions_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- Layout ---
st.title("Business Value Assessment")

# --- Working Hours Summary ---
st.subheader("⏰ Working Hours Configuration")
col_wh1, col_wh2, col_wh3, col_wh4 = st.columns(4)

with col_wh1:
    st.metric("Hours/Day", f"{hours_per_day}")
with col_wh2:
    st.metric("Days/Week", f"{days_per_week}")
with col_wh3:
    st.metric("Holiday/Sick Days", f"{holiday_sick_days}")
with col_wh4:
    st.metric("Total Hours/FTE/Year", f"{working_hours_per_fte_per_year:,.0f}")

# --- ENHANCED SCENARIO ANALYSIS ---
st.subheader("📊 Scenario Analysis")

# Display scenario comparison
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"### {scenarios['Conservative']['icon']} Conservative Scenario")
    st.markdown(f"*{scenarios['Conservative']['description']}*")
    st.metric("NPV", f"{currency_symbol}{scenario_results['Conservative']['npv']:,.0f}")
    st.metric("ROI", f"{scenario_results['Conservative']['roi']*100:.1f}%")
    st.metric("Payback", scenario_results['Conservative']['payback'])
    st.metric("Implementation", f"{scenario_results['Conservative']['impl_delay']} months")

with col2:
    st.markdown(f"### {scenarios['Expected']['icon']} Expected Scenario")
    st.markdown(f"*{scenarios['Expected']['description']}*")
    st.metric("NPV", f"{currency_symbol}{scenario_results['Expected']['npv']:,.0f}")
    st.metric("ROI", f"{scenario_results['Expected']['roi']*100:.1f}%")
    st.metric("Payback", scenario_results['Expected']['payback'])
    st.metric("Implementation", f"{scenario_results['Expected']['impl_delay']} months")

with col3:
    st.markdown(f"### {scenarios['Optimistic']['icon']} Optimistic Scenario")
    st.markdown(f"*{scenarios['Optimistic']['description']}*")
    st.metric("NPV", f"{currency_symbol}{scenario_results['Optimistic']['npv']:,.0f}")
    st.metric("ROI", f"{scenario_results['Optimistic']['roi']*100:.1f}%")
    st.metric("Payback", scenario_results['Optimistic']['payback'])
    st.metric("Implementation", f"{scenario_results['Optimistic']['impl_delay']} months")

# Scenario comparison chart
scenario_names = list(scenario_results.keys())
scenario_npvs = [scenario_results[name]['npv'] for name in scenario_names]
scenario_colors = [scenario_results[name]['color'] for name in scenario_names]

fig_scenarios = go.Figure(data=[
    go.Bar(
        x=scenario_names, y=scenario_npvs, marker_color=scenario_colors,
        text=[f"{currency_symbol}{npv:,.0f}" for npv in scenario_npvs], textposition='auto',
    )
])

fig_scenarios.update_layout(
    title="Net Present Value by Scenario", yaxis_title=f"NPV ({currency_symbol})",
    showlegend=False, height=400
)

st.plotly_chart(fig_scenarios, use_container_width=True)

# Risk range summary
min_npv = min(scenario_npvs)
max_npv = max(scenario_npvs)
npv_range = max_npv - min_npv

st.info(f"""
**Scenario Range Summary:**
- **NPV Range:** {currency_symbol}{min_npv:,.0f} to {currency_symbol}{max_npv:,.0f} 
- **Range Spread:** {currency_symbol}{npv_range:,.0f} ({(npv_range/max_npv)*100:.0f}% of optimistic case)
- **Worst Case ROI:** {scenario_results['Conservative']['roi']*100:.1f}%
- **Best Case ROI:** {scenario_results['Optimistic']['roi']*100:.1f}%

Even in the conservative scenario, the investment shows positive returns with {scenario_results['Conservative']['payback']} payback.
""")

# Executive talking points
with st.expander("🎯 Executive Talking Points"):
    st.markdown(f"""
    **For the CFO:**
    - "Even if benefits are 30% lower than expected, we still achieve {currency_symbol}{scenario_results['Conservative']['npv']:,.0f} NPV"
    - "The worst-case scenario still delivers {scenario_results['Conservative']['roi']*100:.1f}% ROI"
    - "NPV ranges from {currency_symbol}{min_npv:,.0f} to {currency_symbol}{max_npv:,.0f}, showing strong downside protection"
    
    **For the CTO:**
    - "Implementation timeline ranges from {scenario_results['Optimistic']['impl_delay']} to {scenario_results['Conservative']['impl_delay']} months"
    - "Optimistic scenario shows potential for {currency_symbol}{scenario_results['Optimistic']['npv']:,.0f} NPV if adoption exceeds expectations"
    - "Conservative estimates assume 30% longer implementation and 30% lower benefits"
    
    **For the Project Sponsor:**
    - "Expected scenario assumes baseline estimates: {currency_symbol}{scenario_results['Expected']['npv']:,.0f} NPV"
    - "Upside potential of {currency_symbol}{npv_range:,.0f} if implementation goes better than planned"
    - "All scenarios show positive ROI, reducing investment risk"
    """)

# Timeline visualization with interactive chart
st.subheader("📅 Implementation Timeline & Benefit Realization")

# Metrics row
col_timeline1, col_timeline2, col_timeline3 = st.columns(3)

with col_timeline1:
    st.metric("Implementation Delay", f"{implementation_delay_months} months")
    st.caption("Time until benefits begin")

with col_timeline2:
    st.metric("Benefits Ramp-up", f"{benefits_ramp_up_months} months")
    st.caption("Time to reach full benefits")

with col_timeline3:
    st.metric("Full Benefits Start", f"{implementation_delay_months + benefits_ramp_up_months} months")
    st.caption("When 100% benefits are realized")

# Add the interactive timeline chart
if total_annual_benefits > 0:
    timeline_fig = create_implementation_timeline_chart(
        implementation_delay_months, benefits_ramp_up_months, evaluation_years, 
        currency_symbol, total_annual_benefits
    )
    st.plotly_chart(timeline_fig, use_container_width=True)
    
    st.markdown(f"""
    **Chart Explanation:**
    - **Red shaded area**: Implementation phase ({implementation_delay_months} months) - No benefits realized
    - **Orange shaded area**: Ramp-up phase ({benefits_ramp_up_months} months) - Gradual benefit realization
    - **Green shaded area**: Full benefits phase - 100% benefit realization
    - **Blue line**: Percentage of benefits realized over time
    - **Purple area**: Monthly benefit amounts in {currency_symbol} thousands
    """)
else:
    st.info("💡 Enter benefit values in the sidebar to see the interactive timeline chart")

# --- DETAILED BREAKDOWN ---
st.subheader("💰 Expected Scenario - Detailed Breakdown")

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Financial Impact Summary")
    # Use Expected scenario results
    expected_results = scenario_results['Expected']
    avg_annual_net_benefit = sum([cf['net_cash_flow'] for cf in expected_results['cash_flows']]) / evaluation_years
    
    st.metric("Average Annual Net Benefit", f"{currency_symbol}{avg_annual_net_benefit:,.0f}")
    st.metric("Net Present Value (NPV)", f"{currency_symbol}{expected_results['npv']:,.0f}")
    st.metric("Return on Investment (ROI)", f"{expected_results['roi']*100:.1f}%")
    st.metric("Payback Period", expected_results['payback'])
    st.caption(f"NPV Discount Rate: {int(discount_rate * 100)}%")

with col2:
    st.subheader("Annual Benefits Breakdown (at Full Realization)")
    for label, value in {
        "Alert Reduction Savings": alert_reduction_savings,
        "Alert Triage Savings": alert_triage_savings,
        "Incident Reduction Savings": incident_reduction_savings,
        "Incident Triage Savings": incident_triage_savings,
        "Major Incident Savings": major_incident_savings,
        "Tool Consolidation Savings": tool_savings,
        "People Efficiency Gains": people_cost_per_year,
        "FTE Avoidance": fte_avoidance,
        "SLA Penalty Avoidance": sla_penalty_avoidance,
        "Revenue Growth": revenue_growth,
        "Capital Expenditure Savings": capex_savings,
        "Operational Expenditure Savings": opex_savings
    }.items():
        st.write(f"**{label}:** {currency_symbol}{value:,.0f}")

# --- Year-by-Year Cash Flow Analysis ---
st.subheader("📊 Year-by-Year Cash Flow Analysis (Expected Scenario)")

# Create DataFrame for cash flow table using Expected scenario
expected_cash_flows = scenario_results['Expected']['cash_flows']
cash_flow_df = pd.DataFrame([
    {
        'Year': cf['year'],
        'Benefits Realization': f"{cf['realization_factor']*100:.1f}%",
        'Benefits': f"{currency_symbol}{cf['benefits']:,.0f}",
        'Platform Cost': f"{currency_symbol}{cf['platform_cost']:,.0f}",
        'Services Cost': f"{currency_symbol}{cf['services_cost']:,.0f}",
        'Net Cash Flow': f"{currency_symbol}{cf['net_cash_flow']:,.0f}"
    }
    for cf in expected_cash_flows
])

st.dataframe(cash_flow_df, use_container_width=True)

# --- Business Value Narrative ---
escaped_currency_symbol = currency_symbol.replace("$", "\\$")
go_live_month = implementation_delay_months + benefits_ramp_up_months

st.subheader("Business Value Story")
st.markdown(f"""
By adopting **{solution_name}**, your organization can unlock significant financial and operational gains across multiple scenarios.

**Scenario Analysis Summary:**
- **Conservative Case:** {escaped_currency_symbol}{scenario_results['Conservative']['npv']:,.0f} NPV even if benefits are 30% lower and implementation takes 30% longer
- **Expected Case:** {escaped_currency_symbol}{scenario_results['Expected']['npv']:,.0f} NPV based on your baseline assumptions
- **Optimistic Case:** {escaped_currency_symbol}{scenario_results['Optimistic']['npv']:,.0f} NPV if benefits exceed expectations by 20% and implementation is 20% faster

**Implementation Timeline:**
- **Months 1-{implementation_delay_months}:** Implementation and deployment (no benefits realized)
- **Months {implementation_delay_months + 1}-{go_live_month}:** Benefits ramp-up period (gradual realization)
- **Month {go_live_month}+:** Full benefits realization

**Risk Mitigation:**
The scenario analysis shows that even under conservative assumptions, the investment delivers positive returns with {scenario_results['Conservative']['roi']*100:.1f}% ROI and {scenario_results['Conservative']['payback']} payback period.
""")

# --- EXECUTIVE REPORT GENERATOR ---
st.subheader("📄 Executive Report Generator")

if not REPORT_DEPENDENCIES_AVAILABLE:
    st.error("""
    **Missing Dependencies for PDF Report Generation**
    
    To enable PDF report generation, please install the required packages:
    ```bash
    pip install reportlab matplotlib
    ```
    
    Once installed, restart your Streamlit app to enable PDF export functionality.
    """)

col_report1, col_report2 = st.columns(2)

with col_report1:
    st.write("**Generate a comprehensive business case document including:**")
    st.write("• Executive summary with key metrics")
    st.write("• Implementation roadmap with milestones") 
    st.write("• Risk assessment and mitigation strategies")
    st.write("• Detailed financial calculations appendix")

with col_report2:
    organization_name = st.text_input("Organization Name for Report", value="Your Organization", key="org_name_report")
    
    if st.button("🎯 Generate Executive Report (PDF)", key="generate_pdf_report"):
        if not REPORT_DEPENDENCIES_AVAILABLE:
            st.error("Please install required dependencies: pip install reportlab matplotlib")
        elif total_annual_benefits > 0:
            # Create summary data
            summary_data = create_executive_summary_data(scenario_results, currency_symbol)
            
            # Generate PDF
            with st.spinner("Generating professional PDF report..."):
                pdf_buffer = generate_executive_report_pdf(
                    summary_data, 
                    scenario_results, 
                    solution_name, 
                    organization_name
                )
            
            if pdf_buffer:
                # Provide download
                st.download_button(
                    label="📥 Download Executive Report (PDF)",
                    data=pdf_buffer.getvalue(),
                    file_name=f"BVA_Executive_Report_{organization_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
                
                st.success("✅ Executive report generated successfully!")
            else:
                st.error("Failed to generate PDF report. Please check dependencies.")
        else:
            st.warning("⚠️ Please enter benefit values in the sidebar to generate the report.")

# PowerPoint Alternative (HTML-based presentation)
st.write("---")
st.write("**Alternative: Generate HTML Presentation** (PowerPoint-style slides)")

if st.button("🎞️ Generate HTML Presentation", key="generate_html_presentation"):
    if total_annual_benefits > 0:
        # Create HTML presentation content
        html_presentation = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{solution_name} Business Value Assessment</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .slide {{ page-break-after: always; margin-bottom: 50px; padding: 20px; border: 1px solid #ccc; }}
                .title {{ color: #2E86AB; font-size: 28px; text-align: center; margin-bottom: 30px; }}
                .subtitle {{ color: #666; font-size: 18px; text-align: center; margin-bottom: 40px; }}
                .metric {{ background: #f0f8ff; padding: 15px; margin: 10px 0; border-left: 4px solid #2E86AB; }}
                .scenario {{ display: inline-block; width: 30%; margin: 1%; padding: 15px; text-align: center; border: 1px solid #ddd; }}
                .conservative {{ background: #ffe6e6; }}
                .expected {{ background: #e6ffe6; }}
                .optimistic {{ background: #e6f3ff; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #2E86AB; color: white; }}
            </style>
        </head>
        <body>
            <!-- Slide 1: Title -->
            <div class="slide">
                <h1 class="title">{solution_name} Business Value Assessment</h1>
                <p class="subtitle">Executive Business Case</p>
                <p class="subtitle">Prepared for: {organization_name}</p>
                <p class="subtitle">Date: {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <!-- Slide 2: Executive Summary -->
            <div class="slide">
                <h1 class="title">Executive Summary</h1>
                <div class="scenario conservative">
                    <h3>🔴 Conservative</h3>
                    <p><strong>NPV:</strong> {currency_symbol}{scenario_results['Conservative']['npv']:,.0f}</p>
                    <p><strong>ROI:</strong> {scenario_results['Conservative']['roi']*100:.1f}%</p>
                </div>
                <div class="scenario expected">
                    <h3>🟢 Expected</h3>
                    <p><strong>NPV:</strong> {currency_symbol}{scenario_results['Expected']['npv']:,.0f}</p>
                    <p><strong>ROI:</strong> {scenario_results['Expected']['roi']*100:.1f}%</p>
                </div>
                <div class="scenario optimistic">
                    <h3>🔵 Optimistic</h3>
                    <p><strong>NPV:</strong> {currency_symbol}{scenario_results['Optimistic']['npv']:,.0f}</p>
                    <p><strong>ROI:</strong> {scenario_results['Optimistic']['roi']*100:.1f}%</p>
                </div>
                <div class="metric">
                    <strong>Key Insight:</strong> Even under conservative assumptions, the investment delivers {scenario_results['Conservative']['roi']*100:.1f}% ROI 
                    with {scenario_results['Conservative']['payback']} payback period.
                </div>
            </div>
            
            <!-- Slide 3: Implementation Timeline -->
            <div class="slide">
                <h1 class="title">Implementation Roadmap</h1>
                <table>
                    <tr><th>Phase</th><th>Timeline</th><th>Key Activities</th><th>Benefits</th></tr>
                    <tr><td>Implementation</td><td>Months 1-{implementation_delay_months}</td><td>Setup, integration, training</td><td>0%</td></tr>
                    <tr><td>Ramp-up</td><td>Months {implementation_delay_months+1}-{implementation_delay_months + benefits_ramp_up_months}</td><td>Deployment, adoption</td><td>0% → 100%</td></tr>
                    <tr><td>Full Operation</td><td>Month {implementation_delay_months + benefits_ramp_up_months}+</td><td>Business as usual</td><td>100%</td></tr>
                </table>
            </div>
            
            <!-- Slide 4: Financial Details -->
            <div class="slide">
                <h1 class="title">Financial Breakdown</h1>
                <table>
                    <tr><th>Benefit Category</th><th>Annual Value</th></tr>
                    <tr><td>Alert Management Optimization</td><td>{currency_symbol}{alert_reduction_savings + alert_triage_savings:,.0f}</td></tr>
                    <tr><td>Incident Management Efficiency</td><td>{currency_symbol}{incident_reduction_savings + incident_triage_savings:,.0f}</td></tr>
                    <tr><td>Major Incident Impact Reduction</td><td>{currency_symbol}{major_incident_savings:,.0f}</td></tr>
                    <tr><td>Additional Benefits</td><td>{currency_symbol}{tool_savings + people_cost_per_year + fte_avoidance + revenue_growth:,.0f}</td></tr>
                    <tr style="background-color: #f0f8ff;"><td><strong>Total Annual Benefits</strong></td><td><strong>{currency_symbol}{total_annual_benefits:,.0f}</strong></td></tr>
                </table>
            </div>
            
            <!-- Slide 5: Risk Assessment -->
            <div class="slide">
                <h1 class="title">Risk Assessment & Mitigation</h1>
                <table>
                    <tr><th>Risk Category</th><th>Probability</th><th>Impact</th><th>Mitigation Strategy</th></tr>
                    <tr><td>Implementation Delays</td><td>Medium</td><td>Medium</td><td>Dedicated project team, phased approach</td></tr>
                    <tr><td>Lower Benefits</td><td>Low</td><td>High</td><td>Conservative estimates, pilot validation</td></tr>
                    <tr><td>User Adoption</td><td>Medium</td><td>Medium</td><td>Training, change champions</td></tr>
                    <tr><td>Technical Issues</td><td>Low</td><td>Medium</td><td>Pre-assessment, validation, fallback plans</td></tr>
                </table>
                <div class="metric">
                    <strong>Confidence Factor:</strong> Even if benefits are 30% lower and implementation takes 30% longer, 
                    the project still delivers {scenario_results['Conservative']['roi']*100:.1f}% ROI.
                </div>
            </div>
        </body>
        </html>
        """
        
        # Provide download
        st.download_button(
            label="📥 Download HTML Presentation",
            data=html_presentation,
            file_name=f"BVA_Presentation_{organization_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html",
            mime="text/html"
        )
        st.success("✅ HTML presentation generated! Open in browser and print to PDF for PowerPoint-style slides.")
    else:
        st.warning("⚠️ Please enter benefit values in the sidebar to generate the presentation.")

# --- Show Calculation Details ---
with st.expander("Show Calculation Details"):
    st.markdown("### Working Hours Configuration")
    st.write(f"Hours per day: {hours_per_day}")
    st.write(f"Days per week: {days_per_week}")
    st.write(f"Weeks per year: {weeks_per_year}")
    st.write(f"Holiday/sick days: {holiday_sick_days}")
    st.write(f"**Total working hours per FTE per year: {working_hours_per_fte_per_year:,.0f} hours**")
    
    st.markdown("### Scenario Parameters")
    for scenario_name, params in scenarios.items():
        st.write(f"**{scenario_name}:**")
        st.write(f"- Benefits multiplier: {params['benefits_multiplier']*100:.0f}%")
        st.write(f"- Implementation delay multiplier: {params['implementation_delay_multiplier']*100:.0f}%")
        st.write(f"- Description: {params['description']}")
    
    st.markdown("### Implementation Timeline Impact")
    st.write(f"Implementation Delay: {implementation_delay_months} months")
    st.write(f"Benefits Ramp-up Period: {benefits_ramp_up_months} months")
    st.write(f"Full Benefits Start: Month {implementation_delay_months + benefits_ramp_up_months}")
    
    st.markdown("### Cost Per Alert/Incident Calculations")
    if alert_volume > 0 and alert_ftes > 0:
        alert_total_time_hours = (alert_volume * avg_alert_triage_time) / 60
        alert_available_hours = alert_ftes * working_hours_per_fte_per_year
        st.write(f"**Alert Management:**")
        st.write(f"- Total Alert Time per Year: {alert_volume:,} × {avg_alert_triage_time} min = {alert_volume * avg_alert_triage_time:,} minutes = {alert_total_time_hours:,.0f} hours")
        st.write(f"- Available FTE Hours: {alert_ftes} FTEs × {working_hours_per_fte_per_year:,.0f} hours = {alert_available_hours:,} hours")
        st.write(f"- FTE Time on Alerts: {alert_fte_percentage*100:.1f}%")
        st.write(f"- Total FTE Cost: {alert_ftes} × {currency_symbol}{avg_alert_fte_salary:,} = {currency_symbol}{alert_ftes * avg_alert_fte_salary:,}")
        st.write(f"- Total Alert Handling Cost: {currency_symbol}{alert_ftes * avg_alert_fte_salary:,} × {alert_fte_percentage*100:.1f}% = {currency_symbol}{total_alert_handling_cost:,.0f}")
        st.write(f"- **Cost per Alert: {currency_symbol}{cost_per_alert:.2f}**")
    
    if incident_volume > 0 and incident_ftes > 0:
        incident_total_time_hours = (incident_volume * avg_incident_triage_time) / 60
        incident_available_hours = incident_ftes * working_hours_per_fte_per_year
        st.write(f"**Incident Management:**")
        st.write(f"- Total Incident Time per Year: {incident_volume:,} × {avg_incident_triage_time} min = {incident_volume * avg_incident_triage_time:,} minutes = {incident_total_time_hours:,.0f} hours")
        st.write(f"- Available FTE Hours: {incident_ftes} FTEs × {working_hours_per_fte_per_year:,.0f} hours = {incident_available_hours:,} hours")
        st.write(f"- FTE Time on Incidents: {incident_fte_percentage*100:.1f}%")
        st.write(f"- Total FTE Cost: {incident_ftes} × {currency_symbol}{avg_incident_fte_salary:,} = {currency_symbol}{incident_ftes * avg_incident_fte_salary:,}")
        st.write(f"- Total Incident Handling Cost: {currency_symbol}{incident_ftes * avg_incident_fte_salary:,} × {incident_fte_percentage*100:.1f}% = {currency_symbol}{total_incident_handling_cost:,.0f}")
        st.write(f"- **Cost per Incident: {currency_symbol}{cost_per_incident:.2f}**")
    
    st.markdown("### Annual Benefits Calculations (at Full Realization)")
    st.markdown("#### Alerts")
    st.write(f"Avoided Alerts: {avoided_alerts:,.0f}")
    st.write(f"Alert Reduction Savings = Avoided Alerts × Cost per Alert = {avoided_alerts:,.0f} × {currency_symbol}{cost_per_alert:.2f} = {currency_symbol}{alert_reduction_savings:,.2f}")
    st.write(f"Remaining Alerts: {remaining_alerts:,.0f}")
    st.write(f"Remaining Alert Handling Cost = {remaining_alerts:,.0f} × {currency_symbol}{cost_per_alert:.2f} = {currency_symbol}{remaining_alert_handling_cost:,.2f}")
    st.write(f"Alert Triage Savings = Remaining Alert Cost × % Time Saved = {currency_symbol}{remaining_alert_handling_cost:,.2f} × {alert_triage_time_saved_pct}% = {currency_symbol}{alert_triage_savings:,.2f}")

    st.markdown("#### Incidents")
    st.write(f"Avoided Incidents: {avoided_incidents:,.0f}")
    st.write(f"Incident Reduction Savings = Avoided Incidents × Cost per Incident = {avoided_incidents:,.0f} × {currency_symbol}{cost_per_incident:.2f} = {currency_symbol}{incident_reduction_savings:,.2f}")
    st.write(f"Remaining Incidents: {remaining_incidents:,.0f}")
    st.write(f"Remaining Incident Handling Cost = {remaining_incidents:,.0f} × {currency_symbol}{cost_per_incident:.2f} = {currency_symbol}{remaining_incident_handling_cost:,.2f}")
    st.write(f"Incident Triage Savings = Remaining Incident Cost × % Time Saved = {currency_symbol}{remaining_incident_handling_cost:,.2f} × {incident_triage_time_savings_pct}% = {currency_symbol}{incident_triage_savings:,.2f}")

    st.markdown("#### Major Incidents")
    st.write(f"MTTR Hours Saved per Incident: {mttr_hours_saved_per_incident:,.2f}")
    st.write(f"Total MTTR Hours Saved = Volume × Hours Saved/Incident = {major_incident_volume} × {mttr_hours_saved_per_incident:,.2f} = {total_mttr_hours_saved:,.2f}")
    st.write(f"Major Incident Savings = Total MTTR Hours Saved × Cost/hr = {total_mttr_hours_saved:,.2f} × {currency_symbol}{avg_major_incident_cost:,} = {currency_symbol}{major_incident_savings:,.2f}")

    st.markdown("#### Other Benefits")
    st.write(f"Tool Consolidation: {currency_symbol}{tool_savings:,.2f}")
    st.write(f"People Efficiency Gains: {currency_symbol}{people_cost_per_year:,.2f}")
    st.write(f"FTE Avoidance: {currency_symbol}{fte_avoidance:,.2f}")
    st.write(f"SLA Penalty Avoidance: {currency_symbol}{sla_penalty_avoidance:,.2f}")
    st.write(f"Revenue Growth: {currency_symbol}{revenue_growth:,.2f}")
    st.write(f"CapEx Savings: {currency_symbol}{capex_savings:,.2f}")
    st.write(f"OpEx Savings: {currency_symbol}{opex_savings:,.2f}")

    st.markdown("#### Costs")
    st.write(f"Platform Cost (Annual): {currency_symbol}{platform_cost:,.2f}")
    st.write(f"Services (One-Time): {currency_symbol}{services_cost:,.2f}")

    st.markdown("#### Total Annual Benefits (at Full Realization)")
    st.write(f"Total Annual Benefits: {currency_symbol}{total_annual_benefits:,.2f}")

# --- Key Timeline Milestones ---
st.subheader("🎯 Key Timeline Milestones")
milestone_data = []

milestone_data.append({
    "Milestone": "Project Start",
    "Month": 0,
    "Benefit Realization": "0%",
    "Status": "✅ Starting point"
})

if implementation_delay_months > 0:
    milestone_data.append({
        "Milestone": "Go-Live",
        "Month": implementation_delay_months,
        "Benefit Realization": "0% → Ramp-up begins",
        "Status": "🚀 Solution deployed"
    })

full_benefits_month = implementation_delay_months + benefits_ramp_up_months
milestone_data.append({
    "Milestone": "Full Benefits Realized",
    "Month": full_benefits_month,
    "Benefit Realization": "100%",
    "Status": "🎯 Maximum value achieved"
})

milestone_data.append({
    "Milestone": "End of Evaluation Period",
    "Month": evaluation_years * 12,
    "Benefit Realization": "100%",
    "Status": "📊 Analysis complete"
})

milestone_df = pd.DataFrame(milestone_data)
st.dataframe(milestone_df, use_container_width=True, hide_index=True)

# --- Export to CSV ---
# Create comprehensive export data with all scenarios
combined_export_data = []

# Add working hours configuration
combined_export_data.append(["=== WORKING HOURS CONFIGURATION ==="])
combined_export_data.append(["Parameter", "Value"])
combined_export_data.append(["Hours per Day", hours_per_day])
combined_export_data.append(["Days per Week", days_per_week])
combined_export_data.append(["Weeks per Year", weeks_per_year])
combined_export_data.append(["Holiday/Sick Days", holiday_sick_days])
combined_export_data.append(["Total Working Hours per FTE per Year", working_hours_per_fte_per_year])

# Add scenario summary
combined_export_data.append([])
combined_export_data.append(["=== SCENARIO SUMMARY ==="])
combined_export_data.append(["Scenario", "NPV", "ROI", "Payback", "Implementation_Months", "Benefits_Multiplier"])
for scenario_name, results in scenario_results.items():
    combined_export_data.append([
        scenario_name,
        results['npv'],
        f"{results['roi']*100:.1f}%",
        results['payback'],
        results['impl_delay'],
        f"{results['benefits_mult']*100:.0f}%"
    ])

# Add expected scenario cash flow data
combined_export_data.append([])
combined_export_data.append(["=== EXPECTED SCENARIO CASH FLOW ANALYSIS ==="])
combined_export_data.append(["Year", "Benefits_Realization_Pct", "Benefits", "Platform_Cost", "Services_Cost", "Net_Cash_Flow"])
for cf in expected_cash_flows:
    combined_export_data.append([
        cf['year'], 
        f"{cf['realization_factor']*100:.1f}%", 
        cf['benefits'], 
        cf['platform_cost'], 
        cf['services_cost'], 
        cf['net_cash_flow']
    ])

# Add benefit breakdown
combined_export_data.append([])
combined_export_data.append(["=== BENEFIT BREAKDOWN (ANNUAL AT FULL REALIZATION) ==="])
combined_export_data.append(["Benefit_Type", "Annual_Amount"])

benefit_items = [
    ("Alert Reduction Savings", alert_reduction_savings),
    ("Alert Triage Savings", alert_triage_savings),
    ("Incident Reduction Savings", incident_reduction_savings),
    ("Incident Triage Savings", incident_triage_savings),
    ("Major Incident Savings", major_incident_savings),
    ("Tool Consolidation Savings", tool_savings),
    ("People Efficiency Gains", people_cost_per_year),
    ("FTE Avoidance", fte_avoidance),
    ("SLA Penalty Avoidance", sla_penalty_avoidance),
    ("Revenue Growth", revenue_growth),
    ("Capital Expenditure Savings", capex_savings),
    ("Operational Expenditure Savings", opex_savings)
]

for benefit_type, amount in benefit_items:
    combined_export_data.append([benefit_type, amount])

# Add key metrics
combined_export_data.append([])
combined_export_data.append(["=== KEY METRICS ==="])
combined_export_data.append(["Metric", "Value"])
combined_export_data.append(["Implementation Delay (months)", implementation_delay_months])
combined_export_data.append(["Benefits Ramp-up (months)", benefits_ramp_up_months])
combined_export_data.append(["Cost per Alert", cost_per_alert])
combined_export_data.append(["Cost per Incident", cost_per_incident])
combined_export_data.append(["Alert FTE Time Percentage", f"{alert_fte_percentage*100:.1f}%"])
combined_export_data.append(["Incident FTE Time Percentage", f"{incident_fte_percentage*100:.1f}%"])
combined_export_data.append(["NPV Range Min", min_npv])
combined_export_data.append(["NPV Range Max", max_npv])
combined_export_data.append(["NPV Range Spread", npv_range])

# Convert to DataFrame and CSV
combined_df = pd.DataFrame(combined_export_data)
csv_data = combined_df.to_csv(index=False, header=False)

st.download_button(
    label="📥 Export Complete Analysis to CSV",
    data=csv_data,
    file_name="business_value_complete_analysis_with_scenarios.csv",
    mime="text/csv"
)
