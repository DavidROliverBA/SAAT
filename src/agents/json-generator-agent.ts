import { BaseAgent } from './base-agent';
import {
  AgentResult,
  ValidationResult,
  GeneratorParams,
  C4Model,
  Container,
  ExternalSystem,
  DiscoveryResult,
  BusinessContext,
  ExternalDependency,
  ContainerInfo,
} from '../core/types';

export class JSONGeneratorAgent extends BaseAgent<GeneratorParams, C4Model> {
  private idCounters: Map<string, number> = new Map();

  constructor() {
    super({
      name: 'json-generator',
      version: '1.0.0',
      capabilities: [
        'c4_generation',
        'id_management',
        'hierarchy_creation',
        'validation',
      ],
      contextTemplate: `You are a specialized agent for generating C4 model JSON according to enterprise architectural standards.`,
    });
  }

  async execute(task: string, params: GeneratorParams): Promise<AgentResult<C4Model>> {
    try {
      const validation = this.validate(params);
      if (!validation.valid) {
        return this.failure(validation.errors[0]);
      }

      if (task === 'generate' || task === 'generate_model') {
        const model = await this.generateC4Model(params.discovery, params.business);
        return this.success(model);
      }

      return this.failure(`Unknown task: ${task}`);
    } catch (error) {
      return this.failure(error instanceof Error ? error.message : String(error));
    }
  }

  validate(input: GeneratorParams): ValidationResult {
    return this.validateRequired(input as unknown as Record<string, unknown>, ['discovery']);
  }

  /**
   * Generate a C4 model from discovery results
   */
  private async generateC4Model(
    discovery: DiscoveryResult,
    business?: BusinessContext
  ): Promise<C4Model> {
    // Reset ID counters for new model
    this.idCounters.clear();

    const model: C4Model = {
      version: '1.0.0',
      metadata: {
        name: business?.purpose || this.inferSystemName(discovery),
        description: business?.purpose || 'Auto-generated C4 model from code discovery',
        author: 'SAAT',
        created: new Date().toISOString(),
        modified: new Date().toISOString(),
        domain: this.inferDomain(discovery),
        criticality: 'STANDARD',
      },
      systems: [],
      containers: [],
      components: [],
      externals: [],
      relationships: [],
    };

    // Generate containers from discovered services
    model.containers = discovery.containers.map(c => this.mapToContainer(c));

    // Generate external systems from dependencies
    model.externals = discovery.externals.map(e => this.mapToExternal(e));

    // Generate system context
    this.generateSystemContext(model, discovery);

    // Apply criticality standards
    this.applyCriticalityStandards(model, business);

    // Generate relationships
    this.generateRelationships(model, discovery);

    return model;
  }

  /**
   * Infer system name from discovery
   */
  private inferSystemName(discovery: DiscoveryResult): string {
    if (discovery.containers.length > 0) {
      return discovery.containers[0].name;
    }
    return 'Discovered System';
  }

  /**
   * Infer domain from discovery
   */
  private inferDomain(discovery: DiscoveryResult): string {
    // Try to infer from patterns
    if (discovery.patterns.includes('E-commerce')) return 'commerce';
    if (discovery.patterns.includes('Microservices')) return 'services';
    return 'general';
  }

  /**
   * Map ContainerInfo to Container
   */
  private mapToContainer(info: ContainerInfo): Container {
    return {
      id: this.generateId('container', info.technology),
      name: info.name,
      description: `${info.runtime_type} container for ${info.name}`,
      type: 'container',
      technology: info.technology,
      runtime_type: info.runtime_type as Container['runtime_type'],
      criticality: this.inferCriticality(info),
      parent_system: 'SYS-DEFAULT-001',
      tags: info.dependencies,
    };
  }

  /**
   * Map ExternalDependency to ExternalSystem
   */
  private mapToExternal(dep: ExternalDependency): ExternalSystem {
    return {
      id: this.generateId('external', dep.type),
      name: dep.name,
      description: `External system: ${dep.name}`,
      type: 'external',
      classification: this.classifyExternal(dep),
      vendor: dep.type,
    };
  }

  /**
   * Generate system context
   */
  private generateSystemContext(model: C4Model, discovery: DiscoveryResult): void {
    // Create a system for all containers
    const systemId = 'SYS-DEFAULT-001';

    model.systems.push({
      id: systemId,
      name: model.metadata.name,
      description: model.metadata.description,
      type: 'system',
      technology: discovery.technologies.join(', '),
      criticality: model.metadata.criticality || 'STANDARD',
      tags: discovery.patterns,
    });
  }

  /**
   * Apply criticality standards
   */
  private applyCriticalityStandards(model: C4Model, business?: BusinessContext): void {
    // Apply business-driven criticality if available
    if (business?.compliance.some(c => c.framework === 'PCI-DSS')) {
      // Payment systems are critical
      model.containers.forEach(c => {
        if (c.tags?.some(t => t.includes('payment') || t.includes('stripe') || t.includes('paypal'))) {
          c.criticality = 'CS2';
        }
      });
    }

    // Auth systems are critical
    model.containers.forEach(c => {
      if (c.tags?.some(t => t.includes('auth') || t.includes('passport') || t.includes('jwt'))) {
        c.criticality = 'CS2';
      }
    });

    // Customer-facing services get SL1
    model.containers.forEach(c => {
      if (c.tags?.some(t => t.includes('api') || t.includes('express') || t.includes('fastify'))) {
        if (c.criticality === 'STANDARD') {
          c.criticality = 'SL1';
        }
      }
    });
  }

  /**
   * Generate relationships between elements
   */
  private generateRelationships(model: C4Model, discovery: DiscoveryResult): void {
    // Generate relationships from dependencies
    model.containers.forEach(container => {
      // Container to database relationships
      const databases = container.tags?.filter(t =>
        t.includes('pg') || t.includes('mysql') || t.includes('mongodb')
      );

      databases?.forEach(db => {
        const dbExternal = model.externals.find(e =>
          e.name.toLowerCase().includes(db.toLowerCase())
        );

        if (dbExternal) {
          model.relationships.push({
            id: this.generateId('relationship', 'uses'),
            source: container.id,
            target: dbExternal.id,
            description: `Uses ${dbExternal.name} for data storage`,
            protocol: 'TCP',
            async: false,
          });
        }
      });

      // Container to external API relationships
      discovery.externals.forEach(ext => {
        const external = model.externals.find(e => e.name === ext.name);
        if (external) {
          model.relationships.push({
            id: this.generateId('relationship', 'calls'),
            source: container.id,
            target: external.id,
            description: `Calls ${external.name} API`,
            protocol: ext.url?.startsWith('https') ? 'HTTPS' : 'HTTP',
            async: false,
          });
        }
      });
    });
  }

  /**
   * Generate a unique ID
   */
  private generateId(type: string, suffix: string): string {
    const key = `${type}-${suffix}`;
    const current = this.idCounters.get(key) || 0;
    const next = current + 1;
    this.idCounters.set(key, next);

    const prefix = type.toUpperCase().substring(0, 3);
    const seq = next.toString().padStart(3, '0');

    return `${prefix}-${suffix.toUpperCase().replace(/[^A-Z0-9]/g, '')}-${seq}`;
  }

  /**
   * Infer criticality from container info
   */
  private inferCriticality(info: ContainerInfo): Container['criticality'] {
    // Check dependencies for critical systems
    if (info.dependencies.some(d => d.includes('payment') || d.includes('auth'))) {
      return 'CS2';
    }

    // API services get SL1
    if (info.runtime_type === 'service' && info.dependencies.some(d => d.includes('express') || d.includes('fastify'))) {
      return 'SL1';
    }

    return 'STANDARD';
  }

  /**
   * Classify an external system
   */
  private classifyExternal(dep: ExternalDependency): ExternalSystem['classification'] {
    const name = dep.name.toLowerCase();

    if (name.includes('stripe') || name.includes('paypal')) {
      return 'SAAS';
    }

    if (name.includes('aws') || name.includes('azure') || name.includes('gcp')) {
      return 'PAAS';
    }

    if (dep.url) {
      return 'MANAGED_API';
    }

    return 'INDUSTRY_SYSTEM';
  }

  protected calculateConfidence(model: C4Model): number {
    let score = 0.5;

    if (model.containers.length > 0) score += 0.2;
    if (model.externals.length > 0) score += 0.1;
    if (model.systems.length > 0) score += 0.1;
    if (model.relationships.length > 0) score += 0.1;

    return Math.min(score, 1.0);
  }
}
