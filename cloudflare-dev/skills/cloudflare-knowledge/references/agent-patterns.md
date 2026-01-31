---
description: Design patterns for AI agents including prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer
globs: ["src/**/*.ts"]
alwaysApply: false
---

# Agent Design Patterns

Based on: Anthropic's patterns for building effective agents

## Overview

These patterns run in Durable Objects and use the AI SDK for model interactions.

## 1. Prompt Chaining

Decompose tasks into sequential steps where each LLM call processes the output of the previous one.

```
Input → Step 1 → Step 2 → Step 3 → Output
         ↓         ↓         ↓
       Check     Gate      Gate
```

### Example: Marketing Copy with Quality Check

```typescript
import { openai } from "@ai-sdk/openai";
import { generateText, generateObject } from "ai";
import { z } from "zod";

async function generateMarketingCopy(input: string) {
  const model = openai("gpt-4o");

  // Step 1: Generate marketing copy
  const { text: copy } = await generateText({
    model,
    prompt: `Write persuasive marketing copy for: ${input}. Focus on benefits and emotional appeal.`
  });

  // Step 2: Quality check
  const { object: qualityMetrics } = await generateObject({
    model,
    schema: z.object({
      hasCallToAction: z.boolean(),
      emotionalAppeal: z.number().min(1).max(10),
      clarity: z.number().min(1).max(10)
    }),
    prompt: `Evaluate this marketing copy:
    1. Presence of call to action (true/false)
    2. Emotional appeal (1-10)
    3. Clarity (1-10)

    Copy: ${copy}`
  });

  // Step 3: Regenerate if quality fails
  if (!qualityMetrics.hasCallToAction ||
      qualityMetrics.emotionalAppeal < 7 ||
      qualityMetrics.clarity < 7) {
    const { text: improvedCopy } = await generateText({
      model,
      prompt: `Rewrite with improvements:
      ${!qualityMetrics.hasCallToAction ? "- Add clear call to action" : ""}
      ${qualityMetrics.emotionalAppeal < 7 ? "- Stronger emotional appeal" : ""}
      ${qualityMetrics.clarity < 7 ? "- Better clarity" : ""}

      Original: ${copy}`
    });
    return { copy: improvedCopy, qualityMetrics };
  }

  return { copy, qualityMetrics };
}
```

### When to Use
- Tasks with distinct validation steps
- Multi-stage content generation
- Pipelines requiring intermediate checks

## 2. Routing

Classify input and direct to specialized handlers, enabling separation of concerns.

```
Input → Classifier → Route A → Handler A
                  → Route B → Handler B
                  → Route C → Handler C
```

### Example: Customer Support Router

```typescript
import { openai } from "@ai-sdk/openai";
import { generateObject, generateText } from "ai";
import { z } from "zod";

async function handleCustomerQuery(query: string) {
  const model = openai("gpt-4o");

  // Classify the query
  const { object: classification } = await generateObject({
    model,
    schema: z.object({
      reasoning: z.string(),
      type: z.enum(["general", "refund", "technical"]),
      complexity: z.enum(["simple", "complex"])
    }),
    prompt: `Classify this customer query:
    ${query}

    Determine type and complexity with reasoning.`
  });

  // Route based on classification
  const { text: response } = await generateText({
    model: classification.complexity === "simple"
      ? openai("gpt-4o-mini")
      : openai("o1-mini"),
    system: {
      general: "You are a customer service agent handling general inquiries.",
      refund: "You are a refund specialist. Follow company policy and collect necessary info.",
      technical: "You are technical support. Focus on step-by-step troubleshooting."
    }[classification.type],
    prompt: query
  });

  return { response, classification };
}
```

### When to Use
- Different query types need specialized handling
- Cost optimization (simple → smaller model)
- Domain-specific expertise required

## 3. Parallelization

Enable simultaneous task processing for independent analyses.

```
Input → Task A ↘
      → Task B → Aggregator → Output
      → Task C ↗
```

### Example: Parallel Code Review

```typescript
import { openai } from "@ai-sdk/openai";
import { generateText, generateObject } from "ai";
import { z } from "zod";

async function parallelCodeReview(code: string) {
  const model = openai("gpt-4o");

  // Run reviews in parallel
  const [securityReview, performanceReview, maintainabilityReview] =
    await Promise.all([
      generateObject({
        model,
        system: "Expert in code security. Focus on vulnerabilities and injection risks.",
        schema: z.object({
          vulnerabilities: z.array(z.string()),
          riskLevel: z.enum(["low", "medium", "high"]),
          suggestions: z.array(z.string())
        }),
        prompt: `Review this code:\n${code}`
      }),

      generateObject({
        model,
        system: "Expert in performance. Focus on bottlenecks and optimization.",
        schema: z.object({
          issues: z.array(z.string()),
          impact: z.enum(["low", "medium", "high"]),
          optimizations: z.array(z.string())
        }),
        prompt: `Review this code:\n${code}`
      }),

      generateObject({
        model,
        system: "Expert in code quality. Focus on structure and best practices.",
        schema: z.object({
          concerns: z.array(z.string()),
          qualityScore: z.number().min(1).max(10),
          recommendations: z.array(z.string())
        }),
        prompt: `Review this code:\n${code}`
      })
    ]);

  const reviews = [
    { ...securityReview.object, type: "security" },
    { ...performanceReview.object, type: "performance" },
    { ...maintainabilityReview.object, type: "maintainability" }
  ];

  // Aggregate results
  const { text: summary } = await generateText({
    model,
    system: "Technical lead summarizing code reviews.",
    prompt: `Synthesize these reviews into key actions:\n${JSON.stringify(reviews, null, 2)}`
  });

  return { reviews, summary };
}
```

### When to Use
- Independent analyses of same input
- Voting/consensus mechanisms
- Time-sensitive multi-aspect evaluation

## 4. Orchestrator-Workers

Central LLM dynamically breaks down tasks, delegates to workers, and synthesizes results.

```
Request → Orchestrator → Worker 1 ↘
              ↓        → Worker 2 → Synthesizer → Output
           Planner     → Worker 3 ↗
```

### Example: Feature Implementation

```typescript
import { openai } from "@ai-sdk/openai";
import { generateObject } from "ai";
import { z } from "zod";

async function implementFeature(featureRequest: string) {
  // Orchestrator: Plan the implementation
  const { object: plan } = await generateObject({
    model: openai("o1"),
    schema: z.object({
      files: z.array(z.object({
        purpose: z.string(),
        filePath: z.string(),
        changeType: z.enum(["create", "modify", "delete"])
      })),
      estimatedComplexity: z.enum(["low", "medium", "high"])
    }),
    system: "Senior software architect planning implementations.",
    prompt: `Analyze and create implementation plan:\n${featureRequest}`
  });

  // Workers: Execute planned changes
  const fileChanges = await Promise.all(
    plan.files.map(async (file) => {
      const workerPrompt = {
        create: "Expert at implementing new files with best practices.",
        modify: "Expert at modifying code while maintaining consistency.",
        delete: "Expert at safely removing code without breaking changes."
      }[file.changeType];

      const { object: change } = await generateObject({
        model: openai("gpt-4o"),
        schema: z.object({
          explanation: z.string(),
          code: z.string()
        }),
        system: workerPrompt,
        prompt: `Implement changes for ${file.filePath}:
        Purpose: ${file.purpose}
        Feature context: ${featureRequest}`
      });

      return { file, implementation: change };
    })
  );

  return { plan, changes: fileChanges };
}
```

### When to Use
- Complex tasks requiring decomposition
- Multi-file code changes
- Tasks with variable scope

## 5. Evaluator-Optimizer Loop

One LLM generates responses while another evaluates and provides feedback iteratively.

```
Input → Generator → Evaluator → Pass? → Output
            ↑           ↓         No
            └─── Feedback ←───────┘
```

### Example: Translation with Quality Loop

```typescript
import { openai } from "@ai-sdk/openai";
import { generateText, generateObject } from "ai";
import { z } from "zod";

async function translateWithFeedback(text: string, targetLanguage: string) {
  let currentTranslation = "";
  let iterations = 0;
  const MAX_ITERATIONS = 3;

  // Initial translation (smaller model)
  const { text: translation } = await generateText({
    model: openai("gpt-4o-mini"),
    system: "Expert literary translator.",
    prompt: `Translate to ${targetLanguage}, preserving tone and nuance:\n${text}`
  });

  currentTranslation = translation;

  // Evaluation-optimization loop
  while (iterations < MAX_ITERATIONS) {
    // Evaluate (larger model)
    const { object: evaluation } = await generateObject({
      model: openai("gpt-4o"),
      schema: z.object({
        qualityScore: z.number().min(1).max(10),
        preservesTone: z.boolean(),
        preservesNuance: z.boolean(),
        culturallyAccurate: z.boolean(),
        specificIssues: z.array(z.string()),
        improvementSuggestions: z.array(z.string())
      }),
      system: "Expert in evaluating literary translations.",
      prompt: `Evaluate translation quality:

      Original: ${text}
      Translation: ${currentTranslation}`
    });

    // Check if quality meets threshold
    if (evaluation.qualityScore >= 8 &&
        evaluation.preservesTone &&
        evaluation.preservesNuance &&
        evaluation.culturallyAccurate) {
      break;
    }

    // Generate improved translation
    const { text: improvedTranslation } = await generateText({
      model: openai("gpt-4o"),
      system: "Expert literary translator.",
      prompt: `Improve translation based on feedback:
      Issues: ${evaluation.specificIssues.join("\n")}
      Suggestions: ${evaluation.improvementSuggestions.join("\n")}

      Original: ${text}
      Current: ${currentTranslation}`
    });

    currentTranslation = improvedTranslation;
    iterations++;
  }

  return { finalTranslation: currentTranslation, iterationsRequired: iterations };
}
```

### When to Use
- Quality-critical outputs
- Tasks with clear evaluation criteria
- Iterative refinement scenarios

## Pattern Selection Guide

| Pattern | Use When | Complexity |
|---------|----------|------------|
| **Prompt Chaining** | Sequential validation needed | Low |
| **Routing** | Different handling per input type | Low |
| **Parallelization** | Independent analyses | Medium |
| **Orchestrator-Workers** | Dynamic task decomposition | High |
| **Evaluator-Optimizer** | Quality iteration needed | Medium |

## Combining Patterns

Patterns can be combined:
- Router → Orchestrator (route then plan)
- Parallelization → Evaluator (parallel generate, evaluate all)
- Chain → Router → Workers (validate, classify, delegate)

## Sources
- https://developers.cloudflare.com/agents/patterns/
- https://www.anthropic.com/engineering/building-effective-agents
