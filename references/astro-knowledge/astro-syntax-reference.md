# Astro Syntax Reference

**Source**: https://docs.astro.build/en/reference/astro-syntax/

This document provides the authoritative syntax rules for Astro components.

## Component Structure

### Required Structure

Every `.astro` file must have TWO sections separated by `---` code fences:

```astro
---
// SECTION 1: Component frontmatter (JavaScript/TypeScript)
const title = "Hello";
---

<!-- SECTION 2: Component template (HTML + JSX expressions) -->
<h1>{title}</h1>
```

✅ **CORRECT**: Two sections with code fence separator
❌ **INCORRECT**: Missing code fences, template before frontmatter, no clear separation

### Frontmatter Section (Code Fence)

**Purpose**: JavaScript/TypeScript code that runs at build time (server-side)

**Valid operations**:
- Import statements
- Variable declarations
- Data fetching with `await`
- Function definitions
- Type definitions

**Example**:
```astro
---
import Layout from '../layouts/Layout.astro';
import { getCollection } from 'astro:content';

const posts = await getCollection('blog');
const title = "My Blog";
---
```

### Template Section

**Purpose**: HTML markup with JSX-like expressions

**Key characteristics**:
- Must be below the code fence
- Multiple root elements allowed (no wrapper required)
- Supports JSX-like expressions in `{}`
- Uses HTML attribute names (kebab-case), NOT JSX (camelCase)

**Example**:
```astro
<div>{title}</div>
<p>Multiple root elements OK</p>
```

## Template Expressions

### Variable Interpolation

Use curly braces `{}` for dynamic values:

```astro
---
const name = "World";
const count = 42;
---

<h1>Hello {name}!</h1>
<p>Count: {count}</p>
```

### JavaScript Expressions

Full JavaScript expressions work inside `{}`:

```astro
---
const items = ['A', 'B', 'C'];
---

<ul>
  {items.map(item => <li>{item}</li>)}
</ul>

<p>{items.length > 0 ? 'Has items' : 'Empty'}</p>
```

### Dynamic Attributes

```astro
---
const className = "highlight";
const isDisabled = false;
---

<div class={className} data-active={!isDisabled}>
  Content
</div>
```

## HTML Attributes

### Attribute Naming Convention

✅ **CORRECT**: Use `kebab-case` (HTML standard)
```astro
<div class="box" data-value="3" aria-label="Info"></div>
```

❌ **INCORRECT**: Using `camelCase` (JSX convention)
```astro
<div className="box" dataValue="3" ariaLabel="Info"></div>
```

### Special Attributes

| HTML Attribute | Astro | JSX (React) |
|----------------|-------|-------------|
| CSS class | `class` | `className` |
| Data attributes | `data-value` | `dataValue` |
| ARIA attributes | `aria-label` | `ariaLabel` |
| For (label) | `for` | `htmlFor` |

**Key Rule**: Astro follows HTML standards, NOT JSX conventions

## Comments

### HTML Comments
```astro
<!-- HTML comment (visible in source) -->
```

### JavaScript Comments in Templates
```astro
{/* JavaScript comment (removed during build) */}
```

### Comments in Frontmatter
```astro
---
// Single-line comment
/* Multi-line
   comment */
---
```

## Dynamic Tags

### Component Tag Variables

Tag names must be **CAPITALIZED**:

✅ **CORRECT**:
```astro
---
const Element = 'div';
const Heading = 'h1';
---

<Element>Content</Element>
<Heading>Title</Heading>
```

❌ **INCORRECT**: Lowercase variables don't work
```astro
---
const element = 'div';  // Won't work as tag
---
<element>Content</element>  <!-- Renders as <element>, not <div> -->
```

### Restrictions

- ❌ Cannot use `client:*` directives with dynamic tags
- ❌ Cannot use `define:vars` with dynamic tags
- ✅ Can use regular HTML attributes

## Fragments

### Usage

Fragments allow grouping without adding wrapper elements:

**Short syntax**:
```astro
<>
  <h1>Title</h1>
  <p>Paragraph</p>
</>
```

**Named syntax**:
```astro
<Fragment>
  <h1>Title</h1>
  <p>Paragraph</p>
</Fragment>
```

### Use Cases

**With `set:*` directives** to avoid wrapper elements:
```astro
<Fragment set:html={htmlString} />
```

## Event Handlers

### Important Limitation

❌ **Event handlers DON'T work on HTML elements**:
```astro
<!-- This will NOT work -->
<button onClick={handleClick}>Click me</button>
```

**Why**: Astro components render to static HTML by default

**Solution**: Use framework components with `client:*` directives:
```astro
---
import Button from '../components/Button.jsx';  // React component
---

<Button onClick={handleClick} client:load />
```

Or use vanilla JavaScript:
```astro
<button id="myButton">Click me</button>

<script>
  document.getElementById('myButton').addEventListener('click', () => {
    console.log('Clicked!');
  });
</script>
```

## Props

### Accessing Props

All props are available via `Astro.props`:

```astro
---
const { title, description } = Astro.props;
---

<h1>{title}</h1>
<p>{description}</p>
```

### TypeScript Props

```astro
---
interface Props {
  title: string;
  description?: string;
  count?: number;
}

const { title, description = "Default", count = 0 } = Astro.props;
---
```

## Slots

### Default Slot

```astro
<slot />
```

### Named Slots

```astro
<header>
  <slot name="header" />
</header>

<main>
  <slot />  <!-- Default slot -->
</main>
```

### Checking Slots

```astro
---
const hasHeader = Astro.slots.has('header');
---

{hasHeader && (
  <header>
    <slot name="header" />
  </header>
)}
```

## Validation Checklist

When auditing Astro component syntax:

### Structure
- [ ] File has two sections separated by `---` code fences
- [ ] Frontmatter (code) comes first
- [ ] Template (HTML) comes second
- [ ] No code outside frontmatter section

### Attributes
- [ ] Using `class` not `className`
- [ ] Using `kebab-case` for HTML attributes
- [ ] Not using `camelCase` for standard HTML attributes

### Expressions
- [ ] Variables interpolated with `{}`
- [ ] No `await` in template section
- [ ] JavaScript expressions valid

### Dynamic Elements
- [ ] Dynamic tag variables are CAPITALIZED
- [ ] No `client:*` directives on dynamic tags
- [ ] No `define:vars` on dynamic tags

### Event Handlers
- [ ] No event handlers on static HTML elements
- [ ] Framework components have `client:*` directives if interactive
- [ ] Or using `<script>` for vanilla JavaScript events

### Props
- [ ] Props accessed via `Astro.props`
- [ ] Props interface defined (TypeScript)
- [ ] Default values provided where appropriate

## Common Violations

| Violation | Example | Fix |
|-----------|---------|-----|
| Missing code fence | Template at top of file | Add `---` fences |
| JSX attribute naming | `className="box"` | Use `class="box"` |
| Event on HTML | `<button onClick={fn}>` | Use React component with `client:load` |
| Lowercase dynamic tag | `const div = 'div'` | Use `const Div = 'div'` |
| Await in template | `{await getData()}` | Move to frontmatter |
| No props interface | `const {x} = Astro.props` | Add `interface Props` |
