#!/usr/bin/env python3
"""
Comprehensive sanitizer and scanner for awesome-openclaw-skills
- Extracts all skill URLs
- Categorizes skills
- Flags suspicious ones
- Generates report
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

# Categories based on skill names/descriptions
CATEGORIES = {
    'security': [r'security', r'pentest', r'vulnerability', r'audit', r'cve', r'exploit'],
    'crypto': [r'crypto', r'bitcoin', r'ethereum', r'web3', r'defi', r'nft', r'trading'],
    'bot': [r'bot', r'automation', r'scraper', r'crawler', r'proxy'],
    'media': [r'image', r'video', r'audio', r'stream', r'youtube'],
    'dev': [r'github', r'git', r'docker', r'kubernetes', r'ci/cd', r'build'],
}

# Suspicious patterns
SUSPICIOUS_PATTERNS = {
    'critical': [
        r'keylogger',
        r'password.*steal',
        r'credit.*card.*dump',
        r'backdoor.*generator',
        r'malware.*generator',
        r'phish',
        r'skimmer',
    ],
    'high': [
        r'bypass.*captcha',
        r'captcha.*solver',
        r'evad.*detect',
        r'anti.*detect.*browser',
        r'bot.*detector.*evad',
        r'ip.*rotat.*bypass',
    ],
    'medium': [
        r'stealth.*browser',
        r'anti.*detect',
        r'anonymous.*browse',
        r'rotate.*vpn',
    ],
}

def extract_skills(readme_path):
    """Extract all skills from README"""
    skills = []
    current_category = None

    with open(readme_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Track category
        if line.startswith('### ') and 'Table of Contents' not in line:
            current_category = line.strip('# \n')
            continue

        # Extract skill links
        skill_match = re.match(r'- \[([^\]]+)\]\((https://[^)]+)\)\s+-\s+(.+)', line)
        if skill_match:
            name, url, description = skill_match.groups()
            skills.append({
                'name': name,
                'url': url,
                'description': description,
                'category': current_category,
                'risk': 'low',
                'risk_reason': None,
            })

    return skills

def assess_risk(skill):
    """Assess risk level of a skill"""
    description = f"{skill['name']} {skill['description']}".lower()

    # Check critical patterns
    for pattern in SUSPICIOUS_PATTERNS['critical']:
        if re.search(pattern, description):
            return 'critical', f"Matches critical pattern: {pattern}"

    # Check high patterns
    for pattern in SUSPICIOUS_PATTERNS['high']:
        if re.search(pattern, description):
            return 'high', f"Matches high-risk pattern: {pattern}"

    # Check medium patterns
    for pattern in SUSPICIOUS_PATTERNS['medium']:
        if re.search(pattern, description):
            return 'medium', f"Matches medium-risk pattern: {pattern}"

    return 'low', None

def categorize_skill(skill):
    """Categorize skill by keywords"""
    text = f"{skill['name']} {skill['description']}".lower()
    categories = []

    for category, patterns in CATEGORIES.items():
        for pattern in patterns:
            if re.search(pattern, text):
                categories.append(category)
                break

    return categories or ['general']

def generate_report(skills, output_path):
    """Generate comprehensive report"""
    # Assess all skills
    by_risk = defaultdict(list)
    by_category = defaultdict(list)
    suspicious_count = 0

    for skill in skills:
        risk, reason = assess_risk(skill)
        skill['risk'] = risk
        skill['risk_reason'] = reason

        if risk != 'low':
            suspicious_count += 1

        by_risk[risk].append(skill)

        categories = categorize_skill(skill)
        for cat in categories:
            by_category[cat].append(skill)

    # Generate report
    report = {
        'total_skills': len(skills),
        'suspicious_skills': suspicious_count,
        'by_risk': {k: len(v) for k, v in by_risk.items()},
        'by_category': {k: len(v) for k, v in sorted(by_category.items())},
        'critical_risk': [s['name'] for s in by_risk['critical']],
        'high_risk': [s['name'] for s in by_risk['high']],
        'medium_risk': [s['name'] for s in by_risk['medium']],
    }

    # Write JSON report
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 SKILLS SANITIZATION REPORT")
    print(f"{'='*60}")
    print(f"\nTotal Skills: {report['total_skills']}")
    print(f"Suspicious: {report['suspicious_skills']} ({report['suspicious_skills']/report['total_skills']*100:.1f}%)")
    print(f"\nBy Risk Level:")
    for risk, count in sorted(report['by_risk'].items(), key=lambda x: {'critical':0,'high':1,'medium':2,'low':3}.get(x[0],4)):
        emoji = {'critical': '🚨', 'high': '⚠️', 'medium': '⚡', 'low': '✅'}.get(risk, '❓')
        print(f"  {emoji} {risk.upper():8} : {count:4} skills")
    print(f"\nBy Category:")
    for cat, count in sorted(report['by_category'].items(), key=lambda x: -x[1])[:10]:
        print(f"  • {cat:20} : {count:4} skills")

    if report['critical_risk']:
        print(f"\n🚨 CRITICAL RISK SKILLS ({len(report['critical_risk'])}):")
        for name in report['critical_risk']:
            print(f"   - {name}")

    if report['high_risk']:
        print(f"\n⚠️  HIGH RISK SKILLS ({len(report['high_risk'])}):")
        for name in report['high_risk']:
            print(f"   - {name}")

    print(f"\n📄 Detailed report saved to: {output_path}")
    print(f"{'='*60}\n")

    return report

def main():
    readme = Path('README.md')
    report_path = Path('SANITIZATION_REPORT.json')

    if not readme.exists():
        print(f"❌ Error: {readme} not found")
        return

    print(f"🔍 Scanning {readme}...")

    skills = extract_skills(readme)
    print(f"✓ Found {len(skills)} skills")

    report = generate_report(skills, report_path)

    # Save suspicious skills list
    suspicious = [s for s in skills if s['risk'] != 'low']
    if suspicious:
        with open('SUSPICIOUS_SKILLS.json', 'w') as f:
            json.dump(suspicious, f, indent=2)
        print(f"⚠️  Suspicious skills saved to: SUSPICIOUS_SKILLS.json")

if __name__ == '__main__':
    main()
