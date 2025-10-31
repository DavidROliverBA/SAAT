#!/usr/bin/env node

import { Command } from 'commander';
import * as fs from 'fs-extra';
import * as path from 'path';
import { config as loadEnv } from 'dotenv';
import chalk from 'chalk';
import ora from 'ora';
import { ContextBroker } from '../broker/context-broker';
import { DiscoveryAgent } from '../agents/discovery-agent';
import { JSONGeneratorAgent } from '../agents/json-generator-agent';

// Load environment variables
loadEnv();

const program = new Command();

program
  .name('saat')
  .description('Solution Architecture Agent Toolkit - AI-powered C4 model automation')
  .version('1.0.0');

// Initialize command
program
  .command('init')
  .description('Initialize a new SAAT project')
  .option('-p, --project <name>', 'Project name')
  .action(async (options) => {
    const spinner = ora('Initializing SAAT project...').start();

    try {
      const projectName = options.project || 'my-architecture';
      const projectDir = path.join(process.cwd(), projectName);

      // Create project directory
      await fs.ensureDir(projectDir);

      // Create subdirectories
      await fs.ensureDir(path.join(projectDir, 'models'));
      await fs.ensureDir(path.join(projectDir, 'pipelines'));
      await fs.ensureDir(path.join(projectDir, 'docs'));

      // Create .env file
      const envContent = `# SAAT Configuration
CLAUDE_API_KEY=your_claude_api_key_here
# Optional
# OPENAI_API_KEY=your_openai_api_key
# CONFLUENCE_URL=https://confluence.yourcompany.com
# CONFLUENCE_API_KEY=your_confluence_api_key
`;
      await fs.writeFile(path.join(projectDir, '.env'), envContent);

      // Create config file
      const configContent = `agents:
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
    strict: false

  documentation:
    enabled: true
    formats:
      - markdown
      - confluence

llm:
  primary: claude
  claude:
    model: claude-3-5-sonnet-20241022
    max_tokens: 4000
    temperature: 0.3

output:
  directory: ./output
  formats:
    model: json
    diagrams:
      - mermaid
    documentation: markdown
`;
      await fs.writeFile(path.join(projectDir, 'saat.config.yaml'), configContent);

      // Create README
      const readmeContent = `# ${projectName}

Generated with SAAT (Solution Architecture Agent Toolkit)

## Getting Started

1. Configure your API keys in \`.env\`
2. Run discovery: \`saat discover --path /path/to/your/code\`
3. Generate documentation: \`saat generate docs --model models/architecture.json\`

## Directory Structure

- \`models/\` - C4 architecture models
- \`pipelines/\` - Custom pipeline definitions
- \`docs/\` - Generated documentation
`;
      await fs.writeFile(path.join(projectDir, 'README.md'), readmeContent);

      spinner.succeed(`Project initialized: ${projectName}`);
      console.log(chalk.green(`\n✓ Created ${projectName}/`));
      console.log(chalk.gray('  ├── models/'));
      console.log(chalk.gray('  ├── pipelines/'));
      console.log(chalk.gray('  ├── docs/'));
      console.log(chalk.gray('  ├── .env'));
      console.log(chalk.gray('  ├── saat.config.yaml'));
      console.log(chalk.gray('  └── README.md'));
      console.log(chalk.cyan(`\nNext steps:`));
      console.log(chalk.white(`  cd ${projectName}`));
      console.log(chalk.white(`  Edit .env with your API keys`));
      console.log(chalk.white(`  saat discover --path /path/to/code`));
    } catch (error) {
      spinner.fail('Failed to initialize project');
      console.error(chalk.red(error instanceof Error ? error.message : String(error)));
      process.exit(1);
    }
  });

// Discover command
program
  .command('discover')
  .description('Discover architecture from code')
  .requiredOption('-p, --path <path>', 'Repository path to analyze')
  .option('-o, --output <file>', 'Output file', 'architecture.json')
  .option('-d, --depth <number>', 'Scan depth', '3')
  .action(async (options) => {
    const spinner = ora('Discovering architecture...').start();

    try {
      // Verify API key
      if (!process.env.CLAUDE_API_KEY) {
        throw new Error('CLAUDE_API_KEY not set in environment');
      }

      // Initialize broker and agents
      const broker = new ContextBroker();
      const discoveryAgent = new DiscoveryAgent();
      broker.registerAgent(discoveryAgent);

      spinner.text = 'Analyzing repository...';

      // Run discovery
      const result = await discoveryAgent.execute('analyze', {
        path: path.resolve(options.path),
        depth: parseInt(options.depth),
      });

      if (!result.success) {
        throw new Error(result.errors?.[0]?.message || 'Discovery failed');
      }

      spinner.text = 'Generating C4 model...';

      // Generate C4 model
      const generatorAgent = new JSONGeneratorAgent();
      broker.registerAgent(generatorAgent);

      const modelResult = await generatorAgent.execute('generate', {
        discovery: result.data,
      });

      if (!modelResult.success) {
        throw new Error(modelResult.errors?.[0]?.message || 'Model generation failed');
      }

      // Save results
      const outputPath = path.resolve(options.output);
      await fs.ensureDir(path.dirname(outputPath));
      await fs.writeJSON(outputPath, modelResult.data, { spaces: 2 });

      spinner.succeed('Architecture discovered successfully!');

      // Print summary
      console.log(chalk.cyan('\n📊 Discovery Summary:'));
      console.log(chalk.white(`  Technologies: ${result.data.technologies.join(', ')}`));
      console.log(chalk.white(`  Containers: ${result.data.containers.length}`));
      console.log(chalk.white(`  APIs: ${result.data.apis.length}`));
      console.log(chalk.white(`  Databases: ${result.data.databases.length}`));
      console.log(chalk.white(`  External Dependencies: ${result.data.externals.length}`));
      console.log(chalk.white(`  Patterns: ${result.data.patterns.join(', ')}`));

      console.log(chalk.cyan('\n🏗️  C4 Model:'));
      console.log(chalk.white(`  Systems: ${modelResult.data.systems.length}`));
      console.log(chalk.white(`  Containers: ${modelResult.data.containers.length}`));
      console.log(chalk.white(`  Externals: ${modelResult.data.externals.length}`));
      console.log(chalk.white(`  Relationships: ${modelResult.data.relationships.length}`));

      console.log(chalk.green(`\n✓ Model saved to: ${outputPath}`));
      console.log(chalk.gray(`  Confidence: ${Math.round(modelResult.confidence * 100)}%`));
    } catch (error) {
      spinner.fail('Discovery failed');
      console.error(chalk.red(error instanceof Error ? error.message : String(error)));
      process.exit(1);
    }
  });

// Validate command
program
  .command('validate')
  .description('Validate a C4 model')
  .requiredOption('-m, --model <file>', 'Model file to validate')
  .action(async (options) => {
    const spinner = ora('Validating model...').start();

    try {
      const modelPath = path.resolve(options.model);
      const model = await fs.readJSON(modelPath);

      // Basic validation
      const errors: string[] = [];

      if (!model.version) errors.push('Missing version');
      if (!model.metadata) errors.push('Missing metadata');
      if (!Array.isArray(model.containers)) errors.push('Invalid containers');
      if (!Array.isArray(model.systems)) errors.push('Invalid systems');

      if (errors.length > 0) {
        spinner.fail('Validation failed');
        errors.forEach(err => console.log(chalk.red(`  ✗ ${err}`)));
        process.exit(1);
      }

      spinner.succeed('Model is valid!');
      console.log(chalk.green('\n✓ All checks passed'));
      console.log(chalk.white(`  Version: ${model.version}`));
      console.log(chalk.white(`  Name: ${model.metadata.name}`));
      console.log(chalk.white(`  Systems: ${model.systems.length}`));
      console.log(chalk.white(`  Containers: ${model.containers.length}`));
    } catch (error) {
      spinner.fail('Validation failed');
      console.error(chalk.red(error instanceof Error ? error.message : String(error)));
      process.exit(1);
    }
  });

// Generate command
program
  .command('generate <type>')
  .description('Generate outputs (docs, diagrams, etc.)')
  .requiredOption('-m, --model <file>', 'Model file')
  .option('-o, --output <dir>', 'Output directory', './output')
  .action(async (type, options) => {
    const spinner = ora(`Generating ${type}...`).start();

    try {
      const modelPath = path.resolve(options.model);
      const model = await fs.readJSON(modelPath);

      if (type === 'docs') {
        // Generate markdown documentation
        const outputDir = path.resolve(options.output);
        await fs.ensureDir(outputDir);

        const docContent = `# ${model.metadata.name}

## Overview
${model.metadata.description}

**Author**: ${model.metadata.author}
**Created**: ${model.metadata.created}
**Criticality**: ${model.metadata.criticality}

## Architecture

### Systems (${model.systems.length})
${model.systems.map((s: { name: string; description: string; }) => `- **${s.name}**: ${s.description}`).join('\n')}

### Containers (${model.containers.length})
${model.containers.map((c: { name: string; technology: string; description: string; }) => `- **${c.name}** (${c.technology}): ${c.description}`).join('\n')}

### External Systems (${model.externals.length})
${model.externals.map((e: { name: string; description: string; }) => `- **${e.name}**: ${e.description}`).join('\n')}

### Relationships (${model.relationships.length})
${model.relationships.map((r: { source: string; target: string; description: string; }) => `- ${r.source} → ${r.target}: ${r.description}`).join('\n')}
`;

        const docPath = path.join(outputDir, 'architecture.md');
        await fs.writeFile(docPath, docContent);

        spinner.succeed('Documentation generated!');
        console.log(chalk.green(`\n✓ Documentation saved to: ${docPath}`));
      } else {
        spinner.warn(`Generation type "${type}" not yet implemented`);
      }
    } catch (error) {
      spinner.fail('Generation failed');
      console.error(chalk.red(error instanceof Error ? error.message : String(error)));
      process.exit(1);
    }
  });

// Version command
program
  .command('version')
  .description('Show version information')
  .action(() => {
    console.log(chalk.cyan('SAAT - Solution Architecture Agent Toolkit'));
    console.log(chalk.white('Version: 1.0.0'));
    console.log(chalk.gray('Build: 2024-01-01'));
  });

// Parse arguments
program.parse(process.argv);

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
