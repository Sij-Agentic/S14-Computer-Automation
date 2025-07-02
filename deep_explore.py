#!/usr/bin/env python3
"""
Deep Explorer - Comprehensive Application Analysis
Performs exhaustive exploration of applications including nested menus, dialogs, and deep UI hierarchies.
Goes far beyond surface-level analysis to discover all possible application states and functionality.
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn, TextColumn
from rich.tree import Tree
from rich.prompt import Confirm, Prompt, IntPrompt

# Import FDOM framework modules
from utils.fdom.element_interactor import ElementInteractor
from utils.fdom.fdom_creator import FDOMCreator
from utils.fdom.state_manager import StateManager
from utils.fdom.config_manager import ConfigManager

@dataclass
class ExplorationStrategy:
    """Configuration for exploration strategy"""
    max_depth: int = 10                    # Maximum exploration depth
    max_states_per_level: int = 50         # Maximum states to explore per depth level
    max_total_states: int = 500            # Maximum total states to explore
    backtrack_on_deadend: bool = True      # Whether to backtrack from dead ends
    explore_dialogs: bool = True           # Whether to explore dialog boxes
    explore_menus: bool = True             # Whether to explore menu systems
    explore_context_menus: bool = True     # Whether to right-click for context menus
    revisit_states: bool = False           # Whether to revisit already explored states
    safety_timeouts: bool = True           # Whether to use safety timeouts
    state_timeout: int = 30                # Timeout per state exploration (seconds)
    total_timeout: int = 7200             # Total exploration timeout (2 hours)

@dataclass
class ExplorationState:
    """Represents a discovered application state during exploration"""
    state_id: str
    depth: int
    parent_state: Optional[str]
    trigger_element: Optional[str]
    discovered_at: datetime
    element_count: int
    explored: bool = False
    is_deadend: bool = False
    is_dialog: bool = False
    is_menu: bool = False

class DeepExplorer:
    """
    Comprehensive application explorer that discovers all possible UI states and functionality
    """
    
    def __init__(self, app_executable_path: str, strategy: Optional[ExplorationStrategy] = None):
        self.console = Console()
        self.app_executable_path = app_executable_path
        self.strategy = strategy or ExplorationStrategy()
        
        # Initialize exploration tracking
        self.discovered_states: Dict[str, ExplorationState] = {}
        self.exploration_graph: Dict[str, List[str]] = defaultdict(list)  # state -> child states
        self.backtrack_stack: List[Tuple[str, str]] = []  # [(state_id, element_id)]
        self.exploration_queue: List[Tuple[str, int]] = []  # [(state_id, depth)]
        
        # Statistics tracking
        self.stats = {
            'total_states_discovered': 0,
            'total_elements_discovered': 0,
            'total_interactions': 0,
            'successful_interactions': 0,
            'failed_interactions': 0,
            'dialogs_discovered': 0,
            'menus_discovered': 0,
            'deadends_found': 0,
            'max_depth_reached': 0,
            'focus_failures': 0,
            'focus_recoveries': 0,
            'exploration_start_time': None,
            'exploration_end_time': None
        }
        
        # Initialize FDOM framework
        self.console.print(Panel(
            f"[bold]🚀 Deep Explorer Initializing[/bold]\n\n"
            f"🎯 Target: {Path(app_executable_path).name}\n"
            f"📊 Strategy: Max depth {self.strategy.max_depth}, Max states {self.strategy.max_total_states}\n"
            f"🔍 Features: Dialogs={self.strategy.explore_dialogs}, Menus={self.strategy.explore_menus}, Context={self.strategy.explore_context_menus}\n"
            f"⏱️ Timeouts: {self.strategy.state_timeout}s per state, {self.strategy.total_timeout//60}min total",
            title="🔬 Deep Application Explorer",
            border_style="green"
        ))
        
        # Initialize FDOM components
        self.fdom_creator = FDOMCreator()
        self.element_interactor = None
        self.state_manager = None
        
    def run_deep_exploration(self) -> Dict:
        """
        Execute comprehensive deep exploration of the application
        """
        self.stats['exploration_start_time'] = datetime.now()
        
        try:
            # Phase 1: Initialize application and FDOM
            self.console.print("\n[bold yellow]📋 PHASE 1: APPLICATION INITIALIZATION[/bold yellow]")
            if not self._initialize_application():
                return self._create_failure_result("Application initialization failed")
            
            # Phase 2: Discover initial state and build exploration queue
            self.console.print("\n[bold yellow]🔍 PHASE 2: INITIAL STATE DISCOVERY[/bold yellow]")
            if not self._discover_initial_state():
                return self._create_failure_result("Initial state discovery failed")
            
            # Phase 3: Execute depth-first exploration
            self.console.print("\n[bold yellow]🌊 PHASE 3: DEEP EXPLORATION[/bold yellow]")
            self._execute_deep_exploration()
            
            # Phase 4: Analysis and reporting
            self.console.print("\n[bold yellow]📊 PHASE 4: ANALYSIS AND REPORTING[/bold yellow]")
            return self._generate_exploration_report()
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]⚡ Exploration interrupted by user[/yellow]")
            return self._generate_exploration_report()
        except Exception as e:
            self.console.print(f"\n[red]❌ Exploration failed: {e}[/red]")
            return self._create_failure_result(str(e))
        finally:
            self.stats['exploration_end_time'] = datetime.now()
    
    def _initialize_application(self) -> bool:
        """Initialize the application and FDOM framework"""
        try:
            # STEP 1: Screen Selection
            screen_id = self.fdom_creator._handle_screen_selection()
            if not screen_id:
                self.console.print("[red]❌ Screen selection failed[/red]")
                return False
            
            # STEP 2: Launch Application  
            app_result = self.fdom_creator._launch_application(self.app_executable_path, screen_id)
            if not app_result["success"]:
                self.console.print(f"[red]❌ Failed to launch application: {app_result.get('error', 'Unknown error')}[/red]")
                return False
            
            # STEP 3: Initialize App-Specific Modules (loads existing fDOM if present)
            if not self.fdom_creator._initialize_app_modules():
                self.console.print("[red]❌ Failed to initialize app modules[/red]")
                return False
            
            # STEP 4: CONDITIONAL - Create Initial fDOM only if needed
            if len(self.fdom_creator.state_manager.fdom_data.get("states", {})) == 0:
                # Fresh run - create initial fDOM
                self.console.print(f"[yellow]🆕 Fresh session detected - creating initial fDOM[/yellow]")
                initial_state = self.fdom_creator._create_initial_fdom()
                if not initial_state["success"]:
                    self.console.print(f"[red]❌ Initial fDOM creation failed: {initial_state.get('error', 'Unknown error')}[/red]")
                    return False
            else:
                # Existing data - skip Step 4
                self.console.print(f"[green]♻️ Existing session detected - skipping fDOM creation[/green]")
            
            # STEP 5: SKIP THE INTERACTIVE EXPLORATION LOOP - we handle this ourselves
            self.console.print(f"[cyan]🤖 Skipping interactive mode - using automated deep exploration[/cyan]")
            
            # Get initialized components
            self.element_interactor = self.fdom_creator.element_interactor
            self.state_manager = self.fdom_creator.state_manager
            
            if not self.element_interactor or not self.state_manager:
                self.console.print("[red]❌ Failed to get required components from FDOM creator[/red]")
                return False
            
            app_name = getattr(self.fdom_creator, 'current_app_name', 'unknown_app')
            self.console.print(f"[green]✅ Application initialized: {app_name}[/green]")
            return True
            
        except Exception as e:
            self.console.print(f"[red]❌ Application initialization error: {e}[/red]")
            return False
    
    def _discover_initial_state(self) -> bool:
        """Discover and register the initial application state"""
        try:
            # Get current state information
            current_state_id = self.element_interactor.current_state_id
            fdom_data = self.state_manager.fdom_data
            
            if current_state_id not in fdom_data.get("states", {}):
                self.console.print(f"[red]❌ Current state {current_state_id} not found in FDOM[/red]")
                return False
            
            state_data = fdom_data["states"][current_state_id]
            element_count = len(state_data.get("nodes", {}))
            
            # Register initial state
            initial_state = ExplorationState(
                state_id=current_state_id,
                depth=0,
                parent_state=None,
                trigger_element=None,
                discovered_at=datetime.now(),
                element_count=element_count
            )
            
            self.discovered_states[current_state_id] = initial_state
            self.exploration_queue.append((current_state_id, 0))
            
            self.stats['total_states_discovered'] = 1
            self.stats['total_elements_discovered'] = element_count
            
            self.console.print(f"[green]✅ Initial state discovered: {current_state_id} ({element_count} elements)[/green]")
            return True
            
        except Exception as e:
            self.console.print(f"[red]❌ Initial state discovery error: {e}[/red]")
            return False
    
    def _execute_deep_exploration(self) -> None:
        """Execute the main deep exploration loop"""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task("🔍 Deep exploration in progress...", total=None)
            
            while (self.exploration_queue and 
                   self.stats['total_states_discovered'] < self.strategy.max_total_states and
                   self._check_time_limit()):
                
                # Get next state to explore
                current_state_id, depth = self.exploration_queue.pop(0)
                
                if depth > self.strategy.max_depth:
                    continue
                
                # Update progress
                progress.update(task, description=f"🔍 Exploring {current_state_id} (depth {depth})")
                
                # Explore current state
                self._explore_state_comprehensively(current_state_id, depth)
                
                # Update statistics
                self.stats['max_depth_reached'] = max(self.stats['max_depth_reached'], depth)
            
            progress.update(task, description="✅ Deep exploration completed")
    
    def _explore_state_comprehensively(self, state_id: str, depth: int) -> None:
        """Comprehensively explore a single state to discover all possible interactions"""
        
        self.console.print(f"\n[cyan]🎯 Exploring state: {state_id} (depth {depth})[/cyan]")
        
        # Navigate to the target state if not already there
        if self.element_interactor.current_state_id != state_id:
            if not self._navigate_to_state(state_id):
                self.console.print(f"[yellow]⚠️ Could not navigate to state {state_id}[/yellow]")
                return
        
        # Mark state as being explored
        if state_id in self.discovered_states:
            self.discovered_states[state_id].explored = True
        
        # Get all pending elements in this state
        pending_elements = self._get_pending_elements_for_state(state_id)
        
        if not pending_elements:
            self.console.print(f"[yellow]📍 No pending elements in {state_id} - marking as deadend[/yellow]")
            if state_id in self.discovered_states:
                self.discovered_states[state_id].is_deadend = True
                self.stats['deadends_found'] += 1
            return
        
        self.console.print(f"[cyan]📋 Found {len(pending_elements)} elements to explore[/cyan]")
        
        # Explore each element strategically
        for element_id in pending_elements:
            if not self._check_time_limit():
                break
                
            self._explore_element_strategically(element_id, state_id, depth)
            
            # Small delay between interactions for stability
            time.sleep(1)
    
    def _explore_element_strategically(self, element_id: str, current_state_id: str, depth: int) -> None:
        """Strategically explore a single element with comprehensive interaction discovery"""
        
        element_data = self.element_interactor._find_node_in_fdom(element_id)
        if not element_data:
            return
        
        element_name = element_data.get('g_icon_name', 'unknown')
        element_type = element_data.get('g_type', 'unknown')
        
        self.console.print(f"[blue]  🔍 Testing: {element_name} ({element_type})[/blue]")
        
        # Track interaction attempt
        self.stats['total_interactions'] += 1
        
        try:
            # Primary interaction: Left click
            result = self.element_interactor.click_element(element_id)
            
            if result.success:
                self.stats['successful_interactions'] += 1
                
                if result.state_changed:
                    # New state discovered!
                    new_state_id = result.new_state_id
                    self._register_new_state(new_state_id, current_state_id, element_id, depth + 1)
                    
                    # Check if this is a dialog or menu
                    self._classify_new_state(new_state_id, element_name, element_type)
                    
                    self.console.print(f"[green]    ✅ New state discovered: {new_state_id}[/green]")
                else:
                    self.console.print(f"[yellow]    ⚪ Non-interactive element: {element_name}[/yellow]")
            else:
                self.stats['failed_interactions'] += 1
                self.console.print(f"[red]    ❌ Interaction failed: {result.error_message}[/red]")
            
            # Monitor focus status after each interaction
            self._monitor_focus_status()
            
            # Secondary interaction: Right click for context menus (if enabled)
            if (self.strategy.explore_context_menus and 
                element_type in ['icon', 'button'] and 
                not result.state_changed):
                
                self._try_context_menu_interaction(element_id, current_state_id, depth)
                
        except Exception as e:
            self.stats['failed_interactions'] += 1
            self.console.print(f"[red]    ❌ Exception during interaction: {e}[/red]")
    
    def _try_context_menu_interaction(self, element_id: str, current_state_id: str, depth: int) -> None:
        """Try right-click interaction to discover context menus"""
        
        # Note: This would require extending the element_interactor to support right-click
        # For now, we'll log the attempt
        self.console.print(f"[dim]    🖱️ Context menu check: {element_id} (feature pending)[/dim]")
    
    def _register_new_state(self, state_id: str, parent_state_id: str, trigger_element: str, depth: int) -> None:
        """Register a newly discovered state"""
        
        if state_id in self.discovered_states:
            return  # Already discovered
        
        # Get element count for the new state
        fdom_data = self.state_manager.fdom_data
        element_count = 0
        if state_id in fdom_data.get("states", {}):
            element_count = len(fdom_data["states"][state_id].get("nodes", {}))
        
        # Create exploration state record
        new_state = ExplorationState(
            state_id=state_id,
            depth=depth,
            parent_state=parent_state_id,
            trigger_element=trigger_element,
            discovered_at=datetime.now(),
            element_count=element_count
        )
        
        self.discovered_states[state_id] = new_state
        
        # Add to exploration graph
        self.exploration_graph[parent_state_id].append(state_id)
        
        # Add to exploration queue if within limits
        if (depth <= self.strategy.max_depth and 
            len([s for s in self.discovered_states.values() if s.depth == depth]) < self.strategy.max_states_per_level):
            self.exploration_queue.append((state_id, depth))
        
        # Update statistics
        self.stats['total_states_discovered'] += 1
        self.stats['total_elements_discovered'] += element_count
    
    def _classify_new_state(self, state_id: str, trigger_element_name: str, trigger_element_type: str) -> None:
        """Classify the type of newly discovered state"""
        
        if state_id not in self.discovered_states:
            return
        
        state = self.discovered_states[state_id]
        
        # Simple heuristics for classification
        trigger_name_lower = trigger_element_name.lower()
        
        if any(keyword in trigger_name_lower for keyword in ['dialog', 'popup', 'modal', 'alert', 'confirm']):
            state.is_dialog = True
            self.stats['dialogs_discovered'] += 1
            self.console.print(f"[magenta]    📄 Dialog detected: {state_id}[/magenta]")
            
        elif any(keyword in trigger_name_lower for keyword in ['menu', 'dropdown', 'submenu', 'context']):
            state.is_menu = True
            self.stats['menus_discovered'] += 1
            self.console.print(f"[cyan]    📋 Menu detected: {state_id}[/cyan]")
    
    def _get_pending_elements_for_state(self, state_id: str) -> List[str]:
        """Get all pending elements for a specific state"""
        
        pending_elements = []
        
        for pending_node_id in self.state_manager.pending_nodes:
            if pending_node_id.startswith(f"{state_id}::"):
                pending_elements.append(pending_node_id)
        
        return pending_elements
    
    def _navigate_to_state(self, target_state_id: str) -> bool:
        """Navigate to a specific state using the exploration graph"""
        
        if self.element_interactor.current_state_id == target_state_id:
            return True
        
        # Try using the element_interactor's navigation
        try:
            return self.element_interactor.navigate_back_to_state(target_state_id)
        except Exception as e:
            self.console.print(f"[yellow]⚠️ Navigation failed: {e}[/yellow]")
            return False
    
    def _check_time_limit(self) -> bool:
        """Check if we've exceeded the total exploration time limit"""
        
        if not self.strategy.safety_timeouts:
            return True
            
        if not self.stats['exploration_start_time']:
            return True
        
        elapsed = (datetime.now() - self.stats['exploration_start_time']).total_seconds()
        return elapsed < self.strategy.total_timeout
    
    def _monitor_focus_status(self) -> None:
        """Monitor window focus status and update statistics"""
        try:
            if (self.element_interactor and 
                hasattr(self.element_interactor, 'window_focus_manager') and
                self.element_interactor.window_focus_manager):
                
                focus_manager = self.element_interactor.window_focus_manager
                focus_status = focus_manager.get_focus_status_summary()
                
                # Update statistics
                current_failures = focus_status.get('focus_failure_count', 0)
                if current_failures > self.stats['focus_failures']:
                    self.stats['focus_failures'] = current_failures
                
                # Check if focus verification is disabled (indication of recovery issues)
                if not focus_status.get('focus_verification_enabled', True):
                    self.console.print("[yellow]⚠️ Window focus verification has been disabled due to repeated failures[/yellow]")
                
                # Log focus status periodically
                if self.stats['total_interactions'] % 20 == 0 and self.stats['total_interactions'] > 0:  # Every 20 interactions
                    self.console.print(f"[dim]🎯 Focus Status: {current_failures} failures, verification {'enabled' if focus_status.get('focus_verification_enabled', True) else 'disabled'}[/dim]")
                    
        except Exception as e:
            self.console.print(f"[dim yellow]⚠️ Focus monitoring error: {e}[/dim]")
    
    def _generate_exploration_report(self) -> Dict:
        """Generate comprehensive exploration report"""
        
        self.stats['exploration_end_time'] = datetime.now()
        
        if self.stats['exploration_start_time']:
            duration = self.stats['exploration_end_time'] - self.stats['exploration_start_time']
            duration_seconds = duration.total_seconds()
        else:
            duration_seconds = 0
        
        # Create detailed report
        report = {
            "success": True,
            "exploration_summary": {
                "total_duration_seconds": duration_seconds,
                "total_states_discovered": self.stats['total_states_discovered'],
                "total_elements_discovered": self.stats['total_elements_discovered'],
                "total_interactions": self.stats['total_interactions'],
                "successful_interactions": self.stats['successful_interactions'],
                "failed_interactions": self.stats['failed_interactions'],
                "success_rate": (self.stats['successful_interactions'] / max(1, self.stats['total_interactions'])) * 100,
                "dialogs_discovered": self.stats['dialogs_discovered'],
                "menus_discovered": self.stats['menus_discovered'],
                "deadends_found": self.stats['deadends_found'],
                "max_depth_reached": self.stats['max_depth_reached'],
                "focus_failures": self.stats['focus_failures'],
                "focus_recoveries": self.stats['focus_recoveries']
            },
            "discovered_states": {
                state_id: {
                    "depth": state.depth,
                    "parent_state": state.parent_state,
                    "trigger_element": state.trigger_element,
                    "element_count": state.element_count,
                    "explored": state.explored,
                    "is_deadend": state.is_deadend,
                    "is_dialog": state.is_dialog,
                    "is_menu": state.is_menu,
                    "discovered_at": state.discovered_at.isoformat()
                }
                for state_id, state in self.discovered_states.items()
            },
            "exploration_graph": dict(self.exploration_graph),
            "strategy_used": {
                "max_depth": self.strategy.max_depth,
                "max_states_per_level": self.strategy.max_states_per_level,
                "max_total_states": self.strategy.max_total_states,
                "backtrack_on_deadend": self.strategy.backtrack_on_deadend,
                "explore_dialogs": self.strategy.explore_dialogs,
                "explore_menus": self.strategy.explore_menus,
                "explore_context_menus": self.strategy.explore_context_menus
            }
        }
        
        # Display report summary
        self._display_exploration_summary(report)
        
        # Save detailed report to file
        self._save_exploration_report(report)
        
        return report
    
    def _display_exploration_summary(self, report: Dict) -> None:
        """Display a beautiful summary of the exploration results"""
        
        summary = report["exploration_summary"]
        
        # Main summary panel
        summary_panel = Panel(
            f"[bold]🎯 Deep Exploration Complete![/bold]\n\n"
            f"⏱️ Duration: {summary['total_duration_seconds']:.1f} seconds\n"
            f"🌍 States Discovered: {summary['total_states_discovered']}\n"
            f"🔍 Elements Found: {summary['total_elements_discovered']}\n"
            f"🖱️ Interactions: {summary['total_interactions']} (Success: {summary['success_rate']:.1f}%)\n"
            f"📄 Dialogs: {summary['dialogs_discovered']}\n"
            f"📋 Menus: {summary['menus_discovered']}\n"
            f"📊 Max Depth: {summary['max_depth_reached']}\n"
            f"⛔ Dead Ends: {summary['deadends_found']}\n"
            f"🎯 Focus Issues: {summary['focus_failures']} failures",
            title="🔬 Deep Exploration Results",
            border_style="green"
        )
        
        self.console.print(summary_panel)
        
        # State hierarchy tree
        if self.discovered_states:
            self._display_state_hierarchy()
    
    def _display_state_hierarchy(self) -> None:
        """Display the discovered state hierarchy as a tree"""
        
        tree = Tree("🌳 Discovered State Hierarchy")
        
        # Build tree recursively
        root_states = [s for s in self.discovered_states.values() if s.parent_state is None]
        
        for root_state in root_states:
            self._add_state_to_tree(tree, root_state.state_id)
        
        self.console.print(tree)
    
    def _add_state_to_tree(self, parent_node, state_id: str) -> None:
        """Recursively add states to the tree"""
        
        if state_id not in self.discovered_states:
            return
        
        state = self.discovered_states[state_id]
        
        # Create state description
        state_desc = f"{state_id} (depth {state.depth}, {state.element_count} elements)"
        
        if state.is_dialog:
            state_desc += " 📄"
        if state.is_menu:
            state_desc += " 📋"
        if state.is_deadend:
            state_desc += " ⛔"
        if not state.explored:
            state_desc += " ⏳"
        
        node = parent_node.add(state_desc)
        
        # Add child states
        child_states = self.exploration_graph.get(state_id, [])
        for child_state_id in child_states:
            self._add_state_to_tree(node, child_state_id)
    
    def _save_exploration_report(self, report: Dict) -> None:
        """Save the detailed exploration report to file"""
        
        try:
            app_name = getattr(self.state_manager, 'app_name', 'unknown_app')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            apps_dir = Path(__file__).parent / "apps" / app_name
            apps_dir.mkdir(parents=True, exist_ok=True)
            
            report_file = apps_dir / f"deep_exploration_report_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            
            self.console.print(f"[green]💾 Detailed report saved to: {report_file}[/green]")
            
        except Exception as e:
            self.console.print(f"[yellow]⚠️ Could not save report: {e}[/yellow]")
    
    def _create_failure_result(self, error_message: str) -> Dict:
        """Create a failure result dictionary"""
        
        return {
            "success": False,
            "error": error_message,
            "stats": self.stats,
            "discovered_states": {
                state_id: {
                    "depth": state.depth,
                    "element_count": state.element_count,
                    "discovered_at": state.discovered_at.isoformat()
                }
                for state_id, state in self.discovered_states.items()
            }
        }


def main():
    """Main entry point for deep exploration"""
    
    console = Console()
    
    # Configuration options
    console.print(Panel(
        "[bold]🔬 Deep Application Explorer[/bold]\n\n"
        "This tool performs comprehensive deep exploration of applications,\n"
        "discovering nested menus, dialogs, and deep UI hierarchies.",
        title="🚀 Welcome",
        border_style="blue"
    ))
    
    # Get application path
    app_path = Prompt.ask(
        "[blue]Enter application executable path[/blue]",
        default="C:/Program Files/VideoLAN/VLC/vlc.exe"
    )
    
    if not Path(app_path).exists():
        console.print(f"[red]❌ Application not found: {app_path}[/red]")
        return
    
    # Configure exploration strategy
    console.print("\n[yellow]🎛️ Exploration Configuration[/yellow]")
    
    max_depth = IntPrompt.ask("Maximum exploration depth", default=6)
    max_states = IntPrompt.ask("Maximum total states to discover", default=200)
    
    explore_dialogs = Confirm.ask("Explore dialog boxes?", default=True)
    explore_menus = Confirm.ask("Explore menu systems?", default=True)
    
    # Create strategy
    strategy = ExplorationStrategy(
        max_depth=max_depth,
        max_total_states=max_states,
        explore_dialogs=explore_dialogs,
        explore_menus=explore_menus,
        explore_context_menus=True
    )
    
    # Initialize explorer
    explorer = DeepExplorer(app_path, strategy)
    
    # Run exploration
    console.print("\n[green]🚀 Starting deep exploration...[/green]")
    result = explorer.run_deep_exploration()
    
    if result.get("success", False):
        console.print("\n[bold green]✅ Deep exploration completed successfully![/bold green]")
    else:
        console.print(f"\n[bold red]❌ Deep exploration failed: {result.get('error', 'Unknown error')}[/bold red]")


if __name__ == "__main__":
    main() 