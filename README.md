# AI for Finance Teams ROI Calculator

An in-browser calculator to estimate time and cost savings from automating finance workflows (AP, AR, Reconciliation).

## How to Use
- Open `calculator.html` in a browser. The calculator is centered with a guide panel on the left.
- Pick a workflow (Accounts Payable, Accounts Receivable, Reconciliation).
- Select the input you want to edit, then use the keypad to enter values. “Set Default Value” resets only the active field.
- Click `= Calculate` to refresh the results. “AC” resets all fields to defaults.

## Inputs
- Transactions per Month: Monthly transaction volume.
- Minutes per Transaction: Average handling time with no exception.
- Exception Rate and Minutes per Exception: Portion and effort for exception cases.
- Review Hours per Month: Leadership review/approval time.
- Hourly Cost: Fully loaded hourly rate for the work.
- Coverage: Touchless % and Reviewed % (must total ≤ 100%; Manual is derived).
- Time Saved %: Expected time reduction for Touchless and Reviewed work.
- Accuracy: Expected vs Minimum accuracy; savings are zeroed if Expected < Minimum.
- Ramp: Month 1 / Month 2 / Month 3+ ramp percentages for recovered hours.

## Outputs
- Hours Recovered (Steady): Monthly hours saved after applying coverage, time saved %, accuracy gate, and ramp.
- Full-Time Equivalent Capacity: Recovered hours ÷ 160 hours per FTE-month.
- Annual Cost Equivalent: Recovered hours × hourly cost × 12.
- Automation Rate: Touchless + Reviewed coverage; Manual is the remainder.
- Ramp by Month: Hours recovered in Months 1, 2, and 3+ based on ramp.
- Baseline vs Post Hours: Starting hours per month and hours after automation.

## Calculation Logic & Assumptions
- Baseline Hours = ((Transactions × Minutes per Transaction) + (Transactions × Exception Rate × Minutes per Exception)) ÷ 60 + Review Hours.
- Coverage: Touchless % + Reviewed % ≤ 100%; Manual % is derived as the remainder.
- Weighted Time Saved = (Touchless % × Touchless Time Saved %) + (Reviewed % × Reviewed Time Saved %); Manual is assumed 0% time saved by default.
- Recovered Hours = Baseline Hours × Weighted Time Saved.
- Accuracy Gate: If Expected Accuracy < Minimum Accuracy, recovered hours (and dollars) are set to 0.
- Ramp: Month 1/2/3+ recovered hours are the steady recovered hours multiplied by the ramp percentages.
- FTE Capacity = Recovered Hours ÷ 160 hours per FTE-month; Annual Cost = Recovered Hours × Hourly Cost × 12.
- Assumptions are conservative; recovered capacity ≠ guaranteed headcount reduction.
