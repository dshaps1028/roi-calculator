# ROI Calculator + Agent Orchestration

This repo contains:
- `new_calculator.html`: the current ROI calculator (single-file HTML/CSS/JS) with a HubSpot form in a modal.
- `calculator.html`: the legacy calculator.
- `agent.py`: an Agents SDK workflow that uses the Codex MCP server to generate/update `new_calculator.html` and a design QA agent to review it.
- `prompt.md`: the prompt used by the dev agent for generation.

## Quick Start (Calculator)
Open `new_calculator.html` in a browser. It runs entirely client-side.

### Inputs (Current Model)
- Industry (dropdown)
- Role (dropdown)
- Number of days to close the books
- Hours spent on manual work
- In-house bookeeper salary
- Yearly outsourced cost
- Number of finance & accounting FTEs
- No of Accounting Employees

### Outputs (Current Labels)
- Days of Close Eliminated
- Manual Reconciliation Hours Saved
- Annual Labor Cost Savings
- Outsourced Cost Savings
- Finance Capacity Unlocked

### Calculation Notes (Current State)
- Days of Close Eliminated = `days_to_close * 0.65`
- Manual Reconciliation Hours Saved = `manual_work_hours * 0.65 * finance_fte`
- Annual Labor Cost Savings = `min((yearly_inhouse_cost * finance_fte) * 0.6, (hours_saved_monthly * 12 * yearly_inhouse_cost) / 2080)`
- Outsourced Cost Savings = `yearly_outsourced_cost * 0.6`
- Finance Capacity Unlocked = `annual_labor_cost_savings`
- Estimated Annual Net Savings = `annual_labor_cost_savings + outsourced_cost_savings`
- ROI % = `annual_net_savings / current_annual_finance_spend`
- Blank `yearly_inhouse_cost` and `yearly_outsourced_cost` stay as placeholders until entered; blank `finance_fte` defaults to `1`

## HubSpot Form
The form is embedded in a modal that opens when the user clicks **Get my ROI report**.  
The form container lives in `new_calculator.html` near the bottom and is created by `createHsForm()`:
- Update `region`, `portalId`, and `formId`.
- Hidden field internal names are configured in the `HS_FIELDS` map.

## Agent Workflow (agent.py)
`agent.py` uses the OpenAI Agents SDK and the Codex MCP server:
- **Dev Agent**: generates/updates `new_calculator.html` via Codex.
- **Design Agent**: reviews `new_calculator.html` against the prompt and returns `STATUS: OK` or `STATUS: NEEDS_CHANGES`.
- The loop repeats until requirements are met or `DESIGN_REVIEW_MAX_PASSES` is reached.

### Run the Agent
1) Create `.env` with your OpenAI API key:
```
OPENAI_API_KEY=REPLACE_ME
```
2) Install dependencies:
```
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install openai-agents python-dotenv
```
3) Run:
```
python agent.py --prompt-path prompt.md
```

### MCP Server Note
`agent.py` launches the Codex MCP server using:
```
npx -y @openai/codex mcp-server
```

## Environment + Git Hygiene
Add `.env` to `.gitignore` to avoid committing secrets.  
If a push is blocked, remove the secret from commits and rotate your key.
