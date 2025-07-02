#!/usr/bin/env python3
"""
Enhanced Auto Explorer - Fully Automated Deep Application Analysis
Combines the power of the Deep Explorer with full automation for comprehensive app analysis.
This script runs without user interaction and provides exhaustive coverage of app functionality.
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

# Import our modules
from deep_explore import DeepExplorer, ExplorationStrategy
from utils.fdom.element_interactor import ElementInteractor
from utils.fdom.state_manager import StateManager

class EnhancedAutoExplorer:
    """
    Fully automated comprehensive application explorer
    """
    
    def __init__(self, app_executable_path: str, max_runtime_minutes: int = 60):
        self.console = Console()
        self.app_executable_path = app_executable_path
        self.max_runtime_minutes = max_runtime_minutes
        
        # Create aggressive exploration strategy for automated use
        self.exploration_strategy = ExplorationStrategy(
            max_depth=8,                      # Deep exploration
            max_states_per_level=100,         # Aggressive state discovery
            max_total_states=1000,            # Very comprehensive
            backtrack_on_deadend=True,        # Always backtrack
            explore_dialogs=True,             # Explore all dialogs
            explore_menus=True,               # Explore all menus
            explore_context_menus=True,       # Context menus too
            revisit_states=False,             # Efficiency focused
            safety_timeouts=True,             # Safety first
            state_timeout=15,                 # Faster per-state timeout
            total_timeout=max_runtime_minutes * 60  # User-specified runtime
        )
        
        self.console.print(Panel(
            f"[bold]🤖 Enhanced Auto Explorer[/bold]\n\n"
            f"🎯 Target: {Path(app_executable_path).name}\n"
            f"⏱️ Runtime Limit: {max_runtime_minutes} minutes\n"
            f"🔍 Strategy: Comprehensive automated deep exploration\n"
            f"📊 Max States: {self.exploration_strategy.max_total_states}\n"
            f"🌊 Max Depth: {self.exploration_strategy.max_depth}",
            title="🚀 Automated Deep Analysis",
            border_style="blue"
        ))
    
    def run_automated_analysis(self) -> Dict:
        """
        Run fully automated comprehensive analysis
        """
        start_time = datetime.now()
        
        self.console.print("\n[bold green]🤖 Starting automated comprehensive analysis...[/bold green]")
        
        try:
            # Initialize deep explorer
            deep_explorer = DeepExplorer(self.app_executable_path, self.exploration_strategy)
            
            # Run deep exploration
            result = deep_explorer.run_deep_exploration()
            
            # Enhance result with automation-specific analysis
            enhanced_result = self._enhance_analysis_result(result, start_time)
            
            # Generate automated report
            self._generate_automated_report(enhanced_result)
            
            return enhanced_result
            
        except Exception as e:
            self.console.print(f"[red]❌ Automated analysis failed: {e}[/red]")
            return {
                "success": False,
                "error": str(e),
                "analysis_duration": (datetime.now() - start_time).total_seconds()
            }
    
    def _enhance_analysis_result(self, deep_result: Dict, start_time: datetime) -> Dict:
        """
        Enhance the deep exploration result with automation-specific analysis
        """
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        # Extract key metrics
        summary = deep_result.get("exploration_summary", {})
        discovered_states = deep_result.get("discovered_states", {})
        
        # Calculate automation-specific metrics
        automation_metrics = {
            "coverage_efficiency": self._calculate_coverage_efficiency(summary),
            "discovery_rate": summary.get("total_states_discovered", 0) / max(1, total_duration / 60),  # states per minute
            "interaction_success_rate": summary.get("success_rate", 0),
            "depth_coverage": self._analyze_depth_coverage(discovered_states),
            "functionality_coverage": self._analyze_functionality_coverage(discovered_states),
            "automation_score": 0  # Will be calculated below
        }
        
        # Calculate overall automation score (0-100)
        automation_metrics["automation_score"] = self._calculate_automation_score(automation_metrics, summary)
        
        # Enhanced result
        enhanced_result = deep_result.copy()
        enhanced_result.update({
            "automation_analysis": {
                "total_runtime_minutes": total_duration / 60,
                "automation_metrics": automation_metrics,
                "efficiency_assessment": self._assess_efficiency(automation_metrics),
                "coverage_assessment": self._assess_coverage(automation_metrics, summary),
                "recommendations": self._generate_recommendations(automation_metrics, summary)
            }
        })
        
        return enhanced_result
    
    def _calculate_coverage_efficiency(self, summary: Dict) -> float:
        """Calculate how efficiently we covered the application"""
        total_interactions = summary.get("total_interactions", 1)
        total_states = summary.get("total_states_discovered", 1)
        
        # Efficiency = states discovered per interaction
        return total_states / max(1, total_interactions) * 100
    
    def _analyze_depth_coverage(self, discovered_states: Dict) -> Dict:
        """Analyze coverage across different depths"""
        depth_counts = {}
        total_states = len(discovered_states)
        
        for state_data in discovered_states.values():
            depth = state_data.get("depth", 0)
            depth_counts[depth] = depth_counts.get(depth, 0) + 1
        
        return {
            "depth_distribution": depth_counts,
            "max_depth_reached": max(depth_counts.keys()) if depth_counts else 0,
            "average_depth": sum(d * c for d, c in depth_counts.items()) / max(1, total_states),
            "deep_states_ratio": sum(c for d, c in depth_counts.items() if d >= 3) / max(1, total_states)
        }
    
    def _analyze_functionality_coverage(self, discovered_states: Dict) -> Dict:
        """Analyze what types of functionality were discovered"""
        total_states = len(discovered_states)
        dialog_count = sum(1 for s in discovered_states.values() if s.get("is_dialog", False))
        menu_count = sum(1 for s in discovered_states.values() if s.get("is_menu", False))
        deadend_count = sum(1 for s in discovered_states.values() if s.get("is_deadend", False))
        
        return {
            "dialog_coverage": dialog_count / max(1, total_states) * 100,
            "menu_coverage": menu_count / max(1, total_states) * 100,
            "deadend_ratio": deadend_count / max(1, total_states) * 100,
            "functional_states": total_states - deadend_count,
            "functionality_diversity": len([t for t in ["dialog", "menu"] if 
                                          (t == "dialog" and dialog_count > 0) or 
                                          (t == "menu" and menu_count > 0)])
        }
    
    def _calculate_automation_score(self, automation_metrics: Dict, summary: Dict) -> float:
        """Calculate overall automation effectiveness score (0-100)"""
        
        # Weighted scoring components
        components = {
            "success_rate": summary.get("success_rate", 0) * 0.3,          # 30% weight
            "coverage_efficiency": automation_metrics["coverage_efficiency"] * 0.2,  # 20% weight
            "discovery_rate": min(automation_metrics["discovery_rate"] * 10, 100) * 0.2,  # 20% weight
            "depth_coverage": automation_metrics["depth_coverage"]["deep_states_ratio"] * 100 * 0.15,  # 15% weight
            "functionality_diversity": automation_metrics["functionality_coverage"]["functionality_diversity"] * 50 * 0.15  # 15% weight
        }
        
        return sum(components.values())
    
    def _assess_efficiency(self, automation_metrics: Dict) -> str:
        """Assess automation efficiency"""
        discovery_rate = automation_metrics["discovery_rate"]
        
        if discovery_rate >= 5:
            return "Excellent - Very high discovery rate"
        elif discovery_rate >= 3:
            return "Good - Solid discovery rate"
        elif discovery_rate >= 1:
            return "Fair - Moderate discovery rate"
        else:
            return "Poor - Low discovery rate"
    
    def _assess_coverage(self, automation_metrics: Dict, summary: Dict) -> str:
        """Assess coverage comprehensiveness"""
        automation_score = automation_metrics["automation_score"]
        
        if automation_score >= 80:
            return "Excellent - Comprehensive coverage achieved"
        elif automation_score >= 60:
            return "Good - Strong coverage with some gaps"
        elif automation_score >= 40:
            return "Fair - Moderate coverage, significant areas unexplored"
        else:
            return "Poor - Limited coverage, many areas missed"
    
    def _generate_recommendations(self, automation_metrics: Dict, summary: Dict) -> List[str]:
        """Generate recommendations for improving coverage"""
        recommendations = []
        
        success_rate = summary.get("success_rate", 0)
        if success_rate < 70:
            recommendations.append("Consider improving element detection accuracy - low success rate detected")
        
        discovery_rate = automation_metrics["discovery_rate"]
        if discovery_rate < 2:
            recommendations.append("Increase exploration time or reduce delays for better discovery rate")
        
        depth_coverage = automation_metrics["depth_coverage"]["deep_states_ratio"]
        if depth_coverage < 0.3:
            recommendations.append("Increase max_depth setting to explore deeper application layers")
        
        functionality_diversity = automation_metrics["functionality_coverage"]["functionality_diversity"]
        if functionality_diversity < 2:
            recommendations.append("Enable more interaction types (context menus, dialogs) for broader coverage")
        
        if not recommendations:
            recommendations.append("Excellent automation performance - no specific improvements needed")
        
        return recommendations
    
    def _generate_automated_report(self, result: Dict) -> None:
        """Generate and display automated analysis report"""
        
        if not result.get("success", False):
            self.console.print(Panel(
                f"[red]❌ Analysis Failed[/red]\n\n"
                f"Error: {result.get('error', 'Unknown error')}\n"
                f"Duration: {result.get('analysis_duration', 0):.1f} seconds",
                title="🤖 Automated Analysis Report",
                border_style="red"
            ))
            return
        
        # Extract data
        summary = result["exploration_summary"]
        automation_analysis = result["automation_analysis"]
        automation_metrics = automation_analysis["automation_metrics"]
        
        # Main report panel
        report_panel = Panel(
            f"[bold green]✅ Automated Analysis Complete![/bold green]\n\n"
            f"⏱️ Runtime: {automation_analysis['total_runtime_minutes']:.1f} minutes\n"
            f"🌍 States Discovered: {summary['total_states_discovered']}\n"
            f"🔍 Elements Analyzed: {summary['total_elements_discovered']}\n"
            f"🖱️ Interactions: {summary['total_interactions']} (Success: {summary['success_rate']:.1f}%)\n"
            f"📊 Automation Score: {automation_metrics['automation_score']:.1f}/100\n"
            f"🚀 Discovery Rate: {automation_metrics['discovery_rate']:.1f} states/minute\n"
            f"📄 Dialogs Found: {summary['dialogs_discovered']}\n"
            f"📋 Menus Found: {summary['menus_discovered']}\n"
            f"🌊 Max Depth: {summary['max_depth_reached']}",
            title="🤖 Automated Analysis Report",
            border_style="green"
        )
        
        self.console.print(report_panel)
        
        # Efficiency assessment
        efficiency_panel = Panel(
            f"[bold]Efficiency Assessment[/bold]\n\n"
            f"📈 {automation_analysis['efficiency_assessment']}\n"
            f"📊 {automation_analysis['coverage_assessment']}\n\n"
            f"[bold]Recommendations:[/bold]\n" + 
            "\n".join(f"• {rec}" for rec in automation_analysis['recommendations']),
            title="📊 Performance Analysis",
            border_style="blue"
        )
        
        self.console.print(efficiency_panel)
        
        # Save detailed report
        self._save_automation_report(result)
    
    def _save_automation_report(self, result: Dict) -> None:
        """Save detailed automation report to file"""
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            app_name = Path(self.app_executable_path).stem
            
            reports_dir = Path(__file__).parent / "automation_reports"
            reports_dir.mkdir(exist_ok=True)
            
            report_file = reports_dir / f"auto_analysis_{app_name}_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            
            self.console.print(f"[green]💾 Detailed automation report saved to: {report_file}[/green]")
            
        except Exception as e:
            self.console.print(f"[yellow]⚠️ Could not save automation report: {e}[/yellow]")


def main():
    """Main entry point for enhanced auto exploration"""
    
    parser = argparse.ArgumentParser(description="Enhanced Automated Deep Application Analysis")
    parser.add_argument("app_path", help="Path to application executable")
    parser.add_argument("--runtime", type=int, default=60, help="Maximum runtime in minutes (default: 60)")
    parser.add_argument("--max-states", type=int, default=1000, help="Maximum states to discover (default: 1000)")
    parser.add_argument("--max-depth", type=int, default=8, help="Maximum exploration depth (default: 8)")
    parser.add_argument("--no-dialogs", action="store_true", help="Skip dialog exploration")
    parser.add_argument("--no-menus", action="store_true", help="Skip menu exploration")
    parser.add_argument("--no-context", action="store_true", help="Skip context menu exploration")
    
    args = parser.parse_args()
    
    console = Console()
    
    # Validate app path
    if not Path(args.app_path).exists():
        console.print(f"[red]❌ Application not found: {args.app_path}[/red]")
        return 1
    
    # Create enhanced auto explorer
    explorer = EnhancedAutoExplorer(args.app_path, args.runtime)
    
    # Customize strategy based on arguments
    if args.max_states != 1000:
        explorer.exploration_strategy.max_total_states = args.max_states
    if args.max_depth != 8:
        explorer.exploration_strategy.max_depth = args.max_depth
    if args.no_dialogs:
        explorer.exploration_strategy.explore_dialogs = False
    if args.no_menus:
        explorer.exploration_strategy.explore_menus = False
    if args.no_context:
        explorer.exploration_strategy.explore_context_menus = False
    
    # Run automated analysis
    result = explorer.run_automated_analysis()
    
    # Return appropriate exit code
    return 0 if result.get("success", False) else 1


if __name__ == "__main__":
    exit(main()) 