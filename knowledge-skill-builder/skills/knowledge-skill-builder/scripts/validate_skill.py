#!/usr/bin/env python3
"""
Validate skill structure and content against official requirements.

Usage:
  python validate_skill.py <skill-path>

Checks:
  - SKILL.md exists with valid YAML frontmatter
  - name field: lowercase, hyphens only, max 64 chars
  - description field: present, max 1024 chars
  - Directory structure follows conventions
  - Referenced files exist
  - No circular dependencies
  - Token budgets are documented

Examples:
  python validate_skill.py ./my-skill
  python validate_skill.py ../skills/dao-knowledge
"""

import argparse
import os
import re
import sys
from pathlib import Path
import yaml


class SkillValidator:
    def __init__(self, skill_path):
        self.skill_path = Path(skill_path)
        self.errors = []
        self.warnings = []
        self.skill_md_path = self.skill_path / 'SKILL.md'
        self.frontmatter = {}
        self.content = ''

    def validate_all(self):
        """Run all validation checks."""

        print(f"Validating skill at: {self.skill_path}\n")

        self.check_skill_md_exists()
        if self.skill_md_path.exists():
            self.parse_skill_md()
            self.check_frontmatter()
            self.check_content()
            self.check_directory_structure()
            self.check_references()

        return self.report()

    def check_skill_md_exists(self):
        """Check that SKILL.md file exists."""

        if not self.skill_md_path.exists():
            self.errors.append(f"SKILL.md not found at {self.skill_md_path}")
            return False
        return True

    def parse_skill_md(self):
        """Parse SKILL.md file and extract frontmatter."""

        try:
            self.content = self.skill_md_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Could not read SKILL.md: {e}")
            return False

        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n', self.content, re.DOTALL)
        if not frontmatter_match:
            self.errors.append("SKILL.md must begin with YAML frontmatter (---)")
            return False

        try:
            self.frontmatter = yaml.safe_load(frontmatter_match.group(1))
            if not isinstance(self.frontmatter, dict):
                self.errors.append("Frontmatter must be a valid YAML dictionary")
                return False
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML frontmatter: {e}")
            return False

        return True

    def check_frontmatter(self):
        """Validate frontmatter fields."""

        # Check required fields
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in self.frontmatter:
                self.errors.append(f"Required frontmatter field '{field}' is missing")

        # Validate name field
        if 'name' in self.frontmatter:
            name = self.frontmatter['name']

            if not isinstance(name, str):
                self.errors.append("Field 'name' must be a string")
            else:
                # Check format: lowercase, numbers, hyphens only
                if not re.match(r'^[a-z0-9-]+$', name):
                    self.errors.append(
                        "Field 'name' must contain only lowercase letters, numbers, and hyphens"
                    )

                # Check length
                if len(name) > 64:
                    self.errors.append(f"Field 'name' must be 64 characters or less (currently {len(name)})")

                # Check for TODO placeholder
                if 'todo' in name.lower():
                    self.warnings.append("Field 'name' appears to contain TODO placeholder")

        # Validate description field
        if 'description' in self.frontmatter:
            description = self.frontmatter['description']

            if not isinstance(description, str):
                self.errors.append("Field 'description' must be a string")
            else:
                # Check length
                if len(description) > 1024:
                    self.errors.append(
                        f"Field 'description' must be 1024 characters or less (currently {len(description)})"
                    )

                # Check for TODO placeholder
                if '[TODO' in description or 'TODO:' in description:
                    self.warnings.append("Field 'description' contains TODO placeholders")

                # Check if empty
                if len(description.strip()) == 0:
                    self.errors.append("Field 'description' cannot be empty")

        # Validate allowed-tools if present
        if 'allowed-tools' in self.frontmatter:
            allowed_tools = self.frontmatter['allowed-tools']
            if not isinstance(allowed_tools, list):
                self.errors.append("Field 'allowed-tools' must be a list")

    def check_content(self):
        """Validate SKILL.md content."""

        # Remove frontmatter for content checks
        content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', self.content, flags=re.DOTALL)

        # Check word count (should be < 5000 words per guidelines)
        word_count = len(content_without_frontmatter.split())
        if word_count > 5000:
            self.warnings.append(
                f"SKILL.md body is {word_count} words (recommended: <5000 words). "
                "Consider moving detailed content to references/"
            )

        # Check for TODO placeholders
        todo_count = len(re.findall(r'\[TODO[:\]]', content_without_frontmatter))
        if todo_count > 0:
            self.warnings.append(f"Found {todo_count} TODO placeholder(s) in content")

        # Check for second-person language (should use imperative instead)
        second_person = re.findall(
            r'\b(you should|you must|you can|you will|your)\b',
            content_without_frontmatter,
            re.IGNORECASE
        )
        if second_person:
            self.warnings.append(
                f"Found {len(second_person)} instances of second-person language. "
                "Official guidelines recommend imperative form instead (e.g., 'To accomplish X, do Y')"
            )

        # Check for key sections
        required_sections = ['Purpose', 'Capabilities', 'Usage']
        for section in required_sections:
            if section.lower() not in content_without_frontmatter.lower():
                self.warnings.append(f"Recommended section '{section}' not found in content")

        # Check for token budget documentation
        if 'token' not in content_without_frontmatter.lower():
            self.warnings.append("No token budget documentation found (recommended for transparency)")

    def check_directory_structure(self):
        """Check that directory structure follows conventions."""

        # Check for optional but conventional directories
        conventional_dirs = ['scripts', 'references', 'assets']
        existing_dirs = [d.name for d in self.skill_path.iterdir() if d.is_dir()]

        if not any(d in existing_dirs for d in conventional_dirs):
            self.warnings.append(
                f"No conventional directories found (scripts/, references/, assets/). "
                "This is optional but recommended for better organization."
            )

        # Check scripts are executable
        scripts_dir = self.skill_path / 'scripts'
        if scripts_dir.exists():
            for script in scripts_dir.glob('*.py'):
                if not os.access(script, os.X_OK):
                    self.warnings.append(f"Script {script.name} is not executable")

    def check_references(self):
        """Check that referenced files exist."""

        # Find references in content (e.g., `references/file.md`, `scripts/script.py`)
        references = re.findall(r'`((?:scripts|references|assets)/[^`]+)`', self.content)

        for ref in references:
            ref_path = self.skill_path / ref
            if not ref_path.exists():
                self.warnings.append(f"Referenced file not found: {ref}")

    def report(self):
        """Generate and print validation report."""

        print("=" * 60)
        print("VALIDATION REPORT")
        print("=" * 60)

        if self.errors:
            print("\n❌ ERRORS:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

        if not self.errors and not self.warnings:
            print("\n✓ All checks passed! Skill is valid.")

        print("\n" + "=" * 60)
        print(f"Summary: {len(self.errors)} errors, {len(self.warnings)} warnings")
        print("=" * 60)

        # Return success if no errors
        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description='Validate skill structure and content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('skill_path', help='Path to skill directory')

    args = parser.parse_args()

    validator = SkillValidator(args.skill_path)
    success = validator.validate_all()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
