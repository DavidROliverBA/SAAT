export class ContextMemory {
  private storage: Map<string, unknown> = new Map();
  private maxSize: number;

  constructor(maxSize: number = 1000) {
    this.maxSize = maxSize;
  }

  /**
   * Store a value in memory
   */
  store(key: string, value: unknown): void {
    if (this.storage.size >= this.maxSize) {
      // Remove oldest entry (first entry in Map)
      const firstKey = this.storage.keys().next().value;
      if (firstKey) {
        this.storage.delete(firstKey);
      }
    }
    this.storage.set(key, value);
  }

  /**
   * Get a value from memory
   */
  get(key: string): unknown {
    return this.storage.get(key);
  }

  /**
   * Get all relevant context for an agent
   */
  getRelevant(agent: string): Record<string, unknown> {
    const relevant: Record<string, unknown> = {};

    // Get all keys related to this agent
    for (const [key, value] of this.storage.entries()) {
      if (key.includes(agent) || key === 'global') {
        relevant[key] = value;
      }
    }

    return relevant;
  }

  /**
   * Check if a key exists
   */
  has(key: string): boolean {
    return this.storage.has(key);
  }

  /**
   * Delete a value from memory
   */
  delete(key: string): boolean {
    return this.storage.delete(key);
  }

  /**
   * Clear all memory
   */
  clear(): void {
    this.storage.clear();
  }

  /**
   * Get the current size of memory
   */
  size(): number {
    return this.storage.size;
  }

  /**
   * Get all keys in memory
   */
  keys(): string[] {
    return Array.from(this.storage.keys());
  }
}
