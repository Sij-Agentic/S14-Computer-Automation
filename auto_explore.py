import os
import sys
import subprocess
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Path to your application executable
APP_PATH = 'C:/Program Files/VideoLAN/VLC/vlc.exe'
APP_NAME = "vlc"

from utils.fdom.config_manager import ConfigManager

# Step 1: Create initial fDOM structure
print("Step 1: Creating initial fDOM structure...")
subprocess.run(["python", "-m", "utils.fdom.fdom_creator", APP_PATH])

# Step 2: Use manual-click mode for automation
print("Step 2: Starting manual click mode...")
process = subprocess.Popen(
    ["python", "-m", "utils.fdom.element_interactor", "--app-name", APP_NAME, "--manual-click"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1  # Line buffered
)

# Read and display output
for i in range(50):
    # Select node by index (starting with 0)
    print(f"Selecting node {i}/50...")
    process.stdin.write(f"{i}\n")
    process.stdin.flush()
    
    # Wait for interaction to complete
    time.sleep(5)
    
    # Read output
    while True:
        output = process.stdout.readline()
        if not output.strip():
            break
        print(output.strip())

# Exit the process
process.stdin.write("\n")
process.stdin.flush()

print("Auto-exploration complete! Check the fDOM results in apps/" + APP_NAME + "/")
