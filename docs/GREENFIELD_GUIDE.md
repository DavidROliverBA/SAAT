# Greenfield Guide: Designing New Systems with SAAT

**Complete walkthrough for designing a new system from scratch**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Step-by-Step Walkthrough](#step-by-step-walkthrough)
- [Complete Example: E-Commerce Platform](#complete-example-e-commerce-platform)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

### What is Greenfield?

**Greenfield** projects are new systems being designed from scratch - no existing code to analyze. SAAT helps you:

1. **Extract requirements** from documents (PRDs, specs, user stories)
2. **Generate architecture** automatically based on requirements
3. **Evaluate quality** before writing any code
4. **Check compliance** against regulations (PCI-DSS, HIPAA, etc.)
5. **Analyze security** proactively
6. **Generate documentation** for your team
7. **Create infrastructure** code ready to deploy

### Why Use SAAT for Greenfield?

✅ **Catch issues early** - Fix architecture problems before writing code
✅ **Quality by design** - Ensure characteristics like scalability from day one
✅ **Compliance-ready** - Validate against regulations from the start
✅ **Faster time to market** - Auto-generate docs and infrastructure
✅ **Expert guidance** - Get recommendations from industry best practices

---

## Prerequisites

### What You'll Need

1. **SAAT installed** with Claude Code configured
   - See [Installation Guide](../README.md#-installation)
2. **Requirements documents** (at least one):
   - Product Requirements Document (PRD)
   - Technical specifications
   - User stories
   - Compliance requirements
3. **API key** for your AI model (Claude, GPT-4, etc.)

### What You'll Get

After completing this guide, you'll have:
- ✅ Complete C4 architecture model
- ✅ Quality analysis with scores
- ✅ Compliance validation report
- ✅ Security analysis
- ✅ Comprehensive documentation
- ✅ Infrastructure-as-code (Terraform)

---

## Step-by-Step Walkthrough

### Step 1: Prepare Your Requirements

**Gather all requirements documents** into a `docs/` directory:

```
my-new-project/
├── docs/
│   ├── product-requirements.md     # What the product does
│   ├── technical-specs.md          # Technical constraints
│   ├── compliance-needs.md         # Regulations to follow
│   └── user-stories.md             # User perspective
└── (architecture will be generated here)
```

**Tip**: SAAT can work with as little as one document, but more context produces better results!

### Step 2: Start the Orchestrator

Open Claude Code in your project directory and type:

```
/saat-orchestrate
```

The Orchestrator will start a conversation:

```
Orchestrator: Hello! I'm your SAAT architecture consultant.
              What brings you here today?
              1. I have an existing codebase I want to analyze
              2. I want to design a new system (greenfield)
              3. I have an architecture I want to review
              4. I'm not sure - help me figure it out

You: 2 - Design a new system
```

### Step 3: Describe Your Project

The Orchestrator will ask questions to understand your needs:

```
Orchestrator: Great! I'll help you design your new system.

              Tell me about your project:
              1. What's the project name?
              2. What does it do? (brief description)
              3. Do you have requirements documents? Where are they?
              4. Any specific concerns? (performance, security, etc.)
              5. Compliance requirements? (PCI-DSS, HIPAA, GDPR, etc.)

You: Project name: "OrderFlow"
     It's an e-commerce order management system
     Requirements are in docs/requirements.md and docs/tech-specs.md
     Main concerns: scalability and PCI-DSS compliance
     Compliance: PCI-DSS for payment processing
```

### Step 4: Review the Plan

The Orchestrator creates a plan and asks for approval:

```
Orchestrator: Perfect! Based on what you've told me, here's my plan:

              📋 Architecture Design Plan for OrderFlow:

              1. ✅ Extract requirements from documents
                 - docs/requirements.md
                 - docs/tech-specs.md
                 Identify: functional reqs, NFRs, constraints, stakeholders

              2. ✅ Generate C4 architecture model
                 - Recommend architecture style (microservices, monolith, etc.)
                 - Create systems, containers, and components
                 - Define relationships and data flows
                 - Assign criticality levels based on requirements

              3. ✅ Analyze architecture quality (14 characteristics)
                 - Focus on: Scalability (per your concern)
                 - Evaluate all operational, structural, cross-cutting aspects
                 - Identify gaps before implementation

              4. ✅ Validate PCI-DSS compliance
                 - Check all PCI-DSS requirements
                 - Identify what needs to be implemented
                 - Provide compliance checklist

              5. ✅ Security analysis with threat modeling
                 - STRIDE threat model
                 - Payment data protection analysis
                 - Authentication/authorization recommendations

              6. ✅ Generate comprehensive documentation
                 - Architecture overview
                 - C4 diagrams (PlantUML, Mermaid)
                 - Architecture Decision Records (ADRs)
                 - Deployment guide

              7. ✅ Create AWS infrastructure-as-code
                 - Terraform with PCI-DSS configuration
                 - Multi-AZ for critical components
                 - Auto-scaling, backups, monitoring
                 - Ready to deploy

              Estimated time: 8-12 minutes

              Does this plan look good? (y/n)
              Or would you like me to adjust anything?

You: yes, looks perfect
```

### Step 5: Requirements Extraction

The Orchestrator starts executing:

```
Orchestrator: Excellent! Starting design process...

              [1/7] 📋 Extracting requirements...

              Reading documents:
              - docs/requirements.md (2,430 words)
              - docs/tech-specs.md (1,850 words)

              Analyzing...

              ✅ Requirements extraction complete!

              📊 Found:
              - 28 Functional Requirements
                * REQ-F-001: User can browse product catalog
                * REQ-F-002: User can add items to cart
                * REQ-F-003: User can checkout with payment
                * ... (25 more)

              - 12 Non-Functional Requirements
                * REQ-NF-001: System must handle 10,000 concurrent users
                * REQ-NF-002: 99.9% uptime for order processing
                * REQ-NF-003: Payment processing < 2 seconds
                * ... (9 more)

              - 8 Technical Constraints
                * CONST-001: Must use AWS cloud
                * CONST-002: PCI-DSS Level 1 compliance required
                * CONST-003: Microservices architecture preferred
                * ... (5 more)

              - 15 User Stories
                * US-001: As a customer, I want to browse products...
                * US-002: As a customer, I want to save items for later...
                * ... (13 more)

              - 6 Stakeholders identified
                * Product Manager, Engineering Lead, Security Officer, ...

              Saved to: requirements.json

              Moving to architecture generation...
```

### Step 6: Architecture Generation

```
Orchestrator: [2/7] 🏗️ Generating architecture model...

              Based on requirements, I'm recommending:
              **Architecture Style**: Microservices with Event-Driven Communication

              Reasoning:
              - High scalability requirement (10,000 concurrent users)
              - Independent service scaling needed
              - Payment processing isolation for PCI-DSS compliance
              - Multiple bounded contexts identified

              Creating C4 model...

              ✅ Architecture model generated!

              📊 Your System:

              **Systems (3)**:
              1. OrderFlow Platform (Main system)
              2. Payment Gateway (External - PCI-compliant processor)
              3. Inventory Management System (External - 3rd party)

              **Containers (8)**:
              1. API Gateway (CS1 - Mission Critical)
                 - Entry point for all requests
                 - Rate limiting, authentication
                 - Technology: Kong/AWS API Gateway

              2. Product Service (CS2 - Business Critical)
                 - Product catalog management
                 - Search functionality
                 - Technology: Node.js + MongoDB

              3. Order Service (CS1 - Mission Critical)
                 - Order creation and tracking
                 - Order state management
                 - Technology: Java Spring Boot + PostgreSQL

              4. Payment Service (CS1 - Mission Critical)
                 - PCI-DSS compliant payment processing
                 - Tokenization
                 - Technology: Java + PostgreSQL (encrypted)

              5. User Service (CS2 - Business Critical)
                 - Authentication, authorization
                 - User profiles
                 - Technology: Node.js + PostgreSQL

              6. Notification Service (SL1 - Standard)
                 - Email, SMS notifications
                 - Technology: Python + SQS

              7. Web Frontend (CS2 - Business Critical)
                 - Customer-facing UI
                 - Technology: React + Next.js

              8. Event Bus (CS1 - Mission Critical)
                 - Asynchronous communication
                 - Technology: Apache Kafka

              **Components**: 24 total across all containers
              **Relationships**: 45 interactions defined

              Saved to: architecture.json

              Moving to quality analysis...
```

### Step 7: Quality Analysis

```
Orchestrator: [3/7] 📊 Analyzing architecture quality...

              Evaluating against 14 characteristics...

              ✅ Architecture quality analysis complete!

              📊 Overall Score: 78/100 (Good - Ready for implementation with minor improvements)

              **Characteristic Scores**:

              Operational:
              ✅ Availability: 85/100 (Mostly Compliant)
                 - Multi-AZ deployment planned
                 - ⚠️ Gap: Consider active-active for Payment Service

              ✅ Scalability: 88/100 (Mostly Compliant)
                 - Microservices allow independent scaling
                 - Event-driven reduces coupling
                 - ✅ Meets 10,000 concurrent user requirement

              ✅ Performance: 75/100 (Mostly Compliant)
                 - ⚠️ Gap: No caching layer specified
                 - ⚠️ Gap: Database query optimization needed

              ✅ Security: 82/100 (Mostly Compliant)
                 - API Gateway provides auth layer
                 - Payment Service isolated
                 - ⚠️ Gap: Add encryption at rest for all databases

              ✅ Reliability: 80/100 (Mostly Compliant)
              ✅ Fault Tolerance: 78/100 (Mostly Compliant)
              ✅ Recoverability: 85/100 (Mostly Compliant)

              Structural:
              ✅ Maintainability: 82/100 (Mostly Compliant)
              ✅ Testability: 75/100 (Mostly Compliant)
              ✅ Deployability: 88/100 (Mostly Compliant)
              ✅ Configurability: 80/100 (Mostly Compliant)
              ✅ Extensibility: 85/100 (Mostly Compliant)

              Cross-Cutting:
              ✅ Interoperability: 90/100 (Fully Compliant)
              ✅ Usability: 75/100 (Mostly Compliant)

              🎯 Top Recommendations to Reach 90/100:
              1. Add Redis caching layer for Product Service (Performance)
              2. Implement database encryption at rest (Security)
              3. Add circuit breakers for external services (Fault Tolerance)
              4. Implement comprehensive test strategy (Testability)

              Saved to: archchar-analysis.md, archchar-analysis.json

              Moving to compliance validation...
```

### Step 8: Compliance Validation

```
Orchestrator: [4/7] ✅ Validating PCI-DSS compliance...

              Checking all PCI-DSS requirements...

              ✅ Compliance validation complete!

              📊 PCI-DSS Compliance Score: 85/100 (Mostly Compliant - Certifiable with fixes)

              ✅ **Compliant (10 requirements)**:
              - Requirement 1: Firewall configuration (API Gateway)
              - Requirement 2: Vendor defaults changed (configuration planned)
              - Requirement 6: Secure development process (documentation needed)
              - ... (7 more)

              ⚠️ **Needs Attention (2 requirements)**:
              - Requirement 3: Protect stored cardholder data
                * Current: Payment Service uses tokenization ✅
                * Missing: Database encryption at rest ❌
                * Action: Enable encryption for Payment Service database

              - Requirement 4: Encrypt transmission of cardholder data
                * Current: HTTPS for all external communication ✅
                * Missing: Encryption for internal service-to-service ❌
                * Action: Implement mTLS between services

              📋 Compliance Checklist:
              - [ ] Enable database encryption at rest for Payment Service
              - [ ] Implement mTLS for internal service communication
              - [ ] Document secure development practices
              - [ ] Set up quarterly vulnerability scans
              - [ ] Configure automated security testing in CI/CD
              - [ ] Implement access logging and monitoring
              - [ ] Create incident response plan

              Saved to: validation-report.json

              Moving to security analysis...
```

### Step 9: Security Analysis

```
Orchestrator: [5/7] 🔒 Running security analysis with threat modeling...

              Analyzing security posture...
              Generating STRIDE threat model...

              ✅ Security analysis complete!

              📊 Security Score: 80/100 (Good - Production-ready with fixes)

              🚨 **Critical Issues (0)**: None! 🎉

              ⚠️ **High Priority (2)**:
              1. Database Encryption
                 - Issue: Payment Service database not encrypted at rest
                 - Impact: PCI-DSS violation, data exposure risk
                 - Recommendation: Enable AWS RDS encryption
                 - Effort: 1 day

              2. Internal Service Communication
                 - Issue: No encryption between microservices
                 - Impact: Man-in-the-middle attack risk in VPC
                 - Recommendation: Implement mutual TLS (mTLS)
                 - Effort: 3-5 days

              ℹ️ **Medium Priority (4)**:
              1. Rate Limiting Granularity
              2. API Key Rotation
              3. Database Connection Pooling
              4. Logging Sensitive Data

              ℹ️ **Low Priority (6)**:
              (Minor improvements for defense-in-depth)

              🛡️ **STRIDE Threat Model**:

              Spoofing:
              ✅ API Gateway handles authentication
              ✅ JWT tokens with short expiry
              ⚠️ Add service-to-service authentication (mTLS)

              Tampering:
              ✅ HTTPS prevents request tampering
              ⚠️ Add request signing for critical operations

              Repudiation:
              ✅ Comprehensive audit logging planned
              ✅ Event sourcing for order changes

              Information Disclosure:
              ✅ API Gateway prevents unauthorized access
              ⚠️ Encrypt data at rest (payment DB)
              ⚠️ Encrypt inter-service communication

              Denial of Service:
              ✅ Rate limiting at API Gateway
              ✅ Auto-scaling for traffic spikes
              ⚠️ Add circuit breakers for graceful degradation

              Elevation of Privilege:
              ✅ Role-based access control (RBAC)
              ✅ Principle of least privilege
              ✅ Separate payment service with limited access

              Saved to: security-report.json

              Moving to documentation generation...
```

### Step 10: Documentation Generation

```
Orchestrator: [6/7] 📚 Generating comprehensive documentation...

              Creating documentation in multiple formats...

              ✅ Documentation generated!

              📁 Created files in docs/:

              **Architecture Overview**:
              - docs/README.md
                * System overview
                * Architecture decisions
                * Technology choices
                * Getting started guide

              **C4 Diagrams**:
              - docs/diagrams/system-context.puml (PlantUML)
              - docs/diagrams/system-context.svg (rendered)
              - docs/diagrams/container-diagram.puml
              - docs/diagrams/container-diagram.svg
              - docs/diagrams/component-diagrams/*.puml (24 files)

              - docs/diagrams/system-context.mmd (Mermaid)
              - docs/diagrams/container-diagram.mmd
              - docs/diagrams/component-diagrams/*.mmd

              **Architecture Decision Records (ADRs)**:
              - docs/adr/001-microservices-architecture.md
                * Decision: Use microservices
                * Context: Scalability and independent deployment needs
                * Consequences: Increased complexity, better scalability

              - docs/adr/002-event-driven-communication.md
                * Decision: Use Kafka for async communication
                * Context: Loose coupling and scalability
                * Consequences: Eventual consistency, better resilience

              - docs/adr/003-payment-service-isolation.md
                * Decision: Separate payment service
                * Context: PCI-DSS compliance requirement
                * Consequences: Reduced PCI scope, easier compliance

              - docs/adr/004-database-per-service.md
              - docs/adr/005-api-gateway-pattern.md
              - docs/adr/006-jwt-authentication.md

              **Deployment Guide**:
              - docs/DEPLOYMENT.md
                * Prerequisites
                * Infrastructure setup
                * Service deployment order
                * Configuration
                * Monitoring setup
                * Troubleshooting

              **API Documentation**:
              - docs/API.md
                * All endpoints documented
                * Request/response examples
                * Authentication requirements
                * Rate limits

              Moving to infrastructure generation...
```

### Step 11: Infrastructure Generation

```
Orchestrator: [7/7] 🏗️ Creating infrastructure-as-code...

              Generating Terraform for AWS...
              Applying PCI-DSS security configuration...
              Configuring multi-AZ and auto-scaling...

              ✅ Infrastructure code generated!

              📁 Created infrastructure/ directory:

              infrastructure/
              ├── main.tf
              │   - VPC with public/private subnets (3 AZs)
              │   - ECS cluster for microservices
              │   - RDS PostgreSQL (encrypted, multi-AZ)
              │   - MongoDB Atlas cluster
              │   - ElastiCache Redis
              │   - MSK (Managed Kafka)
              │   - Application Load Balancer
              │   - WAF for DDoS protection
              │   - CloudWatch monitoring
              │   - KMS encryption keys
              │
              ├── variables.tf
              │   - Configurable parameters
              │   - Environment-specific values
              │
              ├── outputs.tf
              │   - Endpoint URLs
              │   - Database connection strings
              │   - Monitoring dashboard URLs
              │
              ├── terraform.tfvars.example
              │   - Template for your values
              │
              ├── modules/
              │   ├── api-gateway/
              │   ├── microservice/
              │   ├── database/
              │   └── monitoring/
              │
              └── README.md
                  - Deployment instructions
                  - Cost estimates
                  - Maintenance guide

              **Configuration Highlights**:

              ✅ PCI-DSS Compliant:
              - Encrypted databases (RDS, Redis)
              - Network isolation (private subnets)
              - WAF for protection
              - CloudWatch logs for audit trail

              ✅ Highly Available:
              - Multi-AZ deployment (3 availability zones)
              - Auto-scaling (2-10 instances per service)
              - Load balancing across zones
              - Automated backups (35 days for critical services)

              ✅ Production-Ready:
              - Monitoring and alerting
              - Automated scaling policies
              - Security groups and NACLs
              - Secrets management via AWS Secrets Manager

              **Estimated Monthly Cost**: $2,400 - $4,800 (depending on traffic)

              Breakdown:
              - ECS services: $800 - $2,000
              - RDS databases: $600 - $1,200
              - MongoDB Atlas: $400 - $800
              - MSK (Kafka): $300 - $600
              - Data transfer: $200 - $500
              - Misc (WAF, CloudWatch, etc.): $100 - $300

              Deployment ready!
```

### Step 12: Final Summary & Next Steps

```
Orchestrator: 🎉 Architecture Design Complete for OrderFlow!

              ⏱️ Completed in: 9 minutes 32 seconds

              📊 **Final Summary**:

              Quality:      78/100 (Good - Ready with minor improvements)
              Compliance:   85/100 (PCI-DSS - Certifiable with fixes)
              Security:     80/100 (Production-ready with 2 fixes)
              Architecture: Microservices with Event-Driven Communication
              Services:     8 containers, 24 components
              Cloud:        AWS with multi-AZ deployment

              📁 **Generated Files**:

              ✅ requirements.json           (28 reqs, 15 user stories)
              ✅ architecture.json           (complete C4 model)
              ✅ archchar-analysis.md        (quality analysis)
              ✅ archchar-analysis.json      (machine-readable scores)
              ✅ validation-report.json      (PCI-DSS checklist)
              ✅ security-report.json        (threats & recommendations)
              ✅ docs/                       (comprehensive documentation)
              ✅ infrastructure/             (Terraform IaC)

              🚨 **Before You Deploy - Critical Actions**:

              Priority 1 (Required for PCI-DSS):
              [ ] 1. Enable RDS encryption for Payment Service database
              [ ] 2. Implement mTLS for inter-service communication

              Priority 2 (Highly Recommended):
              [ ] 3. Add Redis caching layer for Product Service
              [ ] 4. Implement circuit breakers for external service calls

              Priority 3 (Quality Improvements):
              [ ] 5. Set up comprehensive integration tests
              [ ] 6. Configure monitoring dashboards and alerts
              [ ] 7. Create runbooks for operations

              🚀 **Ready to Deploy?**

              1. Review the documentation in docs/README.md
              2. Complete the critical actions above
              3. Configure terraform.tfvars with your AWS settings
              4. Deploy infrastructure:
                 ```
                 cd infrastructure
                 terraform init
                 terraform plan
                 terraform apply
                 ```
              5. Deploy services (see docs/DEPLOYMENT.md)
              6. Run security scan and penetration testing
              7. Apply for PCI-DSS certification

              **What would you like to do next?**
              1. Review the architecture model in detail
              2. Understand the PCI-DSS compliance requirements
              3. Walk through the security recommendations
              4. Learn about deployment steps
              5. Refine the architecture (add features, change decisions)
              6. Generate additional documentation
              7. Export for visual editing in bac4-standalone
              8. Something else
```

---

## Complete Example: E-Commerce Platform

### Scenario

You're building an e-commerce platform called "ShopEasy" with:
- Product catalog
- Shopping cart
- Checkout and payment
- Order management
- Customer accounts
- Inventory tracking
- PCI-DSS compliance required

### Requirements Document

Create `docs/requirements.md`:

```markdown
# ShopEasy E-Commerce Platform Requirements

## Project Overview
ShopEasy is a modern e-commerce platform for small to medium businesses.

## Functional Requirements

### Product Management
- FR-001: Users can browse product catalog
- FR-002: Users can search products by keyword
- FR-003: Users can filter products by category, price, rating
- FR-004: Users can view product details with images

### Shopping Cart
- FR-005: Users can add products to cart
- FR-006: Users can update quantities
- FR-007: Users can remove items
- FR-008: Cart persists across sessions

### Checkout & Payment
- FR-009: Users can checkout as guest or registered
- FR-010: Users can enter shipping address
- FR-011: Users can choose shipping method
- FR-012: Users can pay with credit card
- FR-013: System processes payments securely (PCI-DSS)

### Order Management
- FR-014: Users can view order history
- FR-015: Users can track order status
- FR-016: Users receive order confirmation email
- FR-017: Admin can manage orders

### Customer Accounts
- FR-018: Users can register account
- FR-019: Users can login
- FR-020: Users can manage profile
- FR-021: Users can save addresses

## Non-Functional Requirements

### Performance
- NFR-001: Support 10,000 concurrent users
- NFR-002: Product search < 500ms response time
- NFR-003: Checkout process < 3 seconds

### Scalability
- NFR-004: Scale horizontally to handle traffic spikes
- NFR-005: Handle 1000 orders per minute during peak

### Availability
- NFR-006: 99.9% uptime for shopping and checkout
- NFR-007: Graceful degradation if services fail

### Security
- NFR-008: PCI-DSS Level 1 compliance
- NFR-009: HTTPS for all connections
- NFR-010: Secure password storage (bcrypt)
- NFR-011: Rate limiting on APIs

### Reliability
- NFR-012: No data loss for orders
- NFR-013: Automated backups daily

## Technical Constraints
- TC-001: Must use AWS cloud
- TC-002: Microservices preferred for scalability
- TC-003: Use managed services where possible
- TC-004: Support mobile-responsive web UI

## Compliance
- Must comply with PCI-DSS for payment processing
- Must comply with GDPR for customer data

## Stakeholders
- Product Manager: Jane Smith
- Engineering Lead: John Doe
- Security Officer: Sarah Johnson
```

### Running SAAT

```bash
# In Claude Code:
/saat-orchestrate

# Tell the orchestrator:
"Design a new e-commerce platform called ShopEasy.
Requirements are in docs/requirements.md.
Need PCI-DSS compliance."

# SAAT will:
# 1. Extract 21 functional requirements
# 2. Extract 13 non-functional requirements
# 3. Generate microservices architecture
# 4. Analyze quality (target: 80/100+)
# 5. Validate PCI-DSS compliance
# 6. Analyze security
# 7. Generate documentation
# 8. Create AWS Terraform infrastructure

# Result: Complete, deployment-ready architecture in ~10 minutes
```

### What You Get

```
shop-easy/
├── docs/
│   ├── requirements.md           (your input)
│   ├── README.md                 (generated overview)
│   ├── DEPLOYMENT.md             (generated deployment guide)
│   ├── API.md                    (generated API docs)
│   ├── diagrams/                 (generated C4 diagrams)
│   └── adr/                      (generated ADRs)
├── requirements.json             (extracted requirements)
├── architecture.json             (C4 model)
├── archchar-analysis.md          (quality report)
├── validation-report.json        (PCI-DSS checklist)
├── security-report.json          (security analysis)
└── infrastructure/               (Terraform IaC)
    ├── main.tf
    ├── variables.tf
    └── ...
```

---

## Best Practices

### 1. Write Comprehensive Requirements

**Good Requirements Document**:
```markdown
## Functional Requirement
**FR-012**: Users can pay with credit card

**Details**:
- Accept Visa, Mastercard, Amex
- Store card securely (tokenization)
- Support one-time and saved cards
- CVV required for all transactions
- 3D Secure authentication for high-value

**Non-Functional**:
- Processing time < 2 seconds
- 99.99% availability
- PCI-DSS Level 1 compliance
```

**Why It Helps**:
- SAAT can design more accurate architecture
- Better security recommendations
- Compliance checking is more precise

### 2. Be Specific About Compliance

Instead of:
> "Need to be secure and compliant"

Write:
> "Must comply with:
> - PCI-DSS Level 1 (we process >6M transactions/year)
> - GDPR (EU customers)
> - SOC 2 Type II (enterprise customers require it)"

### 3. Include Scale Requirements

Instead of:
> "Should handle lots of users"

Write:
> "Must handle:
> - 50,000 concurrent users (Black Friday peak)
> - 5,000 orders per minute (checkout)
> - 100,000 searches per minute (product catalog)
> - 10TB total data (growing 2TB/year)"

### 4. Specify Technology Constraints

```markdown
## Technical Constraints
- Must use AWS (existing infrastructure)
- Must integrate with existing ERP (SAP)
- Team expertise: Java, Node.js, React
- Cannot use Lambda (cold start issues in past)
- Prefer managed services (small DevOps team)
```

### 5. Iterate and Refine

Don't expect perfection on first try:

```
You: /saat-orchestrate

Orchestrator: [generates architecture]

You: I'd like to change the database for Product Service
     from MongoDB to PostgreSQL for consistency

Orchestrator: No problem! Let me regenerate the architecture
              with PostgreSQL for Product Service...
              [regenerates with changes]

You: Perfect! Can you also add a recommendation service
     for product recommendations?

Orchestrator: Great idea! I'll add a Recommendation Service
              and integrate it with the Product Service...
```

### 6. Use the Orchestrator's Questions

When the Orchestrator asks clarifying questions, **answer them thoroughly**:

```
Orchestrator: I see you need PCI-DSS compliance.
              Do you want to:
              1. Process payments yourself (requires full PCI-DSS)
              2. Use payment gateway (Stripe, Braintree - easier compliance)

You: We want to use Stripe to minimize PCI scope

Orchestrator: Excellent choice! This reduces your PCI-DSS scope
              significantly. I'll design the Payment Service to
              tokenize cards immediately and use Stripe API.
```

---

## Troubleshooting

### Issue: "Requirements extraction found very few requirements"

**Cause**: Document might be too brief or not structured

**Solution**:
1. Add more detail to requirements document
2. Use clear headings: "Functional Requirements", "Non-Functional Requirements"
3. Use bullet points or numbered lists
4. Include multiple documents if needed

### Issue: "Architecture score is low (50/100)"

**Cause**: Requirements might not specify quality needs

**Solution**:
1. Add non-functional requirements (NFRs)
2. Specify scalability needs
3. Mention availability requirements
4. Include performance targets
5. Ask orchestrator: "How can I improve the quality score?"

### Issue: "Compliance validation shows many gaps"

**Cause**: This is normal for initial design!

**Solution**:
- Review the compliance checklist
- Implement the recommended controls
- Ask orchestrator for implementation guidance
- Some requirements need manual processes (policy, training)

### Issue: "Want to change technology choices"

**Solution**:
```
You: Can we use PostgreSQL instead of MongoDB for the Product Service?

Orchestrator: Absolutely! Let me regenerate the architecture...
```

The Orchestrator is conversational - just ask!

### Issue: "Need to add a new service"

**Solution**:
```
You: I'd like to add a Notification Service for sending emails and SMS

Orchestrator: Great idea! I'll:
             1. Add Notification Service to the architecture
             2. Connect it to relevant services (Order, User)
             3. Update quality analysis
             4. Update documentation
             5. Update infrastructure code

             [regenerates everything with new service]
```

---

## Next Steps

After completing your greenfield design:

1. **Review Generated Files**
   - Read `docs/README.md` for architecture overview
   - Review `archchar-analysis.md` for quality improvements
   - Check `validation-report.json` for compliance tasks
   - Study `security-report.json` for security recommendations

2. **Complete Critical Actions**
   - Implement required security controls
   - Set up compliance requirements
   - Configure monitoring and alerting

3. **Deploy Infrastructure**
   - Configure `terraform.tfvars`
   - Run `terraform apply`
   - Deploy services

4. **Build Services**
   - Use architecture as blueprint
   - Follow component specifications
   - Implement recommended patterns

5. **Iterate**
   - Run `/saat-orchestrate` again as requirements change
   - Keep architecture and code in sync

---

## Related Guides

- **[Brownfield Guide](BROWNFIELD_GUIDE.md)** - Analyzing existing codebases
- **[Customization Guide](CUSTOMIZATION_GUIDE.md)** - Customizing SAAT
- **[Orchestrator Guide](ORCHESTRATOR_GUIDE.md)** - Advanced orchestrator usage
- **[Architecture Characteristics Guide](ARCHITECTURE_CHARACTERISTICS_USAGE.md)** - Deep dive into quality analysis

---

**Happy Designing! 🎨🏗️**
