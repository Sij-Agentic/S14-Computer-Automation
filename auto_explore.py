import os
import sys
import subprocess
import time
import threading
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
    text=True,
    bufsize=1  # Line buffered
)

# Function to continuously read output
def read_output(process):
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(f"OUTPUT: {line.strip()}")

# Start thread to read output
output_thread = threading.Thread(target=read_output, args=(process,))
output_thread.daemon = True
output_thread.start()

# Step 3: Explore 50 nodes by selecting them one by one
print("Step 3: Starting exploration of 50 nodes...")

# Wait for the interactive prompt to initialize
time.sleep(5)

# Explore 50 nodes
for i in range(50):
    # Always select the first node (number 1)
    print(f"Selecting node {i+1}/50...")
    process.stdin.write("1\n")
    process.stdin.flush()
    
    # Wait for the interaction to complete
    # This timing might need adjustment based on your application
    time.sleep(10)  # Wait 10 seconds between interactions

# Step 4: Send "quit" to exit interactive mode
print("Step 4: Finishing up...")
process.stdin.write("quit\n")
process.stdin.flush()

# Wait for process to complete
process.wait()

print("Auto-exploration complete! Check the fDOM results in apps/" + APP_NAME + "/")
