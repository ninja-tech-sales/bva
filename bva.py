# Developed by N.A.Pearson, HPE OpsRamp
# v1.2 - June 2025 - Added Implementation Delay Feature & Corrected Alert Cost Calculations

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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

nbv_model = st.sidebar.selectbox(
    "Net Business Value Model",
    [
        "Simple (NBV = NPV)",
        "Risk-Adjusted (user-defined buffer)",
        "Strategic (adds 5% intangible uplift)",
        "CapEx Realized Upfront"
    ],
    key="nbv_model"
)

risk_buffer_pct = 0.0
if nbv_model == "Risk-Adjusted (user-defined buffer)":
    risk_buffer_pct = st.sidebar.slider(
        "Risk Adjustment Buffer (%)", 
        0, 100, 10,
        key="risk_buffer"
    ) / 100

# --- CORRECTED CALCULATIONS ---

# Function to calculate alert costs based on FTE time allocation
def calculate_alert_costs(alert_volume, alert_ftes, avg_alert_triage_time, avg_salary_per_year):
    """
    Calculate the true cost per alert based on FTE time allocation
    """
    if alert_volume == 0 or alert_ftes == 0:
        return 0, 0, 0
    
    # Calculate total time spent on alerts per year (in hours)
    total_alert_time_minutes_per_year = alert_volume * avg_alert_triage_time
    total_alert_time_hours_per_year = total_alert_time_minutes_per_year / 60
    
    # Calculate available working hours per FTE per year
    # Assuming: 8 hours/day, 5 days/week, 52 weeks/year, minus 25 days holiday/sick
    working_days_per_year = (52 * 5) - 25  # 235 working days
    working_hours_per_fte_per_year = working_days_per_year * 8  # 1,880 hours
    
    # Calculate total available FTE hours
    total_available_fte_hours = alert_ftes * working_hours_per_fte_per_year
    
    # Calculate percentage of FTE time spent on alerts
    fte_time_percentage_on_alerts = total_alert_time_hours_per_year / total_available_fte_hours if total_available_fte_hours > 0 else 0
    
    # Calculate total cost of FTEs handling alerts
    total_fte_cost = alert_ftes * avg_salary_per_year
    
    # Cost per alert = (Total FTE cost × % time on alerts) / Total alerts
    total_alert_handling_cost = total_fte_cost * fte_time_percentage_on_alerts
    cost_per_alert = total_alert_handling_cost / alert_volume if alert_volume > 0 else 0
    
    return cost_per_alert, total_alert_handling_cost, fte_time_percentage_on_alerts

# Function to calculate incident costs based on FTE time allocation
def calculate_incident_costs(incident_volume, incident_ftes, avg_incident_triage_time, avg_salary_per_year):
    """Calculate the true cost per incident based on FTE time allocation"""
    if incident_volume == 0 or incident_ftes == 0:
        return 0, 0, 0
    
    total_incident_time_minutes_per_year = incident_volume * avg_incident_triage_time
    total_incident_time_hours_per_year = total_incident_time_minutes_per_year / 60
    
    working_days_per_year = (52 * 5) - 25  # 235 working days
    working_hours_per_fte_per_year = working_days_per_year * 8  # 1,880 hours
    total_available_fte_hours = incident_ftes * working_hours_per_fte_per_year
    
    fte_time_percentage_on_incidents = total_incident_time_hours_per_year / total_available_fte_hours if total_available_fte_hours > 0 else 0
    
    total_fte_cost = incident_ftes * avg_salary_per_year
    total_incident_handling_cost = total_fte_cost * fte_time_percentage_on_incidents
    cost_per_incident = total_incident_handling_cost / incident_volume if incident_volume > 0 else 0
    
    return cost_per_incident, total_incident_handling_cost, fte_time_percentage_on_incidents

# Calculate alert costs using the corrected method
cost_per_alert, total_alert_handling_cost, alert_fte_percentage = calculate_alert_costs(
    alert_volume, alert_ftes, avg_alert_triage_time, avg_alert_fte_salary
)

# Calculate incident costs using the corrected method
cost_per_incident, total_incident_handling_cost, incident_fte_percentage = calculate_incident_costs(
    incident_volume, incident_ftes, avg_incident_triage_time, avg_incident_fte_salary
)

# Calculate savings
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

# Major incident calculations remain the same
mttr_hours_saved_per_incident = (mttr_improvement_pct / 100) * avg_mttr_hours
total_mttr_hours_saved = major_incident_volume * mttr_hours_saved_per_incident
major_incident_savings = total_mttr_hours_saved * avg_major_incident_cost

# Apply risk adjustment if selected
if nbv_model == "Risk-Adjusted (user-defined buffer)":
    for var in [
        'alert_reduction_savings', 'alert_triage_savings', 'incident_reduction_savings',
        'incident_triage_savings', 'major_incident_savings', 'tool_savings',
        'people_cost_per_year', 'fte_avoidance', 'sla_penalty_avoidance', 'revenue_growth'
    ]:
        locals()[var] *= (1 - risk_buffer_pct)

# Total Annual Benefits (at full realization)
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

def create_implementation_timeline_chart(implementation_delay_months, ramp_up_months, evaluation_years, currency_symbol, total_annual_benefits):
    """Create a visual timeline showing benefit realization over time"""
    
    # Create month-by-month data
    total_months = evaluation_years * 12
    months = list(range(1, total_months + 1))
    realization_factors = []
    monthly_benefits = []
    
    for month in months:
        factor = calculate_benefit_realization_factor(
            month, implementation_delay_months, ramp_up_months
        )
        realization_factors.append(factor * 100)  # Convert to percentage
        monthly_benefits.append(total_annual_benefits * factor / 12)  # Monthly benefit amount
    
    # Create the chart with dual y-axes
    fig = go.Figure()
    
    # Add benefit realization percentage line
    fig.add_trace(go.Scatter(
        x=months,
        y=realization_factors,
        mode='lines+markers',
        name='Benefit Realization %',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=4),
        hovertemplate='<b>Month %{x}</b><br>' +
                      'Benefit Realization: %{y:.1f}%<br>' +
                      '<extra></extra>',
        yaxis='y'
    ))
    
    # Add monthly benefit amount as area chart
    fig.add_trace(go.Scatter(
        x=months,
        y=[b/1000 for b in monthly_benefits],  # Convert to thousands for readability
        mode='lines',
        name=f'Monthly Benefits ({currency_symbol}K)',
        line=dict(color='#A23B72', width=2),
        fill='tonexty',
        fillcolor='rgba(162, 59, 114, 0.2)',
        hovertemplate='<b>Month %{x}</b><br>' +
                      f'Monthly Benefit: {currency_symbol}' + '%{customdata:,.0f}<br>' +
                      '<extra></extra>',
        customdata=monthly_benefits,
        yaxis='y2'
    ))
    
    # Add phase annotations with vertical lines
    if implementation_delay_months > 0:
        fig.add_vline(
            x=implementation_delay_months, 
            line_dash="dash", 
            line_color="red",
            line_width=2,
            annotation_text="Go-Live", 
            annotation_position="top",
            annotation=dict(bgcolor="white", bordercolor="red")
        )
    
    if ramp_up_months > 0:
        fig.add_vline(
            x=implementation_delay_months + ramp_up_months, 
            line_dash="dash", 
            line_color="green",
            line_width=2,
            annotation_text="Full Benefits", 
            annotation_position="top",
            annotation=dict(bgcolor="white", bordercolor="green")
        )
    
    # Add shaded regions for different phases
    if implementation_delay_months > 0:
        fig.add_vrect(
            x0=0, x1=implementation_delay_months, 
            fillcolor="red", opacity=0.1,
            layer="below", line_width=0,
            annotation_text="Implementation Phase", 
            annotation_position="top left",
            annotation=dict(textangle=0, font=dict(size=10, color="red"))
        )
    
    if ramp_up_months > 0:
        fig.add_vrect(
            x0=implementation_delay_months, 
            x1=implementation_delay_months + ramp_up_months, 
            fillcolor="orange", opacity=0.1,
            layer="below", line_width=0,
            annotation_text="Ramp-up Phase", 
            annotation_position="top left",
            annotation=dict(textangle=0, font=dict(size=10, color="orange"))
        )
    
    fig.add_vrect(
        x0=implementation_delay_months + ramp_up_months, 
        x1=total_months, 
        fillcolor="green", opacity=0.1,
        layer="below", line_width=0,
        annotation_text="Full Benefits Phase", 
        annotation_position="top left",
        annotation=dict(textangle=0, font=dict(size=10, color="green"))
    )
    
    # Update layout with dual y-axes
    fig.update_layout(
        title={
            'text': 'Implementation Timeline & Benefit Realization',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        xaxis_title="Months from Project Start",
        yaxis=dict(
            title="Benefit Realization (%)",
            side="left",
            range=[0, 105],
            color='#2E86AB'
        ),
        yaxis2=dict(
            title=f"Monthly Benefits ({currency_symbol}K)",
            side="right",
            overlaying="y",
            color='#A23B72'
        ),
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(t=80),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', minor=dict(showgrid=True, gridcolor='lightgray', gridwidth=0.5))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig

# Calculate year-by-year cash flows with implementation delay
annual_cash_flows = []
cumulative_benefits = []
cumulative_costs = []

for year in range(1, evaluation_years + 1):
    # Calculate average benefit realization for this year
    year_start_month = (year - 1) * 12 + 1
    year_end_month = year * 12
    
    monthly_factors = []
    for month in range(year_start_month, year_end_month + 1):
        factor = calculate_benefit_realization_factor(
            month, implementation_delay_months, benefits_ramp_up_months
        )
        monthly_factors.append(factor)
    
    avg_realization_factor = np.mean(monthly_factors)
    
    # Calculate benefits for this year
    year_benefits = total_annual_benefits * avg_realization_factor
    
    # Costs for this year
    year_platform_cost = platform_cost
    year_services_cost = services_cost if year == 1 else 0  # Services cost in year 1 only
    
    # Net cash flow for this year
    year_net_cash_flow = year_benefits - year_platform_cost - year_services_cost
    
    annual_cash_flows.append({
        'year': year,
        'benefits': year_benefits,
        'platform_cost': year_platform_cost,
        'services_cost': year_services_cost,
        'net_cash_flow': year_net_cash_flow,
        'realization_factor': avg_realization_factor
    })
    
    # Update cumulative values
    if year == 1:
        cumulative_benefits.append(year_benefits)
        cumulative_costs.append(year_platform_cost + year_services_cost)
    else:
        cumulative_benefits.append(cumulative_benefits[-1] + year_benefits)
        cumulative_costs.append(cumulative_costs[-1] + year_platform_cost + year_services_cost)

# Calculate NPV with implementation delay
npv = sum([cf['net_cash_flow'] / ((1 + discount_rate) ** cf['year']) for cf in annual_cash_flows])

# NBV Logic
if nbv_model == "Simple (NBV = NPV)":
    net_business_value = npv
elif nbv_model == "Risk-Adjusted (user-defined buffer)":
    net_business_value = npv
elif nbv_model == "Strategic (adds 5% intangible uplift)":
    net_business_value = npv + (0.05 * total_annual_benefits)
elif nbv_model == "CapEx Realized Upfront":
    net_business_value = npv + capex_savings

# ROI and Payback calculations
tco = sum([cf['platform_cost'] + cf['services_cost'] for cf in annual_cash_flows])
roi = npv / tco if tco != 0 else 0

# Calculate payback period (considering implementation delay)
payback_period = "N/A"
cumulative_net_cash_flow = 0
for i, cf in enumerate(annual_cash_flows):
    cumulative_net_cash_flow += cf['net_cash_flow']
    if cumulative_net_cash_flow >= 0:
        payback_period = f"{cf['year']} years"
        break

# Average annual net benefit (across evaluation period)
total_net_benefits = sum([cf['net_cash_flow'] for cf in annual_cash_flows])
avg_annual_net_benefit = total_net_benefits / evaluation_years

# --- Layout ---
st.title("Business Value Assessment")

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
if total_annual_benefits > 0:  # Only show chart if there are benefits to display
    timeline_fig = create_implementation_timeline_chart(
        implementation_delay_months, 
        benefits_ramp_up_months, 
        evaluation_years, 
        currency_symbol, 
        total_annual_benefits
    )
    st.plotly_chart(timeline_fig, use_container_width=True)
    
    # Add explanatory text below the chart
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

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Your Estimated Financial Impact")
    st.metric("Average Annual Net Benefit", f"{currency_symbol}{avg_annual_net_benefit:,.0f}")
    st.metric("Net Present Value (NPV)", f"{currency_symbol}{npv:,.0f}")
    st.metric("Net Business Value (NBV)", f"{currency_symbol}{net_business_value:,.0f}")
    st.metric("Return on Investment (ROI)", f"{roi*100:.1f}%")
    st.metric("Payback Period", payback_period)
    st.caption(f"NPV Discount Rate: {int(discount_rate * 100)}%")
    if nbv_model == "Risk-Adjusted (user-defined buffer)":
        st.caption(f"Risk Buffer: {int(risk_buffer_pct * 100)}%")

with col2:
    st.subheader("Breakdown of Annual Benefits (at Full Realization)")
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
st.subheader("📊 Year-by-Year Cash Flow Analysis")

# Create DataFrame for cash flow table
cash_flow_df = pd.DataFrame([
    {
        'Year': cf['year'],
        'Benefits Realization': f"{cf['realization_factor']*100:.1f}%",
        'Benefits': f"{currency_symbol}{cf['benefits']:,.0f}",
        'Platform Cost': f"{currency_symbol}{cf['platform_cost']:,.0f}",
        'Services Cost': f"{currency_symbol}{cf['services_cost']:,.0f}",
        'Net Cash Flow': f"{currency_symbol}{cf['net_cash_flow']:,.0f}"
    }
    for cf in annual_cash_flows
])

st.dataframe(cash_flow_df, use_container_width=True)

# --- Business Value Narrative ---
escaped_currency_symbol = currency_symbol.replace("$", "\\$")
go_live_month = implementation_delay_months + benefits_ramp_up_months

st.subheader("Business Value Story")
st.markdown(f"""
By adopting **{solution_name}**, your organization can unlock significant financial and operational gains, with benefits realization starting after a **{implementation_delay_months}-month implementation period**.

**Implementation Timeline:**
- **Months 1-{implementation_delay_months}:** Implementation and deployment (no benefits realized)
- **Months {implementation_delay_months + 1}-{go_live_month}:** Benefits ramp-up period (gradual realization)
- **Month {go_live_month}+:** Full benefits realization

**Financial Impact:**
- **Average Annual Net Benefit:** **{escaped_currency_symbol}{avg_annual_net_benefit:,.0f}** (considering implementation delay)
- **Total Cost of Ownership (TCO):** **{escaped_currency_symbol}{tco:,.0f}** over {evaluation_years} years
- **Return on Investment (ROI):** **{roi*100:.1f}%**
- **Payback Period:** **{payback_period}**

**Strategic Value:**
- **Net Present Value (NPV):** **{escaped_currency_symbol}{npv:,.0f}** (time-adjusted value)
- **Net Business Value (NBV):** **{escaped_currency_symbol}{net_business_value:,.0f}** (using {nbv_model} method)

The implementation delay is factored into all calculations, providing a realistic view of when your organization will begin seeing returns on this investment.
""")

# --- Show Calculation Details ---
with st.expander("Show Calculation Details"):
    st.markdown("### Implementation Timeline Impact")
    st.write(f"Implementation Delay: {implementation_delay_months} months")
    st.write(f"Benefits Ramp-up Period: {benefits_ramp_up_months} months")
    st.write(f"Full Benefits Start: Month {implementation_delay_months + benefits_ramp_up_months}")
    
    st.markdown("### Cost Per Alert/Incident Calculations")
    if alert_volume > 0 and alert_ftes > 0:
        st.write(f"**Alert Management:**")
        st.write(f"- Total Alert Time per Year: {alert_volume:,} × {avg_alert_triage_time} min = {alert_volume * avg_alert_triage_time:,} minutes = {(alert_volume * avg_alert_triage_time)/60:,.0f} hours")
        st.write(f"- Available FTE Hours: {alert_ftes} FTEs × 1,880 hours = {alert_ftes * 1880:,} hours")
        st.write(f"- FTE Time on Alerts: {alert_fte_percentage*100:.1f}%")
        st.write(f"- Cost per Alert: {currency_symbol}{cost_per_alert:.2f}")
        st.write(f"- Total Alert Handling Cost: {currency_symbol}{total_alert_handling_cost:,.0f}")
    
    if incident_volume > 0 and incident_ftes > 0:
        st.write(f"**Incident Management:**")
        st.write(f"- Total Incident Time per Year: {incident_volume:,} × {avg_incident_triage_time} min = {incident_volume * avg_incident_triage_time:,} minutes = {(incident_volume * avg_incident_triage_time)/60:,.0f} hours")
        st.write(f"- Available FTE Hours: {incident_ftes} FTEs × 1,880 hours = {incident_ftes * 1880:,} hours")
        st.write(f"- FTE Time on Incidents: {incident_fte_percentage*100:.1f}%")
        st.write(f"- Cost per Incident: {currency_symbol}{cost_per_incident:.2f}")
        st.write(f"- Total Incident Handling Cost: {currency_symbol}{total_incident_handling_cost:,.0f}")
    
    st.markdown("### Annual Benefits Calculations (at Full Realization)")
    st.markdown("#### Alerts")
    st.write(f"Avoided Alerts: {avoided_alerts:,.0f}")
    st.write(f"Alert Reduction Savings = Avoided Alerts × Cost per Alert = {currency_symbol}{alert_reduction_savings:,.2f}")
    st.write(f"Remaining Alerts: {remaining_alerts:,.0f}")
    st.write(f"Alert Triage Savings = Remaining Alert Cost × % Time Saved = {currency_symbol}{alert_triage_savings:,.2f}")

    st.markdown("#### Incidents")
    st.write(f"Avoided Incidents: {avoided_incidents:,.0f}")
    st.write(f"Incident Reduction Savings = Avoided Incidents × Cost per Incident = {currency_symbol}{incident_reduction_savings:,.2f}")
    st.write(f"Remaining Incidents: {remaining_incidents:,.0f}")
    st.write(f"Incident Triage Savings = Remaining Incident Cost × % Time Saved = {currency_symbol}{incident_triage_savings:,.2f}")

    st.markdown("#### Major Incidents")
    st.write(f"MTTR Hours Saved per Incident: {mttr_hours_saved_per_incident:,.2f}")
    st.write(f"Total MTTR Hours Saved = Volume × Hours Saved/Incident = {total_mttr_hours_saved:,.2f}")
    st.write(f"Major Incident Savings = Total MTTR Hours Saved × Cost/hr = {currency_symbol}{major_incident_savings:,.2f}")

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

# Project start
milestone_data.append({
    "Milestone": "Project Start",
    "Month": 0,
    "Benefit Realization": "0%",
    "Status": "✅ Starting point"
})

# Go-live
if implementation_delay_months > 0:
    milestone_data.append({
        "Milestone": "Go-Live",
        "Month": implementation_delay_months,
        "Benefit Realization": "0% → Ramp-up begins",
        "Status": "🚀 Solution deployed"
    })

# Full benefits
full_benefits_month = implementation_delay_months + benefits_ramp_up_months
milestone_data.append({
    "Milestone": "Full Benefits Realized",
    "Month": full_benefits_month,
    "Benefit Realization": "100%",
    "Status": "🎯 Maximum value achieved"
})

# End of evaluation period
milestone_data.append({
    "Milestone": "End of Evaluation Period",
    "Month": evaluation_years * 12,
    "Benefit Realization": "100%",
    "Status": "📊 Analysis complete"
})

milestone_df = pd.DataFrame(milestone_data)
st.dataframe(milestone_df, use_container_width=True, hide_index=True)

# --- Export to CSV ---
export_data = {
    "Year": [cf['year'] for cf in annual_cash_flows],
    "Benefits_Realization_Pct": [cf['realization_factor']*100 for cf in annual_cash_flows],
    "Benefits": [cf['benefits'] for cf in annual_cash_flows],
    "Platform_Cost": [cf['platform_cost'] for cf in annual_cash_flows],
    "Services_Cost": [cf['services_cost'] for cf in annual_cash_flows],
    "Net_Cash_Flow": [cf['net_cash_flow'] for cf in annual_cash_flows]
}

# Add benefit breakdown
benefit_breakdown = {
    "Benefit_Type": [
        "Alert Reduction Savings", "Alert Triage Savings", "Incident Reduction Savings",
        "Incident Triage Savings", "Major Incident Savings", "Tool Consolidation Savings",
        "People Efficiency Gains", "FTE Avoidance", "SLA Penalty Avoidance", "Revenue Growth",
        "Capital Expenditure Savings", "Operational Expenditure Savings"
    ],
    "Annual_Amount_Full_Realization": [
        alert_reduction_savings, alert_triage_savings, incident_reduction_savings,
        incident_triage_savings, major_incident_savings, tool_savings,
        people_cost_per_year, fte_avoidance, sla_penalty_avoidance, revenue_growth,
        capex_savings, opex_savings
    ]
}

cash_flow_df_export = pd.DataFrame(export_data)
benefit_breakdown_df = pd.DataFrame(benefit_breakdown)

# Create combined CSV for export
combined_export_data = []

# Add cash flow data
combined_export_data.append(["=== CASH FLOW ANALYSIS ==="])
combined_export_data.append(["Year", "Benefits_Realization_Pct", "Benefits", "Platform_Cost", "Services_Cost", "Net_Cash_Flow"])
for cf in annual_cash_flows:
    combined_export_data.append([
        cf['year'], 
        f"{cf['realization_factor']*100:.1f}%", 
        cf['benefits'], 
        cf['platform_cost'], 
        cf['services_cost'], 
        cf['net_cash_flow']
    ])

# Add spacing
combined_export_data.append([])
combined_export_data.append(["=== BENEFIT BREAKDOWN (ANNUAL AT FULL REALIZATION) ==="])
combined_export_data.append(["Benefit_Type", "Annual_Amount"])

# Add benefit breakdown
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

# Add summary metrics
combined_export_data.append([])
combined_export_data.append(["=== SUMMARY METRICS ==="])
combined_export_data.append(["Metric", "Value"])
combined_export_data.append(["NPV", npv])
combined_export_data.append(["NBV", net_business_value])
combined_export_data.append(["ROI", f"{roi*100:.1f}%"])
combined_export_data.append(["Payback Period", payback_period])
combined_export_data.append(["Implementation Delay (months)", implementation_delay_months])
combined_export_data.append(["Benefits Ramp-up (months)", benefits_ramp_up_months])
combined_export_data.append(["Cost per Alert", cost_per_alert])
combined_export_data.append(["Cost per Incident", cost_per_incident])
combined_export_data.append(["Alert FTE Time Percentage", f"{alert_fte_percentage*100:.1f}%"])
combined_export_data.append(["Incident FTE Time Percentage", f"{incident_fte_percentage*100:.1f}%"])

# Convert to DataFrame and CSV
combined_df = pd.DataFrame(combined_export_data)
csv_data = combined_df.to_csv(index=False, header=False)

st.download_button(
    label="📥 Export Complete Analysis to CSV",
    data=csv_data,
    file_name="business_value_complete_analysis.csv",
    mime="text/csv"
)
