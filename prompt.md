# Goal
Create a production-ready ROI calculator that looks/behaves like HubSpot’s Marketing ROI calculator UI, but uses the typography + color palette of https://aiforfinanceteams.com/.
Reference layout inspiration: https://www.hubspot.com/roi-calculator/marketing
Brand style source: https://aiforfinanceteams.com/

# New instruction (output target)
- Generate the entire ROI calculator (HTML + CSS + JavaScript, including HubSpot form embed + hidden-field wiring) as a SINGLE self-contained file named:
  - new_calculator.html
- The deliverable must be the full contents of new_calculator.html (ready to paste/save as-is).

# Non-negotiables
- Use plain HTML/CSS/JavaScript (no React, no build step).
- The output must be a single drop-in HTML file that can be used in a HubSpot Landing Page HTML module.
- Include a HubSpot form embed (hbspt.forms.create) and populate hidden fields with calculator outputs.
- Responsive: 2-column desktop, 1-column mobile.
- Accessibility: labels, focus states, keyboard navigation, aria-live for result updates.

# Visual/UX Requirements (match HubSpot calculator structure)
Implement the same overall experience and information architecture as the HubSpot marketing ROI calculator:
- A top header and short explainer text.
- A left-side “Your Settings” input section with grouped fields (like “Your Marketing Settings”).
- A right-side “Results Summary” panel with:
  - A prominent headline metric (“Your return on investment” style) and secondary stats.
  - A breakdown section with 4–6 compact metric tiles (e.g., “Hours saved”, “Annual net savings”, “ROI %”, “Payback”, etc.).
  - A primary CTA button in the results area: “Download your ROI report” / “Email me my ROI report”.
- The results panel should be visually elevated (card), and on desktop should remain visible (sticky) while scrolling inputs.
- Results should update live as inputs change, with sensible placeholders when values are missing.

# Typography + Color Requirements (match aiforfinanceteams.com)
You must match fonts and colors to https://aiforfinanceteams.com/:
1) Inspect the site in a browser (view computed styles and CSS). Determine:
   - Primary font family stack used for headings and body.
   - Primary text color, background color, muted text, border color, and primary accent color(s).
   - Button styles (radius, border, fill, hover) and card styles (radius, shadow).
2) Recreate those values as CSS custom properties in new_calculator.html, e.g.:
   :root {
     --font-sans: ...;
     --bg: ...;
     --surface: ...;
     --text: ...;
     --muted: ...;
     --border: ...;
     --accent: ...;
     --accent-2: ...; (if used)
     --radius: ...;
     --shadow: ...;
   }
3) Apply them consistently across inputs, cards, buttons, and typography.
4) If the brand font is loaded via a hosted font file, include the same <link> or @font-face in new_calculator.html (only if publicly accessible); otherwise choose the closest system fallback and document the discrepancy.

# Calculator Model (finance ROI)
Inputs (with defaults):
- monthly_transactions (number, default 3000)
- minutes_per_transaction (number, default 2.5)
- fully_loaded_hourly_cost (number, default 65)
- automation_coverage_percent (0–100, default 60)
- tool_cost_monthly (number, default 1200)

Outputs:
- hours_saved_monthly = monthly_transactions * minutes_per_transaction * (coverage/100) / 60
- labor_savings_monthly = hours_saved_monthly * fully_loaded_hourly_cost
- net_savings_monthly = labor_savings_monthly - tool_cost_monthly
- annual_net_savings = net_savings_monthly * 12
- roi_percent_annual = (annual_net_savings / (tool_cost_monthly*12)) * 100  (handle divide-by-zero)
- payback_months = tool_cost_monthly / net_savings_monthly (if net_savings_monthly > 0 else “No payback”)

Behavior:
- Validate: no negatives; coverage 0–100.
- Formatting: currency in USD by default; compact separators; ROI as whole %; payback with 1 decimal.
- States: if net_savings_monthly <= 0, show warning copy and “No payback”.

# HubSpot Form Embed + Hidden Fields
In new_calculator.html, embed a HubSpot form directly below the results or in a “Get the report” section.
Use this embed pattern:

<script charset="utf-8" type="text/javascript" src="//js.hsforms.net/forms/v2.js"></script>
<div id="roi-hs-form"></div>
<script>
  hbspt.forms.create({
    region: "na1",
    portalId: "REPLACE_ME",
    formId: "REPLACE_ME",
    target: "#roi-hs-form",
    onFormReady: function($form) { ... },
    onFormSubmit: function($form) { ... }
  });
</script>

Hidden field internal names (must be configurable at the top of the JS as constants):
- roi_hours_saved_monthly
- roi_annual_net_savings
- roi_roi_percent
- roi_payback_months
- roi_inputs_json

Implementation details:
- Maintain a single `state` object of inputs + computed outputs.
- On every calculation, update:
  - The visible results UI
  - Hidden form fields (if the form exists)
- In onFormReady: populate hidden fields immediately.
- In onFormSubmit: re-populate hidden fields one last time to ensure HubSpot captured latest values.

Also:
- Add a “Get my ROI report” button that scrolls smoothly to the form section and focuses the first form input.

# Deliverable
- Output ONLY the full contents of a single file named new_calculator.html.
- new_calculator.html must include:
  - All HTML markup
  - Embedded CSS in a <style> tag
  - Embedded JavaScript in a <script> tag
  - HubSpot forms v2 embed + create call (with REPLACE_ME placeholders)

# Setup notes (at top of file as HTML comments)
Include a short setup note listing what must be replaced:
- portalId, formId, region
- hidden field internal names (if different)

# Testing checklist (at bottom as HTML comments)
- Desktop sticky results
- Mobile layout
- Hidden fields populated
- Submit creates contact and stores values

# Constraints
- No external dependencies (except HubSpot forms v2 script and a publicly accessible brand font link if required).
- Avoid heavy animations; match the clean, premium vibe of the brand site.
- Do not copy HubSpot’s exact content; only replicate layout patterns and interaction design.