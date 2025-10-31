# SAAT - Solution Architecture Agent Toolkit

<p align="center">
  <strong>🤖 AI-Powered C4 Architecture Discovery & Documentation</strong>
</p>

<p align="center">
  Automate architecture discovery, C4 model generation, and documentation using specialized AI agents
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Step-by-Step Setup with Claude Code](#-step-by-step-setup-with-claude-code)
- [Available Agents](#-available-agents)
- [Agent Usage Guide](#-agent-usage-guide)
- [Refining & Improving Agents](#-refining--improving-agents)
- [Recommended Workflow](#-recommended-workflow)
- [Building from Scratch (Greenfield Projects)](#-building-from-scratch-greenfield-projects)
- [Best Practices](#-best-practices)
- [Examples](#-examples)
- [Architecture](#-architecture)
- [Contributing](#-contributing)

---

## 🎯 Overview

SAAT is a context-engineered AI agent toolkit that automates the creation, validation, and documentation of C4 architecture models. It uses specialized agents to:

- 🔍 **Discover** architecture from existing codebases
- 🏗️ **Generate** valid C4 models automatically
- ✅ **Validate** models against best practices
- 📚 **Document** systems comprehensively
- 🔒 **Analyze** security posture
- 🧪 **Create** fitness functions

### Key Benefits

- **Save Time**: Automate weeks of manual architecture documentation
- **Increase Accuracy**: AI-powered analysis reduces human error
- **Maintain Consistency**: Standardized C4 models across all projects
- **Enable Collaboration**: Share architecture knowledge across teams
- **Support Decision Making**: Data-driven insights for architectural choices

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env
# Edit .env and add your CLAUDE_API_KEY

# 4. Build the project
npm run build

# 5. Run discovery on your code
./dist/cli/index.js discover --path /path/to/your/code --output architecture.json

# 6. View the results
cat architecture.json
```

---

## 🛠️ Step-by-Step Setup with Claude Code

### Prerequisites

Before you begin, ensure you have:
- ✅ Node.js 18+ installed
- ✅ npm 9+ installed
- ✅ Claude API key from [console.anthropic.com](https://console.anthropic.com)
- ✅ Git installed
- ✅ Claude Code CLI (optional but recommended)

### Step 1: Clone and Install

```bash
# Clone the SAAT repository
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT

# Install all dependencies
npm install

# Verify installation
npm list --depth=0
```

**Expected Output:**
```
@saat/architecture-toolkit@1.0.0
├── @anthropic-ai/sdk@0.20.0
├── commander@11.0.0
├── express@4.18.2
... (30 total packages)
```

### Step 2: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Open .env in your editor
nano .env  # or vim, code, etc.
```

**Add your API keys:**
```env
# Required
CLAUDE_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# Optional (for advanced features)
OPENAI_API_KEY=sk-YOUR_KEY_HERE
CONFLUENCE_URL=https://confluence.yourcompany.com
CONFLUENCE_API_KEY=your_confluence_key
```

**Security Note:** Never commit `.env` files to version control!

### Step 3: Build the TypeScript Code

```bash
# Compile TypeScript to JavaScript
npm run build

# Verify the build
ls -la dist/

# Make CLI executable
chmod +x dist/cli/index.js
```

**Expected Output:**
```
dist/
├── agents/
├── broker/
├── cli/
├── core/
├── llm/
└── index.js
```

### Step 4: Verify Installation

```bash
# Check CLI version
./dist/cli/index.js version

# Run the demo
npx ts-node demo.ts
```

**Expected Output:**
```
SAAT - Solution Architecture Agent Toolkit
Version: 1.0.0
Build: 2024-01-01
```

### Step 5: Initialize Your First Project

```bash
# Create a new architecture project
./dist/cli/index.js init --project my-system

# Navigate to the project
cd my-system

# Review the generated structure
tree .
```

**Generated Structure:**
```
my-system/
├── models/          # C4 model files
├── pipelines/       # Custom pipelines
├── docs/            # Generated documentation
├── .env             # Configuration
├── saat.config.yaml # SAAT settings
└── README.md        # Project documentation
```

### Step 6: Run Your First Discovery

```bash
# Analyze a codebase
../dist/cli/index.js discover \
  --path /path/to/your/application \
  --output models/architecture.json \
  --depth 3

# View the results
cat models/architecture.json | jq '.'
```

### Step 7: Integrate with Claude Code (Optional)

If you're using Claude Code, you can create custom commands:

```bash
# Create .claude/commands directory
mkdir -p .claude/commands

# Create a discovery command
cat > .claude/commands/discover-arch.md << 'EOF'
Run SAAT discovery on the current project and show me the results.

Use the Discovery Agent to analyze the codebase at the current directory,
generate a C4 model, and provide a summary of:
- Technologies found
- Containers discovered
- Architectural patterns identified
- Recommended improvements
EOF
```

Now in Claude Code, you can type `/discover-arch` to run architecture discovery!

---

## 🤖 Available Agents

SAAT includes several specialized agents, each focused on a specific architectural task:

### 1. Discovery Agent (`discovery-agent`)

**Purpose:** Automatically discovers architecture from existing codebases.

**Capabilities:**
- 🔍 Scans repository structure
- 🏷️ Identifies technologies (Node.js, Java, Python, Go, Docker, Kubernetes)
- 📦 Discovers containers from package.json, docker-compose, pom.xml
- 🌐 Finds APIs from route files and OpenAPI specs
- 🗄️ Detects databases from migrations and dependencies
- 🔗 Extracts external dependencies from .env files
- 🎨 Identifies architectural patterns (Microservices, Monolithic, Event-Driven)

**Current Status:** ✅ Fully Implemented and Tested

### 2. JSON Generator Agent (`json-generator`)

**Purpose:** Converts discovery results into valid C4 model JSON.

**Capabilities:**
- 🏗️ Generates C4 model structure
- 🆔 Automatic ID generation (SYS-XXX-001, CON-XXX-001)
- 🎯 Criticality classification (CS1, CS2, SL1, SL2, STANDARD)
- 🔗 Relationship inference between components
- 📊 System context generation
- 💼 Business context integration

**Current Status:** ✅ Fully Implemented and Tested

### 3. Validation Agent (`validation-agent`)

**Purpose:** Validates C4 models against rules and best practices.

**Capabilities:**
- ✅ Schema validation
- 📋 Business rule checking
- 🔒 Security validation
- 📏 Best practice enforcement
- 🎯 Criticality consistency checks

**Current Status:** 🚧 Ready to Implement (Base structure exists)

### 4. Documentation Agent (`documentation-agent`)

**Purpose:** Generates comprehensive documentation from C4 models.

**Capabilities:**
- 📝 Architecture Decision Records (ADRs)
- 📄 Confluence pages
- 📖 README files
- 🌐 API documentation
- 📚 Runbooks

**Current Status:** 🚧 Ready to Implement (Templates defined)

### 5. Security Agent (`security-agent`)

**Purpose:** Performs security analysis and threat modeling.

**Capabilities:**
- 🛡️ STRIDE threat modeling
- ⚠️ Security control recommendations
- ✓ Compliance checking (GDPR, PCI-DSS, SOC2)
- 🔐 Zero-trust architecture guidance
- 🎯 Attack vector identification

**Current Status:** 🚧 Ready to Implement (Interfaces defined)

### 6. Terraform Agent (`terraform-agent`)

**Purpose:** Generates infrastructure as code from C4 models.

**Capabilities:**
- ☁️ Terraform module generation
- 🎛️ Kubernetes manifest creation
- 🐳 Docker composition
- 🔄 CI/CD pipeline generation
- 📊 Monitoring configuration

**Current Status:** 🚧 Ready to Implement (Patterns defined)

### 7. Fitness Function Agent (`fitness-agent`)

**Purpose:** Creates architectural fitness functions and quality tests.

**Capabilities:**
- 🧪 Performance test generation
- 🔄 Reliability test creation
- 🔒 Security test automation
- 📏 Coupling and cohesion metrics
- 📈 Technical debt tracking

**Current Status:** 🚧 Ready to Implement (Framework ready)

### 8. Architecture Advisor Agent (`advisor-agent`)

**Purpose:** Provides architectural recommendations and pattern suggestions.

**Capabilities:**
- 💡 Pattern recommendation
- ⚠️ Anti-pattern detection
- 📈 Improvement suggestions
- 🔄 Migration strategies
- 🎯 Technology selection guidance

**Current Status:** 🚧 Ready to Implement (Knowledge base defined)

---

## 📚 Agent Usage Guide

### Using the Discovery Agent

#### CLI Usage

```bash
# Basic discovery
./dist/cli/index.js discover --path /path/to/code

# With custom output and depth
./dist/cli/index.js discover \
  --path /path/to/code \
  --output my-architecture.json \
  --depth 5

# Exclude specific directories
./dist/cli/index.js discover \
  --path /path/to/code \
  --exclude node_modules,dist,build
```

#### Programmatic Usage

```typescript
import { DiscoveryAgent } from '@saat/architecture-toolkit';

const agent = new DiscoveryAgent();

// Run discovery
const result = await agent.execute('analyze', {
  path: './my-application',
  depth: 3,
  exclude: ['node_modules', '.git', 'dist']
});

if (result.success) {
  console.log('Technologies:', result.data.technologies);
  console.log('Containers:', result.data.containers.length);
  console.log('Confidence:', result.confidence);
}
```

#### Output Example

```json
{
  "timestamp": "2025-10-31T12:00:00Z",
  "repository": "/path/to/code",
  "technologies": ["Node.js", "TypeScript", "Docker"],
  "containers": [
    {
      "name": "api-service",
      "technology": "Node.js",
      "runtime_type": "service",
      "dependencies": ["express", "pg", "redis"]
    }
  ],
  "patterns": ["Microservices", "REST API"],
  "confidence": 0.9
}
```

### Using the JSON Generator Agent

#### CLI Usage (via discover command)

The generator is automatically invoked by the discover command:

```bash
./dist/cli/index.js discover --path /path/to/code --output model.json
# Runs both discovery AND generation
```

#### Programmatic Usage

```typescript
import { JSONGeneratorAgent } from '@saat/architecture-toolkit';

const generator = new JSONGeneratorAgent();

// Generate C4 model from discovery results
const result = await generator.execute('generate', {
  discovery: discoveryResults,
  business: {
    purpose: 'E-commerce Platform',
    stakeholders: [
      {
        name: 'Customers',
        role: 'End Users',
        needs: ['Fast checkout', 'Secure payments'],
        interactions: ['Web', 'Mobile']
      }
    ],
    capabilities: ['Order Management', 'Payment Processing'],
    compliance: [
      {
        framework: 'PCI-DSS',
        requirements: ['Secure card storage', 'Audit logging'],
        applicable: true
      }
    ]
  }
});

console.log('C4 Model:', result.data);
```

#### Output Example

```json
{
  "version": "1.0.0",
  "metadata": {
    "name": "E-commerce Platform",
    "description": "Auto-generated C4 model",
    "author": "SAAT",
    "criticality": "CS2"
  },
  "systems": [
    {
      "id": "SYS-ECOMMERCE-001",
      "name": "E-commerce Platform",
      "type": "system",
      "criticality": "CS2"
    }
  ],
  "containers": [
    {
      "id": "CON-NODEJS-001",
      "name": "api-service",
      "type": "container",
      "technology": "Node.js",
      "runtime_type": "service",
      "criticality": "CS2"
    }
  ]
}
```

### Using Multiple Agents Together

#### With Context Broker (Recommended)

```typescript
import { ContextBroker } from '@saat/architecture-toolkit';
import { DiscoveryAgent, JSONGeneratorAgent } from '@saat/architecture-toolkit';

// Create broker
const broker = new ContextBroker();

// Register agents
broker.registerAgent(new DiscoveryAgent());
broker.registerAgent(new JSONGeneratorAgent());

// Create a pipeline
broker.registerPipeline({
  name: 'full-analysis',
  version: '1.0.0',
  steps: [
    {
      name: 'discover',
      agent: 'discovery-agent',
      task: 'analyze',
      required: true,
      parameters: {
        path: './my-app',
        depth: 3
      }
    },
    {
      name: 'generate',
      agent: 'json-generator',
      task: 'generate',
      required: true,
      depends_on: ['discover']
    }
  ]
});

// Execute pipeline
const result = await broker.executePipeline('full-analysis', {
  path: './my-app'
});

console.log('Pipeline success:', result.success);
console.log('Duration:', result.duration, 'ms');
```

---

## 🔧 Refining & Improving Agents

Each agent can be refined and improved for your specific needs. Here's how:

### 1. Extending Discovery Agent

**Add New Technology Detection:**

```typescript
// src/agents/discovery-agent.ts

private async discoverTechnologies(repoPath: string): Promise<string[]> {
  const technologies: Set<string> = new Set();

  // ADD YOUR CUSTOM DETECTION
  // Example: Detect Rust
  if (await fs.pathExists(path.join(repoPath, 'Cargo.toml'))) {
    technologies.add('Rust');
  }

  // Example: Detect .NET
  if (await fs.pathExists(path.join(repoPath, '*.csproj'))) {
    technologies.add('.NET');
  }

  // ... existing code ...
  return Array.from(technologies);
}
```

**Add Custom Pattern Detection:**

```typescript
private identifyPatterns(result: DiscoveryResult): string[] {
  const patterns: string[] = [];

  // ADD YOUR CUSTOM PATTERNS
  // Example: Detect CQRS pattern
  if (result.containers.some(c =>
    c.name.includes('command') &&
    result.containers.some(q => q.name.includes('query'))
  )) {
    patterns.push('CQRS');
  }

  // Example: Detect Event Sourcing
  if (result.containers.some(c => c.technology.includes('EventStore'))) {
    patterns.push('Event Sourcing');
  }

  // ... existing code ...
  return patterns;
}
```

**Improve Confidence Scoring:**

```typescript
protected calculateConfidence(result: DiscoveryResult): number {
  let score = 0.5;

  // CUSTOMIZE WEIGHTS
  if (result.containers.length > 0) score += 0.2;
  if (result.technologies.length > 2) score += 0.15; // More tech = higher confidence
  if (result.apis.length > 0) score += 0.1;
  if (result.databases.length > 0) score += 0.05;

  // ADD PENALTIES FOR UNCERTAINTY
  if (result.containers.length === 0) score -= 0.3;
  if (result.technologies.length === 0) score -= 0.5;

  return Math.max(0, Math.min(score, 1.0));
}
```

### 2. Refining JSON Generator Agent

**Customize ID Generation:**

```typescript
private generateId(type: string, suffix: string): string {
  // CUSTOMIZE YOUR ID FORMAT
  const prefix = type.toUpperCase().substring(0, 3);
  const seq = this.getNextId(type).toString().padStart(4, '0'); // 4 digits instead of 3

  // Add project prefix
  const projectPrefix = 'MYORG';
  return `${projectPrefix}-${prefix}-${suffix.toUpperCase()}-${seq}`;
}
```

**Add Custom Criticality Rules:**

```typescript
private inferCriticality(info: ContainerInfo): CriticalityLevel {
  // CUSTOMIZE BASED ON YOUR REQUIREMENTS

  // Payment systems are always CS1
  if (info.dependencies.some(d =>
    d.includes('stripe') ||
    d.includes('paypal') ||
    d.includes('payment')
  )) {
    return 'CS1';
  }

  // Real-time systems are CS2
  if (info.tags?.includes('real-time') || info.tags?.includes('streaming')) {
    return 'CS2';
  }

  // Public APIs are SL1
  if (info.runtime_type === 'service' && info.tags?.includes('public')) {
    return 'SL1';
  }

  // Internal tools are SL2
  if (info.tags?.includes('internal') || info.tags?.includes('admin')) {
    return 'SL2';
  }

  return 'STANDARD';
}
```

### 3. Implementing New Agents

Follow the **BaseAgent** pattern for consistency:

```typescript
// src/agents/my-custom-agent.ts

import { BaseAgent } from './base-agent';
import { AgentResult, ValidationResult } from '../core/types';

interface MyAgentParams {
  input: string;
  options?: Record<string, unknown>;
}

interface MyAgentResult {
  output: string;
  metrics: Record<string, number>;
}

export class MyCustomAgent extends BaseAgent<MyAgentParams, MyAgentResult> {
  constructor() {
    super({
      name: 'my-custom-agent',
      version: '1.0.0',
      capabilities: ['custom-capability-1', 'custom-capability-2'],
      contextTemplate: `You are a specialized agent that does X, Y, Z.`
    });
  }

  async execute(task: string, params: MyAgentParams): Promise<AgentResult<MyAgentResult>> {
    try {
      // Validate input
      const validation = this.validate(params);
      if (!validation.valid) {
        return this.failure(validation.errors[0]);
      }

      // Perform your agent's work
      const result = await this.doCustomWork(params);

      // Return success
      return this.success(result);
    } catch (error) {
      return this.failure(error instanceof Error ? error.message : String(error));
    }
  }

  validate(input: MyAgentParams): ValidationResult {
    return this.validateRequired(
      input as unknown as Record<string, unknown>,
      ['input'] // Required fields
    );
  }

  private async doCustomWork(params: MyAgentParams): Promise<MyAgentResult> {
    // Implement your agent's logic here
    return {
      output: `Processed: ${params.input}`,
      metrics: {
        processingTime: 100,
        itemsProcessed: 1
      }
    };
  }

  protected calculateConfidence(result: MyAgentResult): number {
    // Custom confidence calculation
    return result.metrics.itemsProcessed > 0 ? 0.9 : 0.5;
  }
}
```

### 4. Improving Agent Context Templates

For better LLM responses, refine context templates:

```typescript
// BEFORE (Generic)
contextTemplate: `You are a discovery agent.`

// AFTER (Specific)
contextTemplate: `You are an expert system discovery agent specialized in analyzing enterprise codebases.

Your task is to:
1. Identify all services, databases, and external dependencies
2. Classify each component by technology stack
3. Infer architectural patterns from code structure
4. Rate confidence based on evidence found

Focus on:
- Accuracy: Only report what you can verify
- Completeness: Scan all relevant directories
- Clarity: Provide clear descriptions
- Standards: Follow C4 model conventions

Output structured JSON matching the DiscoveryResult schema.`
```

### 5. Adding Agent Tests

```typescript
// tests/agents/my-agent.test.ts

import { MyCustomAgent } from '../../src/agents/my-custom-agent';

describe('MyCustomAgent', () => {
  let agent: MyCustomAgent;

  beforeEach(() => {
    agent = new MyCustomAgent();
  });

  test('should validate required parameters', () => {
    const result = agent.validate({} as any);
    expect(result.valid).toBe(false);
    expect(result.errors).toHaveLength(1);
  });

  test('should execute successfully with valid input', async () => {
    const result = await agent.execute('process', {
      input: 'test data',
    });

    expect(result.success).toBe(true);
    expect(result.data.output).toBeDefined();
    expect(result.confidence).toBeGreaterThan(0);
  });

  test('should handle errors gracefully', async () => {
    const result = await agent.execute('invalid-task', {
      input: 'test',
    });

    expect(result.success).toBe(false);
    expect(result.errors).toBeDefined();
  });
});
```

---

## 🔄 Recommended Workflow

Here's the **best practice workflow** for using SAAT to document your architecture:

### Phase 1: Discovery & Initial Analysis (Week 1)

**Goal:** Understand the current state of your architecture

```bash
# Step 1: Initialize project
./dist/cli/index.js init --project my-system-architecture
cd my-system-architecture

# Step 2: Run discovery on each major component
./dist/cli/index.js discover \
  --path /path/to/api-service \
  --output models/api-service.json

./dist/cli/index.js discover \
  --path /path/to/web-frontend \
  --output models/web-frontend.json

./dist/cli/index.js discover \
  --path /path/to/backend \
  --output models/backend.json

# Step 3: Review discovery results
cat models/*.json | jq '.technologies' # See all technologies
cat models/*.json | jq '.patterns'     # See all patterns
```

**Deliverables:**
- ✅ Raw discovery JSON for each component
- ✅ Technology inventory
- ✅ Initial pattern identification

### Phase 2: Model Generation & Refinement (Week 2)

**Goal:** Create accurate C4 models with business context

```typescript
// generate-models.ts
import { SAATClient } from '@saat/architecture-toolkit';
import * as fs from 'fs-extra';

async function generateModels() {
  const client = new SAATClient({
    apiKey: process.env.CLAUDE_API_KEY
  });

  // Load discovery results
  const discoveries = await Promise.all([
    fs.readJSON('./models/api-service.json'),
    fs.readJSON('./models/web-frontend.json'),
    fs.readJSON('./models/backend.json')
  ]);

  // Combine with business context
  const businessContext = {
    purpose: 'E-commerce Platform for B2B Sales',
    stakeholders: [
      {
        name: 'Sales Team',
        role: 'Primary Users',
        needs: ['Fast order processing', 'Customer insights'],
        interactions: ['Web Dashboard', 'Mobile App']
      },
      {
        name: 'Customers',
        role: 'End Users',
        needs: ['Easy ordering', 'Order tracking'],
        interactions: ['Customer Portal']
      }
    ],
    capabilities: [
      'Order Management',
      'Inventory Management',
      'Payment Processing',
      'Reporting & Analytics'
    ],
    compliance: [
      {
        framework: 'PCI-DSS',
        requirements: ['Secure payment data', 'Audit logs'],
        applicable: true
      },
      {
        framework: 'GDPR',
        requirements: ['Data privacy', 'Right to deletion'],
        applicable: true
      }
    ]
  };

  // Generate comprehensive C4 model
  for (const discovery of discoveries) {
    const model = await client.generateModel({
      discovery,
      business: businessContext
    });

    await fs.writeJSON(
      `./models/c4-${discovery.repository}.json`,
      model,
      { spaces: 2 }
    );
  }

  console.log('✅ C4 models generated');
}

generateModels().catch(console.error);
```

**Deliverables:**
- ✅ C4 models for each component
- ✅ Business context integrated
- ✅ Criticality levels assigned

### Phase 3: Validation & Quality Assurance (Week 3)

**Goal:** Ensure models are accurate and complete

```bash
# Validate each model
./dist/cli/index.js validate --model models/c4-api-service.json
./dist/cli/index.js validate --model models/c4-web-frontend.json
./dist/cli/index.js validate --model models/c4-backend.json

# Check for common issues:
# - Missing relationships
# - Incorrect criticality
# - Incomplete descriptions
```

**Manual Review Checklist:**
- [ ] All containers have correct technology labels
- [ ] Criticality levels match business importance
- [ ] External dependencies are properly classified
- [ ] Relationships accurately represent data flow
- [ ] System context captures the full scope

### Phase 4: Documentation Generation (Week 4)

**Goal:** Create comprehensive documentation for all stakeholders

```bash
# Generate documentation
./dist/cli/index.js generate docs \
  --model models/c4-complete.json \
  --output docs/

# Generate different formats for different audiences
./dist/cli/index.js generate docs --format markdown  # Developers
./dist/cli/index.js generate docs --format confluence # Architects
./dist/cli/index.js generate adr --model models/c4-complete.json # Decisions
```

**Deliverables:**
- ✅ Architecture overview (README)
- ✅ C4 diagrams (all levels)
- ✅ ADRs for key decisions
- ✅ API documentation
- ✅ Deployment guides

### Phase 5: Continuous Improvement (Ongoing)

**Goal:** Keep architecture documentation up-to-date

```bash
# Set up watch mode (future feature)
./dist/cli/index.js watch --path /path/to/code --auto-update

# Or schedule regular updates
# Add to cron or CI/CD:
# Daily: Run discovery to detect changes
# Weekly: Regenerate C4 models
# Monthly: Full validation and review
```

**Best Practices:**
- 🔄 Run discovery on every major release
- 📊 Track architectural drift over time
- 🎯 Update business context quarterly
- 👥 Review with team during sprint planning
- 📝 Document all architectural decisions (ADRs)

---

## 🏗️ Building from Scratch (Greenfield Projects)

When starting a **new project from scratch**, SAAT becomes a powerful **design-first architecture tool**. Instead of discovering existing code, you design your ideal architecture upfront, validate it, and then implement following that validated design.

### Why Design-First with SAAT?

- ✅ **Validate Before You Build** - Catch architectural issues before writing code
- ✅ **Generate Infrastructure** - Auto-create Terraform, docs, and ADRs from your design
- ✅ **Enforce Standards** - Ensure compliance from day one
- ✅ **Guide Implementation** - Developers follow a validated architecture blueprint
- ✅ **Continuous Validation** - Verify implementation matches design as you build

### Greenfield Workflow: Design → Validate → Generate → Implement

#### Phase 1: Design Your Architecture (Week 1)

**Goal:** Create your ideal C4 architecture model manually

```typescript
// design-architecture.ts - Create your C4 model from scratch
import { C4Model, SystemContext, Container, Component, Relationship } from '@saat/architecture-toolkit';
import * as fs from 'fs-extra';

const myArchitecture: C4Model = {
  version: '1.0.0',
  metadata: {
    project: 'Payment Processing Platform',
    author: 'Architecture Team',
    created: new Date().toISOString(),
    lastModified: new Date().toISOString(),
    description: 'Secure, scalable payment processing for B2B transactions',
    tags: ['fintech', 'payments', 'microservices']
  },

  // Define your system context
  systems: [
    {
      id: 'SYS-PAYMENT-001',
      name: 'Payment Processing Platform',
      description: 'Handles all payment transactions, fraud detection, and reconciliation',
      type: 'SystemContext',
      technology: [],
      tags: ['core-business'],
      responsibilities: [
        'Process payment transactions',
        'Detect fraudulent activity',
        'Generate financial reports',
        'Handle refunds and chargebacks'
      ],
      criticality: 'CS1', // Critical System - 99.99% uptime
      owner: 'payments-team@company.com',
      repository: 'https://github.com/company/payment-platform',
      documentation: 'https://wiki.company.com/payments'
    }
  ],

  // Define your containers (services, databases, etc.)
  containers: [
    {
      id: 'CON-API-001',
      name: 'Payment API',
      description: 'REST API for payment processing',
      type: 'Container',
      technology: ['Node.js', 'Express', 'TypeScript'],
      tags: ['api', 'rest'],
      systemId: 'SYS-PAYMENT-001',
      responsibilities: [
        'Accept payment requests',
        'Validate payment data',
        'Return transaction status'
      ],
      criticality: 'CS1',
      interfaces: [
        {
          protocol: 'HTTPS',
          port: 443,
          authentication: 'OAuth2 + mTLS',
          rateLimit: '1000 req/min'
        }
      ]
    },
    {
      id: 'CON-FRAUD-001',
      name: 'Fraud Detection Service',
      description: 'ML-based fraud detection engine',
      type: 'Container',
      technology: ['Python', 'TensorFlow', 'FastAPI'],
      tags: ['ml', 'security'],
      systemId: 'SYS-PAYMENT-001',
      responsibilities: [
        'Analyze transaction patterns',
        'Score fraud risk',
        'Block suspicious transactions'
      ],
      criticality: 'CS2' // High criticality - 99.9% uptime
    },
    {
      id: 'CON-DB-001',
      name: 'Transaction Database',
      description: 'Primary transactional data store',
      type: 'Database',
      technology: ['PostgreSQL 15', 'TimescaleDB'],
      tags: ['database', 'primary'],
      systemId: 'SYS-PAYMENT-001',
      responsibilities: [
        'Store transaction records',
        'Maintain audit logs',
        'Support real-time queries'
      ],
      criticality: 'CS1',
      interfaces: [
        {
          protocol: 'PostgreSQL',
          port: 5432,
          authentication: 'Certificate-based',
          encrypted: true
        }
      ]
    }
  ],

  // Define external systems
  externals: [
    {
      id: 'EXT-STRIPE-001',
      name: 'Stripe Payment Gateway',
      description: 'Third-party payment processing',
      type: 'ExternalSystem',
      technology: ['REST API'],
      tags: ['payment-gateway', 'third-party'],
      vendor: 'Stripe Inc.',
      sla: '99.99%',
      documentation: 'https://stripe.com/docs'
    },
    {
      id: 'EXT-KYC-001',
      name: 'KYC Verification Service',
      description: 'Customer identity verification',
      type: 'ExternalSystem',
      technology: ['REST API'],
      tags: ['compliance', 'kyc'],
      vendor: 'Onfido',
      sla: '99.9%'
    }
  ],

  // Define relationships between components
  relationships: [
    {
      id: 'REL-001',
      source: 'CON-API-001',
      target: 'CON-DB-001',
      description: 'Stores transaction data',
      type: 'uses',
      protocol: 'PostgreSQL',
      synchronous: true,
      dataFlow: ['Transaction records', 'Query results']
    },
    {
      id: 'REL-002',
      source: 'CON-API-001',
      target: 'CON-FRAUD-001',
      description: 'Requests fraud check',
      type: 'uses',
      protocol: 'gRPC',
      synchronous: false,
      dataFlow: ['Transaction details', 'Risk score']
    },
    {
      id: 'REL-003',
      source: 'CON-API-001',
      target: 'EXT-STRIPE-001',
      description: 'Processes payment',
      type: 'uses',
      protocol: 'HTTPS',
      synchronous: true,
      dataFlow: ['Payment request', 'Payment confirmation']
    }
  ],

  // Define components (internal modules) - optional for initial design
  components: []
};

// Save your design
await fs.writeJSON('./models/payment-platform-design.json', myArchitecture, { spaces: 2 });
console.log('✅ Architecture design created');
```

**Deliverables:**
- ✅ Complete C4 model with systems, containers, and relationships
- ✅ Criticality levels assigned based on business requirements
- ✅ Technology stack decisions documented
- ✅ External dependencies identified

#### Phase 2: Validate Your Design (Week 1-2)

**Goal:** Ensure your architecture follows best practices and meets requirements

```bash
# Validate your design against enterprise standards
./dist/cli/index.js validate --model models/payment-platform-design.json

# Expected output:
# ✅ All containers have technology specifications
# ✅ Criticality levels are appropriate
# ✅ External dependencies are documented
# ⚠️  Warning: CON-FRAUD-001 missing disaster recovery plan
# ⚠️  Warning: No monitoring strategy defined for CS1 systems
```

**Create custom validation rules:**

```typescript
// custom-validation.ts
import { ValidationAgent } from '@saat/architecture-toolkit';

class PaymentValidationAgent extends ValidationAgent {
  async execute(task: string, params: ValidationParams) {
    const baseValidation = await super.execute(task, params);

    // Add payment-specific validations
    const model = params.model;
    const errors: AgentError[] = [];

    // Rule: All payment containers must use encryption
    model.containers.forEach(container => {
      if (container.tags?.includes('payment')) {
        const hasEncryption = container.interfaces?.some(i => i.encrypted === true);
        if (!hasEncryption) {
          errors.push({
            code: 'PAYMENT_ENCRYPTION_REQUIRED',
            message: `Container ${container.name} handles payments but doesn't specify encryption`,
            severity: 'error',
            source: 'PaymentValidationAgent',
            context: { containerId: container.id }
          });
        }
      }
    });

    // Rule: CS1 systems must have redundancy
    model.systems.forEach(system => {
      if (system.criticality === 'CS1') {
        const hasBackup = model.relationships.some(
          r => r.source === system.id && r.description?.includes('backup')
        );
        if (!hasBackup) {
          errors.push({
            code: 'CS1_REDUNDANCY_REQUIRED',
            message: `CS1 system ${system.name} must have backup/redundancy defined`,
            severity: 'error',
            source: 'PaymentValidationAgent',
            context: { systemId: system.id }
          });
        }
      }
    });

    return {
      ...baseValidation.data,
      errors: [...baseValidation.data.errors, ...errors]
    };
  }
}
```

**Deliverables:**
- ✅ Validation report with all issues identified
- ✅ Custom business rules applied
- ✅ Security and compliance gaps documented
- ✅ Refined architecture addressing all critical issues

#### Phase 3: Generate Documentation & Infrastructure (Week 2)

**Goal:** Auto-generate everything you need to start building

```bash
# Generate comprehensive documentation
./dist/cli/index.js generate docs \
  --model models/payment-platform-design.json \
  --output docs/ \
  --format markdown,confluence

# Generate Terraform infrastructure
./dist/cli/index.js generate terraform \
  --model models/payment-platform-design.json \
  --output infrastructure/ \
  --provider aws

# Generate ADRs (Architecture Decision Records)
./dist/cli/index.js generate adrs \
  --model models/payment-platform-design.json \
  --output docs/adr/

# Generate API specifications
./dist/cli/index.js generate openapi \
  --model models/payment-platform-design.json \
  --container CON-API-001 \
  --output api/openapi.yaml
```

**What gets generated:**

**📁 Documentation (`docs/`)**
- System context diagrams (C4 Level 1)
- Container diagrams (C4 Level 2)
- Component diagrams (C4 Level 3)
- Deployment diagrams
- Data flow diagrams
- Architecture decision records (ADRs)

**📁 Infrastructure (`infrastructure/`)**
```hcl
# infrastructure/main.tf - Auto-generated from C4 model
resource "aws_ecs_service" "payment_api" {
  name            = "payment-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.payment_api.arn
  desired_count   = 3  # Based on CS1 criticality

  load_balancer {
    target_group_arn = aws_lb_target_group.payment_api.arn
    container_name   = "payment-api"
    container_port   = 443
  }

  # Auto-scaling based on criticality
  # CS1 = Multi-AZ, auto-scaling, health checks
}

resource "aws_rds_instance" "transactions_db" {
  identifier     = "transaction-database"
  engine         = "postgres"
  engine_version = "15"
  instance_class = "db.r6g.xlarge"

  # CS1 requirements
  multi_az               = true
  backup_retention_period = 35
  deletion_protection    = true

  # From C4 model specifications
  allocated_storage = 100
  storage_encrypted = true

  tags = {
    Criticality = "CS1"
    ManagedBy   = "SAAT"
  }
}
```

**📁 API Specifications (`api/`)**
```yaml
# api/openapi.yaml - Generated from container definition
openapi: 3.0.0
info:
  title: Payment API
  description: REST API for payment processing
  version: 1.0.0

servers:
  - url: https://api.payments.company.com
    description: Production

paths:
  /transactions:
    post:
      summary: Create payment transaction
      security:
        - oauth2: [payments:write]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Transaction'
      responses:
        '201':
          description: Transaction created
        '429':
          description: Rate limit exceeded (1000 req/min)
```

**Deliverables:**
- ✅ Complete documentation suite
- ✅ Infrastructure-as-Code ready to deploy
- ✅ API contracts defined
- ✅ ADRs documenting key decisions

#### Phase 4: Implement Following the Design (Weeks 3-12)

**Goal:** Build your system following the validated architecture

```bash
# Step 1: Set up infrastructure
cd infrastructure/
terraform init
terraform plan
terraform apply

# Step 2: Create service repositories based on containers
mkdir -p services/payment-api
mkdir -p services/fraud-detection
mkdir -p services/shared-libraries

# Step 3: Implement following the C4 model specifications
# For each container in your model:
# - Use the specified technologies
# - Implement the defined responsibilities
# - Follow the interface specifications
# - Connect to defined dependencies
```

**Example: Implementing Payment API Container**

```typescript
// services/payment-api/src/index.ts
// Built following CON-API-001 specification from C4 model

import express from 'express';
import { fraudClient } from './clients/fraud-detection';
import { db } from './clients/database';
import { stripeClient } from './clients/stripe';

const app = express();

// From C4 model: interface specification
// Protocol: HTTPS, Port: 443, Auth: OAuth2 + mTLS, Rate: 1000 req/min
app.post('/transactions', authenticate, rateLimit({ max: 1000 }), async (req, res) => {
  // Responsibility 1: Accept payment requests
  const transaction = req.body;

  // Responsibility 2: Validate payment data
  const validation = validateTransaction(transaction);
  if (!validation.valid) {
    return res.status(400).json({ error: validation.error });
  }

  // REL-002: Request fraud check from CON-FRAUD-001
  const fraudCheck = await fraudClient.analyzeTransaction(transaction);
  if (fraudCheck.riskScore > 0.8) {
    return res.status(403).json({ error: 'Transaction blocked - high fraud risk' });
  }

  // REL-003: Process payment via EXT-STRIPE-001
  const payment = await stripeClient.charge({
    amount: transaction.amount,
    currency: transaction.currency,
    source: transaction.paymentMethod
  });

  // REL-001: Store transaction in CON-DB-001
  await db.transactions.create({
    id: payment.id,
    amount: transaction.amount,
    status: payment.status,
    fraudScore: fraudCheck.riskScore,
    timestamp: new Date()
  });

  // Responsibility 3: Return transaction status
  res.status(201).json({
    transactionId: payment.id,
    status: payment.status
  });
});

// From C4 model: criticality CS1 requires health checks
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(443);
```

**Implementation Guidelines:**
- ✅ Each container becomes a separate service/repository
- ✅ Implement ALL responsibilities defined in the C4 model
- ✅ Follow interface specifications (protocols, ports, auth)
- ✅ Connect to dependencies as defined in relationships
- ✅ Implement health checks for CS1/CS2 containers
- ✅ Add monitoring based on criticality levels

#### Phase 5: Continuous Validation (Weekly)

**Goal:** Ensure implementation matches your design

```bash
# Run discovery on your implementation
./dist/cli/index.js discover \
  --path ./services/payment-api \
  --output models/payment-api-actual.json

# Compare actual vs. design
./dist/cli/index.js compare \
  --expected models/payment-platform-design.json \
  --actual models/payment-api-actual.json \
  --output reports/drift-report.json

# Expected output:
# ✅ All containers implemented
# ✅ Technologies match design (Node.js, TypeScript)
# ⚠️  Warning: Additional dependency found: Redis (not in design)
# ❌ Error: CON-FRAUD-001 not found - missing implementation
```

**Drift Detection:**

```typescript
// check-drift.ts - Run in CI/CD pipeline
import { SAATClient } from '@saat/architecture-toolkit';

async function checkArchitecturalDrift() {
  const client = new SAATClient({ apiKey: process.env.CLAUDE_API_KEY });

  // Load the design (source of truth)
  const design = await fs.readJSON('./models/payment-platform-design.json');

  // Discover actual implementation
  const actual = await client.discover({ path: './services' });

  // Compare
  const drift = await client.compare({
    expected: design,
    actual: actual.model
  });

  if (drift.hasBreakingChanges) {
    console.error('❌ Breaking changes detected!');
    console.error(drift.breakingChanges);
    process.exit(1); // Fail CI/CD
  }

  if (drift.hasWarnings) {
    console.warn('⚠️  Architecture drift detected:');
    console.warn(drift.warnings);
  }

  console.log('✅ Implementation matches design');
}
```

**Deliverables:**
- ✅ Drift reports showing design vs. implementation
- ✅ Automated validation in CI/CD
- ✅ Updated C4 model reflecting any approved changes
- ✅ Working system that matches validated architecture

### Key Benefits for Greenfield Projects

| Benefit | Traditional Approach | SAAT Design-First |
|---------|---------------------|-------------------|
| **Architecture Validation** | After implementation | Before writing code |
| **Documentation** | Manual, often outdated | Auto-generated, always in sync |
| **Infrastructure** | Manual Terraform writing | Auto-generated from design |
| **Compliance** | Checked in audit | Validated upfront |
| **Team Alignment** | Tribal knowledge | Single source of truth |
| **Onboarding** | Weeks to understand | Hours with clear C4 models |
| **Change Management** | Risky, undocumented | Validated, tracked |

### Best Practices for Greenfield

1. **Start with Business Context**
   - Define stakeholders, capabilities, and compliance requirements FIRST
   - Let business needs drive technology choices

2. **Design at the Right Level**
   - Start with System Context (C4 Level 1)
   - Define Containers next (C4 Level 2)
   - Add Components later as implementation progresses (C4 Level 3)

3. **Validate Early, Validate Often**
   - Run validation after each design iteration
   - Create custom validation rules for your domain
   - Get stakeholder approval before implementation

4. **Generate Infrastructure First**
   - Deploy infrastructure before writing code
   - Test connectivity and performance early
   - Validate costs match budget

5. **Implement Container-by-Container**
   - Build one container at a time
   - Validate each implementation matches design
   - Update C4 model with approved changes

6. **Treat Design as Code**
   - Version control your C4 models
   - Review architecture changes like code reviews
   - Use CI/CD to validate drift

### Common Greenfield Patterns

**Pattern 1: Microservices Platform**
```
System: E-commerce Platform
├── Container: API Gateway (Kong)
├── Container: Product Service (Node.js)
├── Container: Order Service (Node.js)
├── Container: Payment Service (Node.js)
├── Container: Notification Service (Python)
├── Database: Product DB (PostgreSQL)
├── Database: Order DB (PostgreSQL)
└── External: Stripe, SendGrid, Auth0
```

**Pattern 2: Data Platform**
```
System: Analytics Platform
├── Container: Data Ingestion API (Python/FastAPI)
├── Container: Stream Processor (Kafka + Flink)
├── Container: Data Warehouse (Snowflake)
├── Container: Analytics API (Node.js)
├── Container: Dashboard UI (React)
└── External: S3, Airflow, Tableau
```

**Pattern 3: Serverless Application**
```
System: Document Processing
├── Container: Upload API (AWS Lambda)
├── Container: Processing Queue (SQS)
├── Container: Document Processor (Lambda)
├── Container: Storage (S3)
├── Container: Notification Service (SNS)
└── External: OCR Service, Database
```

### Next Steps

1. **Create your first design** - Use the example above as a template
2. **Validate it** - Run SAAT validation to catch issues
3. **Generate infrastructure** - Get Terraform/CloudFormation ready
4. **Implement incrementally** - Build one container at a time
5. **Validate continuously** - Check for drift weekly

**Need help?** Check the [Examples](#-examples) section for complete greenfield project walkthroughs.

---

## 📖 Best Practices

### 1. Discovery Best Practices

**DO:**
- ✅ Run discovery on clean, built code (not node_modules)
- ✅ Exclude test files for cleaner results
- ✅ Use appropriate depth (3-5 for most projects)
- ✅ Review and verify auto-detected technologies
- ✅ Combine multiple discovery runs for microservices

**DON'T:**
- ❌ Run on dirty working directories
- ❌ Include build artifacts (dist/, build/)
- ❌ Use excessive depth (>10) - slows down
- ❌ Ignore confidence scores below 70%
- ❌ Trust 100% without manual review

### 2. Model Generation Best Practices

**DO:**
- ✅ Provide rich business context
- ✅ Define clear stakeholders and needs
- ✅ Specify compliance requirements upfront
- ✅ Review and adjust criticality levels
- ✅ Add custom tags for searchability

**DON'T:**
- ❌ Generate without business context
- ❌ Accept auto-generated descriptions blindly
- ❌ Ignore relationship inference
- ❌ Skip validation after generation
- ❌ Forget to version your models

### 3. Agent Customization Best Practices

**DO:**
- ✅ Extend agents via inheritance
- ✅ Add custom validation rules
- ✅ Improve confidence calculations
- ✅ Add domain-specific patterns
- ✅ Test your customizations

**DON'T:**
- ❌ Modify core agent files directly
- ❌ Break the BaseAgent contract
- ❌ Skip error handling
- ❌ Ignore TypeScript types
- ❌ Deploy without tests

### 4. Documentation Best Practices

**DO:**
- ✅ Generate multiple formats (MD, Confluence, HTML)
- ✅ Include diagrams at all C4 levels
- ✅ Link to source code repositories
- ✅ Version your documentation
- ✅ Make it searchable

**DON'T:**
- ❌ Generate once and forget
- ❌ Skip context and purpose
- ❌ Use technical jargon only
- ❌ Ignore stakeholder needs
- ❌ Create documentation silos

### 5. Pipeline Best Practices

**DO:**
- ✅ Use the Context Broker for complex workflows
- ✅ Define clear dependencies between steps
- ✅ Handle failures gracefully
- ✅ Track duration and performance
- ✅ Store intermediate results

**DON'T:**
- ❌ Create circular dependencies
- ❌ Ignore step failures
- ❌ Run all steps sequentially (parallelize!)
- ❌ Skip result validation
- ❌ Hardcode configuration

---

## 💡 Examples

### Example 1: Discover a Node.js Microservice

```bash
./dist/cli/index.js discover \
  --path ~/projects/order-service \
  --output order-service-arch.json \
  --depth 3
```

**Result:**
```json
{
  "technologies": ["Node.js", "TypeScript", "Docker", "PostgreSQL"],
  "containers": [
    {
      "name": "order-service",
      "technology": "Node.js",
      "runtime_type": "service",
      "dependencies": ["express", "pg", "redis"]
    }
  ],
  "databases": [
    {"name": "PostgreSQL", "type": "SQL"},
    {"name": "Redis", "type": "Cache"}
  ],
  "patterns": ["Microservices", "REST API", "CQRS"]
}
```

### Example 2: Generate C4 Model with Business Context

```typescript
import { SAATClient } from '@saat/architecture-toolkit';

const client = new SAATClient();

const model = await client.generateModel({
  discovery: orderServiceDiscovery,
  business: {
    purpose: 'Order Management Microservice for E-commerce Platform',
    stakeholders: [
      {
        name: 'Order Processing Team',
        role: 'Owners',
        needs: ['Scalability', 'Reliability', 'Observability'],
        interactions: ['API', 'Dashboard']
      }
    ],
    capabilities: ['Order Creation', 'Order Tracking', 'Order Fulfillment'],
    compliance: [
      {
        framework: 'PCI-DSS',
        requirements: ['Secure payment data'],
        applicable: true
      }
    ]
  }
});

console.log('Generated C4 Model with', model.containers.length, 'containers');
```

### Example 3: Custom Pipeline for Full Analysis

```typescript
import { ContextBroker } from '@saat/architecture-toolkit';
import { DiscoveryAgent, JSONGeneratorAgent } from '@saat/architecture-toolkit';

const broker = new ContextBroker();

broker.registerAgent(new DiscoveryAgent());
broker.registerAgent(new JSONGeneratorAgent());

// Create custom pipeline
broker.registerPipeline({
  name: 'comprehensive-analysis',
  version: '1.0.0',
  steps: [
    {
      name: 'discover-frontend',
      agent: 'discovery-agent',
      task: 'analyze',
      required: true,
      parameters: { path: './frontend' }
    },
    {
      name: 'discover-backend',
      agent: 'discovery-agent',
      task: 'analyze',
      required: true,
      parameters: { path: './backend' }
    },
    {
      name: 'generate-model',
      agent: 'json-generator',
      task: 'generate',
      required: true,
      depends_on: ['discover-frontend', 'discover-backend']
    }
  ]
});

// Execute
const result = await broker.executePipeline('comprehensive-analysis', {});
console.log('Analysis complete in', result.duration, 'ms');
```

### Example 4: Extending Discovery Agent

```typescript
// my-custom-discovery-agent.ts
import { DiscoveryAgent } from '@saat/architecture-toolkit';

export class MyCustomDiscoveryAgent extends DiscoveryAgent {
  // Override to add Rust detection
  protected async discoverTechnologies(repoPath: string): Promise<string[]> {
    const techs = await super.discoverTechnologies(repoPath);

    // Add Rust
    if (await fs.pathExists(path.join(repoPath, 'Cargo.toml'))) {
      techs.push('Rust');
    }

    // Add Elixir
    if (await fs.pathExists(path.join(repoPath, 'mix.exs'))) {
      techs.push('Elixir');
    }

    return techs;
  }

  // Override to add custom patterns
  protected identifyPatterns(result: DiscoveryResult): string[] {
    const patterns = super.identifyPatterns(result);

    // Detect Hexagonal Architecture
    if (result.containers.some(c =>
      c.path.includes('/ports/') && c.path.includes('/adapters/')
    )) {
      patterns.push('Hexagonal Architecture');
    }

    return patterns;
  }
}
```

---

## 🏗️ Architecture

SAAT uses a modular agent architecture:

```
┌─────────────────────────────────────────────────────┐
│                   CLI / API Layer                    │
│  (Commands, HTTP endpoints, User interactions)       │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│              Context Broker                          │
│  (Agent orchestration, Pipeline execution)           │
└───────────────────┬─────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
┌───────▼──┐  ┌────▼─────┐  ┌─▼──────────┐
│Discovery │  │Generator │  │Validation  │
│  Agent   │  │  Agent   │  │   Agent    │
└──────────┘  └──────────┘  └────────────┘
        │           │           │
        └───────────┼───────────┘
                    │
        ┌───────────▼───────────┐
        │    LLM Integration     │
        │  (Claude API client)   │
        └────────────────────────┘
```

### Key Components

1. **Agents**: Specialized workers for specific tasks
2. **Context Broker**: Orchestrates agents and maintains state
3. **Context Memory**: Caches intermediate results
4. **LLM Client**: Communicates with Claude API
5. **Type System**: Ensures type safety across all components

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Adding a New Agent

1. Create your agent file in `src/agents/`
2. Extend `BaseAgent<TParams, TResult>`
3. Implement `execute()` and `validate()`
4. Add tests in `tests/agents/`
5. Export from `src/index.ts`
6. Update this README

### Improving Existing Agents

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Add/update tests
5. Update documentation
6. Submit a pull request

### Reporting Issues

- 🐛 Bug reports: [GitHub Issues](https://github.com/DavidROliverBA/SAAT/issues)
- 💡 Feature requests: [GitHub Discussions](https://github.com/DavidROliverBA/SAAT/discussions)
- 📖 Documentation improvements: Submit a PR

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **C4 Model** by Simon Brown - [c4model.com](https://c4model.com)
- **Anthropic Claude** - [anthropic.com](https://anthropic.com)
- **TypeScript Community** - [typescriptlang.org](https://typescriptlang.org)

---

**Made with ❤️ by Solution Architects for Solution Architects**

*Last Updated: 2025-10-31*
