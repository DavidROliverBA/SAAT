---
description: Analyze security posture and identify vulnerabilities in architecture
---

I'll help you analyze the security posture of your architecture and identify vulnerabilities.

**What I'll do:**
1. Check encryption & data protection:
   - Unencrypted communications (HTTP vs HTTPS)
   - Unencrypted data at rest
   - Missing encryption for sensitive data
   - Weak encryption algorithms
2. Validate authentication & authorization:
   - Missing authentication
   - Weak authentication (basic auth, no MFA)
   - Missing authorization checks
   - Overly permissive access
3. Analyze data flow security:
   - Sensitive data flowing through insecure channels
   - Logs containing sensitive data
   - Data exfiltration risks
   - Missing data validation
4. Assess infrastructure security:
   - Public access to sensitive systems
   - Missing network segmentation
   - No firewalls or WAF
   - Missing intrusion detection
5. Check compliance requirements:
   - PCI-DSS (payment data)
   - HIPAA (health data)
   - GDPR (personal data)
   - SOC2 requirements

**What I need from you:**
1. Path to your C4 model JSON file (e.g., `architecture.json`)
2. (Optional) Enable threat modeling for detailed attack scenarios

**Output includes:**
- Security score (0-100)
- Issues by severity (critical, high, medium, low)
- Affected elements for each issue
- Detailed recommendations for fixes
- Compliance impact assessment
- Report saved to `security-report.json`

Please provide the path to your C4 model file, and let me know if you want threat modeling enabled.

**After security analysis**, I can help you:
- Fix critical security issues
- Update model with security infrastructure
- Generate documentation with security notes
