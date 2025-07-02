"""
Window Focus Manager - Ensures target window stays focused during exploration
Handles focus loss recovery and prevents clicks on wrong windows
"""

import time
from typing import Optional, Dict, Tuple
from rich.console import Console

class WindowFocusManager:
    """
    Manages window focus to prevent exploration from switching to other windows
    """
    
    def __init__(self, app_controller, config):
        self.app_controller = app_controller
        self.config = config
        self.console = Console()
        
        # Focus management settings
        self.focus_verification_enabled = True
        self.auto_recovery_enabled = True
        self.focus_check_interval = 3  # seconds between focus checks
        self.last_focus_check = 0
        self.focus_failure_count = 0
        self.max_focus_failures = 3
        
        # Window state tracking
        self.expected_window_id = None
        self.expected_window_title = None
        self.last_known_position = None
        
    def ensure_target_window_focused(self, force_check: bool = False) -> bool:
        """
        Ensure the target application window has focus
        
        Args:
            force_check: Skip time-based checks and force verification
            
        Returns:
            True if window is focused, False otherwise
        """
        
        # Skip if focus verification is disabled
        if not self.focus_verification_enabled:
            return True
            
        # Time-based focus checks (unless forced)
        current_time = time.time()
        if not force_check and (current_time - self.last_focus_check) < self.focus_check_interval:
            return True
            
        self.last_focus_check = current_time
        
        try:
            if not self.app_controller.current_app_info:
                self.console.print("[red]❌ No app info available for focus check[/red]")
                return False
            
            window_id = self.app_controller.current_app_info['window_id']
            self.expected_window_id = window_id
            
            # Step 1: Verify window still exists
            window_info = self.app_controller.gui_api.get_window_info(window_id)
            if not window_info:
                self.console.print(f"[red]❌ Target window {window_id} no longer exists[/red]")
                return self._handle_focus_failure("window_not_found")
            
            # Step 2: Check if window is focused/foreground
            hwnd = window_info['window_data']['hwnd']
            is_foreground = self._is_window_foreground(hwnd)
            
            if is_foreground:
                self.console.print(f"[green]✅ Target window is in foreground[/green]")
                self.focus_failure_count = 0  # Reset failure count
                self._update_window_state_tracking(window_info)
                return True
            else:
                self.console.print(f"[yellow]⚠️ Target window lost focus - attempting recovery[/yellow]")
                return self._recover_window_focus(hwnd, window_id)
                
        except Exception as e:
            self.console.print(f"[red]❌ Focus check failed: {e}[/red]")
            return self._handle_focus_failure("check_exception", str(e))
    
    def _is_window_foreground(self, hwnd: int) -> bool:
        """Check if the window is currently in the foreground"""
        try:
            import win32gui
            foreground_hwnd = win32gui.GetForegroundWindow()
            return foreground_hwnd == hwnd
        except Exception as e:
            self.console.print(f"[yellow]⚠️ Could not check foreground window: {e}[/yellow]")
            return False
    
    def _recover_window_focus(self, hwnd: int, window_id: str) -> bool:
        """Attempt to recover focus to the target window"""
        
        self.console.print(f"[cyan]🔄 Attempting focus recovery for window {window_id}[/cyan]")
        
        try:
            # Method 1: Use smart_foreground (minimize/maximize trick)
            focus_success, focus_message = self.app_controller.gui_api.controller.wm.smart_foreground(hwnd)
            
            if focus_success:
                self.console.print(f"[green]✅ Smart foreground successful: {focus_message}[/green]")
                
                # Wait for focus animation
                time.sleep(2)
                
                # Verify focus was restored
                if self._is_window_foreground(hwnd):
                    self.console.print(f"[green]✅ Focus recovery successful[/green]")
                    self.focus_failure_count = 0
                    
                    # Refresh window coordinates after focus recovery
                    self._refresh_window_coordinates_after_focus(window_id)
                    
                    return True
                else:
                    self.console.print(f"[yellow]⚠️ Smart foreground sent but window still not focused[/yellow]")
                    return self._try_alternative_focus_methods(hwnd, window_id)
            else:
                self.console.print(f"[red]❌ Smart foreground failed: {focus_message}[/red]")
                return self._try_alternative_focus_methods(hwnd, window_id)
                
        except Exception as e:
            self.console.print(f"[red]❌ Focus recovery exception: {e}[/red]")
            return self._handle_focus_failure("recovery_exception", str(e))
    
    def _try_alternative_focus_methods(self, hwnd: int, window_id: str) -> bool:
        """Try alternative methods to restore window focus"""
        
        self.console.print(f"[cyan]🔄 Trying alternative focus methods[/cyan]")
        
        try:
            # Method 2: Regular focus command
            if self.app_controller.gui_api.focus_window(window_id):
                time.sleep(1)
                if self._is_window_foreground(hwnd):
                    self.console.print(f"[green]✅ Regular focus command worked[/green]")
                    self.focus_failure_count = 0
                    return True
            
            # Method 3: Click on window to focus it
            self.console.print(f"[cyan]🖱️ Attempting focus via window click[/cyan]")
            window_info = self.app_controller.gui_api.get_window_info(window_id)
            if window_info:
                pos = window_info['window_data']['position']
                size = window_info['window_data']['size']
                
                # Click in the center of the window title bar area
                center_x = pos['x'] + size['width'] // 2
                title_bar_y = pos['y'] + 20  # Approximate title bar location
                
                self.app_controller.gui_api.click(center_x, title_bar_y)
                time.sleep(1)
                
                if self._is_window_foreground(hwnd):
                    self.console.print(f"[green]✅ Click focus method worked[/green]")
                    self.focus_failure_count = 0
                    return True
            
            # All methods failed
            return self._handle_focus_failure("all_methods_failed")
            
        except Exception as e:
            self.console.print(f"[red]❌ Alternative focus methods failed: {e}[/red]")
            return self._handle_focus_failure("alternative_methods_exception", str(e))
    
    def _refresh_window_coordinates_after_focus(self, window_id: str) -> None:
        """Refresh window coordinates after focus recovery"""
        
        self.console.print(f"[cyan]🔄 Refreshing coordinates after focus recovery[/cyan]")
        
        try:
            # Force refresh of window API
            self.app_controller.gui_api.refresh()
            time.sleep(0.5)
            
            # Get fresh window coordinates
            fresh_window_info = self.app_controller.gui_api.get_window_info(window_id)
            if fresh_window_info:
                pos = fresh_window_info['window_data']['position']
                size = fresh_window_info['window_data']['size']
                
                self.console.print(f"[green]📍 Fresh coordinates: ({pos['x']}, {pos['y']}) size {size['width']}×{size['height']}[/green]")
                self._update_window_state_tracking(fresh_window_info)
            else:
                self.console.print(f"[yellow]⚠️ Could not get fresh coordinates after focus recovery[/yellow]")
                
        except Exception as e:
            self.console.print(f"[yellow]⚠️ Coordinate refresh failed: {e}[/yellow]")
    
    def _update_window_state_tracking(self, window_info: Dict) -> None:
        """Update our tracking of the window state"""
        try:
            pos = window_info['window_data']['position']
            size = window_info['window_data']['size']
            
            self.last_known_position = {
                'x': pos['x'],
                'y': pos['y'],
                'width': size['width'],
                'height': size['height']
            }
            
            # Also track window title if available
            if 'title' in window_info['window_data']:
                self.expected_window_title = window_info['window_data']['title']
                
        except Exception as e:
            self.console.print(f"[yellow]⚠️ Window state tracking update failed: {e}[/yellow]")
    
    def _handle_focus_failure(self, failure_type: str, details: str = "") -> bool:
        """Handle focus failure with recovery options"""
        
        self.focus_failure_count += 1
        self.console.print(f"[red]❌ Focus failure #{self.focus_failure_count}: {failure_type} {details}[/red]")
        
        if not self.auto_recovery_enabled:
            return False
            
        if self.focus_failure_count >= self.max_focus_failures:
            self.console.print(f"[red]💥 Max focus failures reached ({self.max_focus_failures}) - disabling focus verification[/red]")
            self.focus_verification_enabled = False
            return False
        
        # Try to restart the app as last resort
        if failure_type in ["window_not_found", "all_methods_failed"]:
            self.console.print(f"[cyan]🔄 Attempting app restart to recover focus[/cyan]")
            try:
                if hasattr(self.app_controller, '_restart_app_for_exploration'):
                    restart_success = self.app_controller._restart_app_for_exploration()
                    if restart_success:
                        self.console.print(f"[green]✅ App restart successful - focus recovered[/green]")
                        self.focus_failure_count = 0
                        return True
                else:
                    self.console.print(f"[yellow]⚠️ App restart method not available[/yellow]")
            except Exception as e:
                self.console.print(f"[red]❌ App restart failed: {e}[/red]")
        
        return False
    
    def prepare_for_screenshot(self) -> bool:
        """Ensure window is focused before taking a screenshot"""
        self.console.print(f"[cyan]📸 Preparing window for screenshot[/cyan]")
        
        # Always force check before screenshots
        success = self.ensure_target_window_focused(force_check=True)
        
        if success:
            # Extra wait for any window animations to complete
            time.sleep(0.5)
            self.console.print(f"[green]✅ Window ready for screenshot[/green]")
        else:
            self.console.print(f"[red]❌ Failed to prepare window for screenshot[/red]")
            
        return success
    
    def prepare_for_interaction(self) -> bool:
        """Ensure window is focused before any click interaction"""
        self.console.print(f"[cyan]🖱️ Preparing window for interaction[/cyan]")
        
        # Always force check before interactions
        success = self.ensure_target_window_focused(force_check=True)
        
        if success:
            # Extra wait for focus to stabilize
            time.sleep(0.3)
            self.console.print(f"[green]✅ Window ready for interaction[/green]")
        else:
            self.console.print(f"[red]❌ Failed to prepare window for interaction[/red]")
            
        return success
    
    def get_focus_status_summary(self) -> Dict:
        """Get summary of current focus management status"""
        return {
            "focus_verification_enabled": self.focus_verification_enabled,
            "auto_recovery_enabled": self.auto_recovery_enabled,
            "focus_failure_count": self.focus_failure_count,
            "max_focus_failures": self.max_focus_failures,
            "expected_window_id": self.expected_window_id,
            "last_known_position": self.last_known_position
        } 