# Installation

## Choose a package

- Use the Plugin ZIP to install all six Skills where Skills-only Plugins are supported.
- Use the standalone Skill ZIP when the host accepts an uploaded Skill directory.
- Use the Manual Mode ZIP when Skill or Plugin installation is unavailable.
- Use the repository marketplace for local Codex development and inspection.

Open source and free download do not imply identical installation, browsing, execution, or data features across plans, regions, surfaces, workspaces, and admin policies.

## GitHub repository marketplace

Add the public repository as a marketplace, then install the Plugin:

```text
codex plugin marketplace add dennis542868487-create/business-feasibility-research-guidelines
codex plugin add business-feasibility-research-guidelines@business-feasibility-research-guidelines
```

For local development, clone or download the repository and replace the GitHub identifier with the absolute path to its root. Restart the ChatGPT desktop app, open the Plugins Directory, choose the marketplace source, and install `business-feasibility-research-guidelines`.

To inspect configured marketplaces:

```text
codex plugin marketplace list
```

The repository marketplace is `.agents/plugins/marketplace.json`; its Plugin source is `./plugins/business-feasibility-research-guidelines` relative to the repository root.

## Plugin ZIP

Build releases with:

```text
python3 scripts/build_release_packages.py
```

Use `releases/business-feasibility-research-guidelines-plugin.zip`. The archive contains one Plugin root with `.codex-plugin/plugin.json`, `skills/`, and presentation assets. It contains no MCP server or app configuration.

Public Plugin Directory submission is a separate process and requires the current OpenAI submission portal, verified publisher identity, production listing information, starter prompts, and test cases.

## Standalone Skill

Use `releases/business-feasibility-research-guidelines-standalone-skill.zip`. Upload or install the contained `business-feasibility-research-guidelines` Skill through the host's supported Skill interface.

The standalone package is complete: it includes the core instructions, detailed references, calculation scripts, report validator, and output templates. It does not depend on the five auxiliary Skills.

Personal Skills may need to be added separately on different ChatGPT surfaces and might not synchronize automatically. Follow the current host documentation.

## Manual Mode

Unzip `releases/business-feasibility-research-guidelines-manual-mode.zip` and provide `manual-mode.md` to the agent. Upload only the templates or scripts needed for the task.

Manual Mode cannot add browsing or computation to a host. If the host lacks those tools, require a research plan, source-request list, or explicit uncalculated formulas.

## Verify an installation

Try:

```text
Use $business-feasibility-research-guidelines to create a research plan for a pre-launch local service. Do not invent demand or an investment budget.
```

Expected behavior:

- asks for or identifies the decision contract;
- distinguishes pre-launch evidence from operating history;
- declares unavailable capabilities;
- proposes paid-behavior validation and stop thresholds;
- does not guarantee success or provide an invented risk amount.

Official references:

- https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/build-plugins
- https://learn.chatgpt.com/docs/submit-plugins
