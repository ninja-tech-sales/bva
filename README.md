Overview & Purpose
What is the BVA Tool?
The Business Value Assessment (BVA) Tool is a comprehensive financial modeling application that helps demonstrate
the business value and ROI of implementing AIOPs & Observability solutions. It provides:
• Financial Impact Analysis: NPV, ROI, and payback calculations
• Scenario Modeling: Conservative, Expected, and Optimistic scenarios
• Stakeholder Reports: Tailored value propositions for different roles
• Executive Summaries: Professional PDF reports for decision-makers
Key Benefits
• Quantify Value: Convert operational improvements into financial metrics
• Risk Assessment: Model different scenarios to understand potential outcomes
• Stakeholder Communication: Generate role-specific value propositions
• Professional Reporting: Create executive-ready documentation
Page 4
Getting Started
Accessing the Tool
1. Open your web browser and navigate to the BVA tool URL:
https://bvatool.streamlit.app/
2. 3. 4. The tool loads with default values - you can start customizing immediately
All inputs are located in the left sidebar
Results and visualizations appear in the main content area
First-Time Setup
1. 2. 3. Solution Name: Enter the name of your solution (default: "AIOPs")
Currency: Select your preferred currency symbol ($, €, £, Kč)
Industry Template: Choose a template or use "Custom" for manual entry
Page 5
Configuration Import/Export
🔄 Exporting Configurations
When to Export:
• Before making major changes (backup)
• To share configurations with colleagues
• To save different customer scenarios
• To create industry templates
How to Export:
1. Navigate to "Configuration Export/Import" section in the sidebar
2. Expand " Export Configuration"
3. Select format: CSV (spreadsheet-friendly) or JSON (technical format)
4. Click "Generate Export File"
5. Click "Download [Format] Configuration" to save the file
File Naming: Files are automatically named with timestamps (e.g., BVA_Config_20250619_143022.csv)
📥 Importing Configurations
When to Import:
• Loading previously saved scenarios
• Using shared configurations from colleagues
• Applying industry templates
• Restoring backup configurations
How to Import:
1. Expand " Import Configuration"
2. 4. 5. Click "Choose configuration file" and select your CSV/JSON file
3. Click "Import Configuration"
Look for success message: "Successfully imported X parameters"
IMPORTANT: Refresh your browser page (F5) to see all imported values
Supported Formats: CSV and JSON files exported from the BVA tool
Input Parameters Guide
📅 Implementation Timeline
Page 6
• Implementation Delay: Months before benefits begin (typical: 3-9 months)
• Benefits Ramp-up: Time to reach full benefits after go-live (typical: 1-6 months)
⏰ Working Hours Configuration
• Working Hours per Day: Standard workday (typically 8 hours)
• Working Days per Week: Usually 5 for business days
• Working Weeks per Year: Standard 52 weeks
• Holiday + Sick Days: Total annual leave (typically 20-30 days)
🚨 Alert Management
• Alert Volume: Total infrastructure alerts managed annually
• Alert FTEs: Number of people managing alerts
• Average Triage Time: Minutes to process each alert
• FTE Salary: Annual salary for alert management staff
• Alert Reduction %: Expected reduction in alert volume
• Triage Time Reduction %: Efficiency improvement in processing
🔧 Incident Management
• Incident Volume: Total infrastructure incidents annually
• Incident FTEs: Number of people managing incidents
• Average Triage Time: Minutes to process each incident
• FTE Salary: Annual salary for incident management staff
• Incident Reduction %: Expected reduction in incident volume
• Triage Time Reduction %: Efficiency improvement in processing
🚨 Major Incidents (Sev1)
• Major Incident Volume: Severe incidents per year
• Cost per Hour: Business impact cost of major incidents
• Average MTTR: Current mean time to resolution (hours)
• MTTR Improvement %: Expected reduction in resolution time
💰 Additional Benefits
• Tool Consolidation Savings: Savings from replacing multiple tools
• People Efficiency Gains: Additional productivity improvements
• FTE Avoidance: Cost of hiring additional staff avoided
• SLA Penalty Avoidance: Penalties avoided through better performance
• Revenue Growth: Additional revenue from improved services
• CAPEX/OPEX Savings: Hardware and operational cost reductions
💳 Solution Costs
• Annual Subscription: Yearly licensing cost (after discounts)
• Implementation Services: One-time implementation cost
Page 7
📊 Financial Settings
• Evaluation Period: Years to analyze (typically 3-5 years)
• NPV Discount Rate: Financial discount rate for NPV calculation (typically 8-12%)
Page 8
Understanding the Calculations
This is the most important section for understanding how the BVA tool works. Many of the financial benefits are
derived from these core calculations.
🧮 Step 1: Working Hours Calculation
Purpose: Establishes the baseline for FTE cost calculations
Formula:
Total Working Days = (Weeks per Year × Days per Week) - Holiday/Sick Days
Working Hours per FTE per Year = Total Working Days × Hours per Day
Example:
- 52 weeks/year × 5 days/week = 260 potential working days
- 260 days - 25 holiday/sick days = 235 actual working days
- 235 days × 8 hours/day = 1,880 working hours per FTE per year
Why This Matters: This determines how much of an FTE's time and cost can be allocated to alert/incident
management.
🚨 Step 2: Alert Cost Calculation
Purpose: Determines the true cost per alert based on FTE time allocation
Formula:
Total Alert Time per Year = Alert Volume × Average Triage Time (minutes)
Total Alert Hours per Year = Total Alert Time ÷ 60
Total Available FTE Hours = Alert FTEs × Working Hours per FTE per Year
FTE Time % on Alerts = Total Alert Hours ÷ Total Available FTE Hours
Page 9
Total Alert Handling Cost = (Alert FTEs × Average Salary) × FTE Time % on Alerts
Cost per Alert = Total Alert Handling Cost ÷ Alert Volume
Example:
- 500,000 alerts/year × 15 minutes = 7,500,000 minutes
- 7,500,000 ÷ 60 = 125,000 hours/year
- 3 FTEs × 1,880 hours = 5,640 available hours
- 125,000 ÷ 5,640 = 2,215% (meaning you need more FTEs!)
- If you had 67 FTEs: 125,000 ÷ (67 × 1,880) = 99% time allocation
- 67 FTEs × $60,000 salary × 99% = $3,980,400 total cost
- $3,980,400 ÷ 500,000 alerts = $7.96 per alert
Key Insight: If the FTE time percentage exceeds 100%, you need more staff or your estimates are incorrect.
🔧 Step 3: Incident Cost Calculation
Purpose: Same logic as alerts, but for incidents
Formula: (Identical to alert calculation, using incident-specific inputs)
Cost per Incident = [(Incident FTEs × Salary × Time Allocation %)] ÷ Incident Volume
Example:
- 50,000 incidents/year × 45 minutes = 2,250,000 minutes
- 2,250,000 ÷ 60 = 37,500 hours/year
Page 10
- 20 FTEs × 1,880 hours = 37,600 available hours
- 37,500 ÷ 37,600 = 99.7% time allocation
- 20 FTEs × $70,000 × 99.7% = $1,395,800 total cost
- $1,395,800 ÷ 50,000 = $27.92 per incident
💰 Step 4: Savings Calculations
Alert Reduction Savings
Purpose: Cost savings from reducing alert volume
Formula:
Avoided Alerts = Alert Volume × (Alert Reduction % ÷ 100)
Alert Reduction Savings = Avoided Alerts × Cost per Alert
Example:
- 500,000 alerts × 30% reduction = 150,000 avoided alerts
- 150,000 × $7.96 = $1,194,000 annual savings
Alert Triage Time Savings
Purpose: Additional savings from processing remaining alerts faster
Formula:
Remaining Alerts = Alert Volume - Avoided Alerts
Remaining Alert Cost = Remaining Alerts × Cost per Alert
Alert Triage Savings = Remaining Alert Cost × (Triage Time Reduction % ÷ 100)
Example:
- 500,000 - 150,000 = 350,000 remaining alerts
- 350,000 × $7.96 = $2,786,000 remaining cost
- $2,786,000 × 25% efficiency = $696,500 additional savings
Page 11
Incident Savings (Same Logic)
Incident Reduction Savings = (Incident Volume × Reduction %) × Cost per Incident
Incident Triage Savings = (Remaining Incidents × Cost per Incident) × Efficiency %
Major Incident Savings
Purpose: Cost savings from faster resolution of critical incidents
Formula:
MTTR Hours Saved per Incident = Current MTTR × (Improvement % ÷ 100)
Total MTTR Hours Saved = Major Incident Volume × MTTR Hours Saved per Incident
Major Incident Savings = Total MTTR Hours Saved × Cost per Hour
Example:
- 8 hours current MTTR × 40% improvement = 3.2 hours saved per incident
- 120 major incidents × 3.2 hours = 384 hours saved annually
- 384 hours × $10,000/hour = $3,840,000 annual savings
🧮 Step 5: Total Annual Benefits
Purpose: Sum all savings categories
Formula:
Total Annual Benefits =
Alert Reduction Savings +
Alert Triage Savings +
Incident Reduction Savings +
Incident Triage Savings +
Major Incident Savings +
Tool Savings +
People Efficiency Gains +
FTE Avoidance +
SLA Penalty Avoidance +
Revenue Growth +
CAPEX Savings +
OPEX Savings
Page 12
📊 Step 6: Implementation Timeline Impact
Purpose: Model when benefits are actually realized
Benefit Realization Factor
Formula:
If Month ≤ Implementation Delay: Factor = 0%
If Implementation Delay < Month ≤ (Implementation Delay + Ramp-up):
Factor = (Month - Implementation Delay) ÷ Ramp-up Period
If Month > (Implementation Delay + Ramp-up): Factor = 100%
Example (6-month implementation, 3-month ramp-up):
- Months 1-6: 0% benefits (still implementing)
- Month 7: 33% benefits (1 month into 3-month ramp-up)
- Month 8: 67% benefits (2 months into ramp-up)
- Month 9+: 100% benefits (full realization)
Monthly Cash Flow
Formula:
Page 13
Monthly Benefit = (Annual Benefits ÷ 12) × Realization Factor
Monthly Platform Cost = Annual Platform Cost ÷ 12
Monthly Net Cash Flow = Monthly Benefit - Monthly Platform Cost
(Plus one-time services cost in Year 1)
💹 Step 7: Financial Metrics
Net Present Value (NPV)
Purpose: Value of future cash flows in today's money.
Formula:
NPV = Σ [Net Cash Flow Year n ÷ (1 + Discount Rate)^n]
Example (3-year evaluation, 10% discount rate):
Year 1: $500,000 ÷ (1.10)¹ = $454,545
Year 2: $1,200,000 ÷ (1.10)² = $991,736
Year 3: $1,200,000 ÷ (1.10)³ = $901,578
NPV = $454,545 + $991,736 + $901,578 = $2,347,859
Return on Investment (ROI)
Formula:
Total Investment = Sum of all platform and services costs
ROI = NPV ÷ Total Investment × 100%
Example:
Page 14
NPV = $2,347,859
Total Investment = $800,000
ROI = $2,347,859 ÷ $800,000 × 100% = 293.5%
Payback Period
Purpose: When cumulative cash flow turns positive
Monthly Calculation:
For each month:
Cumulative Cash Flow += Monthly Net Cash Flow
If Cumulative Cash Flow ≥ 0: Payback achieved
🔄 Step 8: Scenario Adjustments
Conservative Scenario
- Annual Benefits × 0.7 (30% lower)
- Implementation Delay × 1.3 (30% longer)
- Ramp-up period unchanged
Optimistic Scenario
- Annual Benefits × 1.2 (20% higher)
- Implementation Delay × 0.8 (20% shorter)
- Ramp-up period unchanged
🚀 Step 9: FTE Equivalency Calculation
Purpose: Convert operational savings to equivalent headcount
Formula:
Total Operational Savings = Alert + Incident + Major Incident Savings
Average FTE Salary = (Alert FTE Salary + Incident FTE Salary) ÷ 2
Equivalent FTEs = Total Operational Savings ÷ Average FTE Salary
Example:
Total Operational Savings = $2,500,000
Average FTE Salary = ($60,000 + $70,000) ÷ 2 = $65,000
Equivalent FTEs = $2,500,000 ÷ $65,000 = 38.5 FTEs
Page 15
Interpretation: The solution saves the equivalent of 38.5 full-time employees' worth of operational costs annually.
⚠️ Common Calculation Pitfalls
1. FTE Time Allocation Over 100%
Problem: More work than available hours Solution: Either increase FTE count or reduce volume/time estimates
2. Unrealistic Improvement Percentages
Problem: 80%+ reduction claims Solution: Use industry benchmarks (typically 20-50% improvements)
3. Double-Counting Benefits
Problem: Including the same savings in multiple categories Solution: Clearly define what each category covers
4. Ignoring Implementation Reality
Problem: Assuming immediate 100% benefits Solution: Always include realistic ramp-up periods
5. Inconsistent Time Periods
Problem: Mixing monthly and annual figures Solution: Ensure all calculations use consistent time units
🔍 Validation Checklist
Before finalizing your model, verify:
Page 16
FTE time allocation is realistic (ideally 60-90% for operational roles)
Cost per alert/incident makes sense (compare to industry benchmarks)
Total annual benefits are achievable (not more than 50% of current operational costs)
Implementation timeline is realistic (typically 6-12 months for complex solutions)
Conservative scenario still shows positive ROI (risk mitigation)
All calculations use consistent units (annual figures, same currency)
Understanding the Results
📊 Key Metrics Dashboard
Net Present Value (NPV)
• Total financial benefit in today's dollars
• Positive NPV indicates profitable investment
• Higher NPV = better investment
Return on Investment (ROI)
• Percentage return on investment
• Formula: (Benefits - Costs) / Costs × 100
• Higher ROI = more efficient investment
Payback Period
Page 17
• Time to recover initial investment
• Shown in both years and months
• Shorter payback = faster value realization
🚀 Value Reallocation & FTE Equivalency
• Cost Available for Higher Margin Projects: Annual savings that can be redirected
• Equivalent FTEs from Savings: Number of full-time employees worth of savings
📈 Charts and Visualizations
Implementation Timeline Chart
• Shows benefit realization over time
• Identifies implementation, ramp-up, and full benefits phases
• Helps stakeholders understand when value is delivered
Cumulative Cash Flow Chart
• Monthly view of investment recovery
• Shows payback point where cumulative cash flow turns positive
• Useful for cash flow planning
Scenario Comparison
• Visual comparison of Conservative, Expected, and Optimistic outcomes
• Helps assess risk and potential upside
Scenario Analysis
Understanding the Three Scenarios
Conservative Scenario
• Benefits: 30% lower than expected
• Implementation: 30% longer timeline
• Purpose: Risk assessment and worst-case planning
Expected Scenario
• Benefits: As entered in the tool
• Implementation: As planned
• Purpose: Most likely outcome for planning
Optimistic Scenario
• Benefits: 20% higher than expected
• Implementation: 20% faster timeline
Page 18
• Purpose: Best-case outcome and upside potential
Using Scenario Analysis
For Risk Management:
• Present all three scenarios to show range of outcomes
• Use Conservative scenario for budget approvals
• Use Optimistic scenario to show upside potential
For Stakeholder Communication:
• Show that even the Conservative scenario delivers positive ROI
• Highlight the range of potential NPV outcomes
• Demonstrate investment resilience across scenarios
Generating Reports
📄 PDF Executive Report
When to Use:
• Board presentations
• Executive briefings
• Formal project approvals
• Customer presentations
How to Generate:
1. 2. 4. 5. Scroll to "Generate Executive Report" section
Enter "Your Organization Name" for the report
3. Click "Generate PDF Report"
Wait for processing (may take 10-30 seconds)
Click "Download PDF Report" when ready
Report Contents:
• Executive summary with key financial metrics
• Implementation roadmap and milestones
• Scenario analysis comparison
Page 19
• Professional charts and tables
📋 Stakeholder Value Propositions
Available Stakeholder Views:
• CIO: Strategic alignment and digital transformation
• CTO: Technology modernization and resilience
• CFO: Financial returns and cost optimization
• Operations Manager: Operational efficiency and reduced toil
• Service Desk Manager: Service quality and customer satisfaction
How to Use:
1. 2. 3. 4. Navigate to "Stakeholder Value Propositions" section
Click on the relevant stakeholder tab
Copy/paste content for presentations or emails
Customize messaging as needed for specific audiences
Best Practices
🎯 Data Collection Best Practices
Before Starting:
• Gather historical alert/incident data (12+ months)
• Identify current FTE allocation for operations
• Understand current tool costs and contracts
• Validate salary information for accurate calculations
Industry Templates:
• Use templates as starting points only
• Customize all values based on actual customer data
• Don't rely solely on template defaults
💡 Modeling Best Practices
Conservative Estimates:
• Use conservative improvement percentages (20-40%)
• Include realistic implementation timelines
• Account for gradual adoption curves
Benefit Categories:
Page 20
• Focus on quantifiable, measurable benefits
• Avoid "soft benefits" that can't be validated
• Include only benefits directly attributable to the solution
Timeline Modeling:
• Allow adequate time for implementation and ramp-up
• Consider organizational change management
• Plan for training and adoption periods
📊 Presentation Best Practices
For Executives:
• Lead with NPV and ROI metrics
• Show Conservative scenario to demonstrate low risk
• Emphasize payback period for cash flow impact
• Use the generated PDF report for formal presentations
For Technical Audiences:
• Show detailed calculations (use the expandable section)
• Explain methodology and assumptions
• Discuss implementation timeline and dependencies
For Financial Audiences:
• Focus on NPV calculations and discount rates
• Explain cash flow timing and implications
• Show sensitivity analysis across scenarios
Page 21
Common Workflows
🔄 Workflow 1: New Customer Assessment
1. Preparation
a. Gather customer operational data
b. Understand current pain points and costs
c. Research industry benchmarks
2. Initial Modeling
a. Select appropriate industry template
b. Enter customer-specific data
c. Adjust improvement percentages based on current maturity
3. Scenario Development
a. Review all three scenarios
b. Adjust assumptions if needed
c. Validate results make business sense
4. Export and Save
a. Export configuration for future reference
b. Generate PDF report for stakeholder presentation
🔄 Workflow 2: Comparative Analysis
1. Create Baseline
a. Model current state scenario
b. Export configuration as "Customer_Baseline"
2. Model Alternative Solutions
a. Create variations with different improvement levels
b. Export each as separate configuration files
3. Side-by-Side Comparison
a. Import each configuration separately
b. Document key differences in NPV/ROI
Page 22
c. Create summary comparison table
🔄 Workflow 3: Executive Presentation Prep
1. Validate Model
a. Review all inputs for accuracy
b. Ensure Conservative scenario shows positive ROI
c. Check that assumptions are defensible
2. Generate Materials
a. Create PDF executive report
b. Copy stakeholder value propositions
c. Export configuration for backup
3. Presentation Ready
a. Lead with Expected scenario metrics
b. Show Conservative scenario for risk mitigation
c. Have detailed calculations available if questioned
Page 23
Troubleshooting
Common Issues and Solutions
Import Not Working
• Problem: Uploaded file but values didn't change
• Solution: Refresh the browser page (F5) after import
• Prevention: Always refresh after importing configurations
PDF Generation Fails
• Problem: Error when clicking "Generate PDF Report"
• Solution: Check that all required numeric fields have values
• Prevention: Ensure no input fields are left empty
Unrealistic Results
• Problem: NPV or ROI seems too high/low
• Solution: Review input assumptions, especially improvement percentages
• Prevention: Use conservative estimates and validate against benchmarks
Negative Cash Flow
• Problem: All scenarios show negative NPV
• Solution: Review cost assumptions and benefit calculations
• Prevention: Ensure implementation costs are realistic and benefits are achievable
Getting Help
Data Issues:
• Verify input data sources and calculations
Page 24
• Cross-reference with industry benchmarks
• Consult with customer operations teams
Technical Issues:
• Try refreshing the browser
• Clear browser cache if persistent issues
• Use Chrome or Firefox for best compatibility
Methodology Questions:
• Review the detailed calculations in the expandable section
• Consult with finance teams on discount rates and assumptions
• Reference industry best practices for improvement estimates
Page 25
Quick Reference Card
Essential Steps for New Users
1. 2. 3. 4. 5. Choose industry template or enter "Custom"
Enter solution name and select currency
Configure working hours for your organization
Input alert and incident management data
Add cost information (platform + services)
6. Review scenario results
7. Export configuration (backup)
8. Generate PDF report for stakeholders
Key Shortcuts
• F5: Refresh page after importing
• Ctrl+S: Save/bookmark current page state
• Export before major changes: Always backup your work
Success Criteria
• Conservative scenario shows positive ROI
• Payback period is acceptable to organization
• Benefits are realistic and achievable
• All stakeholders can see value in their terms
