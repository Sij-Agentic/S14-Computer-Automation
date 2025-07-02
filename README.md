# S14 Computer Automation - Deep Application Explorer

A sophisticated framework for comprehensive application analysis and automation using computer vision, AI, and deep exploration strategies.

## 🚀 New: Deep Exploration System

This repository now includes advanced deep exploration capabilities that go far beyond surface-level analysis to discover all possible application states and functionality.

### Key Features

- **🔬 Deep Analysis**: Explores applications up to 10 levels deep
- **🧠 Intelligent Navigation**: Smart backtracking and state management
- **📊 Comprehensive Reporting**: Detailed metrics and visual hierarchy mapping
- **🤖 Full Automation**: Run completely automated analyses
- **🎯 Adaptive Strategies**: Configurable exploration parameters
- **📋 Advanced Classification**: Automatically identifies dialogs, menus, and UI patterns

## 🎯 Quick Start

### For Comprehensive Automated Analysis
```bash
# Full automated deep exploration (recommended)
python enhanced_auto_explore.py "C:\Program Files\YourApp\app.exe"

# Extended analysis with custom runtime
python enhanced_auto_explore.py "C:\Program Files\YourApp\app.exe" --runtime 120 --max-depth 10

# Quick assessment (15 minutes)
python enhanced_auto_explore.py "C:\Program Files\YourApp\app.exe" --runtime 15 --max-depth 6
```

### For Interactive Deep Exploration
```bash
# Interactive mode with full control
python deep_explore.py

# View comparison between old vs new approaches
python comparison_demo.py
```

## 📊 Exploration Approaches Comparison

| Feature | Old Approach | New Deep Exploration |
|---------|-------------|---------------------|
| **Depth** | Surface only | Up to 10 levels deep |
| **Coverage** | ~50 elements max | 1000+ states possible |
| **Intelligence** | Sequential clicking | Graph-based traversal |
| **Reporting** | Basic stats | Comprehensive analytics |
| **Automation** | Fixed iterations | Adaptive strategies |

## 🔧 Configuration Options

### Enhanced Auto Explorer Arguments
```bash
python enhanced_auto_explore.py <app_path> [options]

Options:
  --runtime MINUTES       Maximum runtime (default: 60)
  --max-states COUNT      Maximum states to discover (default: 1000)
  --max-depth LEVELS      Maximum exploration depth (default: 8)
  --no-dialogs           Skip dialog exploration
  --no-menus             Skip menu exploration
  --no-context           Skip context menu exploration
```

### Deep Explorer Features
- **Configurable depth limits**: Control how deep to explore nested UIs
- **State relationship mapping**: Track parent-child relationships between UI states
- **Smart backtracking**: Efficiently navigate complex application hierarchies
- **Performance metrics**: Detailed analysis of exploration effectiveness
- **Visual reporting**: Tree-structured view of discovered application states

## 📈 Expected Performance Improvements

- **Coverage**: 10-50x more comprehensive than old approach
- **Discovery**: Finds hidden features and nested functionality
- **Analysis**: Detailed metrics and actionable insights
- **Intelligence**: Adaptive exploration strategies
- **Efficiency**: Smart navigation and backtracking

## 🎛️ Legacy Commands (Deprecated)

The following commands are now superseded by the new deep exploration system:

```bash
# DEPRECATED - Use enhanced_auto_explore.py instead
uv run utils/fdom/element_interactor.py --app-name "app.exe" --interactive
python direct_explore.py
python auto_explore.py
```

## 📋 Example Applications

### Simple Applications (Notepad, Calculator)
```bash
python enhanced_auto_explore.py "C:\Windows\System32\notepad.exe" --runtime 30
```

### Complex Applications (Blender, Office)
```bash
python enhanced_auto_explore.py "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" --runtime 120 --max-depth 10
python enhanced_auto_explore.py "C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE" --runtime 90 --max-depth 8
```

### Media Players (VLC)
```bash
python enhanced_auto_explore.py "C:\Program Files\VideoLAN\VLC\vlc.exe" --runtime 60 --max-depth 7
```

## 📊 Output and Reports

The new system generates:

1. **Real-time Console Output**: Live progress with beautiful formatted displays
2. **State Hierarchy Trees**: Visual representation of discovered UI structures
3. **Comprehensive JSON Reports**: Detailed data for further analysis
4. **Performance Metrics**: Coverage efficiency, discovery rates, automation scores
5. **Actionable Recommendations**: Suggestions for improving exploration coverage

## 🔬 Technical Architecture

### Core Components
- **DeepExplorer**: Main orchestrator for comprehensive exploration
- **ExplorationStrategy**: Configurable parameters for exploration behavior
- **StateManager**: Advanced state tracking with NetworkX graphs
- **SeraphineIntegrator**: Computer vision and AI analysis
- **ElementInteractor**: Enhanced interaction engine with smart navigation

### Analysis Pipeline
1. **Application Launch**: Automated app startup and initial screenshot
2. **Computer Vision Analysis**: YOLO + OCR + Gemini AI for element detection
3. **Deep Exploration**: Graph-based traversal of all discoverable states
4. **Smart Navigation**: Intelligent backtracking and state management
5. **Comprehensive Reporting**: Multi-level analysis and recommendations

## 🎯 Use Cases

- **QA Testing**: Comprehensive UI coverage analysis
- **Application Mapping**: Complete feature discovery
- **Accessibility Auditing**: Deep UI structure analysis
- **Automation Development**: Discover interaction patterns
- **Competitive Analysis**: Understand application capabilities
- **Documentation**: Auto-generate feature maps

## 🚀 Getting Started

1. **Install Dependencies**: `uv install` or `pip install -r requirements.txt`
2. **Run Comparison Demo**: `python comparison_demo.py`
3. **Try Deep Exploration**: `python deep_explore.py`
4. **Full Automation**: `python enhanced_auto_explore.py "path/to/your/app.exe"`

The new deep exploration system represents a quantum leap in application analysis capabilities, providing unprecedented insight into application functionality and structure.