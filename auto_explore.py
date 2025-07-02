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

# Step 2: Launch interactive exploration
print("Step 2: Starting interactive exploration...")
process = subprocess.Popen(
    ["python", "-m", "utils.fdom.element_interactor", "--app-name", APP_NAME, "--interactive"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Step 3: Send "-1" to start auto-exploration
print("Step 3: Triggering auto-exploration...")
process.stdin.write("-1\n")
process.stdin.flush()

# Step 4: Wait for auto-exploration to complete (50 iterations)
print("Step 4: Waiting for exploration to complete")
# The exploration will run for 50 iterations

# Step 5: Send Enter to continue after auto-exploration completes
# Wait for the 50 iterations to complete
# This timing depends on your application and computer speed
time.sleep(300)
process.stdin.write("\n")
process.stdin.flush()

# Step 6: Send "quit" to exit interactive mode
process.stdin.write("quit\n")
process.stdin.flush()

# Wait for process to complete
print("Step 6: Finishing up...")
process.wait()

print("Auto-exploration complete! Check the fDOM results in apps/" + APP_NAME + "/")
