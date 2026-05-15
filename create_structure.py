import os

base_dir = r"C:\Users\phon\.gemini\antigravity\scratch\investment-ai-agent-research"

structure = {
    "": [
        "README.md", "PROJECT_BRIEF.md", "AGENTS.md", "ARCHITECTURE.md",
        "DATABASE_SCHEMA.md", "EVALUATION_PLAN.md", "SECURITY_RULES.md",
        ".env.example", "docker-compose.yml"
    ],
    "shared/database": ["db.py", "models.py", "init_db.py", "__init__.py"],
    "shared/schemas": ["chat_schema.py", "usage_schema.py", "billing_schema.py", "__init__.py"],
    "shared/monitoring": ["token_monitor.py", "cost_monitor.py", "latency_monitor.py", "__init__.py"],
    "shared/guardrails": ["compliance_rules.py", "financial_advice_rules.py", "__init__.py"],
    "project_1_investment_ai_agent/app": ["main.py", "__init__.py"],
    "project_1_investment_ai_agent/app/routes": ["chat.py", "__init__.py"],
    "project_1_investment_ai_agent/app/llm": ["single_llm_client.py", "__init__.py"],
    "project_1_investment_ai_agent/app/prompts": ["big_investment_prompt.py", "__init__.py"],
    "project_1_investment_ai_agent/tests": ["__init__.py"],
    "project_2_investment_ai_agent_intent/app": ["main.py", "__init__.py"],
    "project_2_investment_ai_agent_intent/app/routes": ["chat.py", "history.py", "dashboard.py", "__init__.py"],
    "project_2_investment_ai_agent_intent/app/router": [
        "intent_schema.py", "intent_classifier.py", "domain_router.py", "model_router.py", "token_policy.py", "__init__.py"
    ],
    "project_2_investment_ai_agent_intent/app/llm_gateway": ["openrouter_client.py", "model_registry.py", "usage_parser.py", "__init__.py"],
    "project_2_investment_ai_agent_intent/app/agents": [
        "orchestrator.py", "finance_education_agent.py", "market_snapshot_agent.py",
        "technical_agent.py", "fundamental_agent.py", "portfolio_risk_agent.py",
        "news_macro_agent.py", "suitability_agent.py", "compliance_agent.py", "__init__.py"
    ],
    "project_2_investment_ai_agent_intent/app/tools": ["market_data_tool.py", "technical_indicators.py", "portfolio_metrics.py", "__init__.py"],
    "project_2_investment_ai_agent_intent/tests": ["__init__.py"],
    "frontend": ["streamlit_app.py"],
    "frontend/pages": ["1_Chatbot.py", "2_Token_Dashboard.py", "3_Cost_Dashboard.py", "4_Chat_History.py", "5_Project_Comparison.py"],
    "eval": ["test_set_120.json", "run_project_1_eval.py", "run_project_2_eval.py", "compare_results.py"]
}

for folder, files in structure.items():
    dir_path = os.path.join(base_dir, folder.replace("/", "\\"))
    os.makedirs(dir_path, exist_ok=True)
    for file in files:
        file_path = os.path.join(dir_path, file)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                if file.endswith(".md"):
                    f.write(f"# {file.replace('.md', '')}\n")
                elif file.endswith(".json"):
                    f.write("{\n\n}")
                else:
                    f.write("")

print(f"Directory structure created successfully at: {base_dir}")
