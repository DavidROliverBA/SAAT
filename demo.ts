#!/usr/bin/env node

/**
 * SAAT Demo Script
 * Demonstrates the discovery and C4 model generation capabilities
 */

import { DiscoveryAgent } from './src/agents/discovery-agent';
import { JSONGeneratorAgent } from './src/agents/json-generator-agent';
import * as fs from 'fs-extra';

async function runDemo() {
  console.log('🚀 SAAT Demo - Discovering Architecture\n');

  // Initialize agents
  const discoveryAgent = new DiscoveryAgent();
  const generatorAgent = new JSONGeneratorAgent();

  // Run discovery on SAAT itself
  console.log('📊 Step 1: Running discovery on SAAT repository...');
  const discoveryResult = await discoveryAgent.execute('analyze', {
    path: '/home/user/SAAT',
    depth: 3,
    exclude: ['node_modules', 'dist', '.git'],
  });

  if (!discoveryResult.success) {
    console.error('❌ Discovery failed:', discoveryResult.errors);
    return;
  }

  console.log('✅ Discovery complete!\n');
  console.log('  Technologies:', discoveryResult.data.technologies.join(', '));
  console.log('  Containers:', discoveryResult.data.containers.length);
  console.log('  APIs:', discoveryResult.data.apis.length);
  console.log('  Databases:', discoveryResult.data.databases.length);
  console.log('  Patterns:', discoveryResult.data.patterns.join(', '));
  console.log('  Confidence:', Math.round(discoveryResult.confidence * 100) + '%');

  // Generate C4 model
  console.log('\n🏗️  Step 2: Generating C4 model...');
  const modelResult = await generatorAgent.execute('generate', {
    discovery: discoveryResult.data,
    business: {
      purpose: 'Solution Architecture Agent Toolkit for automating C4 model creation',
      stakeholders: [
        {
          name: 'Solution Architects',
          role: 'Primary Users',
          needs: ['Architecture automation', 'Documentation generation'],
          interactions: ['CLI', 'API'],
        },
      ],
      capabilities: ['Discovery', 'Generation', 'Validation'],
      compliance: [],
    },
  });

  if (!modelResult.success) {
    console.error('❌ Model generation failed:', modelResult.errors);
    return;
  }

  console.log('✅ C4 Model generated!\n');
  console.log('  Systems:', modelResult.data.systems.length);
  console.log('  Containers:', modelResult.data.containers.length);
  console.log('  Externals:', modelResult.data.externals.length);
  console.log('  Relationships:', modelResult.data.relationships.length);
  console.log('  Confidence:', Math.round(modelResult.confidence * 100) + '%');

  // Save results
  console.log('\n💾 Saving results...');
  await fs.writeJSON('/tmp/saat-discovery.json', discoveryResult.data, { spaces: 2 });
  await fs.writeJSON('/tmp/saat-model.json', modelResult.data, { spaces: 2 });

  console.log('✅ Results saved to:');
  console.log('  - /tmp/saat-discovery.json');
  console.log('  - /tmp/saat-model.json');

  // Display sample of the model
  console.log('\n📄 Sample C4 Model:');
  console.log(JSON.stringify(modelResult.data, null, 2).substring(0, 500) + '...\n');

  console.log('✨ Demo complete!');
}

runDemo().catch(console.error);
