# Astro Directives Reference

**Source**: https://docs.astro.build/en/reference/directives-reference/

This document provides authoritative rules for all Astro directives.

## Directive Format

### Structure

All template directives follow the format `X:Y`:

```astro
<Component client:load />
<style is:global />
<div class:list={classes} />
```

### Visibility Requirement

Directives MUST be visible to the compiler:

✅ **CORRECT**: Direct attribute
```astro
<Component client:load />
```

❌ **INCORRECT**: Hidden in spread
```astro
<Component {...{['client:load']: true}} />
```

### Output Behavior

Directives are **never included in final HTML output** - they're compiler instructions only.

## Client Directives

Purpose: Control hydration of framework components (React, Vue, Svelte, etc.)

### `client:load`

**Hydrates**: Immediately on page load (highest priority)

**Syntax**: No value required
```astro
<InteractiveWidget client:load />
```

**When to use**:
- Component must be interactive immediately
- Above-the-fold critical interactions
- User expects instant interactivity

**Validation**:
- [ ] No value provided
- [ ] Component is a framework component (React/Vue/Svelte)
- [ ] Interactivity is truly needed immediately

### `client:idle`

**Hydrates**: When browser becomes idle (uses `requestIdleCallback`)

**Syntax**: Optional timeout in milliseconds
```astro
<ChatWidget client:idle />
<Sidebar client:idle={{timeout: 500}} />
```

**When to use**:
- Important but not immediately critical
- Non-blocking UI elements
- Medium-priority interactions

**Validation**:
- [ ] Value is optional
- [ ] If provided, timeout is a number
- [ ] Component doesn't need instant interactivity

### `client:visible`

**Hydrates**: When component enters viewport (uses `IntersectionObserver`)

**Syntax**: Optional rootMargin
```astro
<HeavyCarousel client:visible />
<Chart client:visible={{rootMargin: "200px"}} />
```

**When to use**:
- Below-the-fold components
- Heavy/expensive components
- Lazy-loaded sections

**Validation**:
- [ ] Value is optional
- [ ] If provided, rootMargin is a valid CSS value
- [ ] Component is actually below fold or in hidden section

### `client:media`

**Hydrates**: When media query matches

**Syntax**: Media query string (REQUIRED)
```astro
<MobileMenu client:media="(max-width: 768px)" />
<DesktopNav client:media="(min-width: 769px)" />
```

**When to use**:
- Components only needed at specific screen sizes
- Mobile-only or desktop-only features
- Responsive behavior optimization

**Validation**:
- [ ] Media query value is PROVIDED (required!)
- [ ] Media query is a valid CSS media query
- [ ] Component truly only needed for that media query

❌ **COMMON ERROR**: Missing media query value
```astro
<MobileMenu client:media />  <!-- ERROR: Missing required value -->
```

### `client:only`

**Hydrates**: Client-only (NO server rendering)

**Syntax**: Framework hint (REQUIRED)
```astro
<ClientOnlyWidget client:only="react" />
<BrowserAPI client:only="vue" />
```

**Valid framework values**:
- `"react"`
- `"preact"`
- `"vue"`
- `"svelte"`
- `"solid-js"`

**When to use**:
- Component uses browser-only APIs (window, document)
- Component breaks during SSR
- Third-party widgets requiring browser environment

**Validation**:
- [ ] Framework hint is PROVIDED (required!)
- [ ] Framework is one of the valid values
- [ ] Component truly needs client-only rendering

❌ **COMMON ERROR**: Missing framework hint
```astro
<BrowserWidget client:only />  <!-- ERROR: Missing required framework -->
```

## Script & Style Directives

### `is:global` (style only)

**Purpose**: Apply styles globally (disable scoping)

**Syntax**: No value
```astro
<style is:global>
  body a { color: red; }
</style>
```

**Equivalent to**:
```astro
<style>
  :global(body a) { color: red; }
</style>
```

**Validation**:
- [ ] Used only on `<style>` tags
- [ ] No value provided
- [ ] Intentional global styling (not accidental)

### `is:inline` (script & style)

**Purpose**: Skip processing, bundling, and optimization

**Script behavior**:
- NOT bundled
- NOT deduplicated (runs every time component is used)
- Imports DON'T work
- Rendered exactly as written

**Style behavior**:
- NOT processed
- NOT optimized
- NOT bundled

```astro
<!-- Script: NOT bundled, runs multiple times -->
<script is:inline>
  console.log('Inline script');
  // ❌ import statements won't work here
</script>

<!-- Style: NOT processed -->
<style is:inline>
  .box { color: red; }
</style>

<!-- External with is:inline -->
<script is:inline src="https://cdn.example.com/script.js"></script>
```

**Validation**:
- [ ] No import statements in `is:inline` scripts
- [ ] Aware of duplication behavior (script runs per component instance)
- [ ] External CDN scripts use `is:inline`

❌ **COMMON ERROR**: Imports in inline scripts
```astro
<script is:inline>
  import { helper } from './utils';  // WON'T WORK!
</script>
```

### `define:vars` (script & style)

**Purpose**: Pass server-side variables to client-side code

**Syntax**: Object with variables
```astro
---
const color = 'red';
const size = 16;
---

<style define:vars={{color, size}}>
  h1 {
    color: var(--color);
    font-size: calc(var(--size) * 1px);
  }
</style>

<script define:vars={{color}}>
  console.log(color);  // Accessible in script
</script>
```

**Important**: `define:vars` on `<script>` implies `is:inline`

**Validation**:
- [ ] Value is an object
- [ ] Variables are serializable (no functions, no complex objects)
- [ ] When on script, aware it becomes `is:inline` (no imports!)
- [ ] Using CSS var syntax in styles: `var(--varName)`

## Common Directives

### `class:list`

**Purpose**: Build class strings from arrays/objects

**Syntax**: Array, object, or nested combination
```astro
---
const isActive = true;
const type = 'primary';
---

<!-- Array -->
<div class:list={['base', type, {active: isActive}]} />
<!-- Result: class="base primary active" -->

<!-- Object -->
<div class:list={{active: isActive, hidden: false}} />
<!-- Result: class="active" -->

<!-- Mixed -->
<div class:list={['base', {active: isActive}, ['extra', 'classes']]} />
```

**Validation**:
- [ ] Value is array, object, or nested combination
- [ ] NOT a plain string
- [ ] Object values are booleans

❌ **COMMON ERROR**: Passing string instead of array/object
```astro
<div class:list="base active" />  <!-- WRONG: Must be array/object -->
```

### `set:html`

**Purpose**: Inject raw HTML (like `dangerouslySetInnerHTML`)

**Syntax**: HTML string
```astro
---
const rawHTML = '<p>HTML content</p>';
---

<Fragment set:html={rawHTML} />
```

**⚠️ XSS RISK**: Never use with user input!

**Validation**:
- [ ] HTML is from trusted source only
- [ ] NOT user-generated content
- [ ] Consider using `set:text` for user input instead

### `set:text`

**Purpose**: Inject text (escaped for safety)

**Syntax**: Text string
```astro
---
const userInput = '<script>alert("xss")</script>';
---

<p set:text={userInput} />
<!-- Safe: Renders as literal text, not HTML -->
```

**Validation**:
- [ ] Used for user-generated content
- [ ] Preferred over `set:html` when injecting dynamic text

## Server Directives

### `server:defer`

**Purpose**: Render component on-demand, outside page scope

**Syntax**: No value
```astro
<HeavyComponent server:defer />
```

**Use cases**:
- Components that slow down initial render
- Non-critical content

**Validation**:
- [ ] Component is truly non-critical for initial page load
- [ ] No value provided

## View Transition Directives

### `transition:name`

**Purpose**: Name element pairs for view transition animations

**Syntax**: Unique string identifier
```astro
<header transition:name="main-header" />
<img transition:name="hero-image" src={image} />
```

**Validation**:
- [ ] Name is unique per page
- [ ] Same name used on corresponding element on target page
- [ ] NOT duplicate names on same page

❌ **COMMON ERROR**: Duplicate transition names
```astro
<div transition:name="header" />
<div transition:name="header" />  <!-- ERROR: Duplicate! -->
```

### `transition:animate`

**Purpose**: Control animation type

**Syntax**: Animation type string
```astro
<div transition:animate="fade" />
<div transition:animate="slide" />
<div transition:animate="initial" />
<div transition:animate="none" />
```

**Valid values**:
- `"fade"` - Fade in/out
- `"slide"` - Slide animation
- `"initial"` - Previously called "morph" (renamed in v3)
- `"none"` - No animation

**Special case**: Disable all default transitions
```astro
<html transition:animate="none">
```

**Validation**:
- [ ] Value is one of the valid animation types
- [ ] NOT using deprecated `"morph"` (use `"initial"`)

❌ **COMMON ERROR**: Using deprecated animation name
```astro
<div transition:animate="morph" />  <!-- DEPRECATED: Use "initial" -->
```

### `transition:persist`

**Purpose**: Persist component state across navigation

**Syntax**: No value
```astro
<VideoPlayer transition:persist />
<audio transition:persist src={audioFile} />
```

**Use cases**:
- Media players that should keep playing
- Form state preservation
- Interactive widgets that maintain state

**Validation**:
- [ ] Component truly needs state persistence
- [ ] No value provided

## Directive Validation Checklist

### Formatting
- [ ] Directive follows `X:Y` format
- [ ] Directive visible (not in spread attributes)
- [ ] Directive only in `.astro` files (limited MDX support)

### Client Directives
- [ ] `client:media` has required media query value
- [ ] `client:only` has required framework hint
- [ ] Only one client directive per component
- [ ] Framework component actually needs hydration

### Script/Style Directives
- [ ] No imports in `is:inline` scripts
- [ ] `define:vars` values are serializable
- [ ] Aware `define:vars` on script implies `is:inline`
- [ ] External CDN scripts use `is:inline`

### Security
- [ ] `set:html` only with trusted content
- [ ] User input uses `set:text`, NOT `set:html`

### View Transitions
- [ ] `transition:name` values are unique
- [ ] Using `"initial"` not deprecated `"morph"`

## Common Directive Errors

| Error | Example | Fix |
|-------|---------|-----|
| Missing required value | `client:media` | `client:media="(max-width: 768px)"` |
| Missing framework hint | `client:only` | `client:only="react"` |
| Imports in inline | `<script is:inline>import x</script>` | Remove `is:inline` or remove import |
| String for class:list | `class:list="classes"` | `class:list={['classes']}` |
| Duplicate transition names | Two elements with same `transition:name` | Use unique names |
| Hidden in spread | `<X {...{'client:load': true}} />` | `<X client:load />` |
| Deprecated animation | `transition:animate="morph"` | `transition:animate="initial"` |
| XSS with set:html | `set:html={userInput}` | `set:text={userInput}` |

## Directive Compatibility

### By Element Type

| Directive | Astro Components | Framework Components | HTML Elements | script/style |
|-----------|-----------------|---------------------|---------------|--------------|
| `client:*` | ✅ (if wrapping framework) | ✅ | ❌ | ❌ |
| `is:global` | ❌ | ❌ | ❌ | ✅ (style only) |
| `is:inline` | ❌ | ❌ | ❌ | ✅ (script/style) |
| `define:vars` | ❌ | ❌ | ❌ | ✅ (script/style) |
| `class:list` | ✅ | ✅ | ✅ | ❌ |
| `set:html` | ✅ | ✅ | ✅ | ❌ |
| `set:text` | ✅ | ✅ | ✅ | ❌ |
| `transition:*` | ✅ | ✅ | ✅ | ❌ |
