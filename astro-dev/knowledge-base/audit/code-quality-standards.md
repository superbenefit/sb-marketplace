# Code Quality Standards for Web Development

This document defines general code quality standards for web development projects, independent of Astro-specific rules.

## Accessibility (a11y)

### Semantic HTML

✅ **CORRECT**: Use appropriate HTML elements
```html
<nav>
  <ul>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Title</h1>
    <p>Content</p>
  </article>
</main>

<footer>
  <p>&copy; 2024 Company</p>
</footer>
```

❌ **INCORRECT**: Divs for everything
```html
<div class="nav">
  <div class="link"><div onclick="navigate()">About</div></div>
</div>

<div class="main">
  <div class="title">Title</div>
  <div class="text">Content</div>
</div>
```

### ARIA Attributes

**When to use**:
- Only when semantic HTML isn't sufficient
- To enhance existing semantics
- For custom interactive widgets

✅ **CORRECT**: Semantic HTML first
```html
<button>Click me</button>  <!-- No ARIA needed -->
```

✅ **CORRECT**: ARIA when needed
```html
<div role="button" tabindex="0" aria-pressed="false">
  Custom button
</div>
```

❌ **INCORRECT**: Redundant ARIA
```html
<button role="button" aria-label="Click me">Click me</button>
<!-- role="button" is redundant -->
```

### Required ARIA Patterns

**Interactive elements**:
- [ ] `tabindex` for keyboard navigation
- [ ] `role` for custom widgets
- [ ] `aria-label` or `aria-labelledby` for screen readers
- [ ] `aria-expanded` for expandable sections
- [ ] `aria-hidden` for decorative elements

**Form elements**:
- [ ] `<label>` associated with inputs
- [ ] `aria-required` for required fields
- [ ] `aria-invalid` and `aria-describedby` for errors

**Images**:
- [ ] `alt` attribute (empty for decorative)
- [ ] Meaningful alt text describing image content

### Keyboard Navigation

All interactive elements must be:
- [ ] Focusable (`tabindex="0"` or native)
- [ ] Operable with keyboard (Enter/Space for activation)
- [ ] Visible focus indicator (`:focus` styles)

✅ **CORRECT**: Keyboard accessible
```html
<button onclick="action()">Click</button>  <!-- Native keyboard support -->

<div
  role="button"
  tabindex="0"
  onkeydown="if(event.key === 'Enter') action()"
>
  Custom button
</div>
```

❌ **INCORRECT**: Not keyboard accessible
```html
<div onclick="action()">Click</div>  <!-- No keyboard support -->
```

### Color Contrast

**WCAG AA Requirements**:
- Normal text: 4.5:1 contrast ratio
- Large text (18pt+ or 14pt+ bold): 3:1
- UI components: 3:1

**Validation**:
- [ ] Sufficient contrast for text
- [ ] Don't rely on color alone for meaning
- [ ] Provide text labels with color indicators

## Performance

### Bundle Size

**Best practices**:
- [ ] Import only what you need (avoid whole libraries)
- [ ] Use tree-shakeable imports
- [ ] Lazy load non-critical resources
- [ ] Code split by route

✅ **CORRECT**: Specific imports
```typescript
import debounce from 'lodash/debounce';  // ~2KB
```

❌ **INCORRECT**: Entire library
```typescript
import _ from 'lodash';  // ~70KB!
```

### Image Optimization

**Requirements**:
- [ ] Use modern formats (WebP, AVIF)
- [ ] Provide width/height to prevent layout shift
- [ ] Lazy load below-the-fold images
- [ ] Use responsive images (`srcset`)
- [ ] Compress images appropriately

✅ **CORRECT**: Optimized image
```html
<img
  src="photo.webp"
  alt="Description"
  width="800"
  height="600"
  loading="lazy"
/>
```

❌ **INCORRECT**: Unoptimized
```html
<img src="photo.png" />  <!-- No dimensions, not lazy, PNG instead of WebP -->
```

### Critical Rendering Path

**Optimization**:
- [ ] Inline critical CSS
- [ ] Defer non-critical JavaScript
- [ ] Minimize render-blocking resources
- [ ] Optimize font loading

**Loading strategy**:
- Critical resources: Load immediately
- Above-the-fold: High priority
- Below-the-fold: Lazy load
- Analytics/tracking: Defer to idle time

## Security

### XSS Prevention

**Rules**:
- [ ] Never use raw HTML from user input
- [ ] Always escape user-generated content
- [ ] Use `textContent` not `innerHTML` for dynamic text
- [ ] Sanitize HTML if absolutely necessary

❌ **CRITICAL ERROR**: XSS vulnerability
```javascript
// NEVER do this with user input!
element.innerHTML = userInput;
document.write(userData);
eval(userCode);
```

✅ **CORRECT**: Safe text insertion
```javascript
element.textContent = userInput;  // Auto-escaped
```

### Secrets Management

**Requirements**:
- [ ] No secrets in client-side code
- [ ] No API keys in source code
- [ ] Use environment variables for secrets
- [ ] Server-side only for sensitive operations

❌ **CRITICAL ERROR**: Exposed secret
```javascript
const apiKey = 'sk_live_abc123...';  // ❌ Hard-coded secret
```

✅ **CORRECT**: Environment variable
```javascript
const apiKey = import.meta.env.SECRET_API_KEY;  // Server-side only
```

### Input Validation

**Requirements**:
- [ ] Validate all user input
- [ ] Sanitize before use
- [ ] Type check dynamic data
- [ ] Limit input length
- [ ] Whitelist allowed values

```typescript
// Validate before use
function processAge(input: string) {
  const age = parseInt(input, 10);

  if (isNaN(age) || age < 0 || age > 150) {
    throw new Error('Invalid age');
  }

  return age;
}
```

## Code Organization

### Function Size

**Best practices**:
- [ ] Keep functions focused (single responsibility)
- [ ] Limit function length (~50 lines max)
- [ ] Extract complex logic into helpers
- [ ] Name functions descriptively

✅ **CORRECT**: Focused functions
```typescript
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function processUserRegistration(data: FormData) {
  const email = data.get('email');
  if (!validateEmail(email)) {
    throw new Error('Invalid email');
  }
  // ...
}
```

### Variable Naming

**Conventions**:
- [ ] Use descriptive names (`userData` not `d`)
- [ ] Boolean prefixes: `is`, `has`, `should`, `can`
- [ ] Constants: `UPPER_SNAKE_CASE`
- [ ] Functions/variables: `camelCase`
- [ ] Classes/Types: `PascalCase`

✅ **CORRECT**: Descriptive names
```typescript
const isUserLoggedIn = checkAuthStatus();
const MAX_RETRY_ATTEMPTS = 3;
const userData = await fetchUser();
```

❌ **INCORRECT**: Unclear names
```typescript
const x = check();
const m = 3;
const d = await fetch();
```

### Comments

**When to comment**:
- [ ] Complex algorithms explaining "why"
- [ ] Non-obvious business logic
- [ ] Workarounds for bugs
- [ ] Public API documentation

**Don't comment**:
- ❌ Obvious code (comment should add information)
- ❌ Redundant information already in code
- ❌ Commented-out code (use version control)

✅ **CORRECT**: Adds information
```typescript
// Use exponential backoff to avoid overwhelming the API
// after network failures (max 5 retries)
async function fetchWithRetry(url: string) { ... }
```

❌ **INCORRECT**: Redundant
```typescript
// Increment counter
counter++;
```

## Error Handling

### Graceful Degradation

**Requirements**:
- [ ] Catch and handle errors appropriately
- [ ] Provide user-friendly error messages
- [ ] Log errors for debugging
- [ ] Don't crash the entire app for one error

✅ **CORRECT**: Graceful handling
```typescript
async function loadUserData() {
  try {
    const data = await fetch('/api/user');
    return await data.json();
  } catch (error) {
    console.error('Failed to load user data:', error);
    return null;  // Graceful fallback
  }
}
```

### User-Facing Errors

**Best practices**:
- [ ] Clear, actionable messages
- [ ] Don't expose technical details to users
- [ ] Provide next steps or solutions
- [ ] Log technical details server-side

✅ **CORRECT**: User-friendly
```typescript
{error ? (
  <div role="alert">
    Failed to load content. Please try again or contact support.
  </div>
) : (
  <Content />
)}
```

❌ **INCORRECT**: Technical error exposed
```typescript
<div>{error.stack}</div>  // Never show stack traces to users
```

## CSS Best Practices

### Scoping

**Prefer**:
- [ ] Component-scoped styles
- [ ] CSS modules
- [ ] Utility classes (Tailwind)

**Avoid**:
- ❌ Global styles for component-specific styling
- ❌ `!important` (indicates specificity issues)
- ❌ Inline styles (hard to maintain)

### Performance

**Best practices**:
- [ ] Minimize CSS file size
- [ ] Avoid deep nesting (max 3-4 levels)
- [ ] Use efficient selectors
- [ ] Remove unused CSS

✅ **CORRECT**: Efficient selector
```css
.card-title { color: blue; }
```

❌ **INCORRECT**: Over-specific
```css
div.container div.row div.col div.card h1.title { color: blue; }
```

### Responsive Design

**Requirements**:
- [ ] Mobile-first approach
- [ ] Use relative units (`rem`, `%`, `vw`)
- [ ] Test at multiple breakpoints
- [ ] Consider touch targets (44x44px minimum)

```css
/* Mobile first */
.button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

/* Desktop enhancement */
@media (min-width: 768px) {
  .button {
    padding: 0.75rem 1.5rem;
    font-size: 1.125rem;
  }
}
```

## Testing Considerations

### Testability

**Write testable code**:
- [ ] Pure functions when possible
- [ ] Dependency injection
- [ ] Avoid tight coupling
- [ ] Separate logic from presentation

✅ **CORRECT**: Testable
```typescript
function calculateTotal(items: Item[], taxRate: number): number {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal * (1 + taxRate);
}

// Easy to test - no side effects
```

❌ **INCORRECT**: Hard to test
```typescript
function processOrder() {
  const items = document.querySelectorAll('.item');  // DOM dependent
  const rate = window.TAX_RATE;  // Global dependent
  // ... hard to test
}
```

## Documentation

### Code Documentation

**Required for**:
- [ ] Public APIs
- [ ] Complex functions
- [ ] Non-obvious behavior
- [ ] Configuration options

**JSDoc format**:
```typescript
/**
 * Fetches user data from the API
 * @param userId - The unique identifier for the user
 * @returns User object or null if not found
 * @throws {ApiError} If the API request fails
 */
async function fetchUser(userId: string): Promise<User | null> {
  // ...
}
```

## Audit Checklist

### Accessibility (Priority 1)
- [ ] Semantic HTML elements
- [ ] Alt text for images
- [ ] ARIA labels for interactive elements
- [ ] Keyboard navigation works
- [ ] Sufficient color contrast
- [ ] Form labels associated

### Security (Priority 1)
- [ ] No XSS vulnerabilities
- [ ] No exposed secrets
- [ ] Input validation
- [ ] Safe HTML handling

### Performance (Priority 2)
- [ ] Optimized images
- [ ] Efficient imports
- [ ] Lazy loading
- [ ] No unnecessary re-renders

### Code Quality (Priority 2)
- [ ] Descriptive naming
- [ ] Appropriate function size
- [ ] Error handling
- [ ] No commented-out code

### CSS (Priority 3)
- [ ] Scoped styles
- [ ] Efficient selectors
- [ ] Responsive design
- [ ] No `!important` abuse
