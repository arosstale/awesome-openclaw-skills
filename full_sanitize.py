#!/usr/bin/env python3
"""
Create fully sanitized README.md - removes high-risk skills
"""

import json
import re
from pathlib import Path

# Load suspicious skills
suspicious_file = Path('SUSPICIOUS_SKILLS.json')
with open(suspicious_file) as f:
    suspicious_skills = json.load(f)

# Get URLs to remove (high-risk only)
remove_urls = {s['url'] for s in suspicious_skills if s['risk'] == 'high'}
keep_urls = {s['url'] for s in suspicious_skills if s['risk'] == 'medium'}

print(f"🔒 Sanitizing README.md")
print(f"   Removing {len(remove_urls)} high-risk skills")
print(f"   Flagging {len(keep_urls)} medium-risk skills")

# Read README
readme_path = Path('README.md')
with open(readme_path) as f:
    lines = f.readlines()

# Process lines
removed_count = 0
flagged_count = 0
output_lines = []
in_code_block = False

for i, line in enumerate(lines):
    # Track code blocks
    if '```' in line:
        in_code_block = not in_code_block
        output_lines.append(line)
        continue

    # Preserve code blocks
    if in_code_block:
        output_lines.append(line)
        continue

    # Check for skill links
    url_match = re.search(r'https://github\.com/openclaw/skills/tree/main/[^)]+', line)
    if url_match:
        url = url_match.group()
        if url in remove_urls:
            removed_count += 1
            print(f"   ❌ Removed high-risk skill at line {i+1}")
            continue
        elif url in keep_urls:
            flagged_count += 1
            # Add warning comment
            output_lines.append(line.rstrip() + ' <!-- ⚠️ SECURITY REVIEW REQUIRED -->\n')
            continue

    output_lines.append(line)

# Add sanitization notice
SANITIZATION_NOTICE = """
---

## 🔒 Sanitization Notice

This README has been automatically sanitized on **2026-02-21**:

### Removed Skills (High Risk)
The following skills have been **removed** from this list:
- Skills that bypass CAPTCHA or bot detection
- Anti-detection browser automation tools
- Tools explicitly designed to evade security measures

### Flagged Skills (Medium Risk)
Some skills are **flagged** with security warnings and require manual review:
- Stealth browser automation
- VPN rotation for bypassing rate limits

**Recommendation:** Always review source code before installing any skill, and check VirusTotal reports on ClawHub.

---

"""

# Find where to insert notice (after first header section)
final_output = []
header_section_done = False

for line in output_lines:
    if not header_section_done and line.startswith('## ') and 'Why' in line:
        final_output.append(SANITIZATION_NOTICE)
        final_output.append(line)
        header_section_done = True
    else:
        final_output.append(line)

# Write output
output_path = Path('README_CLEAN.md')
with open(output_path, 'w') as f:
    f.writelines(final_output)

print(f"\n✅ Sanitization complete!")
print(f"   Removed: {removed_count} high-risk skills")
print(f"   Flagged: {flagged_count} medium-risk skills")
print(f"   Output: {output_path}")
print(f"   Original: {readme_path}")
