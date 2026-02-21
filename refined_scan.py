#!/usr/bin/env python3
"""
Refined GitHub skills sanitization with more precise patterns
"""

import json
import re

# More precise suspicious patterns - only catch actual malicious terms
SUSPICIOUS_PATTERNS = {
    'critical': [
        r'keylogger',
        r'password.*steal',
        r'credit.*card.*dump',
        r'backdoor',
        r'malware',
        r'phish.*ing',  # Must be phishing action, not just fish or phishing-protected
        r'skimmer',
        r'exploit',
    ],
    'high': [
        r'bypass.*captcha',
        r'captcha.*bypass',
        r'captcha.*solver',
        r'evade.*detect',
        r'evad.*detect',
        r'anti.*detect.*browser',
        r'bot.*detector.*evad',
        r'ip.*rotat.*bypass',
        r'brute.*force',
        r'403.*bypass',
    ],
    'medium': [
        r'stealth.*browser',
        r'anonymous.*browser',
        r'rotate.*vpn',
        r'proxy.*bypass',
        r'unblock.*proxy',
    ],
}

def assess_risk(path):
    """Assess risk based on path with more precise patterns"""
    text = path.lower()

    for pattern in SUSPICIOUS_PATTERNS['critical']:
        if re.search(pattern, text):
            return 'critical', f"Critical: {pattern}"

    for pattern in SUSPICIOUS_PATTERNS['high']:
        if re.search(pattern, text):
            return 'high', f"High: {pattern}"

    for pattern in SUSPICIOUS_PATTERNS['medium']:
        if re.search(pattern, text):
            return 'medium', f"Medium: {pattern}"

    return 'low', None

def main():
    # Read the full GitHub tree
    tree_file = "/home/majinbu/pi-mono-workspace/awesome-openclaw-skills/GITHUB_TREE_FULL.json"

    with open(tree_file, 'r') as f:
        tree_data = json.load(f)

    # Extract skill directories
    skills = set()
    tree_items = tree_data.get('tree', [])

    for item in tree_items:
        path = item['path']
        type = item['type']

        if type == 'tree':
            parts = path.split('/')
            if len(parts) >= 3 and parts[0] == 'skills':
                skill_path = '/'.join(parts[:3])
                skills.add(skill_path)

    skills = sorted(list(skills))
    print(f"✓ Extracted {len(skills)} skill directories")

    # Assess risk with refined patterns
    risk_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    suspicious = []

    for i, skill_path in enumerate(skills):
        if i % 500 == 0:
            print(f"   Processing {i}/{len(skills)}...")

        risk, reason = assess_risk(skill_path)
        risk_counts[risk] += 1

        if risk in ['critical', 'high', 'medium']:
            suspicious.append({
                'path': skill_path,
                'name': skill_path.split('/')[-1],
                'risk': risk,
                'reason': reason,
                'url': f"https://github.com/openclaw/skills/tree/main/{skill_path}"
            })

    # Generate report
    report = {
        'total_analyzed': len(skills),
        'risk_counts': risk_counts,
        'suspicious_by_risk': {
            'critical': len([s for s in suspicious if s['risk'] == 'critical']),
            'high': len([s for s in suspicious if s['risk'] == 'high']),
            'medium': len([s for s in suspicious if s['risk'] == 'medium']),
        },
        'suspicious_skills': suspicious
    }

    # Save report
    output_file = "/home/majinbu/pi-mono-workspace/awesome-openclaw-skills/GITHUB_REFINED_SCAN_REPORT.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n📄 Report saved to: {output_file}")

    # Save suspicious skills list
    suspicious_file = "/home/majinbu/pi-mono-workspace/awesome-openclaw-skills/GITHUB_SUSPICIOUS_REFINED.json"
    with open(suspicious_file, 'w') as f:
        json.dump(suspicious, f, indent=2)
    print(f"🚨 Suspicious skills saved to: {suspicious_file}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 GITHUB SKILLS SANITIZATION REPORT (Refined)")
    print(f"{'='*60}")
    print(f"\nTotal Skills Analyzed: {report['total_analyzed']:,}")
    print(f"\nBy Risk Level:")
    total = sum(risk_counts.values())
    for risk, count in sorted(risk_counts.items()):
        emoji = {'critical': '🚨', 'high': '⚠️', 'medium': '⚡', 'low': '✅'}.get(risk, '❓')
        pct = count/total*100 if total > 0 else 0
        print(f"  {emoji} {risk.upper():8} : {count:6,} ({pct:.2f}%)")

    print(f"\n⚠️ SUSPICIOUS SKILLS: {len(suspicious)} ({len(suspicious)/total*100:.2f}%)")

    if suspicious:
        by_risk = {'critical': [], 'high': [], 'medium': []}
        for s in suspicious:
            by_risk[s['risk']].append(s)

        for risk, skills_list in [('critical', by_risk['critical']), ('high', by_risk['high']), ('medium', by_risk['medium'])]:
            if skills_list:
                print(f"\n{risk.upper()} ({len(skills_list)}):")
                for s in skills_list:
                    print(f"  • {s['name']}")
                    print(f"      {s['reason']}")
                    print(f"      {s['url']}")

    print(f"\n{'='*60}\n")

if __name__ == '__main__':
    main()
