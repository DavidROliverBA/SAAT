# Solution Architecture Agent Toolkit - Implementation Prompt

## Project: SA Agent Toolkit (SAAT)

Build a comprehensive agent-based toolkit for solution architects that automates C4 model creation, validation, and documentation generation using context-engineered AI agents.

## Core Architecture

### 1. Type Definitions

First, define all core types and interfaces:

```typescript
// Core C4 Model Types
interface C4Model {
  version: string;
  metadata: ModelMetadata;
  systems: SystemContext[];
  containers: Container[];
  components: Component[];
  externals: ExternalSystem[];
  relationships: Relationship[];
}

interface ModelMetadata {
  name: string;
  description: string;
  author: string;
  created: string;
  modified: string;
  domain?: string;
  criticality?: CriticalityLevel;
}

type CriticalityLevel = 'CS1' | 'CS2' | 'SL1' | 'SL2' | 'STANDARD';

interface SystemContext {
  id: string;
  name: string;
  description: string;
  type: 'system';
  technology?: string;
  criticality: CriticalityLevel;
  tags?: string[];
}

interface Container {
  id: string;
  name: string;
  description: string;
  type: 'container';
  technology: string;
  runtime_type: 'service' | 'database' | 'queue' | 'cache' | 'storage';
  criticality: CriticalityLevel;
  parent_system: string;
  tags?: string[];
}

interface Component {
  id: string;
  name: string;
  description: string;
  type: 'component';
  technology: string;
  component_type: 'api' | 'service' | 'repository' | 'controller' | 'utility';
  parent_container: string;
  tags?: string[];
}

interface ExternalSystem {
  id: string;
  name: string;
  description: string;
  type: 'external';
  classification: 'SAAS' | 'PAAS' | 'MANAGED_API' | 'INDUSTRY_SYSTEM' | 'PARTNER_SYSTEM';
  vendor?: string;
  sla?: SLA;
  integration_pattern?: string;
}

interface Relationship {
  id: string;
  source: string;
  target: string;
  description: string;
  protocol?: string;
  async?: boolean;
}

interface SLA {
  availability: number;
  response_time_ms?: number;
  rate_limit?: RateLimit;
}

interface RateLimit {
  requests: number;
  period: string;
}

// Agent System Types
interface Agent<TParams = unknown, TResult = unknown> {
  name: string;
  version: string;
  capabilities: string[];
  contextTemplate: string;
  execute(task: string, params: TParams): Promise<AgentResult<TResult>>;
  validate(input: TParams): ValidationResult;
}

interface AgentResult<T = unknown> {
  success: boolean;
  data: T;
  confidence: number;
  errors?: AgentError[];
  suggestions?: string[];
  metadata?: Record<string, unknown>;
}

interface AgentError {
  code: string;
  message: string;
  severity: 'error' | 'warning' | 'info';
  element?: string;
  fix?: string;
}

interface ValidationResult {
  valid: boolean;
  score: number;
  errors: AgentError[];
  warnings: AgentError[];
}

// Discovery Types
interface DiscoveryResult {
  timestamp: string;
  repository: string;
  technologies: string[];
  containers: ContainerInfo[];
  apis: APIInfo[];
  databases: DatabaseInfo[];
  externals: ExternalDependency[];
  patterns: string[];
}

interface ContainerInfo {
  name: string;
  path: string;
  technology: string;
  runtime_type: string;
  dependencies: string[];
}

interface APIInfo {
  name: string;
  type: 'REST' | 'GraphQL' | 'gRPC' | 'WebSocket';
  endpoints: Endpoint[];
  specification?: string;
}

interface Endpoint {
  method: string;
  path: string;
  description?: string;
}

interface DatabaseInfo {
  name: string;
  type: string;
  schema?: string;
}

interface ExternalDependency {
  name: string;
  url?: string;
  type: string;
}

// Pipeline Types
interface Pipeline {
  name: string;
  version: string;
  steps: PipelineStep[];
}

interface PipelineStep {
  name: string;
  agent: string;
  task: string;
  required: boolean;
  constraints?: Record<string, unknown>;
  parameters?: Record<string, unknown>;
  depends_on?: string[];
}

interface PipelineResult {
  success: boolean;
  steps: Map<string, StepResult>;
  duration: number;
  errors: AgentError[];
}

interface StepResult {
  success: boolean;
  data: unknown;
  duration: number;
  error?: AgentError;
}

// Context Types
interface ArchitecturalContext {
  model?: C4Model;
  discovery?: DiscoveryResult;
  business?: BusinessContext;
  metadata: Map<string, unknown>;
  getRelevant(agent: string): Record<string, unknown>;
  update(result: unknown): void;
}

interface BusinessContext {
  purpose: string;
  stakeholders: Stakeholder[];
  capabilities: string[];
  compliance: ComplianceRequirement[];
}

interface Stakeholder {
  name: string;
  role: string;
  needs: string[];
  interactions: string[];
}

interface ComplianceRequirement {
  framework: string;
  requirements: string[];
  applicable: boolean;
}

// Configuration Types
interface SAATConfig {
  agents: AgentConfigs;
  llm: LLMConfig;
  pipelines: PipelineConfig;
  output: OutputConfig;
}

interface AgentConfigs {
  discovery?: AgentConfig;
  validation?: AgentConfig;
  documentation?: AgentConfig;
  terraform?: AgentConfig;
  security?: AgentConfig;
  fitness?: AgentConfig;
  advisor?: AgentConfig;
}

interface AgentConfig {
  enabled: boolean;
  model?: string;
  max_tokens?: number;
  temperature?: number;
  [key: string]: unknown;
}

interface LLMConfig {
  primary: string;
  fallback?: string;
  claude?: LLMClientConfig;
  openai?: LLMClientConfig;
}

interface LLMClientConfig {
  api_key: string;
  model: string;
  max_tokens?: number;
  temperature?: number;
}

interface PipelineConfig {
  default: string;
  custom?: string[];
}

interface OutputConfig {
  directory: string;
  formats: {
    model: string;
    diagrams: string[];
    documentation: string;
  };
}
```

### 2. Agent System Design

Create a multi-agent system with the following specialized agents:

```typescript
interface AgentExecutor {
  name: string;
  version: string;
  capabilities: string[];
  contextTemplate: string;
  execute<T, R>(task: string, params: T): Promise<AgentResult<R>>;
  validate<T>(input: T): ValidationResult;
}
```

### 2. Required Agents to Implement

#### Discovery Agent
- **Purpose**: Analyze codebases and extract architectural information
- **Tasks**:
  - Scan repository structure
  - Identify microservices/containers
  - Extract API definitions from OpenAPI/Swagger
  - Find database schemas
  - Detect external dependencies
  - Identify deployment configurations (Docker, K8s, Terraform)

```typescript
class DiscoveryAgent implements Agent {
  async analyzeRepository(path: string): Promise<DiscoveryResult> {
    // Scan for:
    // - Package.json, pom.xml, go.mod (dependencies)
    // - Dockerfile, docker-compose.yml (containers)
    // - *.yaml, *.yml in k8s/ (deployments)
    // - swagger.json, openapi.yaml (APIs)
    // - .env, config/* (configurations)
    // Return structured architectural elements
  }
  
  async scanConfigurations(configPath: string): Promise<ConfigResult> {
    // Extract:
    // - Environment variables
    // - External service URLs
    // - Database connections
    // - API endpoints
  }
  
  async identifyPatterns(code: string): Promise<PatternResult> {
    // Detect:
    // - Architectural patterns (MVC, microservices, event-driven)
    // - Integration patterns (REST, GraphQL, gRPC, messaging)
    // - Data patterns (CQRS, event sourcing)
  }
}
```

#### Business Context Agent
- **Purpose**: Gather business context through structured interviews
- **Tasks**:
  - Conduct stakeholder interviews
  - Extract business capabilities
  - Identify compliance requirements
  - Map user journeys

```typescript
class BusinessContextAgent implements Agent {
  private interviewTemplates = {
    systemPurpose: [
      "What is the primary business purpose of this system?",
      "Who are the main users and stakeholders?",
      "What business processes does it support?",
      "What are the critical business outcomes?"
    ],
    stakeholders: [
      "What is each stakeholder's role?",
      "How do they interact with the system?",
      "What are their key needs?",
      "What data do they need access to?"
    ],
    compliance: [
      "What regulatory frameworks apply?",
      "Are there data residency requirements?",
      "What industry standards must be followed?",
      "What are the audit requirements?"
    ]
  };
  
  async conductInterview(type: string): Promise<InterviewResult> {
    // Interactive Q&A session
    // Store responses
    // Extract structured data
  }
}
```

#### JSON Generator Agent
- **Purpose**: Convert discovered information to C4 JSON format
- **Tasks**:
  - Generate valid C4 JSON
  - Maintain ID consistency
  - Apply criticality rules
  - Handle relationships

```typescript
class JSONGeneratorAgent implements Agent<GeneratorParams, C4Model> {
  private idCounters: Map<string, number> = new Map();

  private idGenerator = {
    system: (domain: string) => `SYS-${domain}-${this.getNextId('system')}`,
    container: (tech: string) => `CON-${tech}-${this.getNextId('container')}`,
    component: (type: string) => `CMP-${type}-${this.getNextId('component')}`,
    external: (vendor: string) => `EXT-${vendor}-${this.getNextId('external')}`
  };

  private getNextId(type: string): string {
    const current = this.idCounters.get(type) || 0;
    const next = current + 1;
    this.idCounters.set(type, next);
    return next.toString().padStart(3, '0');
  }

  async execute(task: string, params: GeneratorParams): Promise<AgentResult<C4Model>> {
    try {
      if (task === 'generate') {
        const model = await this.generateC4Model(params.discovery, params.business);
        return {
          success: true,
          data: model,
          confidence: this.calculateConfidence(model),
        };
      }
      throw new Error(`Unknown task: ${task}`);
    } catch (error) {
      return {
        success: false,
        data: {} as C4Model,
        confidence: 0,
        errors: [{
          code: 'GENERATION_ERROR',
          message: error.message,
          severity: 'error',
        }],
      };
    }
  }

  async generateC4Model(discovery: DiscoveryResult, business?: BusinessContext): Promise<C4Model> {
    const model: C4Model = {
      version: '1.0.0',
      metadata: {
        name: business?.purpose || 'Generated Architecture',
        description: 'Auto-generated C4 model',
        author: 'SAAT',
        created: new Date().toISOString(),
        modified: new Date().toISOString(),
      },
      systems: [],
      containers: [],
      components: [],
      externals: [],
      relationships: [],
    };

    // Map discovery results to C4 elements
    model.containers = discovery.containers.map(c => this.mapToContainer(c));
    model.externals = discovery.externals.map(e => this.mapToExternal(e));

    // Apply criticality standards
    await this.applyCriticalityStandards(model);

    // Generate hierarchical structure
    this.generateHierarchy(model);

    // Validate against schema
    await this.validateSchema(model);

    return model;
  }

  private mapToContainer(info: ContainerInfo): Container {
    return {
      id: this.idGenerator.container(info.technology),
      name: info.name,
      description: `Container for ${info.name}`,
      type: 'container',
      technology: info.technology,
      runtime_type: info.runtime_type as Container['runtime_type'],
      criticality: 'STANDARD',
      parent_system: 'SYS-DEFAULT-001',
      tags: info.dependencies,
    };
  }

  private mapToExternal(dep: ExternalDependency): ExternalSystem {
    return {
      id: this.idGenerator.external(dep.type),
      name: dep.name,
      description: `External dependency: ${dep.name}`,
      type: 'external',
      classification: 'SAAS',
      vendor: dep.type,
    };
  }

  private async applyCriticalityStandards(model: C4Model): Promise<void> {
    // Apply criticality levels based on system analysis
    // CS1: Critical safety systems (99.99% SLA)
    // CS2: Critical business systems (99.9% SLA)
    // SL1: Standard live systems (99.5% SLA)
    // SL2: Standard systems (99% SLA)
    // STANDARD: Everything else

    model.containers.forEach(container => {
      if (container.tags?.includes('payment') || container.tags?.includes('auth')) {
        container.criticality = 'CS2';
      } else if (container.tags?.includes('customer-facing')) {
        container.criticality = 'SL1';
      }
    });
  }

  private generateHierarchy(model: C4Model): void {
    // Ensure all elements have proper parent relationships
    const systems = new Set(model.containers.map(c => c.parent_system));
    systems.forEach(sysId => {
      if (!model.systems.find(s => s.id === sysId)) {
        model.systems.push({
          id: sysId,
          name: `System ${sysId}`,
          description: 'Auto-generated system context',
          type: 'system',
          criticality: 'STANDARD',
        });
      }
    });
  }

  private async validateSchema(model: C4Model): Promise<void> {
    // Validate that all required fields are present
    if (!model.version || !model.metadata) {
      throw new Error('Invalid model: missing required fields');
    }
  }

  validate(input: GeneratorParams): ValidationResult {
    const errors: AgentError[] = [];

    if (!input.discovery) {
      errors.push({
        code: 'MISSING_DISCOVERY',
        message: 'Discovery data is required',
        severity: 'error',
      });
    }

    return {
      valid: errors.length === 0,
      score: errors.length === 0 ? 100 : 0,
      errors,
      warnings: [],
    };
  }

  private calculateConfidence(model: C4Model): number {
    let score = 0.5;
    if (model.containers.length > 0) score += 0.2;
    if (model.externals.length > 0) score += 0.1;
    if (model.systems.length > 0) score += 0.1;
    if (model.relationships.length > 0) score += 0.1;
    return Math.min(score, 1.0);
  }
}

interface GeneratorParams {
  discovery: DiscoveryResult;
  business?: BusinessContext;
}
```

#### Validation Agent
- **Purpose**: Validate C4 models against rules and schemas
- **Tasks**:
  - Schema validation
  - Business rule checking
  - Security validation
  - Best practice checks

```typescript
class ValidationAgent implements Agent {
  private rules = {
    schema: SchemaValidator,
    business: BusinessRuleValidator,
    security: SecurityValidator,
    bestPractices: BestPracticeValidator
  };
  
  async validate(model: C4Model): Promise<ValidationResult> {
    const results = [];
    
    // Schema validation
    results.push(await this.validateSchema(model));
    
    // Business rules
    results.push(await this.validateBusinessRules(model));
    
    // Security checks
    results.push(await this.validateSecurity(model));
    
    // Best practices
    results.push(await this.validateBestPractices(model));
    
    return this.aggregateResults(results);
  }
  
  private validateBusinessRules(model: C4Model): ValidationResult {
    // CS1 systems must have 99.99% SLA
    // Critical systems need fallback strategies
    // External systems need integration containers
    // No direct external connections
  }
}
```

#### Documentation Agent
- **Purpose**: Generate comprehensive documentation
- **Tasks**:
  - Create ADRs
  - Generate Confluence pages
  - Produce README files
  - Create API documentation

```typescript
interface Documentation {
  type: string;
  content: string;
  metadata: {
    title: string;
    author: string;
    created: string;
  };
  attachments?: string[];
}

class DocumentationAgent implements Agent<DocParams, Documentation> {
  private templates: Map<string, (model: C4Model) => Promise<Documentation>>;

  constructor() {
    this.templates = new Map([
      ['adr', this.generateADR.bind(this)],
      ['confluence', this.generateConfluence.bind(this)],
      ['readme', this.generateReadme.bind(this)],
      ['api', this.generateAPIDoc.bind(this)],
    ]);
  }

  async execute(task: string, params: DocParams): Promise<AgentResult<Documentation>> {
    try {
      if (task === 'generate') {
        const doc = await this.generateDocumentation(params.model, params.type);
        return {
          success: true,
          data: doc,
          confidence: 0.9,
        };
      } else if (task === 'publish') {
        await this.publishToConfluence(params.documentation!);
        return {
          success: true,
          data: params.documentation!,
          confidence: 1.0,
        };
      }
      throw new Error(`Unknown task: ${task}`);
    } catch (error) {
      return {
        success: false,
        data: {} as Documentation,
        confidence: 0,
        errors: [{
          code: 'DOCUMENTATION_ERROR',
          message: error.message,
          severity: 'error',
        }],
      };
    }
  }

  async generateDocumentation(model: C4Model, type: string): Promise<Documentation> {
    const generator = this.templates.get(type);

    if (!generator) {
      throw new Error(`Unknown documentation type: ${type}`);
    }

    return await generator(model);
  }

  private async generateADR(model: C4Model): Promise<Documentation> {
    const content = `# ADR-001: ${model.metadata.name}

## Status
Proposed

## Context
${model.metadata.description}

## Decision
Implementing architecture with ${model.containers.length} containers and ${model.externals.length} external systems.

## Consequences
- Improved modularity
- Clear separation of concerns
- Defined integration points

## Alternatives Considered
- Monolithic architecture
- Serverless architecture
`;

    return {
      type: 'adr',
      content,
      metadata: {
        title: `ADR-001: ${model.metadata.name}`,
        author: 'SAAT',
        created: new Date().toISOString(),
      },
    };
  }

  private async generateConfluence(model: C4Model): Promise<Documentation> {
    const content = `h1. ${model.metadata.name}

h2. Overview
${model.metadata.description}

h2. Architecture
* Containers: ${model.containers.length}
* External Systems: ${model.externals.length}
* Components: ${model.components.length}

h2. Containers
${model.containers.map(c => `* *${c.name}*: ${c.description} (${c.technology})`).join('\n')}
`;

    return {
      type: 'confluence',
      content,
      metadata: {
        title: model.metadata.name,
        author: 'SAAT',
        created: new Date().toISOString(),
      },
    };
  }

  private async generateReadme(model: C4Model): Promise<Documentation> {
    const content = `# ${model.metadata.name}

## Overview
${model.metadata.description}

## Architecture

### Containers
${model.containers.map(c => `- **${c.name}** (${c.technology}): ${c.description}`).join('\n')}

### External Dependencies
${model.externals.map(e => `- ${e.name}: ${e.description}`).join('\n')}

## Getting Started
[Add setup instructions]

## Configuration
[Add configuration guide]
`;

    return {
      type: 'readme',
      content,
      metadata: {
        title: model.metadata.name,
        author: 'SAAT',
        created: new Date().toISOString(),
      },
    };
  }

  private async generateAPIDoc(model: C4Model): Promise<Documentation> {
    const apiContainers = model.containers.filter(c =>
      c.tags?.includes('api') || c.runtime_type === 'service'
    );

    const content = `# API Documentation: ${model.metadata.name}

## Services
${apiContainers.map(c => `### ${c.name}\n- Technology: ${c.technology}\n- Description: ${c.description}`).join('\n\n')}
`;

    return {
      type: 'api',
      content,
      metadata: {
        title: `API: ${model.metadata.name}`,
        author: 'SAAT',
        created: new Date().toISOString(),
      },
    };
  }

  async publishToConfluence(doc: Documentation): Promise<void> {
    const confluenceUrl = process.env.CONFLUENCE_URL;
    const apiKey = process.env.CONFLUENCE_API_KEY;

    if (!confluenceUrl || !apiKey) {
      throw new Error('Confluence credentials not configured');
    }

    // Use Confluence REST API to publish
    // This is a placeholder - actual implementation would use a Confluence client
    console.log(`Publishing to Confluence: ${doc.metadata.title}`);

    // Handle attachments (diagrams)
    if (doc.attachments && doc.attachments.length > 0) {
      console.log(`Uploading ${doc.attachments.length} attachments`);
    }

    // Set proper permissions
    console.log('Setting page permissions');
  }

  validate(input: DocParams): ValidationResult {
    const errors: AgentError[] = [];

    if (!input.model) {
      errors.push({
        code: 'MISSING_MODEL',
        message: 'C4 model is required',
        severity: 'error',
      });
    }

    if (!input.type) {
      errors.push({
        code: 'MISSING_TYPE',
        message: 'Documentation type is required',
        severity: 'error',
      });
    }

    return {
      valid: errors.length === 0,
      score: errors.length === 0 ? 100 : 0,
      errors,
      warnings: [],
    };
  }
}

interface DocParams {
  model: C4Model;
  type: string;
  documentation?: Documentation;
}
```

#### Terraform Agent
- **Purpose**: Generate infrastructure as code
- **Tasks**:
  - Create Terraform modules
  - Generate Kubernetes manifests
  - Produce Docker compositions
  - Create CI/CD pipelines

```typescript
class TerraformAgent implements Agent {
  async generateInfrastructure(model: C4Model, provider: string): Promise<Infrastructure> {
    const modules = [];
    
    // For each container
    for (const container of model.containers) {
      if (container.runtime_type === 'service') {
        modules.push(this.generateServiceModule(container, provider));
      } else if (container.runtime_type === 'database') {
        modules.push(this.generateDatabaseModule(container, provider));
      }
    }
    
    return this.combineModules(modules);
  }
  
  private generateServiceModule(container: Container, provider: string): TerraformModule {
    // Based on criticality:
    // CS1: Multi-region, auto-scaling, monitoring
    // CS2: Multi-AZ, backups
    // SL1: Standard HA
    // SL2: Basic setup
  }
}
```

#### Security Agent
- **Purpose**: Security analysis and recommendations
- **Tasks**:
  - Threat modeling (STRIDE)
  - Security control recommendations
  - Compliance checking
  - Zero-trust guidance

```typescript
interface Threat {
  type: 'spoofing' | 'tampering' | 'repudiation' | 'information_disclosure' | 'denial_of_service' | 'elevation_of_privilege';
  element: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  mitigation?: string;
}

interface AttackVector {
  name: string;
  entry_point: string;
  target: string;
  risk_level: string;
}

interface SecurityControl {
  type: string;
  description: string;
  applicable_to: string[];
  implementation: string;
}

interface ThreatModel {
  threats: Threat[];
  attackVectors: AttackVector[];
  controls: SecurityControl[];
  risk_score: number;
}

class SecurityAgent implements Agent<SecurityParams, ThreatModel> {
  async execute(task: string, params: SecurityParams): Promise<AgentResult<ThreatModel>> {
    try {
      if (task === 'threat_model') {
        const threatModel = await this.performThreatModel(params.model);
        return {
          success: true,
          data: threatModel,
          confidence: 0.85,
        };
      }
      throw new Error(`Unknown task: ${task}`);
    } catch (error) {
      return {
        success: false,
        data: {} as ThreatModel,
        confidence: 0,
        errors: [{
          code: 'SECURITY_ANALYSIS_ERROR',
          message: error.message,
          severity: 'error',
        }],
      };
    }
  }

  async performThreatModel(model: C4Model): Promise<ThreatModel> {
    const threats: Threat[] = [];

    // STRIDE analysis on all components
    const allComponents = this.getAllComponents(model);
    for (const component of allComponents) {
      threats.push(...this.analyzeSTRIDE(component));
    }

    // Identify attack vectors
    const attackVectors = this.identifyAttackVectors(model);

    // Recommend controls based on criticality
    const controls = this.recommendControls(threats, model.metadata.criticality || 'STANDARD');

    // Calculate overall risk score
    const risk_score = this.calculateRiskScore(threats);

    return { threats, attackVectors, controls, risk_score };
  }

  private getAllComponents(model: C4Model): Array<Container | Component | ExternalSystem> {
    return [
      ...model.containers,
      ...model.components,
      ...model.externals,
    ];
  }

  private analyzeSTRIDE(component: Container | Component | ExternalSystem): Threat[] {
    const threats: Threat[] = [];
    const elementId = component.id;

    // Spoofing - Identity verification
    if (component.type === 'container' && (component as Container).runtime_type === 'service') {
      threats.push({
        type: 'spoofing',
        element: elementId,
        description: 'Service may be vulnerable to spoofing attacks without proper authentication',
        severity: 'high',
        mitigation: 'Implement OAuth 2.0 or mutual TLS authentication',
      });
    }

    // Tampering - Data integrity
    threats.push({
      type: 'tampering',
      element: elementId,
      description: 'Data in transit may be tampered with',
      severity: 'medium',
      mitigation: 'Use TLS 1.3 for all communications',
    });

    // Repudiation - Audit logging
    if (component.type === 'container') {
      const container = component as Container;
      if (container.criticality === 'CS1' || container.criticality === 'CS2') {
        threats.push({
          type: 'repudiation',
          element: elementId,
          description: 'Critical system lacks audit trail',
          severity: 'high',
          mitigation: 'Implement comprehensive audit logging with SIEM integration',
        });
      }
    }

    // Information Disclosure - Data protection
    if (component.type === 'external') {
      threats.push({
        type: 'information_disclosure',
        element: elementId,
        description: 'External system may expose sensitive data',
        severity: 'medium',
        mitigation: 'Encrypt all data at rest and in transit',
      });
    }

    // Denial of Service - Availability
    threats.push({
      type: 'denial_of_service',
      element: elementId,
      description: 'Component may be vulnerable to DoS attacks',
      severity: 'medium',
      mitigation: 'Implement rate limiting and circuit breakers',
    });

    // Elevation of Privilege - Authorization
    if (component.type === 'component' && (component as Component).component_type === 'api') {
      threats.push({
        type: 'elevation_of_privilege',
        element: elementId,
        description: 'API may allow privilege escalation',
        severity: 'critical',
        mitigation: 'Implement role-based access control (RBAC)',
      });
    }

    return threats;
  }

  private identifyAttackVectors(model: C4Model): AttackVector[] {
    const vectors: AttackVector[] = [];

    // Analyze relationships for potential attack paths
    model.relationships.forEach(rel => {
      const source = model.externals.find(e => e.id === rel.source);
      if (source) {
        vectors.push({
          name: `External Access via ${source.name}`,
          entry_point: rel.source,
          target: rel.target,
          risk_level: 'high',
        });
      }
    });

    // Check for public-facing containers
    model.containers.forEach(container => {
      if (container.tags?.includes('public') || container.tags?.includes('api')) {
        vectors.push({
          name: `Public API Exposure: ${container.name}`,
          entry_point: container.id,
          target: container.id,
          risk_level: 'medium',
        });
      }
    });

    return vectors;
  }

  private recommendControls(threats: Threat[], criticality: CriticalityLevel): SecurityControl[] {
    const controls: SecurityControl[] = [];

    // Base controls for all systems
    controls.push({
      type: 'authentication',
      description: 'Implement strong authentication mechanisms',
      applicable_to: ['all'],
      implementation: 'OAuth 2.0 / SAML 2.0',
    });

    controls.push({
      type: 'encryption',
      description: 'Encrypt data at rest and in transit',
      applicable_to: ['all'],
      implementation: 'TLS 1.3, AES-256',
    });

    // Criticality-specific controls
    if (criticality === 'CS1') {
      controls.push({
        type: 'zero-trust',
        description: 'Implement zero-trust architecture',
        applicable_to: ['CS1'],
        implementation: 'Network segmentation, mTLS, HSM for key management',
      });

      controls.push({
        type: 'audit',
        description: 'Comprehensive audit logging',
        applicable_to: ['CS1'],
        implementation: 'SIEM integration, immutable logs',
      });
    } else if (criticality === 'CS2') {
      controls.push({
        type: 'authentication',
        description: 'Multi-factor authentication',
        applicable_to: ['CS2'],
        implementation: 'MFA for all access',
      });

      controls.push({
        type: 'monitoring',
        description: 'Real-time security monitoring',
        applicable_to: ['CS2'],
        implementation: 'SIEM with automated alerting',
      });
    }

    // Add controls based on threat types
    const hasCriticalThreats = threats.some(t => t.severity === 'critical');
    if (hasCriticalThreats) {
      controls.push({
        type: 'rbac',
        description: 'Role-based access control',
        applicable_to: ['critical-components'],
        implementation: 'Fine-grained RBAC with principle of least privilege',
      });
    }

    return controls;
  }

  private calculateRiskScore(threats: Threat[]): number {
    const severityScores = {
      critical: 10,
      high: 7,
      medium: 4,
      low: 1,
    };

    const total = threats.reduce((sum, threat) => sum + severityScores[threat.severity], 0);
    const max = threats.length * 10;

    return max > 0 ? Math.round((total / max) * 100) : 0;
  }

  validate(input: SecurityParams): ValidationResult {
    const errors: AgentError[] = [];

    if (!input.model) {
      errors.push({
        code: 'MISSING_MODEL',
        message: 'C4 model is required for security analysis',
        severity: 'error',
      });
    }

    return {
      valid: errors.length === 0,
      score: errors.length === 0 ? 100 : 0,
      errors,
      warnings: [],
    };
  }
}

interface SecurityParams {
  model: C4Model;
}
```

#### Fitness Function Agent
- **Purpose**: Create architectural fitness functions
- **Tasks**:
  - Generate fitness tests
  - Measure architecture quality
  - Track technical debt

```typescript
class FitnessAgent implements Agent {
  async generateFitnessTests(model: C4Model): Promise<FitnessTests> {
    const tests = [];
    
    // Performance tests
    tests.push(this.generatePerformanceTests(model));
    
    // Reliability tests
    tests.push(this.generateReliabilityTests(model));
    
    // Security tests
    tests.push(this.generateSecurityTests(model));
    
    // Coupling tests
    tests.push(this.generateCouplingTests(model));
    
    return tests;
  }
  
  private generatePerformanceTests(model: C4Model): Test[] {
    // Response time < threshold
    // Throughput > minimum
    // Resource usage < maximum
  }
}
```

#### Architecture Advisor Agent
- **Purpose**: Provide architectural recommendations
- **Tasks**:
  - Pattern recommendations
  - Anti-pattern detection
  - Improvement suggestions
  - Migration strategies

```typescript
class AdvisorAgent implements Agent {
  private patterns = {
    microservices: MicroservicesPattern,
    eventDriven: EventDrivenPattern,
    cqrs: CQRSPattern,
    saga: SagaPattern
  };
  
  async analyzeAndRecommend(model: C4Model): Promise<Recommendations> {
    const recommendations = [];
    
    // Detect anti-patterns
    const antiPatterns = this.detectAntiPatterns(model);
    
    // Suggest patterns
    const suggestedPatterns = this.suggestPatterns(model);
    
    // Identify improvements
    const improvements = this.identifyImprovements(model);
    
    return { antiPatterns, suggestedPatterns, improvements };
  }
}
```

### 3. Context Broker Implementation

```typescript
class ContextMemory {
  private storage: Map<string, unknown> = new Map();
  private maxSize: number;

  constructor(maxSize: number = 1000) {
    this.maxSize = maxSize;
  }

  store(key: string, value: unknown): void {
    if (this.storage.size >= this.maxSize) {
      // Remove oldest entry
      const firstKey = this.storage.keys().next().value;
      this.storage.delete(firstKey);
    }
    this.storage.set(key, value);
  }

  get(key: string): unknown {
    return this.storage.get(key);
  }

  getRelevant(agent: string): Record<string, unknown> {
    const relevant: Record<string, unknown> = {};

    // Get all keys related to this agent
    for (const [key, value] of this.storage.entries()) {
      if (key.includes(agent) || key === 'global') {
        relevant[key] = value;
      }
    }

    return relevant;
  }

  clear(): void {
    this.storage.clear();
  }
}

class ArchitecturalContextImpl implements ArchitecturalContext {
  model?: C4Model;
  discovery?: DiscoveryResult;
  business?: BusinessContext;
  metadata: Map<string, unknown> = new Map();

  getRelevant(agent: string): Record<string, unknown> {
    const relevant: Record<string, unknown> = {};

    // Include common context for all agents
    if (this.model) relevant.model = this.model;
    if (this.discovery) relevant.discovery = this.discovery;
    if (this.business) relevant.business = this.business;

    // Include agent-specific metadata
    for (const [key, value] of this.metadata.entries()) {
      if (key.startsWith(agent)) {
        relevant[key] = value;
      }
    }

    return relevant;
  }

  update(result: unknown): void {
    // Type-safe updates based on result type
    if (this.isC4Model(result)) {
      this.model = result;
    } else if (this.isDiscoveryResult(result)) {
      this.discovery = result;
    } else if (this.isBusinessContext(result)) {
      this.business = result;
    }
  }

  private isC4Model(obj: unknown): obj is C4Model {
    return typeof obj === 'object' && obj !== null && 'version' in obj && 'containers' in obj;
  }

  private isDiscoveryResult(obj: unknown): obj is DiscoveryResult {
    return typeof obj === 'object' && obj !== null && 'timestamp' in obj && 'repository' in obj;
  }

  private isBusinessContext(obj: unknown): obj is BusinessContext {
    return typeof obj === 'object' && obj !== null && 'purpose' in obj && 'stakeholders' in obj;
  }
}

class PipelineError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'PipelineError';
  }
}

class ContextBroker {
  private agents: Map<string, Agent<unknown, unknown>> = new Map();
  private context: ArchitecturalContext;
  private memory: ContextMemory;
  private pipelines: Map<string, Pipeline>;

  constructor(config?: { memorySize?: number }) {
    this.context = new ArchitecturalContextImpl();
    this.memory = new ContextMemory(config?.memorySize || 1000);
    this.pipelines = new Map();
  }

  registerAgent(agent: Agent<unknown, unknown>): void {
    this.agents.set(agent.name, agent);
  }

  registerPipeline(pipeline: Pipeline): void {
    this.pipelines.set(pipeline.name, pipeline);
  }

  async executePipeline(pipelineName: string, params: Record<string, unknown>): Promise<PipelineResult> {
    const pipeline = this.pipelines.get(pipelineName);

    if (!pipeline) {
      throw new PipelineError(`Pipeline not found: ${pipelineName}`);
    }

    const results = new Map<string, StepResult>();
    const startTime = Date.now();
    const errors: AgentError[] = [];

    for (const step of pipeline.steps) {
      // Check dependencies
      if (step.depends_on) {
        for (const dep of step.depends_on) {
          const depResult = results.get(dep);
          if (!depResult || !depResult.success) {
            errors.push({
              code: 'DEPENDENCY_FAILED',
              message: `Step ${step.name} depends on failed step ${dep}`,
              severity: 'error',
              element: step.name,
            });
            continue;
          }
        }
      }

      const agent = this.agents.get(step.agent);

      if (!agent) {
        errors.push({
          code: 'AGENT_NOT_FOUND',
          message: `Agent not found: ${step.agent}`,
          severity: 'error',
          element: step.name,
        });
        continue;
      }

      // Prepare context
      const stepContext = this.prepareContext(step, results, params);

      // Execute
      const stepStart = Date.now();
      try {
        const result = await agent.execute(step.task, stepContext);

        const stepResult: StepResult = {
          success: result.success,
          data: result.data,
          duration: Date.now() - stepStart,
          error: result.errors?.[0],
        };

        // Store result
        results.set(step.name, stepResult);
        this.memory.store(step.name, result.data);

        // Update context
        this.context.update(result.data);

        // Handle failures
        if (!result.success && step.required) {
          errors.push(...(result.errors || []));
          break; // Stop pipeline on required step failure
        }
      } catch (error) {
        const stepError: AgentError = {
          code: 'STEP_EXECUTION_ERROR',
          message: error.message,
          severity: 'error',
          element: step.name,
        };

        errors.push(stepError);

        results.set(step.name, {
          success: false,
          data: null,
          duration: Date.now() - stepStart,
          error: stepError,
        });

        if (step.required) {
          break; // Stop pipeline on required step failure
        }
      }
    }

    const duration = Date.now() - startTime;
    const success = errors.length === 0 && Array.from(results.values()).every(r => r.success);

    return {
      success,
      steps: results,
      duration,
      errors,
    };
  }

  private prepareContext(
    step: PipelineStep,
    previousResults: Map<string, StepResult>,
    pipelineParams: Record<string, unknown>
  ): Record<string, unknown> {
    const context: Record<string, unknown> = {
      global: this.context.getRelevant(step.agent),
      memory: this.memory.getRelevant(step.agent),
      constraints: step.constraints || {},
      parameters: { ...pipelineParams, ...(step.parameters || {}) },
    };

    // Add previous results if specified
    if (step.depends_on) {
      const previous: Record<string, unknown> = {};
      for (const dep of step.depends_on) {
        const result = previousResults.get(dep);
        if (result) {
          previous[dep] = result.data;
        }
      }
      context.previous = previous;
    }

    return context;
  }

  private aggregateResults(results: Map<string, StepResult>): PipelineResult {
    const errors: AgentError[] = [];
    let totalDuration = 0;

    for (const [_, result] of results.entries()) {
      totalDuration += result.duration;
      if (result.error) {
        errors.push(result.error);
      }
    }

    return {
      success: errors.length === 0,
      steps: results,
      duration: totalDuration,
      errors,
    };
  }

  getAgent(name: string): Agent<unknown, unknown> | undefined {
    return this.agents.get(name);
  }

  getContext(): ArchitecturalContext {
    return this.context;
  }

  clearMemory(): void {
    this.memory.clear();
  }
}
```

### 4. LLM Integration Layer

```typescript
class LLMClient {
  private clients = {
    claude: new ClaudeClient(),
    openai: new OpenAIClient(), // Optional fallback
  };
  
  async query(prompt: string, context: any, agent: string): Promise<LLMResponse> {
    const enrichedPrompt = this.enrichPrompt(prompt, context, agent);
    
    try {
      // Try primary LLM
      const response = await this.clients.claude.complete(enrichedPrompt);
      return this.parseResponse(response);
    } catch (error) {
      // Fallback if configured
      if (this.clients.openai) {
        return await this.clients.openai.complete(enrichedPrompt);
      }
      throw error;
    }
  }
  
  private enrichPrompt(prompt: string, context: any, agent: string): string {
    return `
      You are a ${agent} specialized in solution architecture.
      
      Context:
      ${JSON.stringify(context, null, 2)}
      
      Task:
      ${prompt}
      
      Respond with structured JSON following the expected schema.
    `;
  }
}
```

### 5. CLI Implementation

```typescript
#!/usr/bin/env node

import { Command } from 'commander';
import { SAATClient } from './client';

const program = new Command();

program
  .name('saat')
  .description('Solution Architecture Agent Toolkit')
  .version('1.0.0');

// Initialize command
program
  .command('init')
  .description('Initialize a new C4 model project')
  .option('-p, --project <name>', 'Project name')
  .action(async (options) => {
    const client = new SAATClient();
    await client.init(options.project);
  });

// Discover command
program
  .command('discover')
  .description('Discover architecture from code')
  .option('-p, --path <path>', 'Repository path')
  .option('-o, --output <file>', 'Output file')
  .action(async (options) => {
    const client = new SAATClient();
    const result = await client.discover(options.path);
    await client.save(result, options.output);
  });

// Validate command
program
  .command('validate')
  .description('Validate C4 model')
  .option('-m, --model <file>', 'Model file')
  .action(async (options) => {
    const client = new SAATClient();
    const result = await client.validate(options.model);
    console.log(result);
  });

// Generate command
program
  .command('generate <type>')
  .description('Generate outputs (docs, terraform, tests)')
  .option('-m, --model <file>', 'Model file')
  .option('-f, --format <format>', 'Output format')
  .action(async (type, options) => {
    const client = new SAATClient();
    const result = await client.generate(type, options.model, options.format);
    console.log(`Generated ${type}: ${result.path}`);
  });

// Pipeline command
program
  .command('pipeline')
  .description('Run analysis pipeline')
  .option('-c, --config <file>', 'Pipeline config')
  .action(async (options) => {
    const client = new SAATClient();
    await client.runPipeline(options.config);
  });

// Interactive mode
program
  .command('interactive')
  .description('Start interactive mode')
  .action(async () => {
    const client = new SAATClient();
    await client.startInteractive();
  });

// Watch mode
program
  .command('watch')
  .description('Watch for changes')
  .option('-p, --path <path>', 'Path to watch')
  .action(async (options) => {
    const client = new SAATClient();
    await client.watch(options.path);
  });

program.parse(process.argv);
```

### 6. REST API Implementation

```typescript
import express from 'express';
import { ContextBroker } from './broker';

const app = express();
const broker = new ContextBroker();

// Initialize agents
broker.registerAgent(new DiscoveryAgent());
broker.registerAgent(new ValidationAgent());
broker.registerAgent(new JSONGeneratorAgent());
// ... register all agents

app.post('/api/discover', async (req, res) => {
  try {
    const result = await broker.agents.get('discovery').execute('analyze', {
      path: req.body.path
    });
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/validate', async (req, res) => {
  try {
    const result = await broker.agents.get('validation').execute('validate', {
      model: req.body.model
    });
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Helper function to map generation type to agent
function getAgentForType(type: string): string {
  const mapping: Record<string, string> = {
    docs: 'documentation',
    terraform: 'terraform',
    tests: 'fitness',
    security: 'security',
  };

  const agent = mapping[type];
  if (!agent) {
    throw new Error(`Unknown generation type: ${type}`);
  }

  return agent;
}

app.post('/api/generate/:type', async (req, res) => {
  try {
    const agentName = getAgentForType(req.params.type);
    const agent = broker.getAgent(agentName);

    if (!agent) {
      return res.status(404).json({ error: `Agent not found: ${agentName}` });
    }

    const result = await agent.execute('generate', {
      model: req.body.model,
      format: req.body.format,
    });
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/pipeline', async (req, res) => {
  try {
    const result = await broker.executePipeline(
      req.body.pipeline,
      req.body.params
    );
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => {
  console.log('SAAT API running on port 3000');
});
```

### 7. VS Code Extension

```typescript
// extension.ts
import * as vscode from 'vscode';
import { SAATClient } from './client';

export function activate(context: vscode.ExtensionContext) {
  const client = new SAATClient();
  
  // Command: Discover Architecture
  const discoverCommand = vscode.commands.registerCommand(
    'saat.discover',
    async () => {
      const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
      if (workspaceFolder) {
        const result = await client.discover(workspaceFolder.uri.fsPath);
        
        // Show result in new document
        const doc = await vscode.workspace.openTextDocument({
          content: JSON.stringify(result, null, 2),
          language: 'json'
        });
        vscode.window.showTextDocument(doc);
      }
    }
  );
  
  // Command: Validate Current File
  const validateCommand = vscode.commands.registerCommand(
    'saat.validate',
    async () => {
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        const content = editor.document.getText();
        const result = await client.validateJSON(content);
        
        // Show diagnostics
        const diagnostics = result.errors.map(error => 
          new vscode.Diagnostic(
            error.range,
            error.message,
            vscode.DiagnosticSeverity.Error
          )
        );
        
        const collection = vscode.languages.createDiagnosticCollection('saat');
        collection.set(editor.document.uri, diagnostics);
      }
    }
  );
  
  // Status bar item
  const statusBar = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right
  );
  statusBar.text = '$(circuit-board) SAAT';
  statusBar.command = 'saat.showMenu';
  statusBar.show();
  
  context.subscriptions.push(discoverCommand, validateCommand, statusBar);
}
```

### 8. Configuration System

```yaml
# config.yaml
agents:
  discovery:
    enabled: true
    model: claude-3-opus
    max_tokens: 4000
    temperature: 0.3
    
  validation:
    enabled: true
    strict_mode: true
    rules:
      - ./rules/ba-standards.yaml
      - ./rules/security.yaml
      
  documentation:
    enabled: true
    confluence:
      url: https://confluence.ba.com
      space: ARCHITECTURE
      api_key: ${CONFLUENCE_API_KEY}
      
  terraform:
    enabled: true
    providers:
      aws:
        region: eu-west-2
        state_bucket: ba-terraform-state
      azure:
        subscription: ${AZURE_SUBSCRIPTION}
        
llm:
  primary: claude
  fallback: openai
  claude:
    api_key: ${CLAUDE_API_KEY}
    model: claude-3-opus-20240229
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4-turbo
    
pipelines:
  discovery:
    path: ./pipelines/discovery.yaml
  validation:
    path: ./pipelines/validation.yaml
  generation:
    path: ./pipelines/generation.yaml
    
context_broker:
  memory_size: 1000
  cache_ttl: 3600
  max_retries: 3
  parallel_execution: false
```

### 9. Testing Strategy

```typescript
// Test discovery agent
describe('DiscoveryAgent', () => {
  let agent: DiscoveryAgent;
  
  beforeEach(() => {
    agent = new DiscoveryAgent(config);
  });
  
  test('should discover microservices', async () => {
    const result = await agent.analyzeRepository('./test-data/microservices');
    
    expect(result.containers).toHaveLength(3);
    expect(result.containers[0].technology).toBe('Node.js');
    expect(result.external_systems).toContain('PostgreSQL');
  });
  
  test('should extract API definitions', async () => {
    const result = await agent.scanConfigurations('./test-data/api');
    
    expect(result.apis).toHaveLength(2);
    expect(result.apis[0].type).toBe('REST');
    expect(result.apis[0].endpoints).toHaveLength(10);
  });
});

// Test validation agent
describe('ValidationAgent', () => {
  test('should validate CS1 requirements', async () => {
    const model = {
      containers: [{
        criticality: 'CS1',
        sla: { availability: 99.5 }
      }]
    };
    
    const result = await agent.validate(model);
    
    expect(result.valid).toBe(false);
    expect(result.errors).toContain('CS1 requires 99.99% availability');
  });
});

// Integration test
describe('Pipeline', () => {
  test('should execute full discovery pipeline', async () => {
    const broker = new ContextBroker();
    
    const result = await broker.executePipeline('discovery', {
      path: './test-data/complete-system'
    });
    
    expect(result.model).toBeDefined();
    expect(result.documentation).toBeDefined();
    expect(result.terraform).toBeDefined();
  });
});
```

### 10. Deployment

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source
COPY . .

# Build
RUN npm run build

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

EXPOSE 3000

CMD ["node", "dist/api/server.js"]
```

```yaml
# docker-compose.yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - CONFLUENCE_API_KEY=${CONFLUENCE_API_KEY}
    volumes:
      - ./config:/app/config
      - ./workspace:/workspace
      
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
      
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: saat
      POSTGRES_USER: saat
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
volumes:
  postgres_data:
```

## Implementation Requirements

1. **Core Features**
   - All 9 agents fully implemented with complete execute() and validate() methods
   - Context broker with pipeline orchestration and dependency management
   - LLM integration (Claude primary with retry logic, OpenAI fallback)
   - CLI with all commands (init, discover, validate, generate, pipeline, interactive, watch)
   - REST API with authentication and rate limiting
   - VS Code extension with real-time validation

2. **Data Management**
   - PostgreSQL for model storage with migration system
   - Redis for caching with TTL configuration
   - File-based YAML configuration with validation
   - JSON schema validation using AJV library

3. **Security**
   - Environment-based API key management
   - Role-based access control for API endpoints
   - Secure credential storage using encryption
   - Audit logging to file and database

4. **Performance**
   - Async/parallel processing for independent pipeline steps
   - Multi-level caching (memory, Redis)
   - Rate limiting (100 req/min per API key)
   - Progress tracking with event emitters

5. **Documentation**
   - README with quick start and examples
   - Agent development guide with TypeScript examples
   - Pipeline creation guide with YAML schemas
   - API documentation using OpenAPI/Swagger
   - Example projects (3+ domains)

6. **Testing**
   - Unit tests (>80% line coverage, >70% branch coverage)
   - Integration tests for each agent
   - E2E tests for complete pipelines
   - Performance tests with benchmarking

7. **Deployment**
   - Docker support with multi-stage builds
   - Kubernetes manifests with health checks
   - CI/CD pipelines using GitHub Actions
   - Monitoring setup with Prometheus/Grafana

### Complete package.json

```json
{
  "name": "@saat/architecture-toolkit",
  "version": "1.0.0",
  "description": "Solution Architecture Agent Toolkit for C4 model automation",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "bin": {
    "saat": "dist/cli/index.js"
  },
  "scripts": {
    "build": "tsc && chmod +x dist/cli/index.js",
    "build:dev": "tsc --watch",
    "build:prod": "tsc --project tsconfig.prod.json",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:integration": "jest --testPathPattern=integration",
    "test:e2e": "jest --testPathPattern=e2e",
    "lint": "eslint src --ext .ts",
    "lint:fix": "eslint src --ext .ts --fix",
    "format": "prettier --write \"src/**/*.ts\"",
    "start:api": "node dist/api/server.js",
    "dev:api": "nodemon --exec ts-node src/api/server.ts",
    "docker:build": "docker build -t saat:latest .",
    "docker:run": "docker-compose up -d",
    "prepare": "npm run build"
  },
  "keywords": [
    "architecture",
    "c4-model",
    "solution-architecture",
    "ai-agents",
    "documentation",
    "terraform"
  ],
  "author": "SAAT Contributors",
  "license": "MIT",
  "dependencies": {
    "@anthropic-ai/sdk": "^0.20.0",
    "commander": "^11.0.0",
    "express": "^4.18.2",
    "dotenv": "^16.3.1",
    "yaml": "^2.3.1",
    "ajv": "^8.12.0",
    "fs-extra": "^11.1.1",
    "glob": "^10.3.3",
    "chokidar": "^3.5.3",
    "axios": "^1.4.0",
    "redis": "^4.6.7",
    "pg": "^8.11.1",
    "winston": "^3.10.0",
    "chalk": "^5.3.0",
    "ora": "^6.3.1",
    "inquirer": "^9.2.7",
    "handlebars": "^4.7.8",
    "marked": "^5.1.1",
    "cli-table3": "^0.6.3"
  },
  "devDependencies": {
    "@types/node": "^20.4.2",
    "@types/express": "^4.17.17",
    "@types/fs-extra": "^11.0.1",
    "@types/jest": "^29.5.3",
    "@types/pg": "^8.10.2",
    "@types/inquirer": "^9.0.3",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.45.0",
    "eslint-config-prettier": "^8.8.0",
    "eslint-plugin-prettier": "^5.0.0",
    "jest": "^29.6.1",
    "ts-jest": "^29.1.1",
    "ts-node": "^10.9.1",
    "typescript": "^5.1.6",
    "nodemon": "^3.0.1",
    "prettier": "^3.0.0",
    "supertest": "^6.3.3",
    "@types/supertest": "^2.0.12"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/DavidROliverBA/SAAT.git"
  },
  "bugs": {
    "url": "https://github.com/DavidROliverBA/SAAT/issues"
  },
  "homepage": "https://github.com/DavidROliverBA/SAAT#readme"
}
```

### TypeScript Configuration (tsconfig.json)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

### Jest Configuration (jest.config.js)

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  coverageReporters: ['text', 'lcov', 'html'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  verbose: true,
};
```

## Success Criteria

- Discovers architecture from code repositories automatically
- Generates valid C4 models following BA standards
- Validates models against business rules
- Generates high-quality documentation
- Produces working Terraform code
- Provides actionable architectural recommendations
- Integrates seamlessly with existing tools (Confluence, GitHub)
- Extensible for new agents and pipelines
- Well-documented and easy to use

## Technology Stack

- **Runtime**: Node.js 18+ with TypeScript
- **Framework**: Express.js for API
- **LLM**: Claude API (primary), OpenAI API (fallback)
- **Database**: PostgreSQL, Redis
- **Testing**: Jest, Supertest
- **Build**: Webpack, ESBuild
- **Container**: Docker, Kubernetes
- **CI/CD**: GitHub Actions

This implementation should create a production-ready agent toolkit that significantly accelerates architecture documentation and validation for solution architects.
