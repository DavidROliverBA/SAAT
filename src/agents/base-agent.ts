import { Agent, AgentResult, AgentError, ValidationResult } from '../core/types';

export abstract class BaseAgent<TParams = unknown, TResult = unknown> implements Agent<TParams, TResult> {
  public readonly name: string;
  public readonly version: string;
  public readonly capabilities: string[];
  public readonly contextTemplate: string;

  constructor(config: {
    name: string;
    version: string;
    capabilities: string[];
    contextTemplate: string;
  }) {
    this.name = config.name;
    this.version = config.version;
    this.capabilities = config.capabilities;
    this.contextTemplate = config.contextTemplate;
  }

  /**
   * Execute an agent task
   * Must be implemented by derived classes
   */
  abstract execute(task: string, params: TParams): Promise<AgentResult<TResult>>;

  /**
   * Validate input parameters
   * Must be implemented by derived classes
   */
  abstract validate(input: TParams): ValidationResult;

  /**
   * Calculate confidence score for a result
   * Can be overridden by derived classes
   */
  protected calculateConfidence(result: TResult): number {
    // Default implementation - override in derived classes
    return result ? 0.8 : 0.0;
  }

  /**
   * Format a successful agent result
   */
  protected success(data: TResult, confidence?: number): AgentResult<TResult> {
    return {
      success: true,
      data,
      confidence: confidence ?? this.calculateConfidence(data),
      errors: [],
      suggestions: [],
    };
  }

  /**
   * Format a failed agent result
   */
  protected failure(error: string | AgentError, data?: TResult): AgentResult<TResult> {
    const agentError: AgentError = typeof error === 'string'
      ? {
          code: 'EXECUTION_ERROR',
          message: error,
          severity: 'error',
        }
      : error;

    return {
      success: false,
      data: data as TResult,
      confidence: 0,
      errors: [agentError],
    };
  }

  /**
   * Create an agent error
   */
  protected createError(
    code: string,
    message: string,
    severity: 'error' | 'warning' | 'info' = 'error',
    element?: string,
    fix?: string
  ): AgentError {
    return {
      code,
      message,
      severity,
      element,
      fix,
    };
  }

  /**
   * Validate that required fields are present
   */
  protected validateRequired(
    input: Record<string, unknown>,
    required: string[]
  ): ValidationResult {
    const errors: AgentError[] = [];

    for (const field of required) {
      if (!(field in input) || input[field] === undefined || input[field] === null) {
        errors.push(this.createError(
          'MISSING_FIELD',
          `Required field '${field}' is missing`,
          'error',
          field,
          `Provide a value for '${field}'`
        ));
      }
    }

    return {
      valid: errors.length === 0,
      score: errors.length === 0 ? 100 : Math.max(0, 100 - (errors.length * 20)),
      errors,
      warnings: [],
    };
  }

  /**
   * Get agent info
   */
  public getInfo() {
    return {
      name: this.name,
      version: this.version,
      capabilities: this.capabilities,
    };
  }
}
