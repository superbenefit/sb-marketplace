# TypeScript Standards for Web Projects

This document defines TypeScript best practices and quality standards for web development.

## Type Safety

### Avoid `any`

❌ **INCORRECT**: Using `any`
```typescript
function processData(data: any) {  // Defeats TypeScript's purpose
  return data.value;
}
```

✅ **CORRECT**: Proper typing
```typescript
interface Data {
  value: string;
}

function processData(data: Data): string {
  return data.value;
}
```

**When `any` might be acceptable** (rare):
- Gradual migration from JavaScript
- Truly dynamic data from external sources (prefer `unknown`)
- Complex third-party types (use `@ts-ignore` with comment)

### Use `unknown` for Uncertain Types

✅ **CORRECT**: `unknown` with type checking
```typescript
function processUserInput(input: unknown) {
  if (typeof input === 'string') {
    return input.toUpperCase();
  }
  throw new Error('Expected string input');
}
```

❌ **INCORRECT**: `any` for uncertain types
```typescript
function processUserInput(input: any) {  // No type safety
  return input.toUpperCase();  // Runtime error if not string
}
```

### Strict Null Checks

Enable `strictNullChecks` in `tsconfig.json`:

✅ **CORRECT**: Handle nullish values
```typescript
function getName(user: User | undefined): string {
  if (!user) {
    return 'Guest';
  }
  return user.name;
}

// Or with optional chaining
function getName(user?: User): string {
  return user?.name ?? 'Guest';
}
```

❌ **INCORRECT**: Assuming non-null
```typescript
function getName(user: User | undefined): string {
  return user.name;  // Error: user might be undefined
}
```

## Interface vs Type

### When to Use Interface

**Prefer interfaces for**:
- Object shapes
- Extensible contracts
- Declaration merging

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

// Extensible
interface AdminUser extends User {
  permissions: string[];
}
```

### When to Use Type

**Prefer types for**:
- Unions
- Intersections
- Mapped types
- Primitive aliases
- Tuples

```typescript
type Status = 'pending' | 'approved' | 'rejected';

type Point = [number, number];

type RequiredKeys<T> = {
  [K in keyof T]-?: T[K]
};
```

## Function Types

### Parameter Types

Always type function parameters:

✅ **CORRECT**: Typed parameters
```typescript
function calculateTotal(
  items: Item[],
  taxRate: number,
  discount?: number
): number {
  // ...
}
```

❌ **INCORRECT**: Untyped parameters
```typescript
function calculateTotal(items, taxRate, discount) {  // Implicit any
  // ...
}
```

### Return Types

**Always specify return types for**:
- Public functions
- Exported functions
- Complex functions

✅ **CORRECT**: Explicit return type
```typescript
function fetchUser(id: string): Promise<User | null> {
  return fetch(`/api/users/${id}`)
    .then(r => r.json())
    .catch(() => null);
}
```

**Optional for**:
- Simple, obvious returns
- Private helpers
- Inline arrow functions

```typescript
// Return type obvious from implementation
const double = (n: number) => n * 2;
```

## Type Assertions

### Avoid Type Assertions

✅ **PREFERRED**: Type guards
```typescript
function processValue(value: unknown): string {
  if (typeof value === 'string') {
    return value.toUpperCase();
  }
  return String(value);
}
```

❌ **LESS SAFE**: Type assertion
```typescript
function processValue(value: unknown): string {
  return (value as string).toUpperCase();  // Unsafe!
}
```

### When Assertions Are Acceptable

**Use `as` assertions only when**:
- You have more information than TypeScript
- Working with DOM elements
- Type narrowing not possible

```typescript
const input = document.querySelector('#email') as HTMLInputElement;
const value = input.value;  // TypeScript now knows it's an input
```

**Never use double assertions** (indicates design problem):
```typescript
const value = data as unknown as SpecificType;  // ❌ Code smell
```

## Generics

### Use Generics for Reusability

✅ **CORRECT**: Generic type
```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

function fetchData<T>(url: string): Promise<ApiResponse<T>> {
  return fetch(url).then(r => r.json());
}

// Usage
const users = await fetchData<User[]>('/api/users');
```

### Constrain Generics

Use `extends` to constrain generic types:

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

interface User {
  id: string;
  name: string;
}

const user: User = { id: '1', name: 'Alice' };
const name = getProperty(user, 'name');  // ✅ OK
const invalid = getProperty(user, 'age');  // ❌ Error: 'age' not in User
```

### Default Generic Types

```typescript
interface Props<T = string> {
  value: T;
  onChange: (value: T) => void;
}

// Uses default
const stringProps: Props = {
  value: 'hello',
  onChange: (v) => console.log(v)
};

// Explicit type
const numberProps: Props<number> = {
  value: 42,
  onChange: (v) => console.log(v)
};
```

## Utility Types

### Use Built-in Utility Types

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

// Partial - all properties optional
type UserUpdate = Partial<User>;

// Pick - select specific properties
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit - exclude specific properties
type UserWithoutAge = Omit<User, 'age'>;

// Required - all properties required
type RequiredUser = Required<Partial<User>>;

// Readonly - all properties readonly
type ImmutableUser = Readonly<User>;

// Record - object with specific key/value types
type UserMap = Record<string, User>;
```

### Common Patterns

**Readonly arrays**:
```typescript
function processItems(items: readonly Item[]): void {
  // items.push(newItem);  // ❌ Error: readonly
  const copy = [...items];  // ✅ OK
}
```

**Extract/Exclude from unions**:
```typescript
type Status = 'pending' | 'approved' | 'rejected' | 'archived';

type ActiveStatus = Exclude<Status, 'archived'>;  // 'pending' | 'approved' | 'rejected'
type CompletedStatus = Extract<Status, 'approved' | 'rejected'>;  // 'approved' | 'rejected'
```

## Enums vs Union Types

### Prefer Union Types

✅ **PREFERRED**: Union type
```typescript
type Direction = 'north' | 'south' | 'east' | 'west';

function move(direction: Direction) {
  // ...
}

move('north');  // ✅ Works
move('invalid');  // ❌ Error
```

❌ **LESS PREFERRED**: Enum (adds runtime code)
```typescript
enum Direction {
  North = 'north',
  South = 'south',
  East = 'east',
  West = 'west'
}

function move(direction: Direction) {
  // ...
}

move(Direction.North);  // More verbose
```

**Use enums only when**:
- Need numeric values
- Need reverse mapping
- Interop with external systems requiring enums

## Type Narrowing

### Type Guards

```typescript
// Built-in type guards
function process(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase();  // TypeScript knows it's string
  }
  return value.toFixed(2);  // TypeScript knows it's number
}

// Custom type guard
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj
  );
}

function greetUser(data: unknown) {
  if (isUser(data)) {
    console.log(`Hello, ${data.name}`);  // TypeScript knows it's User
  }
}
```

### Discriminated Unions

```typescript
interface SuccessResult {
  success: true;
  data: User;
}

interface ErrorResult {
  success: false;
  error: string;
}

type Result = SuccessResult | ErrorResult;

function handleResult(result: Result) {
  if (result.success) {
    // TypeScript knows it's SuccessResult
    console.log(result.data.name);
  } else {
    // TypeScript knows it's ErrorResult
    console.log(result.error);
  }
}
```

## Array and Object Typing

### Array Types

```typescript
// Prefer this syntax
const numbers: number[] = [1, 2, 3];
const users: User[] = [];

// Less common (use for complex types)
const matrix: Array<Array<number>> = [[1, 2], [3, 4]];

// Readonly
const immutable: readonly number[] = [1, 2, 3];
// immutable.push(4);  // ❌ Error

// Tuples
const point: [number, number] = [10, 20];
const entry: [string, number] = ['age', 30];
```

### Object Types

```typescript
// Index signatures
interface StringMap {
  [key: string]: string;
}

// Record utility (preferred)
type StringMap = Record<string, string>;

// Optional properties
interface User {
  id: string;
  name: string;
  email?: string;  // Optional
}

// Readonly properties
interface Config {
  readonly apiKey: string;
  readonly endpoint: string;
}
```

## Async/Promise Typing

### Promise Return Types

```typescript
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// Error handling
async function fetchUserSafe(id: string): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${id}`);
    return response.json();
  } catch {
    return null;
  }
}
```

### Typing Promise Values

```typescript
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

type UserPromise = Promise<User>;
type ActualUser = UnwrapPromise<UserPromise>;  // User
```

## Type Imports

### Use `import type`

✅ **CORRECT**: Type-only import
```typescript
import type { User } from './types';
import type { CollectionEntry } from 'astro:content';
```

**Benefits**:
- No runtime code
- Clear intent
- Better tree-shaking

### Combined Imports

```typescript
import { getUser, type User } from './api';
```

## Configuration (tsconfig.json)

### Recommended Strict Settings

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

## Common Type Errors

### Index Signature Issues

❌ **INCORRECT**: Assuming key exists
```typescript
interface Config {
  [key: string]: string;
}

function getValue(config: Config, key: string): string {
  return config[key];  // Might be undefined!
}
```

✅ **CORRECT**: Handle undefined
```typescript
function getValue(config: Config, key: string): string | undefined {
  return config[key];
}

// Or with assertion after check
function getValue(config: Config, key: string): string {
  const value = config[key];
  if (!value) {
    throw new Error(`Missing key: ${key}`);
  }
  return value;
}
```

### Optional Chaining Misuse

✅ **CORRECT**: Intentional optional chaining
```typescript
const name = user?.profile?.name ?? 'Unknown';
```

❌ **CODE SMELL**: Hiding type errors
```typescript
// If this is needed, the types might be wrong
const data = response?.data?.items?.[0]?.value?.toString?.();
```

## Audit Checklist

### Type Safety (Priority 1)
- [ ] No `any` types (or justified with comment)
- [ ] Function parameters typed
- [ ] Public function return types specified
- [ ] No double type assertions

### Best Practices (Priority 2)
- [ ] Using `unknown` instead of `any`
- [ ] Type guards for narrowing
- [ ] Type-only imports (`import type`)
- [ ] Utility types where applicable

### Strictness (Priority 2)
- [ ] Null checks for potentially undefined
- [ ] No implicit any
- [ ] No unsafe assertions
- [ ] Interfaces for object shapes

### Code Quality (Priority 3)
- [ ] Union types preferred over enums
- [ ] Generic constraints where needed
- [ ] Discriminated unions for variants
- [ ] Descriptive type names
