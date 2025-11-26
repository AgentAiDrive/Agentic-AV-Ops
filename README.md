<img width="120" height="89" alt="ipav_agentic av -blue" src="https://github.com/user-attachments/assets/00c68a1d-224f-4170-b44f-9982bf4b5e8d" />
**Agentic AV Ops is designed to  provides a suite of features for creating AI-driven operational workflows converting SOP's using NLP, into agentic recipes exectued by Agents through MCP's and the IPAV framework.**

Go to Runbook.md to view the user manual explaining each feature page and how to use it, step by step. (The features correspond to the pages in the app’s sidebar navigation.)

**Agentic AV Ops** Streamlit Application

Agentic AV Ops - SOP Workflow Orchestration
🏁 Setup Wizard
💬 Chat
🤖 Agents
📜 Recipes
🧰 MCP Tools
⚙️ Settings
🧩 Workflows
🧩 Fixed Workflows (IPAV Orchestrator)
📊 Dashboard
❓ Help & Runbook
🧩 Orchestrator — Multi-Agent / Multi-Recipe
🔎 Run Details
🧪 Prompt Generator
💬 Persona Chat
⚡ Generate a Agent Workflow Shortcut from a SOP
**Try Demo Now:**
https://agentic-workflows.streamlit.app/
**Do NOT Save Keys in Online Demo!**

# Help & Getting Started

Welcome! This app lets you work with AI “agents” to help with AV/IT and operations tasks.

You can:

- Chat with specialized AI helpers (personas)
- Run repeatable workflows (health checks, reports, triage flows)
- Turn SOPs into one-click shortcuts
- See what has been run and whether it succeeded

You do **not** need to be a programmer to use this app.

---

## Table of Contents

- [Core Ideas](#core-ideas)
  - Persona / Agent  
  - Recipe  
  - Workflow  
  - Tools (MCP Tools)  
  - Runs & Run Detail  

- [Page-by-Page Guide](#page-by-page-guide)
  - Home (App)  
  - Setup Wizard  
  - Orchestrator  
  - Chat  
  - Chat Persona  
  - Agent Persona & Profile Builder  
  - Prompt Generator  
  - Shortcuts from SOP  
  - Agents (Catalog)  
  - Recipes  
  - MCP Tools  
  - Workflows (Builder)  
  - Fixed Workflows  
  - Dashboard  
  - Run Detail  
  - Settings  
  - Help  

---

## Core Ideas

<details>
<summary><strong>Persona / Agent</strong></summary>

A persona (or agent) is an AI “character” with a specific job.

- **Role** – who they are (e.g., “AV Triage Agent”, “Rollout Planner”).
- **Domain** – what they know and focus on (AV, IT, events, etc.).
- **Tone** – how they talk (formal, friendly, concise, bilingual, etc.).
- **Tools** – what systems they can use (ticketing, doc search, monitoring).
- **Constraints / guardrails** – important rules they must follow.

Saved personas can be reused in:

- **Chat** (choose who you’re talking to)
- **Chat Persona** (default persona for new chats)
- **Prompt Generator** (source persona for prompt patterns)
- **Orchestrator & Workflows** (steps that “use persona X”)

Personas make the AI behave **consistently** across the app.
</details>

---

<details>
<summary><strong>Recipe</strong></summary>

A recipe is a **multi-step AI playbook**.

- Defines **what steps happen and in what order**.
- Typical pattern: **collect data → analyze → summarize → draft output**.
- Each step can use a **persona** and/or **tools**.
- Recipes can be:
  - Run on their own, or
  - Used inside **Workflows** or **Orchestrator** as building blocks.
- They help you turn frequent tasks into **one-click, repeatable processes**.

Example: `Weekly AV Health Check` recipe  
1. Collect room metrics  
2. Identify rooms with issues  
3. Summarize findings  
4. Draft email to stakeholders  
</details>

---

<details>
<summary><strong>Workflow</strong></summary>

A workflow is a **complete process** built on personas, tools, and recipes.

- Starts with **inputs** (room name, list of rooms, date range, event details).
- Runs **ordered steps** that may:
  - Use personas
  - Call tools
  - Run recipes
- May include **conditional logic** (e.g., if issues found → run extra checks).
- Every run of a workflow is tracked as a **Run**.

There are also **Fixed Workflows**:

- Ready-made, “locked-down” workflows
- Most users **just run them**, they don’t edit them
</details>

---

<details>
<summary><strong>Tools (MCP Tools)</strong></summary>

Tools are **connections to external systems**.

Examples:

- Ticketing systems (e.g., incident/issue tracking)
- Monitoring dashboards or AV telemetry
- Document search / knowledge bases

Key points:

- Tools have **config and status** (connected / error / not configured).
- Personas, Recipes, and Workflows can **call tools behind the scenes**.
- If a tool is misconfigured, steps that depend on it will **fail**.
- The MCP Tools page is where you **see and manage these integrations**.
</details>

---

<details>
<summary><strong>Runs & Run Detail</strong></summary>

Every time you start a **workflow, recipe, or orchestrated task**, you create a **Run**.

- Runs have:
  - Name
  - Time started
  - Who started it (if tracked)
  - Overall status (success / failure)
- The **Dashboard** shows:
  - Number of runs over time
  - Success vs failures
  - Most-used workflows/recipes
- **Run Detail** drills into **one run**:
  - Step-by-step inputs and outputs
  - Tool calls and results

Use Runs and Run Detail to:

- Understand what actually happened
- Debug failures
- Improve personas, recipes, and workflows
</details>

---

## Page-by-Page Guide

<details>
<summary><strong>Home (App)</strong></summary>

The Home page is your **starting point**.

You can:

- Launch the **Setup Wizard** if you are new.
- Open **Orchestrator** for structured, multi-step tasks.
- Open **Chat** to talk to an AI helper.
- Open the **Dashboard** to see what has been running.

Use this page as your **orientation hub**: “Where do I go next?”
</details>

---

<details>
<summary><strong>Setup Wizard</strong></summary>

The Setup Wizard guides you through **initial configuration**.

You typically:

- Add any required **API keys or credentials**.
- Choose **default models**.
- Pick a **default persona** for Chat/Orchestrator.
- Turn **tools on or off** so only configured tools are used.

If you are new, start here.  
A completed Setup Wizard makes the rest of the app work smoothly.
</details>

---

<details>
<summary><strong>Orchestrator</strong></summary>

The Orchestrator is **mission control** for complex tasks.

You can:

- Describe your goal in **plain language**  
  e.g., “Create a weekly AV health report for all rooms.”
- (Optional) Pick a **persona** to lead the work.
- (Optional) Choose a **recipe or workflow template** to structure the steps.
- Click **Run** to watch the system execute each step.

The Orchestrator can:

- Call tools (ticketing, doc search, monitoring)
- Run recipes
- Produce final outputs like reports, plans, or summaries

Every orchestrated run shows up in **Dashboard** and **Run Detail**.
</details>

---

<details>
<summary><strong>Chat</strong></summary>

The Chat page is a **conversational interface** for working with a persona.

You can:

- **Select a persona** (e.g., “AV Triage Agent”).
- Type **questions or tasks** in plain English.
- Use **Shortcuts** (one-click prompts) if they are configured.
- Attach **documents** (if enabled) so the AI can read them.

Examples:

- “We had echo in Room 3 yesterday at 2pm. Help me figure out why.”
- “Here is an SOP; turn it into a short checklist.”

Use Chat for **ad-hoc help**, smaller tasks, and quick experiments before turning them into recipes or workflows.
</details>

---

<details>
<summary><strong>Chat Persona</strong></summary>

The Chat Persona page controls **which persona is used by default** in Chat.

You can:

- Select one **saved persona** as your default Chat persona.
- Have every new chat **start with this persona pre-selected**.

Example:

- Set **“AV Triage Agent”** as the default so all new chats start in troubleshooting mode.

You can still change personas **per chat** if needed.
</details>

---

<details>
<summary><strong>Agent Persona & Profile Builder</strong></summary>

This page is where you **create and edit personas (agents)**.

You fill in:

- **Name** – e.g., “AV Triage Agent”
- **Role** – who they are (job description)
- **Domain** – what they are expert in
- **Tone** – how they speak (e.g., calm, concise, friendly)
- **Tools** – what they are allowed to use
- **Constraints / rules** – what they must or must not do

The app turns these into a **structured system prompt** so the AI behaves reliably.

Saved personas appear in:

- **Chat** (persona picker)
- **Chat Persona** (default persona selection)
- **Prompt Generator** (to generate persona-specific prompts)
- **Workflows & Orchestrator** (steps that use that persona)

Personas let you build a **library of specialized AI helpers**.
</details>

---

<details>
<summary><strong>Prompt Generator</strong></summary>

The Prompt Generator helps you create **high-quality prompts** without being a prompt expert.

You can:

- Pick a **persona** (e.g., AV Triage Agent).
- Choose a **task type**:
  - Summarize
  - Troubleshoot
  - Draft email
  - Checklist
  - And more
- Add **extra context** (room, incident, audience, etc.).
- Click **Generate Prompt** to get a well-structured prompt text.

You can then:

- **Copy** the prompt into Chat, Orchestrator, or another tool.
- **Save** the prompt as a **Shortcut**, so it becomes a one-click button in Chat and Workflows.

Example: Generate a standard **“incident intake questions”** prompt for your AV Triage Agent.
</details>

---

<details>
<summary><strong>Shortcuts from SOP</strong></summary>

This page turns **long SOPs into one-click shortcuts**.

You can:

- Paste or upload an **SOP** (text or document).
- Choose a **persona** that will use the shortcuts.
- Select the **shortcut style**:
  - Checklist
  - Decision flow
  - Summary
  - Other formats
- Click **Generate Shortcuts** to create multiple reusable prompts.
- Review, edit, and **save** the generated shortcuts.

Saved shortcuts:

- Show up as **buttons in Chat** for the selected persona.
- Can be wired into **Workflows** as reusable steps.

This helps you turn static documents into **live, actionable tools**.
</details>

---

<details>
<summary><strong>Agents (Catalog)</strong></summary>

The Agents (Catalog) page shows **all saved personas**.

You can:

- See agents’ **names, descriptions, and domains** at a glance.
- **Open** an agent to edit its profile.
- **Duplicate** an agent to create variants (e.g., a Spanish-language version).
- **Delete** agents (if allowed) to keep the catalog tidy.

Think of this as the **central library** of AI helpers used across the app.
</details>

---

<details>
<summary><strong>Recipes</strong></summary>

The Recipes page lists all **multi-step AI playbooks**.

You can:

- See each recipe’s **name, description, and step count**.
- **Inspect steps** to understand how the process runs.
- Often **run a recipe directly** from this page.
- Link a recipe into:
  - **Orchestrator** runs
  - **Workflows** as steps

Use this page to manage the **building blocks** of your automation.
</details>

---

<details>
<summary><strong>MCP Tools</strong></summary>

The MCP Tools page manages **integrations with external systems**.

You can:

- See which **tools** are available (ticketing, monitoring, doc search, etc.).
- View each tool’s **status** (connected / misconfigured / missing config).
- Enter or update **configuration details** (URLs, keys, accounts).
- Quickly identify why certain steps or workflows may be **failing** (tool issues).

This is the place to ensure your **integrations are healthy** before running workflows that rely on them.
</details>

---

<details>
<summary><strong>Workflows (Builder)</strong></summary>

The Workflows (Builder) page lets you design **end-to-end processes**.

You can:

- Define **input fields** (room name, list of rooms, date range, incident ID, etc.).
- Add **steps**:
  - Use a persona
  - Run a recipe
  - Call an MCP tool
  - Generate a report or summary
- Save workflows for **repeated use** by yourself or your team.
- Test workflows and refine them based on Run results.

Example: Build a **“VIP Event Support Plan”** workflow that:

1. Checks key rooms and devices  
2. Generates checklists for onsite techs  
3. Drafts comms for stakeholders  
</details>

---

<details>
<summary><strong>Fixed Workflows</strong></summary>

Fixed Workflows are **ready-made, locked-down workflows**.

They are designed for **everyday use**:

- Users typically **select a workflow**, enter a few inputs, and **click Run**.
- Steps and logic are **pre-defined** by admins or power users.

Common examples:

- **Standard Room Health Check**
- **New Room Onboarding**
- **Post-Incident Review**

Most users never edit these— they just **run them and review the outputs**.  
Each run shows on the **Dashboard** and in **Run Detail**.
</details>

---

<details>
<summary><strong>Dashboard</strong></summary>

The Dashboard gives a **high-level view** of how automation is being used.

You can see:

- Number of **runs over time**.
- **Success vs failure** rates.
- **Most-used** workflows and recipes.
- A list of **recent runs** with links to Run Detail.

Use the Dashboard to answer questions like:

- “Are people actually using these workflows?”
- “Where are failures happening?”
- “Which automations provide the most value?”
</details>

---

<details>
<summary><strong>Run Detail</strong></summary>

Run Detail focuses on **one specific run** (workflow, recipe, or orchestrated task).

You can see:

- **Summary**: name, time, initiator, overall status.
- **Step-by-step details**:
  - Inputs and outputs
  - Any tool calls and their results

Use Run Detail to:

- Understand **why a run succeeded or failed**.
- Debug weird behavior or errors.
- Improve **personas, recipes, and workflows** based on real data.
</details>

---

<details>
<summary><strong>Settings</strong></summary>

The Settings page controls **global configuration** for the app.

You can:

- Update **API keys** and **models** after initial setup.
- Change the **default persona** used across Chat/Orchestrator.
- Adjust other **global preferences** (if available).

If something changes at the platform level (e.g., new key, new model),  
this is where you **update it**.
</details>

---

<details>
<summary><strong>Help</strong></summary>

You’re here. 🎉

Use the Help page when you want:

- A quick **reminder** of what a concept means (persona, recipe, workflow, tools, runs).
- A simple explanation of **what each page does**.
- Guidance on **where to go next**:
  - New user? → **Setup Wizard** → **Fixed Workflows** → **Chat**
  - Power user? → **Agent Persona**, **Recipes**, **Workflows (Builder)**

Come back here anytime you need a **refresher or orientation**.
</details>
