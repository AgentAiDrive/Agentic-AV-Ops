# Help & Getting Started
Welcome! This app lets you work with AI “agents” to help with AV/IT tasks:
- Chat with specialized AI helpers
- Run repeatable workflows (health checks, reports, triage flows)
- Turn SOPs into one-click shortcuts
- See what has been run and if it worked
You do **not** need to be a programmer to use this app.
---
## Core Ideas

### Persona / Agent
A **persona** (or agent) is an AI “character” with a specific job.
You define:
- **Role** – who they are  
- **Domain** – what they know  
- **Tone** – how they talk  
- **Tools** – what systems they can use  
- **Constraints** – important rules and guardrails

Once you save a persona, you can reuse it in:
- **Chat**
- **Prompt Generator**
- **Orchestrator**
- **Workflows / Recipes**
---

### Recipe
A **recipe** is a multi-step playbook.  
Example: `collect data → analyze → summarize → draft email`.
Recipes define **what steps happen and in what order**.
---

### Workflow
A **workflow** is a more complete process built on top of personas, tools, and recipes.
- Workflows ask for inputs (e.g., room name, date range).
- Then they run the right steps for you.
**Fixed Workflows** are official, locked-down workflows that most users simply **run**, not edit.
---

### Tools (MCP Tools)
Tools are **connections** to external systems, like:
- Ticketing systems
- Monitoring dashboards
- Document search
Agents and workflows call these tools behind the scenes.
---

### Runs & Run Detail
Every time you start a workflow/recipe/orchestrated task, that is a **run**.
- The **Dashboard** shows runs over time.
- **Run Detail** shows what happened in a single run, step by step.
---

## Page-by-Page Guide

### Home (App)
Your starting point.
Use it to:
- Run the **Setup Wizard** if you are new
- Open **Orchestrator** to run structured tasks
- Open **Chat** to talk to an AI helper
- Open **Dashboard** to see what has been running
---

### Setup Wizard
Guides you through initial setup, step by step.
Here you:
- Add any required **keys**
- Choose **default models**
- Pick a **default persona**
- Turn tools on or off
If you are new, start here.
---

### Orchestrator
Describe your **goal**, and the app coordinates personas, tools, and workflows.
1. Type what you want to achieve in normal language  
2. Optionally pick a **persona** and **recipe/workflow**  
3. Click **Run** and watch the steps execute
Examples:
- “Create a weekly AV health report for all rooms.”  
- “Prepare a rollout plan for upgrading AV in all branches.”
---

### Chat
Chat with a specialized AI helper.
You can:
- Select a **persona** (e.g., AV Triage Agent)  
- Type questions or tasks in plain English  
- Use **shortcuts** (one-click prompts)  
- Attach documents (if enabled)
Examples:
- “We had echo in Room 3 yesterday at 2pm. Help me figure out why.”  
- “Here is an SOP; turn it into a short checklist.”
---

### Chat Persona
Choose which persona is used **by default** when you open Chat.
- Set a default persona once
- Chat will start with that persona automatically
Example:
- Set “AV Triage Agent” as your default Chat persona.
---

### Agent Persona & Profile Builder
Define and save AI personas (agents).
You fill in:
- **Name** – e.g., “AV Triage Agent”  
- **Role** – who they are  
- **Domain** – what they know  
- **Tone** – how they speak  
- **Tools** – what they’re allowed to use  
- **Constraints** – important rules
The app turns your choices into a structured system prompt.
Saved personas are available in:
- **Chat**
- **Chat Persona**
- **Prompt Generator**
- **Workflows / Recipes / Orchestrator**
---

### Prompt Generator
Helps you build **good prompts** without being a prompt expert.
1. Pick a **persona**  
2. Choose a **task type** (summarize, troubleshoot, draft email, checklist, etc.)  
3. Click **Generate Prompt**  
4. Copy the prompt or save it as a **Shortcut**
Example:
- Generate a standard “incident intake questions” prompt for your AV Triage Agent.
---

### Shortcuts from SOP
Turn long SOPs into **one-click shortcuts**.
You:
- Paste or upload an SOP  
- Choose a persona and shortcut type (checklist, flow, summary, etc.)  
- Click **Generate Shortcuts**  
- Review and save the shortcuts
These shortcuts show up as buttons in **Chat** (for that persona) and can be used in **Workflows**.
---

### Agents (Catalog)
View and manage all saved personas.
You can:
- See all agents (name, description, domain)
- **Edit** an agent
- **Duplicate** an agent
- **Delete** an agent (if allowed)
Example:
- Duplicate “AV Triage Agent” to create “AV Triage Agent – Spanish” and adjust tone/language.
---

### Recipes
View and manage multi-step AI playbooks.
You can:
- See recipes (name, description, steps)
- Run a recipe directly
- Inspect how Orchestrator/Workflows are structured
Example:
- Recipe “Weekly AV Health Check”:
  1. Collect room metrics  
  2. Identify rooms with issues  
  3. Summarize findings  
  4. Draft email to stakeholders
---

### MCP Tools
View and configure connections to external systems.
You can:
- See which tools exist (ticketing, monitoring, doc search)
- Check their **status** (connected or not)
- Enter / update configuration details (if required)
If a tool is not configured, related workflow steps will fail.
---

### Workflows (Builder)
Design or customize multi-step processes.
You can:
- Define input fields (e.g., room name, date range)
- Add steps (use persona, call tool, run recipe)
- Save and test workflows
Example:
- Build a “VIP Event Support Plan” workflow that checks rooms, generates checklists, and drafts comms.
---

### Fixed Workflows
Ready-made, locked-down workflows for everyday use.
- Choose a workflow
- Click **Run**
- Follow any prompts
Examples:
- “Standard Room Health Check”  
- “New Room Onboarding”  
- “Post-Incident Review”
Most users only **run** these; they don’t edit them.
---

### Dashboard
Gives you a high-level overview of activity.
You see:
- Number of runs over time
- Success vs failures
- Most-used workflows/recipes
- Recent runs with links to **Run Detail**
Use it to see if automation is being used and where problems might be.
---

### Run Detail
Shows what happened in a single run, step by step.
You see:
- Run summary (name, time, status)
- Each step’s input and output
- Any tool calls and results
Use it to:
- Understand why a run succeeded or failed
- Improve personas, recipes, or workflows
---

### Settings
Adjust app-wide configuration after setup.
You can:
- Update keys and models
- Change default persona
- Tweak other global settings
If something changes at the platform level (key, model, etc.), update it here.
---

### Help
You’re here. 🎉

Use this page whenever you want:
- A quick reminder of what a concept means (persona, recipe, workflow, etc.)
- A simple explanation of what each page does
- Guidance on where to go next
