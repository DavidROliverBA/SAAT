// Core types
export * from './core/types';

// Agents
export { BaseAgent } from './agents/base-agent';
export { DiscoveryAgent } from './agents/discovery-agent';
export { JSONGeneratorAgent } from './agents/json-generator-agent';

// Broker
export { ContextBroker, PipelineError } from './broker/context-broker';
export { ContextMemory } from './broker/context-memory';
export { ArchitecturalContextImpl } from './broker/architectural-context';

// LLM Clients
export { ClaudeClient, LLMResponse, LLMOptions } from './llm/claude-client';

// Main client class
import { ContextBroker } from './broker/context-broker';
import { DiscoveryAgent } from './agents/discovery-agent';
import { JSONGeneratorAgent } from './agents/json-generator-agent';
import { ClaudeClient } from './llm/claude-client';
import {
  C4Model,
  DiscoveryParams,
  DiscoveryResult,
  ValidationResult,
  GeneratorParams,
} from './core/types';

export interface SAATClientOptions {
  apiKey?: string;
  config?: string;
}

export class SAATClient {
  private broker: ContextBroker;
  private llmClient?: ClaudeClient;

  constructor(options?: SAATClientOptions) {
    this.broker = new ContextBroker();

    // Initialize LLM client if API key provided
    if (options?.apiKey) {
      this.llmClient = new ClaudeClient(options.apiKey);
    } else if (process.env.CLAUDE_API_KEY) {
      this.llmClient = new ClaudeClient(process.env.CLAUDE_API_KEY);
    }

    // Register default agents
    this.broker.registerAgent(new DiscoveryAgent());
    this.broker.registerAgent(new JSONGeneratorAgent());
  }

  /**
   * Discover architecture from code
   */
  async discover(params: DiscoveryParams): Promise<DiscoveryResult> {
    const agent = this.broker.getAgent('discovery-agent');
    if (!agent) {
      throw new Error('Discovery agent not found');
    }

    const result = await agent.execute('analyze', params);

    if (!result.success) {
      throw new Error(result.errors?.[0]?.message || 'Discovery failed');
    }

    return result.data as DiscoveryResult;
  }

  /**
   * Generate C4 model from discovery results
   */
  async generateModel(params: GeneratorParams): Promise<C4Model> {
    const agent = this.broker.getAgent('json-generator');
    if (!agent) {
      throw new Error('JSON generator agent not found');
    }

    const result = await agent.execute('generate', params);

    if (!result.success) {
      throw new Error(result.errors?.[0]?.message || 'Model generation failed');
    }

    return result.data as C4Model;
  }

  /**
   * Validate a C4 model
   */
  async validate(model: C4Model): Promise<ValidationResult> {
    // Basic validation
    const errors = [];

    if (!model.version) {
      errors.push({
        code: 'MISSING_VERSION',
        message: 'Model is missing version',
        severity: 'error' as const,
      });
    }

    if (!model.metadata) {
      errors.push({
        code: 'MISSING_METADATA',
        message: 'Model is missing metadata',
        severity: 'error' as const,
      });
    }

    if (!Array.isArray(model.containers)) {
      errors.push({
        code: 'INVALID_CONTAINERS',
        message: 'Containers must be an array',
        severity: 'error' as const,
      });
    }

    return {
      valid: errors.length === 0,
      score: errors.length === 0 ? 100 : Math.max(0, 100 - (errors.length * 20)),
      errors,
      warnings: [],
    };
  }

  /**
   * Get the context broker
   */
  getBroker(): ContextBroker {
    return this.broker;
  }

  /**
   * Get the LLM client
   */
  getLLMClient(): ClaudeClient | undefined {
    return this.llmClient;
  }
}
