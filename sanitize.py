#!/usr/bin/env python3
"""
Sanitize awesome-openclaw-skills README.md
Remove or flag potentially dangerous skills
"""

import re
import sys
from pathlib import Path

# Potentially dangerous patterns to flag
DANGEROUS_PATTERNS = {
    'high_risk': [
        r'keylogger',
        r'steal.*password',
        r'credit.*card.*dump',
        r'skimmer',
        r'malware.*generator',
        r'backdoor.*generator',
    ],
    'medium_risk': [
        r'bypass.*captcha',
        r'captcha.*solver',
        r'bot.*detector.*evad',
        r'evasion.*technique',
        r'anti.*detect',
    ],
}

# Skills to remove (by description patterns)
REMOVE_PATTERNS = [
    r'.*keylogger.*',
    r'.*steal.*credit.*card.*',
    r'.*generate.*backdoor.*',
]

# Add additional security warning
SECURITY_WARNING = """
---

## ⚠️ Additional Security Notice (Sanitized)

This list has been automatically sanitized to remove the most high-risk entries. However:
- **Always review source code** before installing any skill
- **Check VirusTotal reports** on ClawHub for each skill
- **Test in isolated environment** before production use
- **Report suspicious skills** to maintainers

### Removed Categories:
- Keyloggers and password stealers
- Backdoor generators
- Credit card skimmers
- Malware generation tools

---

"""

def is_high_risk(line: str) -> tuple[bool, str]:
    """Check if line matches high-risk patterns"""
    for pattern in DANGEROUS_PATTERNS['high_risk']:
        if re.search(pattern, line, re.IGNORECASE):
            return True, pattern
    return False, None

def is_medium_risk(line: str) -> tuple[bool, str]:
    """Check if line matches medium-risk patterns"""
    for pattern in DANGEROUS_PATTERNS['medium_risk']:
        if re.search(pattern, line, re.IGNORECASE):
            return True, pattern
    return False, None

def should_remove(line: str) -> bool:
    """Check if line should be removed"""
    for pattern in REMOVE_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False

def sanitize_readme(input_file: Path, output_file: Path):
    """Sanitize the README.md file"""
    removed_count = 0
    flagged_count = 0
    in_code_block = False

    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    output_lines = []

    for line in lines:
        # Track code blocks
        if '```' in line:
            in_code_block = not in_code_block

        # Skip if in code block (preserve code examples)
        if in_code_block:
            output_lines.append(line)
            continue

        # Check for removal
        if should_remove(line):
            removed_count += 1
            print(f"❌ REMOVED: {line.strip()[:80]}...")
            continue

        # Check for high risk
        high_risk, pattern = is_high_risk(line)
        if high_risk:
            removed_count += 1
            print(f"🚨 HIGH RISK REMOVED ({pattern}): {line.strip()[:80]}...")
            continue

        # Check for medium risk - flag with warning
        medium_risk, pattern = is_medium_risk(line)
        if medium_risk:
            flagged_count += 1
            print(f"⚠️  FLAGGED ({pattern}): {line.strip()[:80]}...")
            # Add warning comment
            output_lines.append(line.rstrip() + ' <!-- ⚠️ Requires security review -->\n')
        else:
            output_lines.append(line)

    # Find location to insert security warning (after first "---" separator)
    warning_inserted = False
    final_output = []
    separator_count = 0

    for line in output_lines:
        if line.startswith('---'):
            separator_count += 1
            if separator_count == 1 and not warning_inserted:
                final_output.append(line)
                final_output.append(SECURITY_WARNING)
                warning_inserted = True
                continue
        final_output.append(line)

    # Write output
    with open(output_file, 'w') as outfile:
        outfile.writelines(final_output)

    print(f"\n✅ Sanitization complete!")
    print(f"   Removed: {removed_count} high-risk entries")
    print(f"   Flagged: {flagged_count} medium-risk entries")
    print(f"   Output: {output_file}")

def main():
    input_file = Path('README.md')
    output_file = Path('README_SANITIZED.md')

    if not input_file.exists():
        print(f"❌ Error: {input_file} not found")
        sys.exit(1)

    print(f"🔒 Sanitizing {input_file}...")
    sanitize_readme(input_file, output_file)

if __name__ == '__main__':
    main()
