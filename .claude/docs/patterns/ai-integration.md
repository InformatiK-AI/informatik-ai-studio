# AI Integration Patterns - InformatiK-AI Studio

> Referenced from: CLAUDE.md [modular_index]
> Load when: Working on AI generation features

## Multi-Model Architecture

### Provider Abstraction

```typescript
// lib/ai/types.ts
export interface AIProvider {
  generateCode(params: GenerateParams): Promise<GenerateResult>;
  generateStream(params: GenerateParams): AsyncIterable<string>;
  estimateTokens(text: string): number;
}

export interface GenerateParams {
  prompt: string;
  systemPrompt?: string;
  model: string;
  maxTokens?: number;
  temperature?: number;
}

export interface GenerateResult {
  code: string;
  language: string;
  tokensInput: number;
  tokensOutput: number;
  model: string;
  durationMs: number;
}
```

### Provider Implementation

```typescript
// lib/ai/providers/anthropic.ts
import Anthropic from 'anthropic';

export class AnthropicProvider implements AIProvider {
  private client: Anthropic;

  constructor() {
    this.client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY!,
    });
  }

  async generateCode(params: GenerateParams): Promise<GenerateResult> {
    const startTime = Date.now();

    const response = await this.client.messages.create({
      model: params.model,
      max_tokens: params.maxTokens ?? 4096,
      temperature: params.temperature ?? 0,
      system: params.systemPrompt ?? SYSTEM_PROMPT,
      messages: [{ role: 'user', content: params.prompt }],
    });

    return {
      code: response.content[0].type === 'text' ? response.content[0].text : '',
      language: 'typescript', // Parse from response
      tokensInput: response.usage.input_tokens,
      tokensOutput: response.usage.output_tokens,
      model: params.model,
      durationMs: Date.now() - startTime,
    };
  }

  async *generateStream(params: GenerateParams): AsyncIterable<string> {
    const stream = await this.client.messages.create({
      model: params.model,
      max_tokens: params.maxTokens ?? 4096,
      system: params.systemPrompt ?? SYSTEM_PROMPT,
      messages: [{ role: 'user', content: params.prompt }],
      stream: true,
    });

    for await (const event of stream) {
      if (event.type === 'content_block_delta' &&
          event.delta.type === 'text_delta') {
        yield event.delta.text;
      }
    }
  }
}
```

### Model Router

```typescript
// lib/ai/router.ts
import { AnthropicProvider } from './providers/anthropic';
import { OpenAIProvider } from './providers/openai';

export class ModelRouter {
  private providers: Map<string, AIProvider>;

  constructor() {
    this.providers = new Map([
      ['anthropic', new AnthropicProvider()],
      ['openai', new OpenAIProvider()],
    ]);
  }

  async generate(
    params: GenerateParams,
    options?: { fallback?: boolean }
  ): Promise<GenerateResult> {
    const provider = this.getProviderForModel(params.model);

    try {
      return await provider.generateCode(params);
    } catch (error) {
      if (options?.fallback && this.canFallback(params.model)) {
        const fallbackModel = this.getFallbackModel(params.model);
        const fallbackProvider = this.getProviderForModel(fallbackModel);
        return await fallbackProvider.generateCode({
          ...params,
          model: fallbackModel,
        });
      }
      throw error;
    }
  }

  private getProviderForModel(model: string): AIProvider {
    if (model.startsWith('claude')) return this.providers.get('anthropic')!;
    if (model.startsWith('gpt')) return this.providers.get('openai')!;
    throw new Error(`Unknown model: ${model}`);
  }

  private getFallbackModel(model: string): string {
    const fallbacks: Record<string, string> = {
      'claude-3-5-sonnet-20241022': 'gpt-4o',
      'gpt-4o': 'claude-3-5-sonnet-20241022',
    };
    return fallbacks[model] ?? 'gpt-4o-mini';
  }
}
```

## System Prompts

### Code Generation Prompt

```typescript
// lib/ai/prompts/code-generation.ts
export const CODE_GENERATION_SYSTEM = `You are an expert software developer.
Generate clean, production-ready code based on the user's requirements.

Rules:
- Use TypeScript for all code
- Include proper types and interfaces
- Add helpful comments for complex logic
- Follow React best practices for components
- Use modern ES6+ syntax
- Handle errors gracefully
- Do NOT include package.json or configuration files unless asked

Output format:
- Use markdown code blocks with language identifiers
- Separate multiple files with clear headers
- Explain key decisions briefly
`;
```

### Code Fix Prompt

```typescript
export const CODE_FIX_SYSTEM = `You are an expert code reviewer and debugger.
Analyze the code and fix the issue described.

Rules:
- Explain what was wrong
- Show the corrected code
- Explain why the fix works
- Preserve existing functionality
- Don't change unrelated code
`;
```

## Token Management

### Token Estimation

```typescript
// lib/ai/tokens.ts
import { encode } from 'gpt-tokenizer';

export function estimateTokens(text: string): number {
  // Use GPT tokenizer as approximation for all models
  return encode(text).length;
}

export function checkTokenLimit(
  prompt: string,
  maxContextTokens: number,
  reservedOutputTokens: number
): { allowed: boolean; inputTokens: number; availableForOutput: number } {
  const inputTokens = estimateTokens(prompt);
  const availableForOutput = maxContextTokens - inputTokens;

  return {
    allowed: availableForOutput >= reservedOutputTokens,
    inputTokens,
    availableForOutput,
  };
}
```

### Usage Tracking

```typescript
// lib/ai/usage.ts
export async function trackUsage(
  userId: string,
  generation: GenerateResult
): Promise<void> {
  const supabase = createClient();

  await supabase.from('generations').insert({
    user_id: userId,
    model: generation.model,
    tokens_input: generation.tokensInput,
    tokens_output: generation.tokensOutput,
    duration_ms: generation.durationMs,
  });
}
```

## Error Handling

### AI-Specific Errors

```typescript
// lib/ai/errors.ts
export class AIError extends Error {
  constructor(
    message: string,
    public code: AIErrorCode,
    public provider: string,
    public retryable: boolean = false
  ) {
    super(message);
    this.name = 'AIError';
  }
}

export type AIErrorCode =
  | 'RATE_LIMITED'
  | 'TOKEN_LIMIT_EXCEEDED'
  | 'INVALID_API_KEY'
  | 'PROVIDER_UNAVAILABLE'
  | 'CONTENT_FILTERED'
  | 'TIMEOUT';

export function handleProviderError(error: unknown, provider: string): never {
  if (error instanceof Anthropic.RateLimitError) {
    throw new AIError('Rate limited', 'RATE_LIMITED', provider, true);
  }
  // ... handle other cases
}
```

## Streaming Implementation

### API Route with Streaming

```typescript
// app/api/generate/stream/route.ts
import { ModelRouter } from '@/lib/ai/router';

export async function POST(req: Request) {
  const { prompt, model } = await req.json();

  const router = new ModelRouter();
  const stream = router.generateStream({ prompt, model });

  const encoder = new TextEncoder();

  return new Response(
    new ReadableStream({
      async start(controller) {
        try {
          for await (const chunk of stream) {
            controller.enqueue(
              encoder.encode(`data: ${JSON.stringify({ text: chunk })}\n\n`)
            );
          }
          controller.enqueue(encoder.encode('data: [DONE]\n\n'));
          controller.close();
        } catch (error) {
          controller.error(error);
        }
      },
    }),
    {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    }
  );
}
```

### Client-Side Streaming Consumer

```typescript
// hooks/use-generation.ts
export function useCodeGeneration() {
  const [output, setOutput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const generate = async (prompt: string) => {
    setIsGenerating(true);
    setOutput('');

    const response = await fetch('/api/generate/stream', {
      method: 'POST',
      body: JSON.stringify({ prompt, model: 'claude-3-5-sonnet-20241022' }),
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;

      const text = decoder.decode(value);
      const lines = text.split('\n').filter(line => line.startsWith('data: '));

      for (const line of lines) {
        const data = line.slice(6);
        if (data === '[DONE]') continue;
        const { text: chunk } = JSON.parse(data);
        setOutput(prev => prev + chunk);
      }
    }

    setIsGenerating(false);
  };

  return { output, isGenerating, generate };
}
```
