import {
  Agent,
  Pipeline,
  PipelineResult,
  PipelineStep,
  StepResult,
  AgentError,
  ArchitecturalContext,
} from '../core/types';
import { ContextMemory } from './context-memory';
import { ArchitecturalContextImpl } from './architectural-context';

export class PipelineError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'PipelineError';
  }
}

export class ContextBroker {
  private agents: Map<string, Agent<unknown, unknown>> = new Map();
  private context: ArchitecturalContext;
  private memory: ContextMemory;
  private pipelines: Map<string, Pipeline>;

  constructor(config?: { memorySize?: number }) {
    this.context = new ArchitecturalContextImpl();
    this.memory = new ContextMemory(config?.memorySize || 1000);
    this.pipelines = new Map();
  }

  /**
   * Register an agent with the broker
   */
  registerAgent(agent: Agent<unknown, unknown>): void {
    this.agents.set(agent.name, agent);
  }

  /**
   * Register a pipeline with the broker
   */
  registerPipeline(pipeline: Pipeline): void {
    this.pipelines.set(pipeline.name, pipeline);
  }

  /**
   * Get a registered agent by name
   */
  getAgent(name: string): Agent<unknown, unknown> | undefined {
    return this.agents.get(name);
  }

  /**
   * Get a registered pipeline by name
   */
  getPipeline(name: string): Pipeline | undefined {
    return this.pipelines.get(name);
  }

  /**
   * Get the architectural context
   */
  getContext(): ArchitecturalContext {
    return this.context;
  }

  /**
   * Execute a pipeline
   */
  async executePipeline(
    pipelineName: string,
    params: Record<string, unknown>
  ): Promise<PipelineResult> {
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
        const depCheck = this.checkDependencies(step, results);
        if (!depCheck.satisfied) {
          errors.push(...depCheck.errors);
          if (step.required) {
            break;
          }
          continue;
        }
      }

      // Get the agent
      const agent = this.agents.get(step.agent);
      if (!agent) {
        const error: AgentError = {
          code: 'AGENT_NOT_FOUND',
          message: `Agent not found: ${step.agent}`,
          severity: 'error',
          element: step.name,
        };
        errors.push(error);
        if (step.required) {
          break;
        }
        continue;
      }

      // Execute the step
      const stepResult = await this.executeStep(step, agent, results, params);
      results.set(step.name, stepResult);

      // Handle failures
      if (!stepResult.success && step.required) {
        if (stepResult.error) {
          errors.push(stepResult.error);
        }
        break;
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

  /**
   * Execute a single pipeline step
   */
  private async executeStep(
    step: PipelineStep,
    agent: Agent<unknown, unknown>,
    previousResults: Map<string, StepResult>,
    pipelineParams: Record<string, unknown>
  ): Promise<StepResult> {
    const stepStart = Date.now();

    try {
      // Prepare context for this step
      const stepContext = this.prepareContext(step, previousResults, pipelineParams);

      // Execute the agent task
      const result = await agent.execute(step.task, stepContext);

      // Store result in memory
      this.memory.store(step.name, result.data);

      // Update global context
      this.context.update(result.data);

      return {
        success: result.success,
        data: result.data,
        duration: Date.now() - stepStart,
        error: result.errors?.[0],
      };
    } catch (error) {
      const stepError: AgentError = {
        code: 'STEP_EXECUTION_ERROR',
        message: error instanceof Error ? error.message : String(error),
        severity: 'error',
        element: step.name,
      };

      return {
        success: false,
        data: null,
        duration: Date.now() - stepStart,
        error: stepError,
      };
    }
  }

  /**
   * Prepare context for a pipeline step
   */
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

    // Add previous results if dependencies specified
    if (step.depends_on) {
      const previous: Record<string, unknown> = {};
      for (const dep of step.depends_on) {
        const result = previousResults.get(dep);
        if (result && result.success) {
          previous[dep] = result.data;
        }
      }
      context.previous = previous;
    }

    return context;
  }

  /**
   * Check if step dependencies are satisfied
   */
  private checkDependencies(
    step: PipelineStep,
    results: Map<string, StepResult>
  ): { satisfied: boolean; errors: AgentError[] } {
    const errors: AgentError[] = [];

    if (!step.depends_on) {
      return { satisfied: true, errors: [] };
    }

    for (const dep of step.depends_on) {
      const depResult = results.get(dep);
      if (!depResult || !depResult.success) {
        errors.push({
          code: 'DEPENDENCY_FAILED',
          message: `Step ${step.name} depends on failed step ${dep}`,
          severity: 'error',
          element: step.name,
        });
      }
    }

    return {
      satisfied: errors.length === 0,
      errors,
    };
  }

  /**
   * Clear memory
   */
  clearMemory(): void {
    this.memory.clear();
  }

  /**
   * Clear context
   */
  clearContext(): void {
    this.context.clear();
  }

  /**
   * Get all registered agent names
   */
  getAgentNames(): string[] {
    return Array.from(this.agents.keys());
  }

  /**
   * Get all registered pipeline names
   */
  getPipelineNames(): string[] {
    return Array.from(this.pipelines.keys());
  }
}
