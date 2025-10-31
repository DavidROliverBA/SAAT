import {
  ArchitecturalContext,
  C4Model,
  DiscoveryResult,
  BusinessContext,
} from '../core/types';

export class ArchitecturalContextImpl implements ArchitecturalContext {
  model?: C4Model;
  discovery?: DiscoveryResult;
  business?: BusinessContext;
  metadata: Map<string, unknown> = new Map();

  /**
   * Get relevant context for a specific agent
   */
  getRelevant(agent: string): Record<string, unknown> {
    const relevant: Record<string, unknown> = {};

    // Include common context for all agents
    if (this.model) relevant.model = this.model;
    if (this.discovery) relevant.discovery = this.discovery;
    if (this.business) relevant.business = this.business;

    // Include agent-specific metadata
    for (const [key, value] of this.metadata.entries()) {
      if (key.startsWith(agent) || key.startsWith('global')) {
        relevant[key] = value;
      }
    }

    return relevant;
  }

  /**
   * Update context with new result
   */
  update(result: unknown): void {
    // Type-safe updates based on result type
    if (this.isC4Model(result)) {
      this.model = result;
      this.metadata.set('last_model_update', new Date().toISOString());
    } else if (this.isDiscoveryResult(result)) {
      this.discovery = result;
      this.metadata.set('last_discovery_update', new Date().toISOString());
    } else if (this.isBusinessContext(result)) {
      this.business = result;
      this.metadata.set('last_business_update', new Date().toISOString());
    }
  }

  /**
   * Set metadata value
   */
  setMetadata(key: string, value: unknown): void {
    this.metadata.set(key, value);
  }

  /**
   * Get metadata value
   */
  getMetadata(key: string): unknown {
    return this.metadata.get(key);
  }

  /**
   * Clear all context
   */
  clear(): void {
    this.model = undefined;
    this.discovery = undefined;
    this.business = undefined;
    this.metadata.clear();
  }

  /**
   * Type guard for C4Model
   */
  private isC4Model(obj: unknown): obj is C4Model {
    return (
      typeof obj === 'object' &&
      obj !== null &&
      'version' in obj &&
      'containers' in obj &&
      'metadata' in obj
    );
  }

  /**
   * Type guard for DiscoveryResult
   */
  private isDiscoveryResult(obj: unknown): obj is DiscoveryResult {
    return (
      typeof obj === 'object' &&
      obj !== null &&
      'timestamp' in obj &&
      'repository' in obj &&
      'technologies' in obj
    );
  }

  /**
   * Type guard for BusinessContext
   */
  private isBusinessContext(obj: unknown): obj is BusinessContext {
    return (
      typeof obj === 'object' &&
      obj !== null &&
      'purpose' in obj &&
      'stakeholders' in obj
    );
  }
}
