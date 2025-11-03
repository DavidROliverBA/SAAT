# Brownfield Guide: Analyzing Existing Systems with SAAT

**Complete walkthrough for analyzing and improving existing codebases**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Step-by-Step Walkthrough](#step-by-step-walkthrough)
- [Complete Example: Legacy Payment System](#complete-example-legacy-payment-system)
- [Common Scenarios](#common-scenarios)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

### What is Brownfield?

**Brownfield** projects are existing systems with code already written - you want to understand, improve, or modernize them. SAAT helps you:

1. **Discover architecture** automatically from code
2. **Generate C4 models** showing how everything connects
3. **Evaluate quality** against 14 standard characteristics
4. **Identify technical debt** and improvement opportunities
5. **Check compliance** (PCI-DSS, HIPAA, GDPR, SOC2)
6. **Analyze security** vulnerabilities and threats
7. **Generate documentation** that's been missing
8. **Create infrastructure** code to modernize deployment

### Why Use SAAT for Brownfield?

✅ **Understand quickly** - Reverse-engineer architecture in minutes, not weeks
✅ **Find problems** - Identify scalability, security, compliance issues
✅ **Document automatically** - Generate docs for undocumented systems
✅ **Plan modernization** - Get recommendations for improvements
✅ **Compliance audits** - Prepare for audits with validation reports
✅ **Onboard teams** - Help new developers understand the system

### Common Use Cases

- 📊 **Architecture review** - Understand what you inherited
- 🔍 **Pre-acquisition due diligence** - Evaluate a system you're buying
- 🏥 **Compliance audit prep** - Get ready for PCI-DSS, HIPAA, SOC2
- 🔐 **Security assessment** - Find vulnerabilities before attackers do
- 📈 **Modernization planning** - Identify what needs improvement
- 📚 **Knowledge capture** - Document before key people leave
- 👥 **Team onboarding** - Help new hires understand the system

---

## Prerequisites

### What You'll Need

1. **SAAT installed** with Claude Code configured
   - See [Installation Guide](../README.md#-installation)
2. **Access to the codebase**
   - Local clone or path to repository
   - Read access (SAAT only reads, never modifies code)
3. **API key** for your AI model

### What SAAT Can Analyze

✅ **Languages**: Java, Python, JavaScript/TypeScript, C#, Go, Ruby, PHP, and more
✅ **Frameworks**: Spring Boot, Django, Express, .NET, Rails, Laravel, etc.
✅ **Architectures**: Monoliths, microservices, serverless, layered, hexagonal
✅ **Databases**: Relational, NoSQL, in-memory, any type
✅ **Infrastructure**: On-premise, cloud, hybrid

### What You'll Get

After analysis:
- ✅ C4 architecture model (system, container, component levels)
- ✅ Quality assessment (scores for 14 characteristics)
- ✅ Compliance validation (if requested)
- ✅ Security analysis with threat model
- ✅ Comprehensive documentation
- ✅ Infrastructure-as-code (to modernize deployment)
- ✅ Actionable recommendations

---

## Step-by-Step Walkthrough

### Step 1: Prepare Your Codebase

**Ensure the codebase is accessible**:

```bash
# Option 1: Clone repository locally
git clone https://github.com/your-org/legacy-app.git
cd legacy-app

# Option 2: Use existing local copy
cd /path/to/existing/codebase

# Verify you can access the code
ls -la
```

**Optional: Gather context documents** (if available):
```
legacy-app/
├── src/                    # The code SAAT will analyze
├── docs/                   # Any existing docs (optional but helpful)
│   ├── architecture.md
│   ├── deployment.md
│   └── api-spec.md
└── README.md
```

### Step 2: Start the Orchestrator

Open Claude Code in the codebase directory:

```
/saat-orchestrate
```

The Orchestrator starts:

```
Orchestrator: Hello! I'm your SAAT architecture consultant.
              What brings you here today?
              1. I have an existing codebase I want to analyze (brownfield)
              2. I want to design a new system (greenfield)
              3. I have an architecture I want to review
              4. I'm not sure - help me figure it out

You: 1 - Analyze my existing codebase
```

### Step 3: Describe Your Situation

```
Orchestrator: Great! I'll help you analyze your existing codebase.

              Tell me about your situation:
              1. What's the codebase path? (current directory or specify path)
              2. What's the system name?
              3. What do you want to focus on?
                 - General understanding
                 - Quality assessment
                 - Security analysis
                 - Compliance check (PCI-DSS, HIPAA, GDPR, SOC2)
                 - Modernization planning
                 - All of the above
              4. Any specific concerns? (performance, scalability, security, etc.)
              5. Do you have existing architecture documentation?

You: Current directory (/app/payment-processor)
     System name: "PaymentProcessor"
     Focus: All of the above - need complete assessment
     Concerns: Security and PCI-DSS compliance
     No existing documentation
```

### Step 4: The Orchestrator Investigates

```
Orchestrator: Let me first explore your codebase to understand what we're working with...

              🔍 Quick reconnaissance...

              Found:
              - Repository type: Git
              - Size: ~45,000 lines of code
              - Languages: Java (85%), XML (10%), SQL (5%)
              - Framework detected: Spring Boot 2.3.x
              - Build tool: Maven
              - Databases: PostgreSQL, Redis
              - External dependencies: Stripe API, SendGrid

              This looks like a Java Spring Boot application for payment processing.

              Based on your concerns (security, PCI-DSS) and what I see
              (payment processing, Stripe integration), here's my recommendation:

              📋 Recommended Analysis Plan:

              1. ✅ Discover architecture (deep scan)
                 - Analyze all Java files, configs, dependencies
                 - Map services, components, data flows
                 - Identify technologies and patterns

              2. ✅ Generate C4 architecture model
                 - System context (external integrations)
                 - Container diagram (apps, databases, queues)
                 - Component diagrams (internal structure)

              3. ✅ Analyze architecture quality (14 characteristics)
                 - Focus on: Security, Scalability, Maintainability
                 - Identify improvement opportunities
                 - Estimate technical debt

              4. ✅ Validate PCI-DSS compliance
                 - Check all 12 PCI-DSS requirements
                 - Identify gaps and risks
                 - Provide remediation checklist

              5. ✅ Deep security analysis
                 - Vulnerability scan
                 - STRIDE threat model
                 - Payment data flow analysis
                 - Authentication/authorization review

              6. ✅ Generate comprehensive documentation
                 - Architecture overview (currently missing)
                 - C4 diagrams
                 - API documentation
                 - Deployment guide
                 - ADRs (reverse-engineer decisions)

              7. ✅ Create modernized infrastructure code
                 - Terraform for cloud deployment
                 - Docker containerization
                 - CI/CD pipeline recommendations

              Estimated time: 10-15 minutes (larger codebase)

              Does this plan look good? (y/n)
              Or would you like me to focus on specific areas?

You: Yes, perfect
```

### Step 5: Discovery & Analysis

```
Orchestrator: Excellent! Starting deep analysis...

              [1/7] 🔍 Discovering architecture...

              Scanning codebase...
              - Analyzing 1,247 Java files
              - Parsing Spring configurations
              - Mapping database schemas
              - Identifying external dependencies
              - Tracing data flows

              Progress: [████████████████████] 100%

              ✅ Discovery complete!

              📊 Found:

              **Services & Components (45)**:
              - PaymentController (REST API - 18 endpoints)
              - PaymentService (business logic)
              - StripeIntegration (external payment gateway)
              - FraudDetectionService (risk analysis)
              - TransactionRepository (data access)
              - UserAuthenticationFilter (security)
              - AuditLogger (compliance logging)
              ... (38 more components)

              **Databases (2)**:
              1. PostgreSQL (main database)
                 - Tables: payments, transactions, users, audit_log
                 - Relationships: properly normalized
                 - Encryption: ⚠️ NOT ENABLED

              2. Redis (caching)
                 - Session storage
                 - Rate limiting counters
                 - Encryption: ⚠️ NOT ENABLED

              **External Integrations (4)**:
              1. Stripe API (payment processing)
                 - Used for card tokenization ✅
                 - PCI scope reduction ✅

              2. SendGrid (email notifications)
                 - Transactional emails
                 - No sensitive data sent ✅

              3. Twilio (SMS notifications)
                 - 2FA codes
                 - Transaction alerts

              4. Internal ERP System
                 - Order synchronization
                 - ⚠️ HTTP (not HTTPS)

              **Architecture Pattern Detected**:
              - Monolithic with layered architecture
              - Controller → Service → Repository pattern
              - Some domain logic in controllers (⚠️ anti-pattern)

              **Technologies**:
              - Java 11
              - Spring Boot 2.3.4
              - PostgreSQL 12
              - Redis 6
              - Maven
              - JUnit (tests present, ~45% coverage)

              **Deployment**:
              - Current: Single EC2 instance (⚠️ single point of failure)
              - No auto-scaling
              - No load balancer
              - Manual deployment

              **Code Quality Observations**:
              - Test coverage: 45% (⚠️ low for payment system)
              - Commented code: High amount
              - Code duplication: Moderate (15% duplicate code)
              - Dependency age: Some outdated dependencies ⚠️

              Saved to: discovery.json

              Moving to model generation...
```

### Step 6: Architecture Model Generation

```
Orchestrator: [2/7] 🏗️ Generating C4 architecture model...

              Creating architecture model from discovered components...

              ✅ C4 Model generated!

              **System Context (Level 1)**:

              Main System:
              - PaymentProcessor (CS1 - Mission Critical)

              External Systems:
              - Stripe (Payment Gateway)
              - SendGrid (Email Service)
              - Twilio (SMS Service)
              - Internal ERP (Order Management)
              - Customer Web App (makes API calls)
              - Admin Dashboard (management interface)

              **Container Diagram (Level 2)**:

              Containers (4):

              1. Payment API (CS1 - Mission Critical)
                 - Type: Spring Boot REST API
                 - Port: 8080
                 - Criticality: CS1 (handles payments)
                 - Issues found:
                   ⚠️ No authentication on /health endpoint
                   ⚠️ Admin endpoints use same auth as customer endpoints

              2. PostgreSQL Database (CS1 - Mission Critical)
                 - Version: 12
                 - Tables: 8
                 - Encryption: ❌ NOT ENABLED (CRITICAL for PCI-DSS)
                 - Backups: ⚠️ Daily (should be hourly for CS1)

              3. Redis Cache (CS2 - Business Critical)
                 - Version: 6
                 - Use: Sessions, rate limiting
                 - Encryption: ❌ NOT ENABLED
                 - Persistence: AOF enabled ✅

              4. Background Job Processor (SL1 - Standard)
                 - Type: Spring @Scheduled tasks
                 - Jobs: Email retry, report generation
                 - Issue: ⚠️ Runs in same JVM as API (resource contention)

              **Component Diagram (Level 3)**:

              45 components mapped across containers:
              - Controllers (8)
              - Services (15)
              - Repositories (8)
              - Security (4)
              - Integration clients (4)
              - Utilities (6)

              **Relationships (72 identified)**:
              - API → Database (read/write)
              - API → Redis (read/write)
              - API → Stripe (payment processing)
              - API → SendGrid (email)
              - API → Twilio (SMS)
              - API → ERP (⚠️ HTTP not HTTPS)
              - Background Jobs → Database
              - Background Jobs → SendGrid

              **Data Flow Analysis**:

              Payment Flow:
              1. Customer → API (POST /payments)
              2. API → FraudDetectionService (risk check)
              3. API → Stripe (tokenize & process)
              4. Stripe → API (result)
              5. API → Database (store transaction)
              6. API → ERP (sync order) ⚠️ UNENCRYPTED
              7. API → SendGrid (confirmation email)
              8. API → Customer (response)

              Issues in flow:
              - ⚠️ Database stores card details (last 4 digits, brand) - OK
              - ⚠️ Database not encrypted at rest - CRITICAL
              - ⚠️ ERP communication not encrypted - HIGH
              - ⚠️ No retry mechanism for ERP failures - MEDIUM

              Saved to: architecture.json

              Moving to quality analysis...
```

### Step 7: Quality Analysis

```
Orchestrator: [3/7] 📊 Analyzing architecture quality against 14 characteristics...

              ✅ Architecture quality analysis complete!

              📊 Overall Score: 58/100 (Needs Improvement)

              This is typical for legacy systems. Let me break down the scores:

              **Operational Characteristics**:

              ❌ Availability: 35/100 (Non-Compliant)
                 Issues:
                 - Single EC2 instance (single point of failure)
                 - No load balancer
                 - No failover mechanism
                 - Manual deployment causes downtime

                 Impact: System goes down during deployments and server failures

                 Recommendations:
                 1. Deploy multi-AZ with load balancer (effort: 3 days)
                 2. Implement blue-green deployments (effort: 2 days)
                 3. Add health checks and auto-restart (effort: 1 day)

              ⚠️ Scalability: 40/100 (Partially Compliant)
                 Issues:
                 - No auto-scaling
                 - Monolithic = can't scale components independently
                 - Background jobs compete with API for resources

                 Impact: Can't handle traffic spikes, poor Black Friday readiness

                 Recommendations:
                 1. Add auto-scaling (2-10 instances) (effort: 2 days)
                 2. Extract background jobs to separate service (effort: 5 days)
                 3. Consider microservices for future (effort: major refactor)

              ⚠️ Performance: 55/100 (Partially Compliant)
                 Issues:
                 - No caching layer for frequent queries
                 - N+1 queries in transaction history endpoint
                 - Large payload responses (include unnecessary data)

                 Impact: Slow response times under load

                 Recommendations:
                 1. Add Redis caching for product catalog (effort: 2 days)
                 2. Fix N+1 queries with JPA fetch strategies (effort: 1 day)
                 3. Implement response pagination (effort: 2 days)

              ❌ Security: 45/100 (Partially Compliant)
                 Issues:
                 - Database not encrypted at rest ⚠️ CRITICAL
                 - ERP communication unencrypted ⚠️ HIGH
                 - Weak password policy (6 chars min) ⚠️ MEDIUM
                 - Admin endpoints lack additional security

                 Impact: PCI-DSS non-compliance, data breach risk

                 Recommendations:
                 1. Enable database encryption (effort: 1 day)
                 2. Use HTTPS for ERP communication (effort: 1 day)
                 3. Implement strong password policy (12+ chars, complexity) (effort: 0.5 days)
                 4. Add MFA for admin users (effort: 3 days)

              ⚠️ Reliability: 50/100 (Partially Compliant)
              ⚠️ Fault Tolerance: 48/100 (Partially Compliant)
              ⚠️ Recoverability: 60/100 (Mostly Compliant)

              **Structural Characteristics**:

              ⚠️ Maintainability: 52/100 (Partially Compliant)
                 Issues:
                 - Code duplication (15%)
                 - Inconsistent naming conventions
                 - Large classes (some >1000 lines)
                 - Business logic in controllers

                 Recommendations:
                 1. Refactor large classes (effort: ongoing)
                 2. Extract duplicate code to utilities (effort: 3 days)
                 3. Move business logic to services (effort: 5 days)

              ⚠️ Testability: 45/100 (Partially Compliant)
                 Issues:
                 - 45% test coverage (need 80%+)
                 - Few integration tests
                 - Tight coupling makes mocking hard

                 Recommendations:
                 1. Increase test coverage to 80% (effort: 10 days)
                 2. Add integration tests for critical paths (effort: 5 days)
                 3. Introduce dependency injection for testability (effort: 3 days)

              ✅ Deployability: 65/100 (Mostly Compliant)
              ⚠️ Configurability: 58/100 (Partially Compliant)
              ⚠️ Extensibility: 55/100 (Partially Compliant)

              **Cross-Cutting Characteristics**:

              ✅ Interoperability: 70/100 (Mostly Compliant)
              ⚠️ Usability: 60/100 (Mostly Compliant)

              🎯 **Priority Actions to Reach 80/100**:

              Critical (Fix First):
              1. Enable database encryption (Security: +15 points)
              2. Deploy multi-AZ with load balancer (Availability: +25 points)
              3. Add auto-scaling (Scalability: +20 points)

              High Priority:
              4. Encrypt ERP communication (Security: +5 points)
              5. Fix N+1 queries (Performance: +10 points)
              6. Increase test coverage to 80% (Testability: +25 points)
              7. Extract background jobs (Scalability: +10 points)

              Estimated effort: 25-30 developer days
              Expected new score: 82/100 (Good)

              Saved to: archchar-analysis.md, archchar-analysis.json

              Moving to compliance validation...
```

### Step 8: PCI-DSS Compliance Check

```
Orchestrator: [4/7] ✅ Validating PCI-DSS compliance...

              Analyzing against all 12 PCI-DSS requirements...

              ✅ Compliance check complete!

              📊 PCI-DSS Compliance Score: 58/100 (Non-Compliant - NOT certifiable)

              ⚠️ **CRITICAL FINDING**: Cannot achieve certification without fixes

              **Requirement Status**:

              ❌ Requirement 1: Install and maintain firewall configuration
                 Status: Partially Compliant
                 Issues:
                 - No Web Application Firewall (WAF)
                 - Security groups not properly restrictive
                 Action: Implement AWS WAF, tighten security groups

              ⚠️ Requirement 2: Don't use vendor defaults
                 Status: Mostly Compliant
                 Issues:
                 - PostgreSQL using default port 5432
                 - Admin interface on standard port
                 Action: Use non-standard ports

              ❌ Requirement 3: Protect stored cardholder data
                 Status: Non-Compliant ⚠️ CRITICAL
                 Issues:
                 - Database not encrypted at rest ⚠️ BLOCKER
                 - Logs may contain card data (need audit)
                 - Redis not encrypted
                 Action: IMMEDIATE - Enable encryption for all data stores

              ❌ Requirement 4: Encrypt transmission of cardholder data
                 Status: Partially Compliant
                 Issues:
                 - HTTPS to Stripe ✅
                 - HTTPS for customer API ✅
                 - HTTP to internal ERP ❌ (sends order data)
                 - No TLS for Redis connections ❌
                 Action: Enable TLS for all internal communications

              ✅ Requirement 5: Protect against malware
                 Status: Compliant
                 - Antivirus on servers ✅
                 - Regular updates ✅

              ⚠️ Requirement 6: Develop secure systems
                 Status: Partially Compliant
                 Issues:
                 - Using outdated Spring Boot (2.3.4, current is 2.7.x)
                 - Some dependencies have known CVEs
                 - No secure code review process
                 Action: Update dependencies, implement security review

              ⚠️ Requirement 7: Restrict access by business need
                 Status: Partially Compliant
                 Issues:
                 - All employees can access production database
                 - No role-based access control (RBAC)
                 Action: Implement RBAC, principle of least privilege

              ⚠️ Requirement 8: Identify and authenticate access
                 Status: Partially Compliant
                 Issues:
                 - Weak password policy (6 char minimum)
                 - No MFA for admin access
                 - API keys in application.properties (not rotated)
                 Action: Strong passwords, MFA, use Secrets Manager

              ⚠️ Requirement 9: Restrict physical access
                 Status: Mostly Compliant (AWS handles most)
                 - Using AWS (inherits AWS compliance) ✅
                 - Document physical security procedures

              ❌ Requirement 10: Track and monitor all access
                 Status: Partially Compliant
                 Issues:
                 - Logging exists but incomplete
                 - No log aggregation or SIEM
                 - Logs not tamper-proof
                 - No real-time alerting
                 Action: Implement CloudWatch + SIEM, configure alerts

              ⚠️ Requirement 11: Regularly test security
                 Status: Partially Compliant
                 Issues:
                 - No regular penetration testing
                 - No vulnerability scanning
                 - No intrusion detection system (IDS)
                 Action: Quarterly pen tests, automated vuln scans, IDS

              ⚠️ Requirement 12: Maintain information security policy
                 Status: Partially Compliant
                 Issues:
                 - Security policy exists but outdated
                 - No incident response plan
                 - No annual security training
                 Action: Update policies, create IR plan, train staff

              📋 **Blocker Issues (Must Fix for Certification)**:

              🚨 BLOCKER 1: Database encryption
                 - Enable AWS RDS encryption at rest
                 - Effort: 1 day
                 - Downtime: 2-4 hours for migration

              🚨 BLOCKER 2: Internal communications encryption
                 - Enable HTTPS for ERP communication
                 - Enable TLS for Redis
                 - Effort: 2 days
                 - Downtime: None (gradual rollout)

              🚨 BLOCKER 3: Access controls
                 - Implement RBAC
                 - Add MFA for admin
                 - Effort: 5 days

              🚨 BLOCKER 4: Logging and monitoring
                 - Complete audit logging
                 - Implement SIEM
                 - Configure real-time alerts
                 - Effort: 5 days

              📅 **Timeline to PCI-DSS Certification**:

              Phase 1: Fix Blockers (2-3 weeks)
              Phase 2: Address High Priority (4-6 weeks)
              Phase 3: Complete Medium Priority (4-6 weeks)
              Phase 4: Documentation & Policies (2-3 weeks)
              Phase 5: QSA Audit (4-8 weeks)

              Total: 4-6 months to certification

              Saved to: validation-report.json

              Moving to security analysis...
```

### Step 9: Security Analysis & Threat Model

```
Orchestrator: [5/7] 🔒 Running comprehensive security analysis...

              Analyzing code for vulnerabilities...
              Generating STRIDE threat model...
              Analyzing authentication & authorization...
              Checking for common security issues...

              ✅ Security analysis complete!

              📊 Security Score: 52/100 (Needs Immediate Attention)

              🚨 **Critical Issues (3)**:

              1. **Database Not Encrypted** ⚠️ CRITICAL
                 - File: application.properties
                 - Issue: PostgreSQL RDS instance without encryption
                 - Impact: If attacker gains access to AWS, can read all payment data
                 - Risk: Data breach, PCI-DSS non-compliance, legal liability
                 - CVSS Score: 8.1 (High)
                 - Fix: Enable encryption (1-line config + database migration)
                 ```properties
                 # Add to terraform:
                 storage_encrypted = true
                 ```
                 - Effort: 1 day
                 - Priority: FIX IMMEDIATELY

              2. **Unencrypted Internal Communication** ⚠️ CRITICAL
                 - File: ERPClient.java:45
                 - Issue: HTTP connection to internal ERP
                 ```java
                 // Current (INSECURE):
                 String erpUrl = "http://internal-erp:8080/api";

                 // Should be:
                 String erpUrl = "https://internal-erp:8443/api";
                 ```
                 - Impact: Man-in-the-middle attacks in VPC
                 - Risk: Order data interception, tampering
                 - CVSS Score: 7.5 (High)
                 - Effort: 1 day

              3. **SQL Injection Vulnerability** ⚠️ CRITICAL
                 - File: TransactionRepository.java:127
                 - Issue: String concatenation in query
                 ```java
                 // VULNERABLE CODE:
                 String sql = "SELECT * FROM transactions WHERE user_id = '" + userId + "'";
                 ```
                 - Impact: Attacker can execute arbitrary SQL
                 - Risk: Data breach, data manipulation, DoS
                 - CVSS Score: 9.8 (Critical)
                 - Fix: Use parameterized queries
                 ```java
                 // FIXED:
                 @Query("SELECT t FROM Transaction t WHERE t.userId = :userId")
                 List<Transaction> findByUserId(@Param("userId") String userId);
                 ```
                 - Effort: 2 hours
                 - Priority: FIX IMMEDIATELY

              ⚠️ **High Priority Issues (5)**:

              4. **Weak Password Hashing**
                 - File: UserService.java:89
                 - Issue: Using MD5 for password hashing
                 - Fix: Upgrade to bcrypt
                 - Effort: 1 day (+ password reset for all users)

              5. **Missing Authentication on Admin Endpoints**
                 - File: AdminController.java
                 - Issue: @PreAuthorize missing on critical endpoints
                 - Fix: Add @PreAuthorize("hasRole('ADMIN')")
                 - Effort: 0.5 days

              6. **Hardcoded API Keys**
                 - File: application.properties
                 - Issue: Stripe API key in source control
                 - Fix: Move to AWS Secrets Manager
                 - Effort: 0.5 days

              7. **No Rate Limiting on Login**
                 - File: AuthController.java
                 - Issue: Brute force attack possible
                 - Fix: Implement rate limiting (Redis)
                 - Effort: 1 day

              8. **CORS Misconfiguration**
                 - File: SecurityConfig.java:56
                 - Issue: Allows all origins (*)
                 - Fix: Whitelist specific origins
                 - Effort: 0.5 days

              ℹ️ **Medium Priority Issues (8)**:
              - Outdated dependencies with CVEs
              - Missing security headers (CSP, HSTS)
              - Verbose error messages expose system details
              - Session timeout too long (24 hours)
              - No CSRF protection on state-changing endpoints
              - Insufficient input validation
              - Missing API rate limiting
              - Logging sensitive data

              🛡️ **STRIDE Threat Model Analysis**:

              **Spoofing**:
              ✅ JWT authentication implemented
              ❌ No service-to-service authentication
              ❌ Weak password policy (6 char minimum)
              ⚠️ No MFA for admin accounts

              **Tampering**:
              ✅ HTTPS for external traffic
              ❌ HTTP for internal ERP communication
              ❌ No request signing for critical operations
              ⚠️ Database integrity checks missing

              **Repudiation**:
              ⚠️ Audit logging incomplete
              ⚠️ Logs not tamper-proof
              ❌ No log aggregation/SIEM

              **Information Disclosure**:
              ❌ Database not encrypted at rest
              ❌ Redis not encrypted
              ⚠️ Error messages leak system information
              ⚠️ API returns unnecessary data

              **Denial of Service**:
              ⚠️ Rate limiting only on API Gateway
              ❌ No rate limiting on login
              ❌ No circuit breakers for external services
              ⚠️ Large payload attacks possible

              **Elevation of Privilege**:
              ⚠️ RBAC incomplete
              ❌ Missing authorization on admin endpoints
              ⚠️ Over-permissive database access

              📋 **Immediate Action Plan**:

              Week 1 (Critical):
              [ ] Fix SQL injection vulnerability (2 hours)
              [ ] Enable database encryption (1 day, requires maintenance window)
              [ ] Enable HTTPS for ERP communication (1 day)
              [ ] Move API keys to Secrets Manager (0.5 days)

              Week 2 (High Priority):
              [ ] Upgrade password hashing to bcrypt (1 day)
              [ ] Add authentication to admin endpoints (0.5 days)
              [ ] Implement login rate limiting (1 day)
              [ ] Fix CORS configuration (0.5 days)
              [ ] Update dependencies with CVEs (1 day)

              Week 3-4 (Medium Priority):
              [ ] Add security headers (0.5 days)
              [ ] Implement comprehensive audit logging (2 days)
              [ ] Add CSRF protection (1 day)
              [ ] Implement API rate limiting (1 day)
              [ ] Add input validation (3 days)
              [ ] Reduce session timeout to 2 hours (0.5 days)
              [ ] Set up SIEM and alerting (3 days)

              Saved to: security-report.json

              Moving to documentation generation...
```

### Step 10: Documentation Generation

```
Orchestrator: [6/7] 📚 Generating comprehensive documentation...

              Creating documentation you've been missing...

              ✅ Documentation generated!

              📁 Created in docs/:

              **Architecture Overview** (docs/README.md):
              # PaymentProcessor - Architecture Overview

              ## System Overview
              PaymentProcessor is a Java Spring Boot application that handles
              payment processing for e-commerce orders. It integrates with
              Stripe for credit card processing and syncs with the internal
              ERP system for order management.

              ## Current State
              - Monolithic Spring Boot application
              - Single EC2 instance deployment
              - 45,000 lines of Java code
              - 45% test coverage
              - Deployed manually

              ## Architecture Scores
              - Overall Quality: 58/100 (Needs Improvement)
              - PCI-DSS Compliance: 58/100 (Non-Compliant)
              - Security: 52/100 (Immediate Attention Required)

              ## Critical Issues
              1. Database not encrypted (BLOCKER for PCI-DSS)
              2. Single point of failure (no HA)
              3. SQL injection vulnerability (CRITICAL)
              ... (full list)

              **C4 Diagrams**:
              - system-context.puml / .svg
              - container-diagram.puml / .svg
              - component-diagrams/* (45 component diagrams)
              - All in PlantUML and Mermaid formats

              **API Documentation** (docs/API.md):
              # API Documentation

              ## Authentication
              All endpoints require JWT token in Authorization header...

              ## Endpoints

              ### POST /api/v1/payments
              Process a payment

              Request:
              ```json
              {
                "amount": 1000,
                "currency": "USD",
                "card_token": "tok_...",
                "order_id": "ORD-123"
              }
              ```

              Response:
              ```json
              {
                "transaction_id": "txn_...",
                "status": "completed",
                "timestamp": "2024-01-15T10:30:00Z"
              }
              ```

              ... (all 18 endpoints documented)

              **Deployment Guide** (docs/DEPLOYMENT.md):
              # Deployment Guide

              ## Current Deployment Process
              1. SSH into EC2 instance
              2. Pull latest code from git
              3. Run `mvn clean package`
              4. Stop application: `./stop.sh`
              5. Copy new JAR
              6. Start application: `./start.sh`

              **Issues with current process**:
              - Downtime during deployment (2-5 minutes)
              - Manual process (error-prone)
              - No rollback mechanism
              - No health checks

              **Recommended New Process**:
              See infrastructure/ for automated deployment...

              **Architecture Decision Records**:

              docs/adr/001-spring-boot-framework.md:
              # 1. Use Spring Boot Framework

              Date: 2019-03-15 (inferred from initial commit)

              ## Status
              Accepted

              ## Context
              Need to build a payment processing API quickly with
              minimal boilerplate. Team has Java expertise.

              ## Decision
              Use Spring Boot 2.x for REST API development.

              ## Consequences
              Positive:
              - Fast development
              - Large ecosystem
              - Team familiar with Java

              Negative:
              - Monolithic architecture limits scaling
              - Spring can be "magical" (lots of auto-configuration)

              ... (6 more ADRs reverse-engineered from code)

              docs/adr/002-postgresql-database.md
              docs/adr/003-stripe-integration.md
              docs/adr/004-jwt-authentication.md
              docs/adr/005-redis-caching.md
              docs/adr/006-scheduled-jobs.md

              Saved to: docs/

              Moving to infrastructure code generation...
```

### Step 11: Infrastructure Code Generation

```
Orchestrator: [7/7] 🏗️ Generating modernized infrastructure code...

              Creating Terraform to improve your deployment...

              ✅ Infrastructure code generated!

              📁 Created infrastructure/ directory:

              **What's Included**:

              infrastructure/
              ├── main.tf                    # Main infrastructure
              ├── variables.tf               # Configurable parameters
              ├── outputs.tf                 # Endpoint URLs, etc.
              ├── terraform.tfvars.example   # Template for your values
              ├── modules/
              │   ├── networking/            # VPC, subnets, security groups
              │   ├── compute/               # ECS, auto-scaling
              │   ├── database/              # RDS with encryption
              │   ├── cache/                 # Redis with encryption
              │   ├── monitoring/            # CloudWatch, alarms
              │   └── security/              # WAF, Secrets Manager
              └── README.md

              **Key Improvements Over Current Setup**:

              ✅ **High Availability**:
              - Multi-AZ deployment (3 availability zones)
              - Application Load Balancer
              - Auto-scaling (2-10 instances based on CPU)
              - Zero-downtime deployments (blue-green)

              ✅ **Security (PCI-DSS Compliant)**:
              - RDS encryption at rest ✅
              - TLS for Redis connections ✅
              - AWS WAF for DDoS protection ✅
              - Secrets Manager for API keys ✅
              - Security groups properly configured ✅
              - Private subnets for databases ✅

              ✅ **Monitoring & Ops**:
              - CloudWatch dashboards
              - Automated alerts (high CPU, errors, etc.)
              - Centralized logging
              - X-Ray tracing
              - Automated backups

              ✅ **Cost Optimization**:
              - Right-sized instances (t3.medium)
              - Auto-scaling saves money during low traffic
              - Reserved instances support
              - Spot instances for dev/test

              **Deployment Steps**:

              1. Review and customize:
              ```bash
              cd infrastructure
              cp terraform.tfvars.example terraform.tfvars
              # Edit terraform.tfvars with your settings
              ```

              2. Initialize Terraform:
              ```bash
              terraform init
              ```

              3. Plan (see what will be created):
              ```bash
              terraform plan
              ```

              4. Apply (create infrastructure):
              ```bash
              terraform apply
              ```

              **Migration Plan** (from current single EC2):

              Phase 1: Create new infrastructure (no impact)
              Phase 2: Deploy app to new infrastructure
              Phase 3: Test thoroughly
              Phase 4: Update DNS to point to new load balancer
              Phase 5: Monitor for 48 hours
              Phase 6: Decommission old EC2

              **Estimated Costs**:

              Current setup: ~$150/month (1x t3.medium EC2)

              New setup: ~$450-800/month
              - ECS (2-10 instances): $150-500/month
              - RDS Multi-AZ: $180/month
              - ElastiCache: $50/month
              - Load Balancer: $20/month
              - Misc (WAF, CloudWatch): $50/month

              Cost increase: $300-650/month
              Benefits: 99.9% uptime, PCI-DSS compliant, auto-scaling

              ROI: Cost of 1 hour of downtime typically exceeds monthly increase

              Saved to: infrastructure/
```

### Step 12: Summary & Recommendations

```
Orchestrator: 🎉 Complete Analysis Finished for PaymentProcessor!

              ⏱️ Completed in: 12 minutes 48 seconds

              📊 **Current State Summary**:

              Quality:      58/100 (Needs Improvement)
              Compliance:   58/100 (NOT certifiable without fixes)
              Security:     52/100 (3 CRITICAL issues)
              Architecture: Monolithic layered (Spring Boot)
              Deployment:   Single EC2, manual deployment
              Code:         45K lines, 45% test coverage

              🚨 **CRITICAL FINDINGS**:

              Must Fix Immediately:
              1. SQL Injection vulnerability (2 hours to fix)
              2. Database not encrypted (1 day, critical for PCI-DSS)
              3. Unencrypted ERP communication (1 day)

              Cannot Achieve PCI-DSS Without:
              - Database encryption ❌
              - Internal TLS ❌
              - Complete audit logging ❌
              - RBAC implementation ❌

              📁 **Generated Files**:

              ✅ discovery.json              (45 components discovered)
              ✅ architecture.json           (C4 model)
              ✅ archchar-analysis.md        (quality assessment)
              ✅ archchar-analysis.json      (scores)
              ✅ validation-report.json      (PCI-DSS checklist)
              ✅ security-report.json        (vulnerabilities + threats)
              ✅ docs/                       (comprehensive docs)
              ✅ infrastructure/             (Terraform for AWS)

              📋 **Recommended Action Plan**:

              🚨 **Week 1 - Critical Security (URGENT)**:
              [ ] Fix SQL injection (2 hours) - CANNOT DELAY
              [ ] Enable database encryption (1 day)
              [ ] Enable HTTPS for ERP (1 day)
              [ ] Move secrets to AWS Secrets Manager (4 hours)
              Effort: 3 days | Impact: Eliminates critical vulnerabilities

              ⚠️ **Week 2-3 - High Availability**:
              [ ] Deploy Terraform infrastructure (3 days)
              [ ] Migrate to new multi-AZ setup (2 days)
              [ ] Implement blue-green deployment (2 days)
              Effort: 7 days | Impact: 99.9% uptime, zero-downtime deploys

              📈 **Week 4-6 - PCI-DSS Compliance**:
              [ ] Implement RBAC (5 days)
              [ ] Complete audit logging + SIEM (5 days)
              [ ] Add MFA for admins (3 days)
              [ ] Update security policies (3 days)
              Effort: 16 days | Impact: PCI-DSS certifiable

              🎯 **Week 7-10 - Quality Improvements**:
              [ ] Increase test coverage to 80% (10 days)
              [ ] Refactor large classes (5 days)
              [ ] Fix N+1 queries (2 days)
              [ ] Add monitoring and alerting (3 days)
              Effort: 20 days | Impact: Quality score → 80/100

              **Total Effort**: ~46 developer days (2-3 months with 1 developer)

              **Expected Results After Fixes**:
              - Quality: 58 → 82/100
              - Compliance: 58 → 92/100 (certifiable)
              - Security: 52 → 85/100
              - Availability: 35 → 95/100
              - Deployment: Manual → Automated CI/CD

              💰 **Business Impact**:

              Current State Risks:
              - PCI-DSS non-compliance → Cannot process payments legally
              - SQL injection → Potential massive data breach
              - No HA → Revenue loss during outages
              - Manual deployment → 2-5 min downtime each release

              Post-Improvement:
              - PCI-DSS compliant → Legal to process payments
              - Critical vulns fixed → Dramatically reduced breach risk
              - 99.9% uptime → Only 8.76 hours downtime per year
              - Zero-downtime deploys → Deploy anytime without impact

              📅 **Recommended Timeline**:

              Month 1: Fix critical security issues, deploy HA infrastructure
              Month 2: Complete PCI-DSS requirements
              Month 3: Quality improvements, testing, documentation

              **What would you like to do next?**
              1. Review the SQL injection fix in detail
              2. Understand the database encryption migration
              3. See the full PCI-DSS compliance checklist
              4. Review the infrastructure deployment plan
              5. Discuss the refactoring strategy
              6. Estimate costs for improvements
              7. Create a presentation for leadership
              8. Something else
```

---

## Complete Example: Legacy Payment System

See the walkthrough above for the complete example!

---

## Common Scenarios

### Scenario 1: Pre-Acquisition Due Diligence

**Situation**: Your company is acquiring another company. You need to assess their codebase quality.

```
You: /saat-orchestrate

You: We're acquiring a company. Need to evaluate their payment system at
     /acquisitions/target-company-code/

     Focus: Architecture quality, technical debt, security risks,
     estimated refactoring costs

Orchestrator: [Runs complete analysis]

              Results:
              - Quality: 42/100 (Significant Technical Debt)
              - Security: 38/100 (Multiple critical issues)
              - Estimated refactoring: 6-9 months, $300K-500K
              - Recommendation: Factor into acquisition price

              [Generates detailed report for executive team]
```

### Scenario 2: Compliance Audit Prep

**Situation**: PCI-DSS audit in 3 months, need to prepare.

```
You: /saat-orchestrate

You: PCI-DSS audit in 3 months. Need gap analysis and remediation plan.
     Codebase: current directory

Orchestrator: [Focuses on PCI-DSS validation]

              Compliance: 65/100

              Gaps found: 18
              - 4 Critical (blockers)
              - 7 High
              - 7 Medium

              Remediation timeline: 10 weeks (with buffer)

              [Generates detailed checklist and weekly plan]
```

### Scenario 3: Modernization Planning

**Situation**: Legacy monolith needs to be modernized.

```
You: /saat-orchestrate

You: Have a 10-year-old monolith. Want to modernize. Should we:
     1. Refactor in place
     2. Migrate to microservices
     3. Rewrite from scratch

Orchestrator: [Analyzes architecture]

              My recommendation: Refactor in place first (3-6 months),
              then gradually extract microservices (12-18 months)

              Reasoning:
              - Code quality: 55/100 (salvageable)
              - Business logic: Well-organized in services layer
              - Tests exist (45% coverage)
              - Rewrite too risky (lose 10 years of bug fixes)

              Phase 1 (Refactor in place):
              - Deploy as containers
              - Add HA and auto-scaling
              - Increase test coverage
              - Fix critical issues
              Cost: $150K, 6 months

              Phase 2 (Extract microservices):
              - Extract payment service (PCI scope reduction)
              - Extract notification service
              - Extract reporting service
              Cost: $300K, 12-18 months

              Total: $450K, 18-24 months
              vs. Rewrite: $1.2M, 24-36 months (much higher risk)

              [Generates detailed modernization roadmap]
```

### Scenario 4: Security Audit

**Situation**: Just hired a security officer. They want a complete security assessment.

```
You: /saat-orchestrate

You: New security officer wants complete security audit.
     Focus only on security, skip other aspects.

Orchestrator: [Deep security analysis]

              Security Score: 48/100

              🚨 Critical: 4
              ⚠️ High: 8
              ℹ️ Medium: 12
              ℹ️ Low: 18

              [Generates comprehensive security report with STRIDE model]
              [Provides remediation plan with effort estimates]
              [Creates executive summary for CISO]
```

---

## Best Practices

### 1. Start with the Orchestrator

**Don't** try to run individual agents yourself:
```
❌ /saat-discover
❌ /saat-generate
❌ /saat-analyze
```

**Do** let the Orchestrator guide you:
```
✅ /saat-orchestrate
   (Orchestrator will run the right agents in the right order)
```

### 2. Be Specific About Your Focus

**Vague**:
> "Analyze my code"

**Specific**:
> "I need to prepare for a PCI-DSS audit in 3 months. Focus on compliance gaps and security issues. Code is in current directory."

### 3. Provide Context

Help SAAT give better recommendations:

```
You: /saat-orchestrate

Orchestrator: What are you working with?

You: Legacy Java monolith, 5 years old, processes payments.
     Team of 3 developers, all Java experts.
     Currently deployed on single EC2 instance.
     Main concern: System goes down during deployments, losing revenue.
     Budget: $50K for improvements.
     Timeline: Want to fix in next quarter.
```

Better context → Better recommendations

### 4. Ask Questions

The Orchestrator is conversational:

```
You: Why did you recommend PostgreSQL over MongoDB for this service?

Orchestrator: Great question! Here's my reasoning:
              1. Your data is highly relational (orders, users, transactions)
              2. You need ACID guarantees for financial data
              3. PostgreSQL is better for complex queries
              4. Your team already uses PostgreSQL (consistency)

              However, if you prefer MongoDB, I can regenerate...

You: No, that makes sense. Let's go with PostgreSQL.
```

### 5. Iterate and Refine

Don't expect perfection on first try:

```
You: The architecture looks good, but can you add a caching layer
     for the product catalog? It gets hit hard.

Orchestrator: Excellent idea! Adding Redis caching for product catalog...
              [Regenerates architecture with caching]

              I've also updated:
              - Performance score: 55 → 75/100
              - Recommended caching strategy
              - Updated infrastructure to include ElastiCache
```

### 6. Save the Generated Files

SAAT generates valuable documentation:

```bash
# Commit to version control
git add architecture.json docs/ infrastructure/
git commit -m "Add SAAT architecture analysis and documentation"

# Share with team
# - architecture.json: Architects
# - docs/: All developers
# - security-report.json: Security team
# - validation-report.json: Compliance team
# - infrastructure/: DevOps team
```

### 7. Use Reports for Planning

```
# Sprint planning
Use archchar-analysis.md to prioritize technical debt

# Budget planning
Use effort estimates from reports: "Need $200K for PCI-DSS compliance"

# Hiring decisions
Use quality scores: "Need senior dev to tackle technical debt"

# Executive updates
Use generated summaries for status reports
```

---

## Troubleshooting

### Issue: "Discovery found very few components"

**Causes**:
- Code might be in unusual structure
- Using uncommon frameworks
- Mostly configuration, not code

**Solutions**:
1. Tell Orchestrator the framework: "It's a Python Flask app"
2. Point to specific directories: "The code is in src/main/java"
3. Provide context: "It's a microservices system with 5 repos"

### Issue: "Quality scores seem too low"

**This is normal for legacy systems!**

Average scores:
- Legacy (5+ years): 45-60/100
- Maintained systems: 60-75/100
- Modern systems: 75-85/100
- Best in class: 85-95/100

Don't be discouraged - use the recommendations to improve!

### Issue: "Want to focus on specific issues"

```
You: The full analysis is overwhelming. Can we just focus on the
     security issues for now?

Orchestrator: Absolutely! Let me rerun focusing only on security...
              [Runs deep security analysis]
```

### Issue: "Codebase is huge (500K+ lines)"

**SAAT can handle it**, but analysis will take longer:

```
Orchestrator: This is a large codebase (500K lines).
              Analysis will take 20-30 minutes.

              Options:
              1. Analyze entire codebase (thorough)
              2. Analyze specific modules (faster)
              3. Start with high-level, then drill down

              What would you prefer?
```

### Issue: "Want to analyze multiple repositories"

```
You: I have a microservices system across 8 repositories.
     How do I analyze all of them?

Orchestrator: Great question! Here's my recommendation:

              Option 1: Analyze each repo separately, then combine
              Option 2: Clone all repos into one parent directory

              Let's do Option 2:
              ```
              mkdir my-microservices
              cd my-microservices
              git clone repo1
              git clone repo2
              ...
              # Then run /saat-orchestrate
              ```

              I'll discover all services and show how they connect.
```

---

## Next Steps

After completing your brownfield analysis:

1. **Prioritize Fixes**
   - Critical security issues first
   - Then compliance blockers
   - Then quality improvements

2. **Create Action Plan**
   - Use effort estimates from reports
   - Assign to sprint backlog
   - Track progress

3. **Monitor Progress**
   - Re-run `/saat-orchestrate` quarterly
   - Watch quality scores improve
   - Celebrate wins!

4. **Keep Architecture Updated**
   - Update `architecture.json` as you make changes
   - Re-generate docs periodically
   - Keep team aligned

5. **Deploy Improvements**
   - Use generated `infrastructure/` code
   - Follow migration plans
   - Test thoroughly

---

## Related Guides

- **[Greenfield Guide](GREENFIELD_GUIDE.md)** - Designing new systems
- **[Customization Guide](CUSTOMIZATION_GUIDE.md)** - Customizing SAAT
- **[Orchestrator Guide](ORCHESTRATOR_GUIDE.md)** - Advanced orchestrator usage
- **[Architecture Characteristics Guide](ARCHITECTURE_CHARACTERISTICS_USAGE.md)** - Quality analysis deep dive

---

**Happy Analyzing! 🔍📊**
