#!/usr/bin/env python3
"""
Extract PlantUML diagrams from markdown files and save as .puml files
"""

import re
import os
from pathlib import Path

def extract_plantuml_blocks(md_content):
    """Extract all PlantUML code blocks from markdown content"""
    pattern = r'```plantuml\n(.*?)```'
    matches = re.findall(pattern, md_content, re.DOTALL)
    return matches

def process_markdown_file(md_path, output_dir):
    """Process a single markdown file and extract PlantUML diagrams"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = extract_plantuml_blocks(content)
    
    if not blocks:
        print(f"No PlantUML blocks found in {md_path}")
        return
    
    base_name = Path(md_path).stem
    
    for idx, block in enumerate(blocks, 1):
        if len(blocks) == 1:
            output_file = output_dir / f"{base_name}.puml"
        else:
            output_file = output_dir / f"{base_name}_{idx:02d}.puml"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(block)
        
        print(f"✅ Created: {output_file}")

def main():
    # Directories
    arch_dir = Path("/Users/juns/code/work/mobis/PBL/architecture/system-architecture")
    diagrams_dir = arch_dir / "diagrams"
    puml_dir = diagrams_dir / "puml"
    
    # Create output directory
    puml_dir.mkdir(exist_ok=True)
    
    # Process architecture_overview.md
    print("\n📄 Processing architecture_overview.md...")
    process_markdown_file(arch_dir / "architecture_overview.md", puml_dir)
    
    # Process all diagram markdown files
    print("\n📁 Processing diagram files...")
    for md_file in diagrams_dir.glob("*.md"):
        print(f"\n📄 Processing {md_file.name}...")
        process_markdown_file(md_file, puml_dir)
    
    print(f"\n✅ All PlantUML diagrams extracted to: {puml_dir}")
    print(f"\n💡 You can now use VSCode PlantUML extension to render .puml files")

if __name__ == "__main__":
    main()
