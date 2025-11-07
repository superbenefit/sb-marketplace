#!/usr/bin/env python3
"""
Package a skill into distributable ZIP archive.

Usage:
  python package_skill.py <skill-path> [--output <output-dir>]

Validates:
  - SKILL.md exists with valid frontmatter
  - Directory structure is correct
  - References are linked properly
  - Passes all validation checks

Examples:
  python package_skill.py ./my-skill
  python package_skill.py ./dao-knowledge --output ./dist
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
import zipfile


def validate_skill(skill_path):
    """Run validation checks before packaging."""

    # Find validate_skill.py in same directory as this script
    script_dir = Path(__file__).parent
    validate_script = script_dir / 'validate_skill.py'

    if not validate_script.exists():
        print(f"Warning: validate_skill.py not found at {validate_script}")
        print("Skipping validation checks...")
        return True

    print("Running validation checks...\n")

    try:
        result = subprocess.run(
            [sys.executable, str(validate_script), str(skill_path)],
            capture_output=True,
            text=True
        )

        # Print validation output
        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode != 0:
            print("\n❌ Skill validation failed. Please fix errors before packaging.")
            return False

        return True

    except Exception as e:
        print(f"Error running validation: {e}")
        print("Continuing with packaging anyway...\n")
        return True


def package_skill(skill_path, output_dir=None):
    """Create ZIP archive of skill."""

    skill_path = Path(skill_path)
    if not skill_path.exists():
        print(f"Error: Skill path {skill_path} does not exist")
        return False

    if not skill_path.is_dir():
        print(f"Error: {skill_path} is not a directory")
        return False

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        print(f"Error: SKILL.md not found in {skill_path}")
        return False

    # Determine output path
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path.cwd()

    skill_name = skill_path.name
    zip_path = output_dir / f"{skill_name}.zip"

    # Check if zip already exists
    if zip_path.exists():
        response = input(f"\n{zip_path} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Packaging cancelled.")
            return False

    print(f"\nPackaging skill: {skill_name}")
    print(f"Source: {skill_path}")
    print(f"Output: {zip_path}\n")

    # Create ZIP archive
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files in skill directory
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # Skip certain files
                    if any(part.startswith('.') for part in file_path.parts):
                        continue
                    if file_path.suffix in ['.pyc', '.pyo']:
                        continue
                    if '__pycache__' in str(file_path):
                        continue

                    # Add file to archive with relative path
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Adding: {arcname}")

        # Get final size
        zip_size = zip_path.stat().st_size
        print(f"\n✓ Skill packaged successfully!")
        print(f"  Archive: {zip_path}")
        print(f"  Size: {zip_size:,} bytes ({zip_size / 1024:.1f} KB)")

        # Print installation instructions
        print(f"\nTo install this skill:")
        print(f"  1. Extract {zip_path.name}")
        print(f"  2. Move to skills directory in a plugin")
        print(f"  3. Add to plugin.json skills array")
        print(f"  4. Install plugin via Claude Code\n")

        return True

    except Exception as e:
        print(f"\n❌ Error creating package: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Package skill into distributable ZIP archive',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--output', '-o', help='Output directory for ZIP file (default: current directory)')
    parser.add_argument('--skip-validation', action='store_true',
                        help='Skip validation checks (not recommended)')

    args = parser.parse_args()

    # Run validation unless skipped
    if not args.skip_validation:
        if not validate_skill(args.skill_path):
            sys.exit(1)

    # Package skill
    if not package_skill(args.skill_path, args.output):
        sys.exit(1)


if __name__ == '__main__':
    main()
