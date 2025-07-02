# Deep Exploration System - Usage Guide

## 🚀 Quick Start

### 1. Validate System Setup
```bash
# Test that everything is installed correctly
python test_deep_exploration.py
```

### 2. See the Improvements
```bash
# View comparison between old vs new approaches
python comparison_demo.py
```

### 3. Run Automated Deep Analysis
```bash
# Basic automated analysis (60 minutes)
python enhanced_auto_explore.py "C:\Program Files\YourApp\app.exe"

# Extended analysis (2 hours, deeper exploration)
python enhanced_auto_explore.py "C:\Program Files\YourApp\app.exe" --runtime 120 --max-depth 10

# Quick assessment (15 minutes)
python enhanced_auto_explore.py "C:\Program Files\YourApp\app.exe" --runtime 15 --max-depth 6
```

### 4. Interactive Deep Exploration
```bash
# Interactive mode with full control
python deep_explore.py
```

## 📊 What's New vs Old System

| Capability | Old System | New Deep System |
|------------|------------|-----------------|
| **Exploration Depth** | Surface only (1 level) | Up to 10 levels deep |
| **Element Discovery** | ~50 elements max | 1000+ states possible |
| **Navigation** | Basic click-through | Smart backtracking |
| **State Tracking** | Simple success/fail | Full state graph with relationships |
| **Reporting** | Basic console output | Rich analytics + visual trees |
| **Automation** | Fixed 50 iterations | Adaptive strategies with time limits |
| **Analysis** | Count of interactions | Coverage metrics, efficiency scores |

## 🎯 Use Cases & Examples

### Simple Applications
**Notepad, Calculator, Simple Utilities**
```bash
# 30-minute analysis is usually sufficient
python enhanced_auto_explore.py "C:\Windows\System32\notepad.exe" --runtime 30 --max-depth 5
```

**Expected Results:**
- Discovers all menu items and dialogs
- Maps keyboard shortcuts
- Finds preferences and settings
- Explores help systems

### Complex Applications  
**Blender, PhotoShop, IDEs, Office Suite**
```bash
# 2+ hour analysis for comprehensive coverage
python enhanced_auto_explore.py "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" --runtime 120 --max-depth 10
```

**Expected Results:**
- Maps entire menu hierarchy
- Discovers tool panels and modifiers
- Explores render settings and materials
- Finds advanced configuration options
- Maps plugin/addon interfaces

### Media Applications
**VLC, Windows Media Player, Spotify**
```bash
# 60-90 minute analysis
python enhanced_auto_explore.py "C:\Program Files\VideoLAN\VLC\vlc.exe" --runtime 90 --max-depth 8
```

**Expected Results:**
- Discovers all media format support
- Maps audio/video settings
- Finds codec options
- Explores playlist and library features
- Maps equalizer and effects

## ⚙️ Configuration Options

### Enhanced Auto Explorer Parameters
```bash
python enhanced_auto_explore.py <app_path> [options]

# Core Parameters
--runtime MINUTES       # Maximum runtime (default: 60)
--max-states COUNT      # Maximum states to discover (default: 1000)  
--max-depth LEVELS      # Maximum exploration depth (default: 8)

# Feature Toggles
--no-dialogs           # Skip dialog box exploration
--no-menus             # Skip menu system exploration  
--no-context           # Skip context menu exploration
```

### Strategy Examples
```bash
# Quick Assessment (good for CI/CD)
python enhanced_auto_explore.py app.exe --runtime 15 --max-depth 4

# Balanced Analysis (recommended for most apps)
python enhanced_auto_explore.py app.exe --runtime 60 --max-depth 8

# Comprehensive Analysis (for complex applications)
python enhanced_auto_explore.py app.exe --runtime 180 --max-depth 12

# Menu-focused Analysis
python enhanced_auto_explore.py app.exe --runtime 45 --no-dialogs --max-depth 6

# Dialog-focused Analysis  
python enhanced_auto_explore.py app.exe --runtime 45 --no-menus --max-depth 8
```

## 📊 Understanding the Output

### Real-time Console Output
- **Live Progress**: See states being discovered in real-time
- **Interaction Results**: Success/failure of each click
- **Navigation Updates**: State transitions and backtracking
- **Discovery Notifications**: New dialogs, menus, and features found

### Final Reports
The system generates comprehensive reports including:

#### 1. Summary Statistics
- Total states discovered
- Elements analyzed
- Interaction success rate
- Discovery rate (states per minute)
- Coverage efficiency

#### 2. State Hierarchy Tree
Visual representation showing:
- Parent-child relationships between UI states
- Depth levels achieved
- Dialog and menu classifications
- Dead-end identification

#### 3. Performance Metrics
- **Automation Score** (0-100): Overall effectiveness
- **Coverage Efficiency**: States discovered per interaction
- **Depth Distribution**: How many states at each level
- **Functionality Coverage**: Types of UI elements found

#### 4. Actionable Recommendations
- Suggestions for improving coverage
- Performance optimization tips
- Configuration adjustments

### Sample Output Analysis
```
🎯 Deep Exploration Complete!

⏱️ Runtime: 62.3 minutes
🌍 States Discovered: 247
🔍 Elements Analyzed: 1,832
🖱️ Interactions: 405 (Success: 87.2%)
📊 Automation Score: 84.5/100
🚀 Discovery Rate: 4.0 states/minute
📄 Dialogs Found: 23
📋 Menus Found: 31
🌊 Max Depth: 8

Efficiency Assessment: Good - Solid discovery rate
Coverage Assessment: Excellent - Comprehensive coverage achieved
```

## 🎛️ Advanced Usage

### Interactive Deep Exploration
```bash
python deep_explore.py
```

This provides:
- Manual control over exploration strategy
- Real-time configuration adjustment
- Step-by-step state navigation
- Custom depth and timeout settings

### Batch Analysis
```bash
# Analyze multiple applications
for app in "notepad.exe" "calc.exe" "mspaint.exe"; do
    python enhanced_auto_explore.py "C:\Windows\System32\$app" --runtime 30
done
```

### Integration with CI/CD
```bash
# Quick validation in automated pipeline
python enhanced_auto_explore.py "$APP_PATH" --runtime 10 --max-depth 3 --no-context
```

## 🔧 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Verify system setup
python test_deep_exploration.py

# Install missing dependencies
uv install
```

#### Application Launch Failures
- Verify application path is correct
- Check application permissions
- Ensure app can be launched normally
- Try using shorter paths or UNC paths

#### Low Discovery Rates
- Increase `--runtime` parameter
- Increase `--max-depth` parameter  
- Check if app requires specific startup conditions
- Verify app is not showing splash screens or loading dialogs

#### Memory/Performance Issues
- Reduce `--max-states` parameter
- Decrease `--max-depth` 
- Use `--no-context` to skip context menus
- Monitor system resources during long runs

### Optimization Tips

#### For Complex Applications
- Start with shorter runtime (30 min) to assess coverage rate
- Gradually increase depth based on initial results
- Use feature flags to focus on specific UI areas
- Consider running multiple focused sessions

#### For Simple Applications  
- Use shorter runtimes (15-30 minutes)
- Lower max-depth (4-6 levels)
- Enable all feature exploration
- Focus on comprehensive coverage

## 📈 Migration from Old System

### Deprecated Scripts
❌ **Don't use these anymore:**
- `direct_explore.py` 
- `auto_explore.py`
- Manual `element_interactor.py` calls

### Migration Steps
1. **Test new system**: `python test_deep_exploration.py`
2. **Compare approaches**: `python comparison_demo.py`  
3. **Replace old calls**: Use `enhanced_auto_explore.py` instead
4. **Adjust parameters**: Set appropriate runtime and depth for your apps
5. **Update documentation**: Reference new command structure

### Command Translation
```bash
# OLD (deprecated)
python direct_explore.py
python auto_explore.py

# NEW (recommended)  
python enhanced_auto_explore.py "app.exe" --runtime 60 --max-depth 8
```

## 🎯 Best Practices

### Runtime Planning
- **Simple apps**: 15-30 minutes
- **Medium apps**: 30-90 minutes  
- **Complex apps**: 90-180 minutes
- **Unknown apps**: Start with 30 minutes, then extend

### Depth Configuration
- **Start conservative**: Begin with depth 6-8
- **Increase gradually**: Add depth based on results
- **Monitor performance**: Higher depth = longer runtime
- **App complexity**: Complex apps benefit from deeper exploration

### Resource Management
- **Monitor CPU/Memory**: Long runs can be resource intensive
- **Plan timing**: Run during off-hours for complex analysis
- **Save progress**: Reports are auto-saved for later review
- **Parallel analysis**: Can run multiple simple apps simultaneously

## 📋 Output Files

### Generated Reports
```
automation_reports/
├── auto_analysis_notepad_20241201_143022.json
├── auto_analysis_vlc_20241201_151543.json
└── ...

apps/
├── notepad/
│   ├── fdom.json
│   ├── screenshots/
│   └── deep_exploration_report_20241201_143022.json
└── ...
```

### Report Contents
- **Detailed exploration log**: Every interaction and result
- **State relationship graph**: Parent-child mappings
- **Element classifications**: Dialog/menu/button categorization
- **Performance analytics**: Timing and efficiency metrics
- **Actionable insights**: Recommendations for improvement

The new deep exploration system provides unprecedented insight into application functionality and represents a major advancement in automated application analysis capabilities. 