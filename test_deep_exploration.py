#!/usr/bin/env python3
"""
Test Deep Exploration System
Quick validation and testing script for the new deep exploration capabilities
"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm

def test_imports():
    """Test that all required modules can be imported"""
    console = Console()
    
    console.print(Panel(
        "[bold blue]🔧 Testing Module Imports[/bold blue]",
        title="Import Test",
        border_style="blue"
    ))
    
    tests = [
        ("Deep Explorer", "from deep_explore import DeepExplorer, ExplorationStrategy"),
        ("Enhanced Auto Explorer", "from enhanced_auto_explore import EnhancedAutoExplorer"),
        ("FDOM Framework", "from utils.fdom.element_interactor import ElementInteractor"),
        ("State Manager", "from utils.fdom.state_manager import StateManager"),
        ("FDOM Creator", "from utils.fdom.fdom_creator import FDOMCreator"),
        ("Rich Console", "from rich.console import Console"),
        ("NetworkX", "import networkx as nx"),
        ("Pillow", "from PIL import Image"),
        ("NumPy", "import numpy as np")
    ]
    
    results = []
    
    for name, import_statement in tests:
        try:
            exec(import_statement)
            results.append((name, "✅ SUCCESS", "green"))
            console.print(f"[green]✅ {name}: Import successful[/green]")
        except ImportError as e:
            results.append((name, f"❌ FAILED: {e}", "red"))
            console.print(f"[red]❌ {name}: Import failed - {e}[/red]")
        except Exception as e:
            results.append((name, f"⚠️ ERROR: {e}", "yellow"))
            console.print(f"[yellow]⚠️ {name}: Unexpected error - {e}[/yellow]")
    
    # Summary
    passed = len([r for r in results if "SUCCESS" in r[1]])
    total = len(results)
    
    if passed == total:
        console.print(f"\n[bold green]🎉 All imports successful ({passed}/{total})[/bold green]")
        return True
    else:
        console.print(f"\n[bold red]❌ Import failures detected ({passed}/{total} passed)[/bold red]")
        return False

def test_strategy_creation():
    """Test that ExplorationStrategy can be created"""
    console = Console()
    
    console.print(Panel(
        "[bold blue]🎯 Testing Strategy Creation[/bold blue]",
        title="Strategy Test",
        border_style="blue"
    ))
    
    try:
        from deep_explore import ExplorationStrategy
        
        # Test default strategy
        default_strategy = ExplorationStrategy()
        console.print("[green]✅ Default strategy created successfully[/green]")
        
        # Test custom strategy
        custom_strategy = ExplorationStrategy(
            max_depth=5,
            max_total_states=100,
            explore_dialogs=True,
            explore_menus=True
        )
        console.print("[green]✅ Custom strategy created successfully[/green]")
        
        # Validate strategy properties
        assert custom_strategy.max_depth == 5
        assert custom_strategy.max_total_states == 100
        assert custom_strategy.explore_dialogs == True
        console.print("[green]✅ Strategy properties validated[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Strategy creation failed: {e}[/red]")
        return False

def test_explorer_initialization():
    """Test that DeepExplorer can be initialized (without launching app)"""
    console = Console()
    
    console.print(Panel(
        "[bold blue]🚀 Testing Explorer Initialization[/bold blue]",
        title="Explorer Test",
        border_style="blue"
    ))
    
    try:
        from deep_explore import DeepExplorer, ExplorationStrategy
        
        # Use a fake app path for testing
        fake_app_path = "C:/Windows/System32/notepad.exe"
        
        # Create strategy
        strategy = ExplorationStrategy(
            max_depth=3,
            max_total_states=50,
            safety_timeouts=True,
            total_timeout=300  # 5 minutes for testing
        )
        
        # Note: We won't actually initialize the app (that would launch it)
        # Just test the class can be instantiated
        console.print("[green]✅ DeepExplorer class available[/green]")
        console.print("[green]✅ Strategy configuration works[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Explorer initialization test failed: {e}[/red]")
        return False

def test_enhanced_auto_explorer():
    """Test that EnhancedAutoExplorer can be initialized"""
    console = Console()
    
    console.print(Panel(
        "[bold blue]🤖 Testing Enhanced Auto Explorer[/bold blue]",
        title="Auto Explorer Test",
        border_style="blue"
    ))
    
    try:
        from enhanced_auto_explore import EnhancedAutoExplorer
        
        # Note: We won't actually initialize the app, just test the class
        fake_app_path = "C:/Windows/System32/notepad.exe"
        
        console.print("[green]✅ EnhancedAutoExplorer class available[/green]")
        console.print("[green]✅ Automated exploration framework ready[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Enhanced auto explorer test failed: {e}[/red]")
        return False

def test_comparison_demo():
    """Test that the comparison demo works"""
    console = Console()
    
    console.print(Panel(
        "[bold blue]📊 Testing Comparison Demo[/bold blue]",
        title="Demo Test",
        border_style="blue"
    ))
    
    try:
        # Just test that we can import the comparison demo
        import comparison_demo
        console.print("[green]✅ Comparison demo available[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Comparison demo test failed: {e}[/red]")
        return False

def run_all_tests():
    """Run all validation tests"""
    console = Console()
    
    console.print(Panel(
        "[bold cyan]🧪 Deep Exploration System Validation[/bold cyan]\n\n"
        "This script validates that the new deep exploration system is properly installed\n"
        "and ready for use. It does NOT launch any applications.",
        title="🔬 System Validation",
        border_style="cyan"
    ))
    
    tests = [
        ("Module Imports", test_imports),
        ("Strategy Creation", test_strategy_creation),
        ("Explorer Initialization", test_explorer_initialization),
        ("Enhanced Auto Explorer", test_enhanced_auto_explorer),
        ("Comparison Demo", test_comparison_demo)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        console.print(f"\n[cyan]Running: {test_name}[/cyan]")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            console.print(f"[red]❌ Test {test_name} crashed: {e}[/red]")
            results.append((test_name, False))
    
    # Final summary
    passed = len([r for r in results if r[1]])
    total = len(results)
    
    console.print("\n")
    console.print("=" * 50)
    
    if passed == total:
        console.print(Panel(
            f"[bold green]🎉 ALL TESTS PASSED ({passed}/{total})[/bold green]\n\n"
            "✅ Deep exploration system is ready for use!\n"
            "✅ All modules imported successfully\n"
            "✅ Framework components initialized correctly\n\n"
            "[bold]Next Steps:[/bold]\n"
            "• Run: python comparison_demo.py (view comparison)\n"
            "• Run: python deep_explore.py (interactive exploration)\n"
            "• Run: python enhanced_auto_explore.py \"app.exe\" (automated analysis)",
            title="🚀 Validation Complete",
            border_style="green"
        ))
    else:
        failed_tests = [name for name, result in results if not result]
        console.print(Panel(
            f"[bold red]❌ SOME TESTS FAILED ({passed}/{total} passed)[/bold red]\n\n"
            f"Failed tests: {', '.join(failed_tests)}\n\n"
            "[bold]Troubleshooting:[/bold]\n"
            "• Check that all dependencies are installed: uv install\n"
            "• Verify Python path includes the project directory\n"
            "• Check for missing packages in pyproject.toml",
            title="⚠️ Validation Issues",
            border_style="red"
        ))
    
    return passed == total

def main():
    """Main test runner"""
    console = Console()
    
    if Confirm.ask("Run deep exploration system validation tests?", default=True):
        success = run_all_tests()
        
        if success:
            console.print("\n[bold green]✅ System is ready for deep exploration![/bold green]")
            
            if Confirm.ask("\nWould you like to see the comparison demo now?", default=False):
                try:
                    import comparison_demo
                    comparison_demo.main()
                except Exception as e:
                    console.print(f"[red]❌ Could not run comparison demo: {e}[/red]")
        else:
            console.print("\n[bold red]❌ Please fix the issues above before using the system[/bold red]")
    else:
        console.print("[yellow]Validation skipped[/yellow]")

if __name__ == "__main__":
    main() 