import urllib.request
import json

def fetch_report():
    try:
        req = urllib.request.Request('http://localhost:8803/investment-ai-agent-intent/report')
        with urllib.request.urlopen(req) as response:
            data = response.read().decode()
            with open("report_output_8803.txt", "w", encoding="utf-8") as f:
                f.write(f"STATUS: {response.status}\n\n")
                f.write(data)
    except urllib.error.HTTPError as e:
        with open("report_output_8803.txt", "w", encoding="utf-8") as f:
            f.write(f"STATUS: {e.code}\n\n")
            f.write(e.read().decode())
    except Exception as e:
        with open("report_output_8803.txt", "w", encoding="utf-8") as f:
            f.write(f"ERROR: {str(e)}\n")

if __name__ == "__main__":
    fetch_report()
