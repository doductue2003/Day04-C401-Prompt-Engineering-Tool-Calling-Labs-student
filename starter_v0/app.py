from pathlib import Path
import streamlit as st

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from agent import ResearchAgent

ROOT = Path(__file__).parent
load_lab_env(ROOT)

MODEL_OPTIONS = {
    "gemini": ["gemini-2.5-flash", "gemini-3.5-flash"],
    "openai": ["gpt-4o-mini", "gpt-4.1-mini"],
    "openrouter": ["google/gemini-2.5-flash", "openai/gpt-4o-mini"],
    "anthropic": ["claude-3-5-haiku-latest", "claude-3-5-sonnet-latest"],
}

st.set_page_config(page_title="Research Agent", layout="wide")
st.title("Research Agent")

provider_name = st.selectbox("Provider", list(MODEL_OPTIONS.keys()))
model = st.selectbox("Model", MODEL_OPTIONS[provider_name])
query = st.text_area("User request", "Lay 3 tweet moi nhat cua Sam Altman")

if st.button("Run"):
    system_prompt = (ROOT / "artifacts" / "system_prompt.md").read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(ROOT / "artifacts" / "tools.yaml")
    openai_tools = to_openai_tools(tool_declarations)

    provider = make_provider(provider_name)
    agent = ResearchAgent(provider, system_prompt=system_prompt, tools=openai_tools, model=model)

    try:
        result = agent.run([{"role": "user", "content": query}])

        st.subheader("Assistant Text")
        st.write(result.text or "")

        st.subheader("Tool Calls")
        st.json([{"name": c.name, "args": c.args} for c in result.tool_calls])

        st.subheader("Tool Results")
        st.json(result.tool_results)
    except Exception as exc:
        st.error(f"{type(exc).__name__}: {exc}")