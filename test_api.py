import urllib.request
import urllib.error
import json

def test_api():
    try:
        req = urllib.request.Request('http://localhost:8802/investment-ai-agent-intent/report')
        with urllib.request.urlopen(req) as response:
            print("Status code:", response.status)
            data = json.loads(response.read().decode())
            print(data)
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code)
        error_body = e.read().decode()
        print("Error Body:", error_body)
    except Exception as e:
        print("Other Error:", e)

if __name__ == "__main__":
    test_api()
