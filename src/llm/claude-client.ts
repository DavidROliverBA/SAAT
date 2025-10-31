import Anthropic from '@anthropic-ai/sdk';

export interface LLMResponse {
  content: string;
  usage?: {
    input_tokens: number;
    output_tokens: number;
  };
}

export interface LLMOptions {
  model?: string;
  max_tokens?: number;
  temperature?: number;
  system?: string;
}

export class ClaudeClient {
  private client: Anthropic;
  private defaultModel: string;
  private defaultMaxTokens: number;
  private defaultTemperature: number;

  constructor(apiKey: string, options?: {
    model?: string;
    max_tokens?: number;
    temperature?: number;
  }) {
    this.client = new Anthropic({
      apiKey,
    });

    this.defaultModel = options?.model || 'claude-3-5-sonnet-20241022';
    this.defaultMaxTokens = options?.max_tokens || 4000;
    this.defaultTemperature = options?.temperature || 0.3;
  }

  /**
   * Send a prompt to Claude and get a response
   */
  async complete(
    prompt: string,
    options?: LLMOptions
  ): Promise<LLMResponse> {
    try {
      const message = await this.client.messages.create({
        model: options?.model || this.defaultModel,
        max_tokens: options?.max_tokens || this.defaultMaxTokens,
        temperature: options?.temperature || this.defaultTemperature,
        system: options?.system,
        messages: [
          {
            role: 'user',
            content: prompt,
          },
        ],
      });

      // Extract text content
      const textContent = message.content.find(block => block.type === 'text');
      const content = textContent && 'text' in textContent ? textContent.text : '';

      return {
        content,
        usage: {
          input_tokens: message.usage.input_tokens,
          output_tokens: message.usage.output_tokens,
        },
      };
    } catch (error) {
      throw new Error(`Claude API error: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Send a prompt with JSON mode enabled
   */
  async completeJSON<T = unknown>(
    prompt: string,
    options?: LLMOptions
  ): Promise<{ data: T; raw: string }> {
    const enhancedPrompt = `${prompt}\n\nRespond with valid JSON only. Do not include any explanatory text outside the JSON.`;

    const response = await this.complete(enhancedPrompt, options);

    try {
      // Try to extract JSON from the response
      const jsonMatch = response.content.match(/```json\n?([\s\S]*?)\n?```/) ||
                       response.content.match(/\{[\s\S]*\}/);

      const jsonString = jsonMatch ? (jsonMatch[1] || jsonMatch[0]) : response.content;
      const data = JSON.parse(jsonString.trim()) as T;

      return {
        data,
        raw: response.content,
      };
    } catch (error) {
      throw new Error(`Failed to parse JSON response: ${error instanceof Error ? error.message : String(error)}\n\nResponse: ${response.content}`);
    }
  }

  /**
   * Complete a prompt with retry logic
   */
  async completeWithRetry(
    prompt: string,
    options?: LLMOptions,
    maxRetries: number = 3
  ): Promise<LLMResponse> {
    let lastError: Error | null = null;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        return await this.complete(prompt, options);
      } catch (error) {
        lastError = error instanceof Error ? error : new Error(String(error));

        // Wait before retrying (exponential backoff)
        if (attempt < maxRetries - 1) {
          await this.sleep(Math.pow(2, attempt) * 1000);
        }
      }
    }

    throw new Error(`Failed after ${maxRetries} attempts: ${lastError?.message}`);
  }

  /**
   * Sleep for a specified duration
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
