# Awesome OpenClaw Skills - Sanitization Report

**Date:** 2026-02-21
**Repository:** /home/majinbu/pi-mono-workspace/awesome-openclaw-skills
**Source:** https://github.com/VoltAgent/awesome-openclaw-skills

---

## Summary

The awesome-openclaw-skills repository contains a curated list of 3,002 community-built OpenClaw skills. This sanitization report documents the security assessment and cleanup performed.

### Scan Results

| Metric | Count | Percentage |
|---------|--------|------------|
| **Total Skills** | 3,020 | 100% |
| **Suspicious Skills** | 9 | 0.3% |
| **High Risk** | 4 | 0.13% |
| **Medium Risk** | 5 | 0.17% |
| **Low Risk** | 3,011 | 99.7% |

---

## Removed Skills (High Risk)

These 4 skills have been **removed** from `README_CLEAN.md`:

| Skill | Reason |
|-------|--------|
| **camoufox** | Anti-detect browser automation |
| **stealthy-auto-browse** | Evades bot detection |
| **aluvia-web-proxy** | Bypass CAPTCHAs and 403 errors |
| **aluvia-web-unblock** | Bypass CAPTCHAs and 403 errors |

**Justification:** These tools are explicitly designed to evade security measures (bot detection, CAPTCHAs) and could be misused for malicious purposes.

---

## Flagged Skills (Medium Risk)

These 5 skills are **flagged** with security warnings but retained in `README_CLEAN.md`:

| Skill | Reason |
|-------|--------|
| **kesslerio-stealth-browser** | Anti-bot browser |
| **camoufox-stealth** | Anti-bot browser |
| **camoufox-stealth-browser** | Anti-bot browser |
| **stealth-browser** | Stealth browser |
| **vpn-rotate-skill** | Bypass API rate limits |

**Justification:** These may have legitimate use cases (testing, research) but require manual security review before use.

---

## Risk Assessment Criteria

### Critical Risk (Not Found)
- Keyloggers
- Password stealers
- Credit card skimmers
- Backdoor generators
- Malware generation tools

**Note:** These were already excluded by the original curator.

### High Risk (Removed)
- Tools that bypass CAPTCHAs
- Anti-detection browser automation
- Bot detection evasion techniques

### Medium Risk (Flagged)
- Stealth browser automation
- VPN rotation for rate limit bypass
- Anti-bot tools

---

## Categories Analyzed

| Category | Skills |
|-----------|---------|
| General | 2,413 |
| Media | 196 |
| Bot/Automation | 194 |
| Dev | 145 |
| Security | 87 |
| Crypto | 17 |

---

## Files Generated

| File | Description |
|------|-------------|
| `README_CLEAN.md` | Sanitized README with high-risk skills removed |
| `SANITIZATION_REPORT.json` | Detailed JSON report |
| `SUSPICIOUS_SKILLS.json` | Full details on suspicious skills |
| `sanitize.py` | Basic sanitization script |
| `comprehensive_sanitize.py` | Full scanner with categorization |
| `full_sanitize.py` | Creates clean README |
| `SANITIZATION_REPORT.md` | This report |

---

## Recommendations

1. **Always Review Source Code**
   - Check skill source code before installation
   - Look for suspicious imports, obfuscated code
   - Verify data handling practices

2. **Use VirusTotal**
   - Check VirusTotal reports on ClawHub for each skill
   - Look for malware flags from security vendors

3. **Test in Isolation**
   - Test new skills in isolated environment first
   - Monitor network traffic and file access
   - Check for unusual behavior

4. **Report Suspicious Skills**
   - Report to OpenClaw maintainers
   - Open issues in the skills repo
   - Flag in awesome-openclaw-skills

---

## Original Curator Filters

The original awesome list already excluded 2,748 skills:

| Category | Excluded |
|-----------|----------|
| Spam/bulk accounts | 1,180 |
| Crypto/blockchain/finance | 672 |
| Duplicates | 492 |
| Malicious (security audited) | 396 |
| Non-English | 8 |

**Total excluded:** 2,748 from 5,705 total skills

---

## Conclusion

The awesome-openclaw-skills repository is a valuable resource for discovering OpenClaw capabilities. After sanitization:
- **99.87%** of skills remain in the clean version
- All **high-risk** entries have been removed
- **Medium-risk** entries are flagged with warnings

**Repository Status:** ✅ Safe for use with proper security review practices

---

*Generated automatically on 2026-02-21*
