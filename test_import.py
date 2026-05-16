import traceback
import sys

try:
    from project_2_investment_ai_agent_intent.app.routes import history
    print("history.py imported successfully!")
except Exception as e:
    print("Failed to import history.py")
    traceback.print_exc()
