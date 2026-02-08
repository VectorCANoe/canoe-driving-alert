#!/usr/bin/env python3
"""
Create consolidated PlantUML files - one file per subsystem with all diagrams
"""

import re
from pathlib import Path

def extract_plantuml_blocks(md_content):
    """Extract all PlantUML code blocks with their titles"""
    # Find all plantuml blocks
    pattern = r'```plantuml\n(.*?)```'
    blocks = re.findall(pattern, md_content, re.DOTALL)
    
    # Find titles before each plantuml block
    title_pattern = r'##\s+\d+\.\s+(.+?)\n\n```plantuml'
    titles = re.findall(title_pattern, md_content, re.DOTALL)
    
    return list(zip(titles, blocks)) if titles else [(f"Diagram {i+1}", block) for i, block in enumerate(blocks)]

def create_consolidated_file(md_path, output_path):
    """Create a single .puml file with all diagrams from a markdown file"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    diagrams = extract_plantuml_blocks(content)
    
    if not diagrams:
        return
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, (title, block) in enumerate(diagrams, 1):
            # Add separator comment
            f.write(f"' ============================================\n")
            f.write(f"' {idx}. {title}\n")
            f.write(f"' ============================================\n\n")
            
            # Write the diagram
            f.write(block)
            f.write("\n\n")
            
            # Add newpage for multi-page rendering (except last diagram)
            if idx < len(diagrams):
                f.write("@newpage\n\n")
    
    print(f"✅ Created: {output_path.name} ({len(diagrams)} diagrams)")

def main():
    arch_dir = Path("/Users/juns/code/work/mobis/PBL/architecture/system-architecture")
    diagrams_dir = arch_dir / "diagrams"
    puml_dir = diagrams_dir / "puml"
    
    # Create consolidated files
    files_to_process = [
        (arch_dir / "architecture_overview.md", puml_dir / "00_architecture_overview.puml"),
        (diagrams_dir / "lighting_control_architecture.md", puml_dir / "01_lighting_control.puml"),
        (diagrams_dir / "safety_system_architecture.md", puml_dir / "02_safety_system.puml"),
        (diagrams_dir / "ota_diagnostic_sequence.md", puml_dir / "03_ota_diagnostic.puml"),
        (diagrams_dir / "fault_injection_workflow.md", puml_dir / "04_fault_injection.puml"),
        (diagrams_dir / "can_communication_stack.md", puml_dir / "05_can_communication.puml"),
    ]
    
    print("\n📦 Creating consolidated PlantUML files...\n")
    
    for md_file, puml_file in files_to_process:
        if md_file.exists():
            create_consolidated_file(md_file, puml_file)
    
    print(f"\n✅ All consolidated files created in: {puml_dir}")
    print(f"\n💡 Each .puml file contains all diagrams for that subsystem")
    print(f"   Use @newpage navigation in PlantUML preview to switch between diagrams")

if __name__ == "__main__":
    main()
