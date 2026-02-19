# codex_mcp_agents_sdk_demo.py
import argparse
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_api
from agents.mcp import MCPServerStdio


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run agent with an optional prompt file.")
    parser.add_argument(
        "--prompt-path",
        default=os.getenv("PROMPT_PATH", "prompt.md"),
        help="Path to a prompt markdown file (default: PROMPT_PATH env or prompt.md).",
    )
    args = parser.parse_args()

    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY. Put it in a .env file or your environment.")

    set_default_openai_api(api_key)

    async with MCPServerStdio(
        name="Codex CLI",
        params={
            "command": "npx",
            "args": ["-y", "@openai/codex", "mcp-server"],
        },
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        dev_agent = Agent(
            name="Dev Agent",
            instructions=(
                "You are a careful software engineer.\n"
                "Use the Codex MCP tool to do the work.\n"
                "When calling codex, set approval-policy to 'never' and sandbox to 'workspace-write'.\n\n"
                "Workflow:\n"
                "- Use the provided prompt to generate/update `new_calculator.html` via Codex.\n"
                "- Ensure the file on disk is the source of truth for the final output.\n"
            ),
            handoff_description="Implements the requested HTML and applies design feedback.",
            mcp_servers=[codex_mcp_server],
        )

        design_agent = Agent(
            name="Design Agent",
            instructions=(
                "You are a design QA agent.\n"
                "Verify the implementation satisfies the design requirements in the provided prompt.\n"
                "Only return STATUS: OK if ALL of the following are true:\n"
                "- The entire page background color is exactly #000.\n"
                "- All text color is exactly #fff.\n"
                "- Button backgrounds are exactly:\n"
                "  linear-gradient(270deg, rgb(208, 255, 0) 0%, "
                "rgb(212, 255, 31) 106%, rgb(255, 255, 255) "
                "114.77147016011644%, var(--token-df95533b-9397-4d55-a4ec-0858bad08d10, "
                "rgb(217, 255, 47)) 243.00000000000003%)\n"
                "- Header text uses Instrument Serif.\n"
                "- All body text uses Instrument Sans.\n"
                "- Button text uses Space Grotesk.\n"
                "- Button text color is exactly #000.\n"
                "If issues are found, respond with a line starting exactly:\n"
                "STATUS: NEEDS_CHANGES\n"
                "Then list the issues as bullet points, and a short 'Suggested fix' section.\n"
                "After that, hand off to the Dev Agent with the feedback.\n\n"
                "If everything is satisfied, respond with:\n"
                "STATUS: OK\n"
                "and a one-paragraph confirmation.\n"
            ),
            handoff_description="Reviews HTML against the prompt and returns OK or needed changes.",
        )

        dev_agent.handoffs = [design_agent]
        design_agent.handoffs = [dev_agent]

        prompt_path = Path(args.prompt_path)
        prompt_text = prompt_path.read_text(encoding="utf-8")

        max_passes = int(os.getenv("DESIGN_REVIEW_MAX_PASSES", "5"))
        current_prompt = prompt_text

        for pass_index in range(1, max_passes + 1):
            dev_result = await Runner.run(dev_agent, current_prompt)
            print(f"\n=== Dev agent result (pass {pass_index}) ===")
            print(dev_result.final_output)

            html_path = Path("new_calculator.html")
            if html_path.exists():
                html_text = html_path.read_text(encoding="utf-8")
            else:
                raise FileNotFoundError(
                    "new_calculator.html not found. The dev agent must generate it before review."
                )

            design_review_prompt = (
                "Review the HTML file content below against the prompt.\n\n"
                "PROMPT:\n"
                f"{prompt_text}\n\n"
                "HTML FILE CONTENTS:\n"
                f"{html_text}\n"
            )
            design_result = await Runner.run(design_agent, design_review_prompt)
            print(f"\n=== Design agent result (pass {pass_index}) ===")
            print(design_result.final_output)

            if "STATUS: OK" in (design_result.final_output or ""):
                break

            current_prompt = (
                "Update `new_calculator.html` to address the design feedback below.\n\n"
                "PROMPT:\n"
                f"{prompt_text}\n\n"
                "DESIGN FEEDBACK:\n"
                f"{design_result.final_output}\n"
            )
        else:
            print(
                f"\n=== Max passes reached ({max_passes}) ===\n"
                "Design requirements are still not satisfied. "
                "Review the last design feedback and increase DESIGN_REVIEW_MAX_PASSES if needed."
            )


if __name__ == "__main__":
    asyncio.run(main())
