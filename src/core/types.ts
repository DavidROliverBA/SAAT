// Core C4 Model Types
export interface C4Model {
  version: string;
  metadata: ModelMetadata;
  systems: SystemContext[];
  containers: Container[];
  components: Component[];
  externals: ExternalSystem[];
  relationships: Relationship[];
}

export interface ModelMetadata {
  name: string;
  description: string;
  author: string;
  created: string;
  modified: string;
  domain?: string;
  criticality?: CriticalityLevel;
}

export type CriticalityLevel = 'CS1' | 'CS2' | 'SL1' | 'SL2' | 'STANDARD';

export interface SystemContext {
  id: string;
  name: string;
  description: string;
  type: 'system';
  technology?: string;
  criticality: CriticalityLevel;
  tags?: string[];
}

export interface Container {
  id: string;
  name: string;
  description: string;
  type: 'container';
  technology: string;
  runtime_type: 'service' | 'database' | 'queue' | 'cache' | 'storage';
  criticality: CriticalityLevel;
  parent_system: string;
  tags?: string[];
}

export interface Component {
  id: string;
  name: string;
  description: string;
  type: 'component';
  technology: string;
  component_type: 'api' | 'service' | 'repository' | 'controller' | 'utility';
  parent_container: string;
  tags?: string[];
}

export interface ExternalSystem {
  id: string;
  name: string;
  description: string;
  type: 'external';
  classification: 'SAAS' | 'PAAS' | 'MANAGED_API' | 'INDUSTRY_SYSTEM' | 'PARTNER_SYSTEM';
  vendor?: string;
  sla?: SLA;
  integration_pattern?: string;
}

export interface Relationship {
  id: string;
  source: string;
  target: string;
  description: string;
  protocol?: string;
  async?: boolean;
}

export interface SLA {
  availability: number;
  response_time_ms?: number;
  rate_limit?: RateLimit;
}

export interface RateLimit {
  requests: number;
  period: string;
}

// Agent System Types
export interface Agent<TParams = unknown, TResult = unknown> {
  name: string;
  version: string;
  capabilities: string[];
  contextTemplate: string;
  execute(task: string, params: TParams): Promise<AgentResult<TResult>>;
  validate(input: TParams): ValidationResult;
}

export interface AgentResult<T = unknown> {
  success: boolean;
  data: T;
  confidence: number;
  errors?: AgentError[];
  suggestions?: string[];
  metadata?: Record<string, unknown>;
}

export interface AgentError {
  code: string;
  message: string;
  severity: 'error' | 'warning' | 'info';
  element?: string;
  fix?: string;
}

export interface ValidationResult {
  valid: boolean;
  score: number;
  errors: AgentError[];
  warnings: AgentError[];
}

// Discovery Types
export interface DiscoveryResult {
  timestamp: string;
  repository: string;
  technologies: string[];
  containers: ContainerInfo[];
  apis: APIInfo[];
  databases: DatabaseInfo[];
  externals: ExternalDependency[];
  patterns: string[];
}

export interface ContainerInfo {
  name: string;
  path: string;
  technology: string;
  runtime_type: string;
  dependencies: string[];
}

export interface APIInfo {
  name: string;
  type: 'REST' | 'GraphQL' | 'gRPC' | 'WebSocket';
  endpoints: Endpoint[];
  specification?: string;
}

export interface Endpoint {
  method: string;
  path: string;
  description?: string;
}

export interface DatabaseInfo {
  name: string;
  type: string;
  schema?: string;
}

export interface ExternalDependency {
  name: string;
  url?: string;
  type: string;
}

// Pipeline Types
export interface Pipeline {
  name: string;
  version: string;
  steps: PipelineStep[];
}

export interface PipelineStep {
  name: string;
  agent: string;
  task: string;
  required: boolean;
  constraints?: Record<string, unknown>;
  parameters?: Record<string, unknown>;
  depends_on?: string[];
}

export interface PipelineResult {
  success: boolean;
  steps: Map<string, StepResult>;
  duration: number;
  errors: AgentError[];
}

export interface StepResult {
  success: boolean;
  data: unknown;
  duration: number;
  error?: AgentError;
}

// Context Types
export interface ArchitecturalContext {
  model?: C4Model;
  discovery?: DiscoveryResult;
  business?: BusinessContext;
  metadata: Map<string, unknown>;
  getRelevant(agent: string): Record<string, unknown>;
  update(result: unknown): void;
  clear(): void;
}

export interface BusinessContext {
  purpose: string;
  stakeholders: Stakeholder[];
  capabilities: string[];
  compliance: ComplianceRequirement[];
}

export interface Stakeholder {
  name: string;
  role: string;
  needs: string[];
  interactions: string[];
}

export interface ComplianceRequirement {
  framework: string;
  requirements: string[];
  applicable: boolean;
}

// Configuration Types
export interface SAATConfig {
  agents: AgentConfigs;
  llm: LLMConfig;
  pipelines: PipelineConfig;
  output: OutputConfig;
  context_broker?: BrokerConfig;
}

export interface AgentConfigs {
  discovery?: AgentConfig;
  validation?: AgentConfig;
  documentation?: AgentConfig;
  terraform?: AgentConfig;
  security?: AgentConfig;
  fitness?: AgentConfig;
  advisor?: AgentConfig;
}

export interface AgentConfig {
  enabled: boolean;
  model?: string;
  max_tokens?: number;
  temperature?: number;
  [key: string]: unknown;
}

export interface LLMConfig {
  primary: string;
  fallback?: string;
  claude?: LLMClientConfig;
  openai?: LLMClientConfig;
}

export interface LLMClientConfig {
  api_key: string;
  model: string;
  max_tokens?: number;
  temperature?: number;
}

export interface PipelineConfig {
  default: string;
  custom?: string[];
}

export interface OutputConfig {
  directory: string;
  formats: {
    model: string;
    diagrams: string[];
    documentation: string;
  };
}

export interface BrokerConfig {
  memory_size?: number;
  cache_ttl?: number;
  max_retries?: number;
  parallel_execution?: boolean;
}

// Documentation Types
export interface Documentation {
  type: string;
  content: string;
  metadata: {
    title: string;
    author: string;
    created: string;
  };
  attachments?: string[];
}

// Security Types
export interface Threat {
  type: 'spoofing' | 'tampering' | 'repudiation' | 'information_disclosure' | 'denial_of_service' | 'elevation_of_privilege';
  element: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  mitigation?: string;
}

export interface AttackVector {
  name: string;
  entry_point: string;
  target: string;
  risk_level: string;
}

export interface SecurityControl {
  type: string;
  description: string;
  applicable_to: string[];
  implementation: string;
}

export interface ThreatModel {
  threats: Threat[];
  attackVectors: AttackVector[];
  controls: SecurityControl[];
  risk_score: number;
}

// Discovery Parameters
export interface DiscoveryParams {
  path: string;
  depth?: number;
  exclude?: string[];
}

// Generator Parameters
export interface GeneratorParams {
  discovery: DiscoveryResult;
  business?: BusinessContext;
}

// Documentation Parameters
export interface DocParams {
  model: C4Model;
  type: string;
  documentation?: Documentation;
}

// Security Parameters
export interface SecurityParams {
  model: C4Model;
}

// Validation Parameters
export interface ValidationParams {
  model: C4Model;
  strict?: boolean;
  rules?: string[];
}
