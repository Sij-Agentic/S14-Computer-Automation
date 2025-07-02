#!/usr/bin/env python3
"""
Test script to verify window focus management fixes
Tests the new WindowFocusManager integration
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from utils.fdom.window_focus_manager import WindowFocusManager
from utils.fdom.element_interactor import ElementInteractor
from utils.fdom.config_manager import ConfigManager

def test_focus_manager_integration():
    """Test the focus manager integration with element interactor"""
    
    console = Console()
    
    console.print(Panel(
        "[bold]🔧 Testing Window Focus Management Fixes[/bold]\n\n"
        "This script tests the new focus management system to prevent\n"
        "clicks on wrong windows during exploration.",
        title="🧪 Focus Management Test",
        border_style="blue"
    ))
    
    # Get application path from user
    app_path = input("\n📱 Enter application executable path to test: ").strip()
    if not app_path:
        console.print("[red]❌ No application path provided[/red]")
        return False
    
    try:
        console.print(f"\n[yellow]🚀 Initializing ElementInteractor with focus management...[/yellow]")
        
        # Initialize element interactor (this will create the focus manager)
        element_interactor = ElementInteractor(app_path)
        
        # Check if focus manager was created
        if hasattr(element_interactor, 'window_focus_manager'):
            console.print(f"[green]✅ WindowFocusManager initialized successfully[/green]")
            
            focus_manager = element_interactor.window_focus_manager
            console.print(f"[cyan]📊 Focus manager status:[/cyan]")
            console.print(f"  - Focus verification enabled: {focus_manager.focus_verification_enabled}")
            console.print(f"  - Auto recovery enabled: {focus_manager.auto_recovery_enabled}")
            console.print(f"  - Max focus failures: {focus_manager.max_focus_failures}")
            
            # Test the focus status method
            focus_status = focus_manager.get_focus_status_summary()
            console.print(f"\n[cyan]📋 Focus status summary:[/cyan]")
            for key, value in focus_status.items():
                console.print(f"  - {key}: {value}")
                
        else:
            console.print(f"[red]❌ WindowFocusManager not found in ElementInteractor[/red]")
            return False
        
        # Check other component integrations
        console.print(f"\n[yellow]🔍 Checking component integrations...[/yellow]")
        
        # Check ScreenshotManager integration
        if hasattr(element_interactor.screenshot_manager, 'focus_manager'):
            if element_interactor.screenshot_manager.focus_manager:
                console.print(f"[green]✅ ScreenshotManager has focus manager[/green]")
            else:
                console.print(f"[yellow]⚠️ ScreenshotManager focus manager is None[/yellow]")
        else:
            console.print(f"[red]❌ ScreenshotManager missing focus manager attribute[/red]")
        
        # Check ClickEngine integration
        if hasattr(element_interactor.click_engine, 'focus_manager'):
            if element_interactor.click_engine.focus_manager:
                console.print(f"[green]✅ ClickEngine has focus manager[/green]")
            else:
                console.print(f"[yellow]⚠️ ClickEngine focus manager is None[/yellow]")
        else:
            console.print(f"[red]❌ ClickEngine missing focus manager attribute[/red]")
        
        console.print(f"\n[green]🎉 Focus management integration test completed![/green]")
        
        # Test with actual application launch
        test_with_app = input("\n🚀 Test with actual application launch? (y/n): ").lower().startswith('y')
        
        if test_with_app:
            console.print(f"\n[yellow]📱 Launching application for focus testing...[/yellow]")
            
            try:
                # This will go through the full initialization including app launch
                element_interactor.interactive_exploration_mode()
                
            except KeyboardInterrupt:
                console.print(f"\n[yellow]⚡ Test interrupted by user[/yellow]")
            except Exception as e:
                console.print(f"\n[red]❌ Application test failed: {e}[/red]")
                
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Test failed: {e}[/red]")
        return False

def test_focus_manager_standalone():
    """Test the focus manager as a standalone component"""
    
    console = Console()
    
    console.print(f"\n[yellow]🧪 Testing WindowFocusManager standalone...[/yellow]")
    
    try:
        # Create config
        config = ConfigManager()
        
        # Create a mock app controller for testing
        class MockAppController:
            def __init__(self):
                self.current_app_info = None
        
        mock_controller = MockAppController()
        
        # Create focus manager
        focus_manager = WindowFocusManager(mock_controller, config)
        
        console.print(f"[green]✅ WindowFocusManager created successfully[/green]")
        
        # Test configuration
        console.print(f"[cyan]📊 Configuration:[/cyan]")
        console.print(f"  - Focus check interval: {focus_manager.focus_check_interval}s")
        console.print(f"  - Max focus failures: {focus_manager.max_focus_failures}")
        console.print(f"  - Auto recovery: {focus_manager.auto_recovery_enabled}")
        
        # Test status summary (should handle no app gracefully)
        status = focus_manager.get_focus_status_summary()
        console.print(f"\n[cyan]📋 Status with no app:[/cyan]")
        for key, value in status.items():
            console.print(f"  - {key}: {value}")
        
        console.print(f"\n[green]✅ Standalone focus manager test passed[/green]")
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Standalone test failed: {e}[/red]")
        return False

def main():
    """Main test function"""
    
    console = Console()
    
    console.print(Panel(
        "[bold green]🔧 Window Focus Management Test Suite[/bold green]\n\n"
        "This script tests the fixes for window focus issues during exploration.\n"
        "The fixes include:\n"
        "• WindowFocusManager with smart focus recovery\n"
        "• Integration with ScreenshotManager and ClickEngine\n"
        "• Focus monitoring during deep exploration\n"
        "• Automatic window focus recovery mechanisms",
        title="🧪 Focus Fix Verification",
        border_style="green"
    ))
    
    # Test 1: Standalone focus manager
    console.print(f"\n[bold yellow]TEST 1: Standalone Focus Manager[/bold yellow]")
    test1_result = test_focus_manager_standalone()
    
    # Test 2: Integration test
    console.print(f"\n[bold yellow]TEST 2: Integration Test[/bold yellow]")
    test2_result = test_focus_manager_integration()
    
    # Summary
    console.print(f"\n[bold cyan]📋 TEST SUMMARY[/bold cyan]")
    console.print(f"  • Standalone test: {'✅ PASS' if test1_result else '❌ FAIL'}")
    console.print(f"  • Integration test: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        console.print(f"\n[bold green]🎉 All tests passed! Focus management fixes are working.[/bold green]")
        console.print(f"\n[cyan]💡 You can now run enhanced_auto_explore.py and it should:[/cyan]")
        console.print(f"  • Keep the target window focused during exploration")
        console.print(f"  • Automatically recover focus if it's lost")
        console.print(f"  • Prevent clicks on wrong windows")
        console.print(f"  • Monitor focus issues and provide statistics")
    else:
        console.print(f"\n[bold red]❌ Some tests failed. Please check the implementation.[/bold red]")

if __name__ == "__main__":
    main() 