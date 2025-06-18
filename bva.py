# Developed by N.A.Pearson, HPE OpsRamp
# v1.1 - June 2025 - Added Implementation Delay Feature

import streamlit as st
import numpy as np
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Business Value Assessment Tool", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.header("Customize Your Financial Impact Model Inputs")

# Solution Name Input
solution_name = st.sidebar.text_input("Solution Name", value="AIOPs")

# --- Implementation Timeline ---
st.sidebar.subheader("📅 Implementation Timeline")
implementation_delay_months = st.sidebar.slider(
    "Implementation Delay (months)", 
    0, 24, 6, 
    help="Time from project start until benefits begin to be realized"
)
benefits_ramp_up_months = st.sidebar.slider(
    "Benefits Ramp-up Period (months)", 
    0, 12, 3,
    help="Time to reach full benefits after go-live (gradual adoption)"
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

selected_template = st.sidebar.selectbox("Select Industry Template", list(industry_templates.keys()))
template = industry_templates[selected_template]
st.sidebar.caption("📌 Industry templates provide baseline values for estimation only. Adjust any field as needed.")

# --- Currency Selection ---
currency_symbol = st.sidebar.selectbox("Currency", ["$", "€", "£", "Kč"])

# --- Input Fields with Template Prefill ---
alert_volume = st.sidebar.number_input("Total Infrastructure Related Alerts Managed per Year", value=template.get("alert_volume", 0))
alert_ftes = st.sidebar.number_input("Total FTEs Managing Infrastructure Alerts", value=0)
avg_alert_triage_time = st.sidebar.number_input("Average Alert Triage Time (minutes)", value=template.get("avg_alert_triage_time", 0))
alert_triage_cost_per_hour = st.sidebar.number_input("Average Alert Triage Cost per Hour for all FTEs", value=0)
alert_reduction_pct = st.sidebar.slider("% Alert Reduction", 0, 100, value=template.get("alert_reduction_pct", 0))
alert_triage_time_saved_pct = st.sidebar.slider("% Alert Triage Time Reduction", 0, 100, 0)

incident_volume = st.sidebar.number_input("Total Infrastucture Related Incident Volumes Managed per Year", value=template.get("incident_volume", 0))
incident_ftes = st.sidebar.number_input("Total FTEs Managing Infrastructure Incidents", value=0)
avg_incident_triage_time = st.sidebar.number_input("Average Incident Triage Time (minutes)", value=template.get("avg_incident_triage_time", 0))
incident_triage_cost_per_hour = st.sidebar.number_input("Average Incident Triage Cost per Hour for all FTEs", value=0)
incident_reduction_pct = st.sidebar.slider("% Incident Reduction", 0, 100, value=template.get("incident_reduction_pct", 0))
incident_triage_time_savings_pct = st.sidebar.slider("% Incident Triage Time Reduction", 0, 100, 0)

major_incident_volume = st.sidebar.number_input("Total Infrastructure Related Major Incidents per Year (Sev1)", value=template.get("major_incident_volume", 0))
avg_major_incident_cost = st.sidebar.number_input("Average Major Incident Cost per Hour", value=0)
avg_mttr_hours = st.sidebar.number_input("Average MTRS (hours)", value=0.0)
mttr_improvement_pct = st.sidebar.slider("MTRS Improvement Percentage", 0, 100, value=template.get("mttr_improvement_pct", 0))

tool_savings = st.sidebar.number_input("Tool Consolidation Savings", value=0)
people_cost_per_year = st.sidebar.number_input("People Efficiency Gains", value=0)
fte_avoidance = st.sidebar.number_input("FTE Avoidance (annualized value in local currency)", value=0)
sla_penalty_avoidance = st.sidebar.number_input("SLA Penalty Avoidance (Service Providers)", value=0)
revenue_growth = st.sidebar.number_input("Revenue Growth (Service Providers)", value=0)
platform_cost = st.sidebar.number_input("Annual Subscription Cost (After discounts)", value=0)
services_cost = st.sidebar.number_input("Implementation & Services (One-Time)", value=0)
capex_savings = st.sidebar.number_input("Capital Expenditure Savings (Hardware)", value=0)
opex_savings = st.sidebar.number_input("Operational Expenditure Savings (e.g. Storage Costs)", value=0)
evaluation_years = st.sidebar.slider("Evaluation Period (Years)", 1, 5, 3)

discount_rate = st.sidebar.slider("NPV Discount Rate (%)", 0, 20, 10) / 100

nbv_model = st.sidebar.selectbox(
    "Net Business Value Model",
    [
        "Simple (NBV = NPV)",
        "Risk-Adjusted (user-defined buffer)",
        "Strategic (adds 5% intangible uplift)",
        "CapEx Realized Upfront"
    ]
)

risk_buffer_pct = 0.0
if nbv_model == "Risk-Adjusted (user-defined buffer)":
    risk_buffer_pct = st.sidebar.slider("Risk Adjustment Buffer (%)", 0, 100, 10) / 100

# --- Calculations ---
avoided_alerts = alert_volume * (alert_reduction_pct / 100)
remaining_alerts = alert_volume - avoided_alerts
alert_reduction_savings = avoided_alerts * avg_alert_triage_time / 60 * alert_triage_cost_per_hour
total_alert_triage_cost = remaining_alerts * avg_alert_triage_time / 60 * alert_triage_cost_per_hour
alert_triage_savings = total_alert_triage_cost * (alert_triage_time_saved_pct / 100)

avoided_incidents = incident_volume * (incident_reduction_pct / 100)
remaining_incidents = incident_volume - avoided_incidents
incident_reduction_savings = avoided_incidents * avg_incident_triage_time / 60 * incident_triage_cost_per_hour
total_incident_triage_cost = remaining_incidents * avg_incident_triage_time / 60 * incident_triage_cost_per_hour
incident_triage_savings = total_incident_triage_cost * (incident_triage_time_savings_pct / 100)

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

# --- NEW: Calculate Year-by-Year Cash Flows with Implementation Delay ---
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

# Calculate cash flows for each year
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

# Timeline visualization
st.subheader("📅 Implementation Timeline")
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
    
    st.markdown("### Annual Benefits Calculations (at Full Realization)")
    st.markdown("#### Alerts")
    st.write(f"Avoided Alerts: {avoided_alerts:,.0f}")
    st.write(f"Alert Reduction Savings = Avoided Alerts × Triage Time × Cost/hr = {currency_symbol}{alert_reduction_savings:,.2f}")
    st.write(f"Remaining Alerts: {remaining_alerts:,.0f}")
    st.write(f"Alert Triage Savings = Remaining Alerts × Triage Time × Cost/hr × % Saved = {currency_symbol}{alert_triage_savings:,.2f}")

    st.markdown("#### Incidents")
    st.write(f"Avoided Incidents: {avoided_incidents:,.0f}")
    st.write(f"Incident Reduction Savings = Avoided Incidents × Triage Time × Cost/hr = {currency_symbol}{incident_reduction_savings:,.2f}")
    st.write(f"Remaining Incidents: {remaining_incidents:,.0f}")
    st.write(f"Incident Triage Savings = Remaining Incidents × Triage Time × Cost/hr × % Saved = {currency_symbol}{incident_triage_savings:,.2f}")

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

# Convert to DataFrame and CSV
combined_df = pd.DataFrame(combined_export_data)
csv_data = combined_df.to_csv(index=False, header=False)

st.download_button(
    label="📥 Export Complete Analysis to CSV",
    data=csv_data,
    file_name="business_value_complete_analysis.csv",
    mime="text/csv"
)
