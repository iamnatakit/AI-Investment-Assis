import subprocess
import traceback

def check_db():
    try:
        # Check if docker is available
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        with open("docker_debug.txt", "w", encoding="utf-8") as f:
            f.write("=== DOCKER PS ===\n")
            f.write(result.stdout)
            f.write(result.stderr)
            f.write("\n\n")
            
        # Try to ping db container
        result2 = subprocess.run(
            ["docker", "exec", "scratch-db-1", "pg_isready", "-U", "user", "-d", "investment_chatbot"], 
            capture_output=True, text=True
        )
        with open("docker_debug.txt", "a", encoding="utf-8") as f:
            f.write("=== PG_ISREADY ===\n")
            f.write(result2.stdout)
            f.write(result2.stderr)
            
    except Exception as e:
        with open("docker_debug.txt", "a", encoding="utf-8") as f:
            f.write(f"\nERROR: {str(e)}\n{traceback.format_exc()}")

if __name__ == "__main__":
    check_db()
