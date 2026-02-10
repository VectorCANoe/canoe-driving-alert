#!/bin/bash
# Re-enable PlantUML themes after VSCode configuration
# Run this AFTER configuring VSCode to use local PlantUML CLI

PUML_DIR="/Users/juns/code/work/mobis/PBL/architecture/system-architecture/diagrams/puml"

echo "🎨 Re-enabling PlantUML themes in consolidated files..."

cd "$PUML_DIR"

# Replace commented theme with active theme
sed -i '' "s/^' !theme silver.*$/!theme silver/g" 00_architecture_overview.puml
sed -i '' "s/^' !theme silver.*$/!theme silver/g" 01_lighting_control.puml
sed -i '' "s/^' !theme silver.*$/!theme silver/g" 02_safety_system.puml
sed -i '' "s/^' !theme silver.*$/!theme silver/g" 03_ota_diagnostic.puml
sed -i '' "s/^' !theme silver.*$/!theme silver/g" 04_fault_injection.puml
sed -i '' "s/^' !theme silver.*$/!theme silver/g" 05_can_communication.puml

echo "✅ Themes re-enabled in all 6 consolidated .puml files"
echo ""
echo "📋 Next steps:"
echo "1. Restart VSCode completely"
echo "2. Open any .puml file"
echo "3. Press Alt+D (Option+D on Mac) to preview"
echo "4. Check version at bottom of preview window (should show 1.2026.1)"
echo ""
echo "If you see 'Syntax Error', the VSCode extension is still using the old version."
echo "Make sure you set 'Plantuml: Render = Local' in VSCode settings!"
