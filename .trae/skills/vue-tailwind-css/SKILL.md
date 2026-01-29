---
name: "vue-tailwind-css"
description: "Generates Vue components with Tailwind CSS using a structured orchestration approach and specific formatting rules. Invoke when user asks for Vue component styling or creation."
---

# Vue Tailwind CSS Orchestrator

This skill guides the generation of Vue components styled with Tailwind CSS, emphasizing a top-down orchestration approach and strict formatting rules.

## Core Principles

1.  **Orchestrated Styling**:
    *   **Parent First**: When styling a component structure, define the parent component's layout (grids, flex containers) *before* implementing the child components.
    *   **Integration**: Ensure child components fit naturally into the pre-defined parent layout.

2.  **Tailwind Usage Strategy**:
    *   **Default to Inline**: For most elements, write styles directly in the HTML tags using Tailwind utility classes.
    *   **Complex/Repeated Styles**: If a specific style combination is complex and used repeatedly *within a single component*, define it in `<style scoped>` using a class selector.
    *   **`@apply` Syntax**: When using `<style>`, **ALWAYS** use `@apply` to maintain Tailwind consistency.
        *   **Requirement**: You MUST include `@reference 'tailwindcss';` or `@import 'tailwindcss';` at the top of the `<style>` block before using `@apply`.
        *   **Separate Lines**: Split `@apply` rules by category (Layout vs. Aesthetics).
        *   *Example*:
            ```css
            @reference 'tailwindcss';

            .ctl-panel {
                @apply w-full flex flex-col justify-between p-4; /* Layout */
                @apply bg-gray-800 rounded-lg shadow-xl border border-gray-700; /* Aesthetics */
            }
            ```

3.  **Global vs. Local Utilities**:
    *   **Check First**: Before writing new CSS, check if a global utility already exists.
    *   **Global (`style.css`)**: Use ONLY for generic utilities missing from Tailwind (e.g., `hide-scrollbar`, `text-stroke`). NEVER put component-specific logic (like `.ctl-panel`) here.
    *   **Local**: Component-specific utilities must remain in the component's `<style scoped>`.

4.  **Structured Formatting (Universal Rule)**:
    *   This rule applies to both **inline classes** and **`@apply` blocks**.
    *   **Line 1 (Layout)**: Width, Height, Positioning, Flexbox, Grid, Margin, Padding (layout-affecting).
    *   **Line 2+ (Aesthetics)**: Colors, Shadows, Borders, Typography, Backgrounds, Effects, Transitions.

    *Inline Example*:
    ```vue
    <div class="
      w-full h-64 flex items-center justify-center relative
      bg-white shadow-lg rounded-xl border border-gray-100 text-gray-800
    ">
      <!-- Content -->
    </div>
    ```

## Checklist

- [ ] **Orchestration**: Is the parent layout defined first?
- [ ] **Scoping**: Are component-specific styles kept local?
- [ ] **Global Check**: Did you check/use global utilities for generic features (e.g., scrollbar)?
- [ ] **Formatting**: Are classes (inline or `@apply`) split into Layout (Line 1) and Aesthetics (Line 2)?
- [ ] **Implementation**: Are complex repeated styles extracted to `@apply`, while simple ones remain inline?
- [ ] **Tailwind Reference**: If using `@apply`, is `@reference 'tailwindcss';` or `@import 'tailwindcss';` included in the `<style>` block?
