# Architecture Characteristics Reference

**Source**: Fundamentals of Software Architecture by Mark Richards and Neal Ford
**Purpose**: Knowledge base for SAAT architecture characteristics analysis

---

## Overview

Architecture characteristics (also called "non-functional requirements" or "-ilities") define the success criteria of a system. They determine **how well** a system performs its functions under real-world conditions, as opposed to functional requirements which dictate **what** a system does.

### Key Principles

1. **Limit the Number**: Try to identify and prioritize only the most critical characteristics (typically 7 or fewer driving characteristics)
2. **Explicit Over Implicit**: Make architecture characteristics explicit rather than assumed
3. **Measurable**: Each characteristic should be measurable or testable
4. **Context-Dependent**: The importance of characteristics varies based on business requirements and system context

---

## Three Categories of Architecture Characteristics

### 1. Operational Characteristics

**Definition**: Characteristics related to how the system operates at runtime, including reliability, resilience, and performance under load.

**Key Aspects**:
- Day-to-day behavior of the software
- Overlap heavily with operations and DevOps concerns
- Most often require special structural support from architects
- Critical for system availability and user experience

**Common Operational Characteristics**:

| Characteristic | Definition | Considerations |
|---------------|------------|----------------|
| **Availability** | System is accessible and operational when required | Uptime requirements, failover strategies, redundancy |
| **Scalability** | Ability to handle increased workload by adding resources | Horizontal vs vertical scaling, elasticity, load patterns |
| **Performance** | Speed and efficiency in executing tasks | Response time, throughput, latency requirements |
| **Reliability** | Ability to function correctly and consistently over time | Error rates, MTBF (Mean Time Between Failures) |
| **Recoverability** | Ability to restore functionality after a failure | RTO (Recovery Time Objective), RPO (Recovery Point Objective) |
| **Fault Tolerance** | Ability to continue operating despite component failures | Graceful degradation, circuit breakers, redundancy |

### 2. Structural Characteristics

**Definition**: Characteristics related to the code structure, organization, and ease of modification.

**Key Aspects**:
- Internal quality of the codebase
- Architect's responsibility for code quality concerns
- Enable long-term system evolution
- Impact development velocity and team productivity

**Common Structural Characteristics**:

| Characteristic | Definition | Considerations |
|---------------|------------|----------------|
| **Maintainability** | Ease of applying changes and enhancements | Code clarity, documentation, modularity |
| **Testability** | Ease of testing the system for defects | Test coverage, automation, isolated components |
| **Deployability** | Ease and frequency of deployment | CI/CD pipelines, deployment automation, rollback capabilities |
| **Configurability** | Ability to change system behavior through configuration | Environment-specific settings, feature flags |
| **Extensibility** | Ease of adding new functionality | Plugin architecture, extension points, open/closed principle |

### 3. Cross-Cutting Characteristics

**Definition**: Characteristics that affect multiple modules or components throughout the application, spanning across the system as a whole.

**Key Aspects**:
- Concern multiple areas of the system simultaneously
- Often require architectural decisions that impact the entire codebase
- Include concerns that don't fit neatly into operational or structural categories

**Common Cross-Cutting Characteristics**:

| Characteristic | Definition | Considerations |
|---------------|------------|----------------|
| **Security** | Protection of data and functionality from unauthorized access | Authentication, authorization, encryption, compliance |
| **Interoperability** | Ability to exchange data and interact with other systems | API standards, data formats, protocols |
| **Usability** | Ease of use and user experience | UI/UX design, accessibility, learning curve |

---

## Architecture Characteristics in Detail

### Availability
- **Definition**: The percentage of time a system is operational and accessible
- **Measurement**: Uptime percentage (e.g., 99.9%, 99.99%)
- **Patterns**: Active-active clusters, load balancing, geographic distribution
- **Trade-offs**: Often conflicts with cost; high availability is expensive

### Scalability
- **Types**:
  - **Vertical Scaling**: Adding more power to existing machines
  - **Horizontal Scaling**: Adding more machines
  - **Elasticity**: Automatic scaling based on demand
- **Measurement**: Requests per second, concurrent users, data volume capacity
- **Patterns**: Microservices, caching, database sharding, load balancing
- **Trade-offs**: Complexity increases with distributed systems

### Performance
- **Aspects**:
  - **Latency**: Time to process a single request
  - **Throughput**: Number of requests processed per unit time
  - **Resource Utilization**: CPU, memory, network, disk usage
- **Measurement**: Response time (p50, p95, p99), transactions per second
- **Patterns**: Caching, CDNs, database optimization, asynchronous processing
- **Trade-offs**: Often conflicts with flexibility and ease of development

### Security
- **Layers**:
  - **Authentication**: Verifying identity
  - **Authorization**: Controlling access
  - **Confidentiality**: Protecting data privacy
  - **Integrity**: Ensuring data accuracy
  - **Non-repudiation**: Proving actions occurred
- **Measurement**: Vulnerability assessments, penetration testing, audit compliance
- **Patterns**: Defense in depth, least privilege, encryption at rest and in transit
- **Trade-offs**: Often conflicts with usability and performance

### Reliability
- **Metrics**:
  - **MTBF**: Mean Time Between Failures
  - **MTTR**: Mean Time To Recovery
  - **Error Rate**: Percentage of failed operations
- **Patterns**: Redundancy, health checks, graceful degradation
- **Trade-offs**: Reliability often requires additional complexity and cost

### Maintainability
- **Aspects**:
  - **Code Quality**: Readability, consistency, documentation
  - **Modularity**: Separation of concerns, low coupling
  - **Technical Debt**: Accumulated shortcuts and compromises
- **Measurement**: Cyclomatic complexity, code coverage, technical debt ratio
- **Patterns**: Clean architecture, SOLID principles, refactoring
- **Trade-offs**: Time spent on maintainability vs. feature delivery

### Testability
- **Types**:
  - **Unit Testing**: Individual component testing
  - **Integration Testing**: Component interaction testing
  - **System Testing**: End-to-end testing
  - **Performance Testing**: Load and stress testing
- **Measurement**: Test coverage, test execution time, defect detection rate
- **Patterns**: Dependency injection, mocking, test automation
- **Trade-offs**: Test infrastructure requires time and resources

### Deployability
- **Aspects**:
  - **Deployment Frequency**: How often can you deploy?
  - **Deployment Duration**: How long does deployment take?
  - **Deployment Risk**: What's the impact of a failed deployment?
- **Measurement**: Deployment frequency, lead time, rollback time
- **Patterns**: CI/CD, blue-green deployment, canary releases, feature flags
- **Trade-offs**: Automation requires upfront investment

### Fault Tolerance
- **Strategies**:
  - **Redundancy**: Multiple instances of components
  - **Circuit Breakers**: Preventing cascade failures
  - **Bulkheads**: Isolating failures
  - **Timeouts**: Preventing indefinite waits
- **Measurement**: Failure detection time, recovery time, degradation impact
- **Patterns**: Retry logic, fallback mechanisms, health monitoring

### Recoverability
- **Requirements**:
  - **RTO (Recovery Time Objective)**: Maximum acceptable downtime
  - **RPO (Recovery Point Objective)**: Maximum acceptable data loss
- **Strategies**: Backups, replication, disaster recovery plans
- **Measurement**: Backup frequency, restoration time, data loss amount
- **Trade-offs**: Faster recovery requires more resources and complexity

### Interoperability
- **Aspects**:
  - **Data Exchange**: APIs, message formats, protocols
  - **Standards Compliance**: Industry standards, compatibility
  - **Integration Patterns**: Synchronous vs asynchronous, event-driven
- **Measurement**: Integration points, data format compatibility, API versioning
- **Patterns**: REST APIs, GraphQL, message queues, event buses

### Configurability
- **Types**:
  - **Environment Configuration**: Dev, test, prod settings
  - **Feature Flags**: Enabling/disabling features
  - **User Configuration**: User-specific settings
- **Patterns**: Configuration management, externalized configuration
- **Trade-offs**: Too much configurability increases complexity

### Extensibility
- **Approaches**:
  - **Plugin Architecture**: Adding functionality via plugins
  - **Open/Closed Principle**: Open for extension, closed for modification
  - **Extension Points**: Defined interfaces for customization
- **Patterns**: Strategy pattern, decorator pattern, dependency injection
- **Trade-offs**: Premature extensibility can lead to over-engineering

### Usability
- **Aspects**:
  - **Learnability**: How quickly can users learn the system?
  - **Efficiency**: How efficiently can users complete tasks?
  - **Memorability**: How easily do users remember how to use it?
  - **Error Prevention**: How well does the system prevent errors?
- **Measurement**: User satisfaction scores, task completion time, error rates
- **Patterns**: User-centered design, accessibility standards, progressive disclosure

---

## Identifying Architecture Characteristics

### Sources for Identifying Characteristics

1. **Explicit Domain Requirements**
   - Stated non-functional requirements
   - SLAs (Service Level Agreements)
   - Compliance requirements

2. **Implicit Domain Knowledge**
   - Industry standards
   - Common expectations
   - Domain expertise

3. **Business Context**
   - Time to market → agility, testability, deployability
   - Mergers and acquisitions → interoperability, scalability, adaptability, extensibility
   - User satisfaction → performance, availability, usability

### Prioritization Strategy

**The Rule of 7**: Try to identify no more than 7 driving architecture characteristics

**Why Limit?**
- Each characteristic requires architectural effort
- Too many characteristics lead to conflicts and trade-offs
- Focus on what truly matters for success
- Some characteristics naturally support others

**Prioritization Process**:
1. Identify all potential characteristics from requirements
2. Analyze business priorities and context
3. Consider technical constraints
4. Rank by criticality to system success
5. Select top 7 (or fewer) driving characteristics
6. Document rationale for selection

---

## Measuring Architecture Characteristics

### Operational Metrics
- **Availability**: Uptime percentage, downtime incidents
- **Performance**: Response time, throughput, latency percentiles
- **Scalability**: Load capacity, resource utilization under load
- **Reliability**: Error rate, MTBF, MTTR

### Structural Metrics
- **Maintainability**: Cyclomatic complexity, code churn, technical debt
- **Testability**: Test coverage, test execution time
- **Deployability**: Deployment frequency, lead time, failure rate

### Cross-Cutting Metrics
- **Security**: Vulnerability count, audit findings, compliance status
- **Usability**: User satisfaction scores, task completion rates

---

## Architecture Characteristics and Patterns

Different architectural patterns support different characteristics:

| Pattern | Strong Support For | Weak Support For |
|---------|-------------------|------------------|
| **Layered** | Simplicity, testability | Performance, scalability |
| **Microservices** | Scalability, deployability, fault tolerance | Simplicity, consistency, performance |
| **Event-Driven** | Scalability, extensibility, fault tolerance | Simplicity, testability, consistency |
| **Space-Based** | Scalability, performance, availability | Consistency, simplicity |
| **Service-Based** | Domain partitioning, deployability | Scalability, fault tolerance |
| **Serverless** | Scalability, elasticity, cost efficiency | Performance, vendor lock-in |

---

## Trade-offs and Conflicts

Common conflicts between architecture characteristics:

- **Performance vs. Security**: Encryption adds overhead
- **Scalability vs. Consistency**: CAP theorem trade-offs
- **Flexibility vs. Simplicity**: More options increase complexity
- **Cost vs. Availability**: High availability is expensive
- **Speed to Market vs. Maintainability**: Quick solutions may create technical debt

**Resolution Strategy**:
1. Understand business priorities
2. Quantify the impact of trade-offs
3. Make explicit decisions
4. Document rationale
5. Revisit as context changes

---

## Using This Reference

This document serves as a knowledge base for:
1. Understanding what architecture characteristics mean
2. Identifying relevant characteristics for a system
3. Evaluating system designs against characteristics
4. Making informed architectural decisions
5. Analyzing and providing recommendations

**For Analysis**: When analyzing a system, refer to the detailed descriptions to understand what each characteristic requires in terms of patterns, structures, and trade-offs.

**For Recommendations**: Use the patterns and considerations sections to provide specific, actionable recommendations for improving systems to meet their architecture characteristics.

---

## References

- **Fundamentals of Software Architecture** (1st Edition, 2020) - Mark Richards, Neal Ford
- **Fundamentals of Software Architecture** (2nd Edition, 2024) - Mark Richards, Neal Ford
- Mark Richards' Architecture Characteristics Worksheet
- DeveloperToArchitect.com

---

**Last Updated**: 2025-10-31
**For**: SAAT (Solution Architecture Agent Toolkit)
**Purpose**: Reference for architecture characteristics analysis agent
