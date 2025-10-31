# Solution Architecture Agent Toolkit - Implementation Prompt

## Project: SA Agent Toolkit (SAAT)

Build a comprehensive agent-based toolkit for solution architects that automates C4 model creation, validation, and documentation generation using context-engineered AI agents.

## Core Architecture

### 1. Agent System Design

Create a multi-agent system with the following specialized agents:

```typescript
interface Agent {
  name: string;
  version: string;
  capabilities: string[];
  contextTemplate: string;
  execute(task: string, params: any): Promise<AgentResult>;
  validate(input: any): ValidationResult;
}

interface AgentResult {
  success: boolean;
  data: any;
  confidence: number;
  errors?: string[];
  suggestions?: string[];
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
class JSONGeneratorAgent implements Agent {
  private idGenerator = {
    system: (domain: string) => `SYS-${domain}-${this.getNextId()}`,
    container: (tech: string) => `CON-${tech}-${this.getNextId()}`,
    component: (type: string) => `CMP-${type}-${this.getNextId()}`,
    external: (vendor: string) => `EXT-${vendor}-${this.getNextId()}`
  };
  
  async generateC4Model(discovery: any, business: any): Promise<C4Model> {
    // Map discovery results to C4 elements
    // Apply BA-specific rules
    // Generate hierarchical structure
    // Validate against schema
  }
  
  async applyBAStandards(model: C4Model): Promise<C4Model> {
    // Apply criticality (CS1, CS2, SL1, SL2)
    // Add required metadata
    // Ensure compliance with BA patterns
  }
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
class DocumentationAgent implements Agent {
  private templates = {
    adr: ADRTemplate,
    confluence: ConfluenceTemplate,
    readme: ReadmeTemplate,
    api: APIDocTemplate
  };
  
  async generateDocumentation(model: C4Model, type: string): Promise<Documentation> {
    switch(type) {
      case 'adr':
        return this.generateADR(model);
      case 'confluence':
        return this.generateConfluence(model);
      case 'readme':
        return this.generateReadme(model);
      case 'api':
        return this.generateAPIDoc(model);
    }
  }
  
  async publishToConfluence(doc: Documentation): Promise<void> {
    // Use Confluence API to publish
    // Handle attachments (diagrams)
    // Set proper permissions
  }
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
class SecurityAgent implements Agent {
  async performThreatModel(model: C4Model): Promise<ThreatModel> {
    const threats = [];
    
    // STRIDE analysis
    for (const component of model.getAllComponents()) {
      threats.push(...this.analyzeSTRIDE(component));
    }
    
    // Identify attack vectors
    const attackVectors = this.identifyAttackVectors(model);
    
    // Recommend controls
    const controls = this.recommendControls(threats, model.criticality);
    
    return { threats, attackVectors, controls };
  }
  
  private analyzeSTRIDE(component: Component): Threat[] {
    // Spoofing, Tampering, Repudiation
    // Information Disclosure, DoS, Elevation
  }
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
class ContextBroker {
  private agents: Map<string, Agent> = new Map();
  private context: ArchitecturalContext;
  private memory: ContextMemory;
  private pipelines: Map<string, Pipeline>;
  
  registerAgent(agent: Agent): void {
    this.agents.set(agent.name, agent);
    agent.setContext(this.context);
  }
  
  async executePipeline(pipelineName: string, params: any): Promise<PipelineResult> {
    const pipeline = this.pipelines.get(pipelineName);
    const results = new Map();
    
    for (const step of pipeline.steps) {
      const agent = this.agents.get(step.agent);
      
      // Prepare context
      const stepContext = this.prepareContext(step, results);
      
      // Execute
      const result = await agent.execute(step.task, stepContext);
      
      // Store result
      results.set(step.name, result);
      this.memory.store(step.name, result);
      
      // Update context
      this.context.update(result);
      
      // Handle failures
      if (!result.success && step.required) {
        throw new PipelineError(`Step ${step.name} failed`);
      }
    }
    
    return this.aggregateResults(results);
  }
  
  private prepareContext(step: PipelineStep, previousResults: Map): Context {
    return {
      global: this.context.getRelevant(step.agent),
      previous: previousResults,
      memory: this.memory.getRelevant(step.agent),
      constraints: step.constraints,
      parameters: step.parameters
    };
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

app.post('/api/generate/:type', async (req, res) => {
  try {
    const agent = getAgentForType(req.params.type);
    const result = await broker.agents.get(agent).execute('generate', {
      model: req.body.model,
      format: req.body.format
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
   - All 9 agents fully implemented
   - Context broker with pipeline orchestration
   - LLM integration (Claude primary, OpenAI fallback)
   - CLI with all commands
   - REST API
   - VS Code extension

2. **Data Management**
   - PostgreSQL for model storage
   - Redis for caching
   - File-based configuration
   - JSON schema validation

3. **Security**
   - API key management
   - Role-based access control
   - Secure credential storage
   - Audit logging

4. **Performance**
   - Async/parallel processing
   - Caching layer
   - Rate limiting
   - Progress tracking

5. **Documentation**
   - README with quick start
   - Agent development guide
   - Pipeline creation guide
   - API documentation
   - Example projects

6. **Testing**
   - Unit tests (>80% coverage)
   - Integration tests
   - E2E tests
   - Performance tests

7. **Deployment**
   - Docker support
   - Kubernetes manifests
   - CI/CD pipelines
   - Monitoring setup

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
