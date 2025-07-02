import os
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import required modules
from utils.fdom.element_interactor import ElementInteractor
from utils.fdom.fdom_creator import FDOMCreator

# Configuration
APP_PATH = 'C:/Program Files/VideoLAN/VLC/vlc.exe'
APP_NAME = "vlc"
ITERATIONS = 50

def run_automated_exploration():
    """Run fully automated exploration without interactive prompts"""
    print(f"Starting automated exploration of {APP_PATH}")
    
    # Step 1: Create initial fDOM structure if needed
    app_folder = Path("apps") / APP_NAME
    if not app_folder.exists():
        print(f"Creating initial fDOM structure for {APP_NAME}...")
        creator = FDOMCreator()
        result = creator.create_fdom_for_app(APP_PATH)
        if not result.get("success", False):
            print(f"Failed to create fDOM: {result.get('error', 'Unknown error')}")
            return False
    else:
        print(f"App folder already exists: {app_folder}")
    
    # Step 2: Create element interactor
    print("Initializing element interactor...")
    interactor = ElementInteractor(APP_NAME)
    
    # Step 3: Explore nodes one by one
    explored_count = 0
    successful_count = 0
    
    print(f"Starting exploration of up to {ITERATIONS} nodes...")
    
    while explored_count < ITERATIONS:
        # Get list of pending nodes
        pending_nodes = list(interactor.state_manager.pending_nodes)
        
        if not pending_nodes:
            print("No more pending nodes to explore.")
            break
        
        # Get next node
        node_id = pending_nodes[0]
        
        # Get node info
        node_data = interactor._find_node_in_fdom(node_id)
        element_name = node_data.get('g_icon_name', 'unknown') if node_data else 'unknown'
        
        print(f"\n[{explored_count + 1}/{ITERATIONS}] Exploring: {element_name} ({node_id})")
        
        # Click the element
        try:
            result = interactor.click_element(node_id)
            
            if result.success:
                successful_count += 1
                if result.state_changed:
                    print(f"Success: State changed to {result.new_state_id}")
                else:
                    print(f"Success: Element marked as {result.interaction_type}")
            else:
                print(f"Failed: {result.error_message}")
            
            # Increment counter
            explored_count += 1
            
            # Small delay between explorations
            time.sleep(2)
            
        except Exception as e:
            print(f"Error exploring {node_id}: {e}")
            explored_count += 1
    
    # Print summary
    print("\n=== Exploration Summary ===")
    print(f"Total nodes explored: {explored_count}")
    print(f"Successful interactions: {successful_count}")
    print(f"Failed interactions: {explored_count - successful_count}")
    
    # Get final stats
    explored_total = len(interactor.state_manager.explored_nodes)
    pending_total = len(interactor.state_manager.pending_nodes)
    non_interactive_total = len(interactor.state_manager.non_interactive_nodes)
    
    print(f"\nFinal fDOM Statistics:")
    print(f"Explored nodes: {explored_total}")
    print(f"Pending nodes: {pending_total}")
    print(f"Non-interactive nodes: {non_interactive_total}")
    
    return True

if __name__ == "__main__":
    run_automated_exploration()
