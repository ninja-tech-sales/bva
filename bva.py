# Developed by N.A.Pearson, HPE OpsRamp
# v1.0 - May 2025

import streamlit as st
import numpy as np
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Business Value Assessment Tool", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.header("Customize Your Financial Impact Model Inputs")

# Solution Name Input
solution_name = st.sidebar.text_input("Solution Name", value="AIOPs")

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
evaluation_years = st.sidebar.slider("Evaluation Period (Years)", 1, 3, 5)

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

# Total Benefits
total_benefits = (
    alert_reduction_savings + alert_triage_savings + incident_reduction_savings +
    incident_triage_savings + major_incident_savings + tool_savings + people_cost_per_year +
    fte_avoidance + sla_penalty_avoidance + revenue_growth + capex_savings + opex_savings
)

annual_net_benefit = total_benefits - platform_cost
annual_net_benefit -= services_cost / evaluation_years

# NPV
npv = sum([annual_net_benefit / ((1 + discount_rate) ** year) for year in range(1, evaluation_years + 1)])

# NBV Logic
if nbv_model == "Simple (NBV = NPV)":
    net_business_value = npv
elif nbv_model == "Risk-Adjusted (user-defined buffer)":
    net_business_value = npv
elif nbv_model == "Strategic (adds 5% intangible uplift)":
    net_business_value = npv + (0.05 * total_benefits)
elif nbv_model == "CapEx Realized Upfront":
    net_business_value = npv + capex_savings

# ROI and Payback
tco = (platform_cost * evaluation_years) + services_cost
roi = (npv - tco) / tco if tco != 0 else 0
payback_period = tco / annual_net_benefit if annual_net_benefit != 0 else 0

# --- Layout ---
st.title("Business Value Assessment")

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Your Estimated Financial Impact")
    st.metric("Annual Net Benefit", f"{currency_symbol}{annual_net_benefit:,.0f}")
    st.metric("Net Present Value (NPV)", f"{currency_symbol}{npv:,.0f}")
    st.metric("Net Business Value (NBV)", f"{currency_symbol}{net_business_value:,.0f}")
    st.caption(f"NPV Discount Rate: {int(discount_rate * 100)}%")
    if nbv_model == "Risk-Adjusted (user-defined buffer)":
        st.caption(f"Risk Buffer: {int(risk_buffer_pct * 100)}%")

with col2:
    st.subheader("Breakdown of Benefits")
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

# --- Business Value Narrative ---
escaped_currency_symbol = currency_symbol.replace("$", "\\$")
st.subheader("Business Value Story")
st.markdown(f"""
By adopting **{solution_name}**, your organization can unlock significant financial and operational gains.

- **Annual Net Benefit:** Estimated at **{escaped_currency_symbol}{annual_net_benefit:,.0f} per year**, driven by fewer alerts and incidents, faster resolution times, tool consolidation, and workforce efficiency.
- **Total Cost of Ownership (TCO):** Over the {evaluation_years}-year period, total investment is projected at **{escaped_currency_symbol}{tco:,.0f}**, including platform and service costs.
- **Return on Investment (ROI):** The initiative yields an ROI of **{roi*100:.1f}%**, showcasing strong value generation relative to cost.
- **Payback Period:** Your investment is expected to break even in **{payback_period:.2f} years**.

From a financial perspective:
- **Net Present Value (NPV):** The investment yields a discounted cash value of **{escaped_currency_symbol}{npv:,.0f}**, reflecting the time value of money.
- **Net Business Value (NBV):** Using the **{nbv_model}** method, overall strategic value is estimated at **{escaped_currency_symbol}{net_business_value:,.0f}**.
""")

# --- Show Calculation Details ---
with st.expander("Show Calculation Details"):
    st.markdown("### Alerts")
    st.write(f"Avoided Alerts: {avoided_alerts:,.0f}")
    st.write(f"Alert Reduction Savings = Avoided Alerts × Triage Time × Cost/hr = {currency_symbol}{alert_reduction_savings:,.2f}")
    st.write(f"Remaining Alerts: {remaining_alerts:,.0f}")
    st.write(f"Alert Triage Savings = Remaining Alerts × Triage Time × Cost/hr × % Saved = {currency_symbol}{alert_triage_savings:,.2f}")

    st.markdown("### Incidents")
    st.write(f"Avoided Incidents: {avoided_incidents:,.0f}")
    st.write(f"Incident Reduction Savings = Avoided Incidents × Triage Time × Cost/hr = {currency_symbol}{incident_reduction_savings:,.2f}")
    st.write(f"Remaining Incidents: {remaining_incidents:,.0f}")
    st.write(f"Incident Triage Savings = Remaining Incidents × Triage Time × Cost/hr × % Saved = {currency_symbol}{incident_triage_savings:,.2f}")

    st.markdown("### Major Incidents")
    st.write(f"MTTR Hours Saved per Incident: {mttr_hours_saved_per_incident:,.2f}")
    st.write(f"Total MTTR Hours Saved = Volume × Hours Saved/Incident = {total_mttr_hours_saved:,.2f}")
    st.write(f"Major Incident Savings = Total MTTR Hours Saved × Cost/hr = {currency_symbol}{major_incident_savings:,.2f}")

    st.markdown("### Other Benefits")
    st.write(f"Tool Consolidation: {currency_symbol}{tool_savings:,.2f}")
    st.write(f"People Efficiency Gains: {currency_symbol}{people_cost_per_year:,.2f}")
    st.write(f"FTE Avoidance: {currency_symbol}{fte_avoidance:,.2f}")
    st.write(f"SLA Penalty Avoidance: {currency_symbol}{sla_penalty_avoidance:,.2f}")
    st.write(f"Revenue Growth: {currency_symbol}{revenue_growth:,.2f}")
    st.write(f"CapEx Savings: {currency_symbol}{capex_savings:,.2f}")
    st.write(f"OpEx Savings: {currency_symbol}{opex_savings:,.2f}")

    st.markdown("### Costs")
    st.write(f"Platform Cost (Annual): {currency_symbol}{platform_cost:,.2f}")
    st.write(f"Services (One-Time): {currency_symbol}{services_cost:,.2f}")

    st.markdown("### Annual Net Benefit")
    st.write(f"Total Benefits: {currency_symbol}{total_benefits:,.2f}")
    st.write(f"Annual Net Benefit = Total Benefits - Platform Cost - (Services ÷ Years) = {currency_symbol}{annual_net_benefit:,.2f}")

# --- Export to CSV ---
export_data = {
    "Benefit": [
        "Alert Reduction Savings", "Alert Triage Savings", "Incident Reduction Savings",
        "Incident Triage Savings", "Major Incident Savings", "Tool Consolidation Savings",
        "People Efficiency Gains", "FTE Avoidance", "SLA Penalty Avoidance", "Revenue Growth",
        "Capital Expenditure Savings", "Operational Expenditure Savings"
    ],
    "Amount": [
        alert_reduction_savings, alert_triage_savings, incident_reduction_savings,
        incident_triage_savings, major_incident_savings, tool_savings,
        people_cost_per_year, fte_avoidance, sla_penalty_avoidance, revenue_growth,
        capex_savings, opex_savings
    ]
}
df = pd.DataFrame(export_data)
st.download_button(
    label="Export Summary to CSV",
    data=df.to_csv(index=False),
    file_name="business_value_summary.csv",
    mime="text/csv"
)

