# Solution Architecture Agent Toolkit (SAAT)

<p align="center">
  <img src="./docs/images/saat-logo.png" alt="SAAT Logo" width="200"/>
</p>

<p align="center">
  <a href="https://github.com/your-org/saat/actions"><img src="https://github.com/your-org/saat/workflows/CI/badge.svg" alt="CI Status"></a>
  <a href="https://www.npmjs.com/package/@your-org/saat"><img src="https://img.shields.io/npm/v/@your-org/saat.svg" alt="NPM Version"></a>
  <a href="https://github.com/your-org/saat/blob/main/LICENSE"><img src="https://img.shields.io/github/license/your-org/saat.svg" alt="License"></a>
  <a href="https://github.com/your-org/saat/stargazers"><img src="https://img.shields.io/github/stars/your-org/saat.svg" alt="Stars"></a>
</p>

## 🚀 Overview

SAAT is a context-engineered AI agent toolkit that automates C4 architecture model creation, validation, and documentation generation for solution architects. It leverages specialized AI agents to analyze codebases, generate architecture diagrams, validate against best practices, and produce comprehensive documentation.

### Key Features

- 🔍 **Automatic Discovery** - Analyzes codebases to extract architectural components
- 🏗️ **C4 Model Generation** - Creates valid C4 architecture models following industry standards
- ✅ **Intelligent Validation** - Validates against business rules and best practices
- 📚 **Documentation Generation** - Produces ADRs, Confluence pages, and README files
- 🔧 **Infrastructure as Code** - Generates Terraform, Kubernetes, and Docker configurations
- 🔒 **Security Analysis** - Performs threat modeling and security assessments
- 📊 **Fitness Functions** - Creates architectural fitness tests
- 💡 **Architecture Advisor** - Provides recommendations and detects anti-patterns

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Agents](#-agents)
- [Pipelines](#-pipelines)
- [API Reference](#-api-reference)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Quick Start

```bash
# Install globally
npm install -g @your-org/saat

# Initialize a new project
saat init my-architecture

# Discover architecture from existing code
saat discover --path ./my-app --output architecture.json

# Validate the model
saat validate --model architecture.json

# Generate documentation
saat generate docs --model architecture.json --format confluence

# Run complete pipeline
saat pipeline run --config complete-analysis.yaml
```

## 📦 Installation

### Prerequisites

- Node.js 18+ and npm
- Docker (optional, for containerized deployment)
- Git
- API Keys:
  - Claude API key (required)
  - OpenAI API key (optional, for fallback)
  - Confluence API key (for documentation publishing)

### Install from NPM

```bash
npm install -g @your-org/saat
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/your-org/saat.git
cd saat

# Install dependencies
npm install

# Build the project
npm run build

# Link globally
npm link

# Verify installation
saat --version
```

### Docker Installation

```bash
# Pull the image
docker pull your-org/saat:latest

# Run with Docker
docker run -it \
  -v $(pwd):/workspace \
  -e CLAUDE_API_KEY=$CLAUDE_API_KEY \
  your-org/saat discover /workspace
```

### VS Code Extension

Install the SAAT extension from the VS Code marketplace:

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "SAAT - Solution Architecture Toolkit"
4. Click Install

Or install via command line:

```bash
code --install-extension your-org.saat-vscode
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Required
CLAUDE_API_KEY=sk-ant-api03-...

# Optional
OPENAI_API_KEY=sk-...
CONFLUENCE_API_KEY=...
CONFLUENCE_URL=https://confluence.yourcompany.com
GITHUB_TOKEN=ghp_...

# AWS (for Terraform generation)
AWS_REGION=eu-west-2
AWS_PROFILE=default

# Azure (for Terraform generation)
AZURE_SUBSCRIPTION_ID=...
AZURE_TENANT_ID=...
```

### Configuration File

Create `saat.config.yaml`:

```yaml
# Agent Configuration
agents:
  discovery:
    enabled: true
    depth: 3
    exclude:
      - node_modules
      - .git
      - dist
      - build
    
  validation:
    enabled: true
    strict: true
    rules:
      - ./rules/company-standards.yaml
      - ./rules/security-policies.yaml
    
  documentation:
    enabled: true
    formats:
      - markdown
      - confluence
      - html
    confluence:
      space: ARCH
      parent: "Architecture Documentation"
    
  terraform:
    enabled: true
    provider: aws
    backend: s3
    state_bucket: my-terraform-state

# LLM Configuration
llm:
  primary: claude
  fallback: openai
  claude:
    model: claude-3-opus-20240229
    max_tokens: 4000
    temperature: 0.3
  openai:
    model: gpt-4-turbo
    max_tokens: 4000

# Pipeline Configuration
pipelines:
  default: complete-analysis
  custom:
    - ./pipelines/discovery.yaml
    - ./pipelines/validation.yaml
    - ./pipelines/documentation.yaml

# Output Configuration
output:
  directory: ./architecture
  formats:
    model: json
    diagrams: 
      - plantuml
      - mermaid
    documentation: markdown
```

## 🎮 Usage

### CLI Commands

#### Initialize Project

```bash
saat init [project-name]

# Options:
#   --template <template>  Use a project template (microservices, monolith, serverless)
#   --force               Overwrite existing files
```

#### Discover Architecture

```bash
saat discover --path <repository-path>

# Options:
#   --output <file>       Output file (default: architecture.json)
#   --depth <n>          Scan depth (default: 3)
#   --include-tests      Include test files in analysis
#   --format <format>    Output format (json, yaml)
```

#### Validate Model

```bash
saat validate --model <model-file>

# Options:
#   --rules <file>       Custom validation rules
#   --strict            Enable strict mode
#   --fix              Auto-fix issues where possible
```

#### Generate Outputs

```bash
# Generate documentation
saat generate docs --model <model-file>

# Generate Terraform
saat generate terraform --model <model-file> --provider aws

# Generate Kubernetes manifests
saat generate k8s --model <model-file>

# Generate fitness tests
saat generate tests --model <model-file>

# Options:
#   --format <format>    Output format
#   --output <dir>      Output directory
#   --template <file>   Custom template
```

#### Run Pipeline

```bash
saat pipeline run --config <pipeline-file>

# Options:
#   --watch             Watch for changes
#   --parallel         Run steps in parallel where possible
#   --continue-on-error Continue pipeline on errors
```

#### Interactive Mode

```bash
saat interactive

# Commands in interactive mode:
> discover ./src
> validate
> generate docs
> advise improvements
> export
> help
> exit
```

#### Watch Mode

```bash
saat watch --path <repository-path>

# Options:
#   --validate         Auto-validate on changes
#   --fitness         Run fitness tests on changes
#   --debounce <ms>   Debounce delay (default: 1000)
```

### API Usage

#### JavaScript/TypeScript

```typescript
import { SAATClient } from '@your-org/saat';

const client = new SAATClient({
  apiKey: process.env.CLAUDE_API_KEY,
  config: './saat.config.yaml'
});

// Discover architecture
const discovery = await client.discover({
  path: './my-app',
  depth: 3
});

// Generate C4 model
const model = await client.generateModel({
  discovery,
  businessContext: {
    capability: 'customer_management',
    stakeholders: ['customers', 'support', 'sales']
  }
});

// Validate model
const validation = await client.validate(model);

if (validation.valid) {
  // Generate outputs
  const docs = await client.generateDocumentation(model, 'confluence');
  const terraform = await client.generateTerraform(model, 'aws');
  
  console.log('Architecture analysis complete!');
} else {
  console.error('Validation errors:', validation.errors);
}
```

#### REST API

Start the API server:

```bash
saat serve --port 3000
```

Make requests:

```bash
# Discover architecture
curl -X POST http://localhost:3000/api/discover \
  -H "Content-Type: application/json" \
  -d '{"path": "./my-app"}'

# Validate model
curl -X POST http://localhost:3000/api/validate \
  -H "Content-Type: application/json" \
  -d @architecture.json

# Generate documentation
curl -X POST http://localhost:3000/api/generate/docs \
  -H "Content-Type: application/json" \
  -d @architecture.json
```

### VS Code Extension

The VS Code extension provides:

- **Command Palette** (Ctrl+Shift+P):
  - `SAAT: Discover Architecture`
  - `SAAT: Validate Current File`
  - `SAAT: Generate Documentation`
  - `SAAT: Run Pipeline`

- **Status Bar**: Click the SAAT icon for quick actions

- **Code Lens**: Inline validation and suggestions

- **Diagnostics**: Real-time validation errors

## 🤖 Agents

SAAT uses specialized agents for different tasks:

### Discovery Agent
Analyzes codebases to extract architectural information:
- Repository structure analysis
- Technology stack detection
- API discovery
- Database schema extraction
- External dependency mapping

### Business Context Agent
Gathers business context through structured interviews:
- Stakeholder identification
- Business capability mapping
- Compliance requirement extraction
- User journey mapping

### JSON Generator Agent
Converts discovered information to C4 JSON format:
- ID generation and consistency
- Hierarchy management
- Criticality classification
- Relationship mapping

### Validation Agent
Validates models against rules and best practices:
- Schema validation
- Business rule checking
- Security validation
- Best practice enforcement

### Documentation Agent
Generates comprehensive documentation:
- Architecture Decision Records (ADRs)
- Confluence pages
- README files
- API documentation
- Runbooks

### Terraform Agent
Generates infrastructure as code:
- AWS/Azure/GCP resources
- Kubernetes manifests
- Docker compositions
- CI/CD pipelines
- Monitoring configurations

### Security Agent
Performs security analysis:
- STRIDE threat modeling
- Security control recommendations
- Compliance checking
- Zero-trust architecture guidance

### Fitness Function Agent
Creates architectural fitness tests:
- Performance tests
- Reliability tests
- Security tests
- Coupling metrics

### Architecture Advisor Agent
Provides architectural recommendations:
- Pattern suggestions
- Anti-pattern detection
- Improvement recommendations
- Migration strategies

## 🔄 Pipelines

Pipelines orchestrate multiple agents:

### Complete Analysis Pipeline

```yaml
name: complete-analysis
version: 1.0.0

steps:
  - name: discover
    agent: discovery-agent
    task: analyze_repository
    
  - name: context
    agent: business-context-agent
    task: gather_context
    
  - name: generate
    agent: json-generator-agent
    task: generate_model
    
  - name: validate
    agent: validation-agent
    task: validate_model
    required: true
    
  - name: security
    agent: security-agent
    task: threat_model
    
  - name: document
    agent: documentation-agent
    task: generate_docs
    
  - name: terraform
    agent: terraform-agent
    task: generate_infrastructure
    
  - name: fitness
    agent: fitness-agent
    task: generate_tests
    
  - name: advise
    agent: advisor-agent
    task: provide_recommendations
```

### Custom Pipeline Example

```yaml
name: quick-validation
version: 1.0.0

steps:
  - name: discover
    agent: discovery-agent
    task: quick_scan
    params:
      depth: 1
      
  - name: validate
    agent: validation-agent
    task: basic_validation
    
  - name: report
    agent: documentation-agent
    task: generate_report
    params:
      format: markdown
```

## 📚 API Reference

### SAATClient

```typescript
class SAATClient {
  constructor(options: SAATOptions)
  
  // Discovery
  discover(options: DiscoverOptions): Promise<DiscoveryResult>
  
  // Model Generation
  generateModel(options: ModelOptions): Promise<C4Model>
  
  // Validation
  validate(model: C4Model): Promise<ValidationResult>
  
  // Documentation
  generateDocumentation(model: C4Model, format: string): Promise<Documentation>
  
  // Infrastructure
  generateTerraform(model: C4Model, provider: string): Promise<TerraformModule>
  
  // Pipeline
  runPipeline(config: PipelineConfig): Promise<PipelineResult>
}
```

### Types

```typescript
interface C4Model {
  version: string
  systems: SystemContext[]
  containers: Container[]
  components: Component[]
  externals: ExternalSystem[]
  relationships: Relationship[]
}

interface ValidationResult {
  valid: boolean
  score: number
  errors: ValidationError[]
  warnings: ValidationWarning[]
  suggestions: Suggestion[]
}

interface DiscoveryResult {
  timestamp: string
  repository: string
  technologies: string[]
  containers: ContainerInfo[]
  apis: APIInfo[]
  databases: DatabaseInfo[]
  externals: ExternalDependency[]
}
```

## 🛠️ Development

### Project Structure

```
saat/
├── src/
│   ├── agents/           # Agent implementations
│   ├── broker/          # Context broker
│   ├── cli/            # CLI interface
│   ├── api/           # REST API
│   ├── core/         # Core models
│   ├── utils/       # Utilities
│   └── llm/        # LLM clients
├── templates/     # Output templates
├── rules/        # Validation rules
├── pipelines/   # Pipeline configs
├── tests/      # Test suites
├── docs/      # Documentation
└── examples/ # Example projects
```

### Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test suite
npm test -- agents/discovery

# Run integration tests
npm run test:integration

# Run E2E tests
npm run test:e2e
```

### Building

```bash
# Development build
npm run build:dev

# Production build
npm run build

# Watch mode
npm run watch
```

### Debugging

```bash
# Run with debug logging
DEBUG=saat:* saat discover --path ./

# Use VS Code debugger
# Press F5 with provided launch configuration
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Clone your fork
3. Install dependencies: `npm install`
4. Create a feature branch: `git checkout -b feature/my-feature`
5. Make changes and add tests
6. Run tests: `npm test`
7. Commit with conventional commits: `git commit -m "feat: add new agent"`
8. Push and create a Pull Request

### Adding New Agents

1. Create agent class in `src/agents/`
2. Implement `BaseAgent` interface
3. Add agent configuration
4. Register in context broker
5. Add tests
6. Update documentation

See [Agent Development Guide](docs/agent-development.md) for details.

## 📖 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [Agent Development Guide](docs/agent-development.md)
- [Pipeline Creation Guide](docs/pipeline-guide.md)
- [API Documentation](docs/api.md)
- [Configuration Reference](docs/configuration.md)
- [Troubleshooting](docs/troubleshooting.md)

## 📊 Examples

Check the [`examples/`](examples/) directory for:

- Microservices architecture discovery
- Monolithic application analysis
- Serverless architecture validation
- Legacy system documentation
- Cloud migration assessment

## 🔗 Resources

- [C4 Model](https://c4model.com/) - Learn about C4 architecture diagrams
- [British Airways Architecture Standards](docs/ba-standards.md) - BA-specific guidelines
- [Claude API Documentation](https://docs.anthropic.com/) - LLM integration
- [Confluence API](https://developer.atlassian.com/cloud/confluence/) - Documentation publishing

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Simon Brown for the C4 Model
- Anthropic for Claude API
- The open-source community

## 💬 Support

- [GitHub Issues](https://github.com/your-org/saat/issues) - Bug reports and feature requests
- [Discussions](https://github.com/your-org/saat/discussions) - General discussions
- [Stack Overflow](https://stackoverflow.com/questions/tagged/saat) - Technical questions
- [Discord](https://discord.gg/saat) - Community chat

## 🚦 Status

- Build: ![CI Status](https://github.com/your-org/saat/workflows/CI/badge.svg)
- Coverage: ![Coverage](https://codecov.io/gh/your-org/saat/branch/main/graph/badge.svg)
- Version: ![NPM Version](https://img.shields.io/npm/v/@your-org/saat.svg)
- Downloads: ![NPM Downloads](https://img.shields.io/npm/dm/@your-org/saat.svg)

---

<p align="center">
  Made with ❤️ by Solution Architects for Solution Architects
</p>
