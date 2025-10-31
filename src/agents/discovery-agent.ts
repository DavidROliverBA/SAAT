import { BaseAgent } from './base-agent';
import {
  AgentResult,
  ValidationResult,
  DiscoveryParams,
  DiscoveryResult,
  ContainerInfo,
  APIInfo,
  DatabaseInfo,
  ExternalDependency,
} from '../core/types';
import * as fs from 'fs-extra';
import * as path from 'path';
import { glob } from 'glob';

export class DiscoveryAgent extends BaseAgent<DiscoveryParams, DiscoveryResult> {
  constructor() {
    super({
      name: 'discovery-agent',
      version: '1.0.0',
      capabilities: [
        'code_analysis',
        'config_parsing',
        'api_discovery',
        'dependency_mapping',
      ],
      contextTemplate: `You are an expert system discovery agent specialized in analyzing codebases and infrastructure to extract architectural information.`,
    });
  }

  async execute(task: string, params: DiscoveryParams): Promise<AgentResult<DiscoveryResult>> {
    try {
      // Validate input
      const validation = this.validate(params);
      if (!validation.valid) {
        return this.failure(validation.errors[0]);
      }

      if (task === 'analyze' || task === 'analyze_repository') {
        const result = await this.analyzeRepository(params);
        return this.success(result);
      }

      return this.failure(`Unknown task: ${task}`);
    } catch (error) {
      return this.failure(error instanceof Error ? error.message : String(error));
    }
  }

  validate(input: DiscoveryParams): ValidationResult {
    return this.validateRequired(input as unknown as Record<string, unknown>, ['path']);
  }

  /**
   * Analyze a repository to discover architecture
   */
  private async analyzeRepository(params: DiscoveryParams): Promise<DiscoveryResult> {
    const { path: repoPath, exclude = ['node_modules', '.git', 'dist', 'build'] } = params;

    // Verify path exists
    if (!await fs.pathExists(repoPath)) {
      throw new Error(`Path does not exist: ${repoPath}`);
    }

    const result: DiscoveryResult = {
      timestamp: new Date().toISOString(),
      repository: repoPath,
      technologies: [],
      containers: [],
      apis: [],
      databases: [],
      externals: [],
      patterns: [],
    };

    // Discover technologies
    result.technologies = await this.discoverTechnologies(repoPath);

    // Discover containers
    result.containers = await this.discoverContainers(repoPath, exclude);

    // Discover APIs
    result.apis = await this.discoverAPIs(repoPath, exclude);

    // Discover databases
    result.databases = await this.discoverDatabases(repoPath, exclude);

    // Discover external dependencies
    result.externals = await this.discoverExternalDependencies(repoPath, exclude);

    // Identify patterns
    result.patterns = this.identifyPatterns(result);

    return result;
  }

  /**
   * Discover technologies used in the repository
   */
  private async discoverTechnologies(repoPath: string): Promise<string[]> {
    const technologies: Set<string> = new Set();

    // Check for package.json (Node.js)
    if (await fs.pathExists(path.join(repoPath, 'package.json'))) {
      technologies.add('Node.js');
      technologies.add('JavaScript');
    }

    // Check for tsconfig.json (TypeScript)
    if (await fs.pathExists(path.join(repoPath, 'tsconfig.json'))) {
      technologies.add('TypeScript');
    }

    // Check for pom.xml (Java/Maven)
    if (await fs.pathExists(path.join(repoPath, 'pom.xml'))) {
      technologies.add('Java');
      technologies.add('Maven');
    }

    // Check for build.gradle (Java/Gradle)
    if (await fs.pathExists(path.join(repoPath, 'build.gradle'))) {
      technologies.add('Java');
      technologies.add('Gradle');
    }

    // Check for requirements.txt or setup.py (Python)
    if (await fs.pathExists(path.join(repoPath, 'requirements.txt')) ||
        await fs.pathExists(path.join(repoPath, 'setup.py'))) {
      technologies.add('Python');
    }

    // Check for go.mod (Go)
    if (await fs.pathExists(path.join(repoPath, 'go.mod'))) {
      technologies.add('Go');
    }

    // Check for Dockerfile
    if (await fs.pathExists(path.join(repoPath, 'Dockerfile'))) {
      technologies.add('Docker');
    }

    // Check for docker-compose.yml
    const dockerComposeFiles = await glob('docker-compose*.{yml,yaml}', { cwd: repoPath });
    if (dockerComposeFiles.length > 0) {
      technologies.add('Docker Compose');
    }

    // Check for Kubernetes manifests
    const k8sFiles = await glob('**/*.{yaml,yml}', { cwd: repoPath, ignore: ['node_modules/**'] });
    for (const file of k8sFiles.slice(0, 10)) {
      const content = await fs.readFile(path.join(repoPath, file), 'utf-8');
      if (content.includes('apiVersion:') && content.includes('kind:')) {
        technologies.add('Kubernetes');
        break;
      }
    }

    return Array.from(technologies);
  }

  /**
   * Discover containers (deployable units)
   */
  private async discoverContainers(repoPath: string, exclude: string[]): Promise<ContainerInfo[]> {
    const containers: ContainerInfo[] = [];

    // Check for package.json files (Node.js services)
    const packageFiles = await glob('**/package.json', {
      cwd: repoPath,
      ignore: exclude.map(e => `${e}/**`),
    });

    for (const pkgFile of packageFiles) {
      const pkgPath = path.join(repoPath, pkgFile);
      const pkg = await fs.readJSON(pkgPath);

      containers.push({
        name: pkg.name || path.basename(path.dirname(pkgPath)),
        path: path.dirname(pkgFile),
        technology: 'Node.js',
        runtime_type: 'service',
        dependencies: Object.keys(pkg.dependencies || {}),
      });
    }

    // Check for Docker Compose
    const composeFiles = await glob('docker-compose*.{yml,yaml}', { cwd: repoPath });
    if (composeFiles.length > 0) {
      // Parse docker-compose to find services
      // Simplified - in production would use yaml parser
      const composeFile = composeFiles[0];
      const content = await fs.readFile(path.join(repoPath, composeFile), 'utf-8');

      if (content.includes('postgres')) {
        containers.push({
          name: 'postgres',
          path: '.',
          technology: 'PostgreSQL',
          runtime_type: 'database',
          dependencies: [],
        });
      }

      if (content.includes('redis')) {
        containers.push({
          name: 'redis',
          path: '.',
          technology: 'Redis',
          runtime_type: 'cache',
          dependencies: [],
        });
      }
    }

    return containers;
  }

  /**
   * Discover APIs
   */
  private async discoverAPIs(repoPath: string, exclude: string[]): Promise<APIInfo[]> {
    const apis: APIInfo[] = [];

    // Look for OpenAPI/Swagger specs
    const specFiles = await glob('**/{swagger,openapi}.{json,yaml,yml}', {
      cwd: repoPath,
      ignore: exclude.map(e => `${e}/**`),
    });

    for (const specFile of specFiles) {
      apis.push({
        name: path.basename(path.dirname(specFile)),
        type: 'REST',
        endpoints: [],
        specification: specFile,
      });
    }

    // Look for Express/Fastify route files
    const routeFiles = await glob('**/{routes,controllers,api}/**/*.{js,ts}', {
      cwd: repoPath,
      ignore: exclude.map(e => `${e}/**`),
    });

    if (routeFiles.length > 0) {
      apis.push({
        name: 'API',
        type: 'REST',
        endpoints: routeFiles.map(f => ({
          method: 'GET',
          path: `/${path.basename(f, path.extname(f))}`,
        })),
      });
    }

    return apis;
  }

  /**
   * Discover databases
   */
  private async discoverDatabases(repoPath: string, exclude: string[]): Promise<DatabaseInfo[]> {
    const databases: DatabaseInfo[] = [];

    // Look for migration files
    const migrationDirs = await glob('**/{migrations,migrate}', {
      cwd: repoPath,
      ignore: exclude.map(e => `${e}/**`),
    });

    if (migrationDirs.length > 0) {
      databases.push({
        name: 'database',
        type: 'SQL',
      });
    }

    // Check package.json for database drivers
    const packageJson = path.join(repoPath, 'package.json');
    if (await fs.pathExists(packageJson)) {
      const pkg = await fs.readJSON(packageJson);
      const deps = { ...pkg.dependencies, ...pkg.devDependencies };

      if (deps.pg || deps.postgres) {
        databases.push({ name: 'PostgreSQL', type: 'SQL' });
      }
      if (deps.mysql || deps.mysql2) {
        databases.push({ name: 'MySQL', type: 'SQL' });
      }
      if (deps.mongodb) {
        databases.push({ name: 'MongoDB', type: 'NoSQL' });
      }
      if (deps.redis) {
        databases.push({ name: 'Redis', type: 'Cache' });
      }
    }

    return databases;
  }

  /**
   * Discover external dependencies
   */
  private async discoverExternalDependencies(repoPath: string, exclude: string[]): Promise<ExternalDependency[]> {
    const externals: ExternalDependency[] = [];

    // Look for .env files
    const envFiles = await glob('**/.env*', {
      cwd: repoPath,
      ignore: exclude.map(e => `${e}/**`),
    });

    for (const envFile of envFiles) {
      const content = await fs.readFile(path.join(repoPath, envFile), 'utf-8');

      // Look for API URLs
      const urlMatches = content.matchAll(/(?:API_URL|SERVICE_URL|ENDPOINT)=(.+)/g);
      for (const match of urlMatches) {
        const url = match[1].trim();
        if (url) {
          externals.push({
            name: 'External API',
            url,
            type: 'API',
          });
        }
      }
    }

    return externals;
  }

  /**
   * Identify architectural patterns
   */
  private identifyPatterns(result: DiscoveryResult): string[] {
    const patterns: string[] = [];

    // Microservices pattern
    if (result.containers.length > 3) {
      patterns.push('Microservices');
    }

    // Monolithic pattern
    if (result.containers.length === 1 && result.containers[0].runtime_type === 'service') {
      patterns.push('Monolithic');
    }

    // Event-driven pattern
    if (result.containers.some(c => c.technology.includes('Kafka') || c.technology.includes('RabbitMQ'))) {
      patterns.push('Event-Driven');
    }

    // REST API pattern
    if (result.apis.some(api => api.type === 'REST')) {
      patterns.push('REST API');
    }

    // Database per service
    if (result.databases.length >= result.containers.filter(c => c.runtime_type === 'service').length) {
      patterns.push('Database per Service');
    }

    return patterns;
  }

  protected calculateConfidence(result: DiscoveryResult): number {
    let score = 0.5;

    if (result.containers.length > 0) score += 0.2;
    if (result.technologies.length > 0) score += 0.1;
    if (result.apis.length > 0) score += 0.1;
    if (result.databases.length > 0) score += 0.05;
    if (result.patterns.length > 0) score += 0.05;

    return Math.min(score, 1.0);
  }
}
