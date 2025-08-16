# Dialog System

A global dialog system for Vue applications using Shadcn-vue components with internationalization support.

## Features

- ✅ Global dialog state management with Pinia store
- ✅ Multiple dialog types: confirm, alert, info
- ✅ Customizable icons, text, and variants
- ✅ Internationalization support
- ✅ Promise-based API for easy handling
- ✅ TypeScript support
- ✅ Accessible design with Shadcn-vue components

## Quick Start

### Basic Usage

```typescript
import { useDialog } from '@/composables/useDialog'

const dialog = useDialog()

// Simple confirmation
const confirmed = await dialog.confirm('Are you sure?')
if (confirmed) {
  // User confirmed
}

// Simple alert
await dialog.alert('Operation completed successfully!')

// Info message
await dialog.info('This is some useful information.')
```

### Advanced Usage

```typescript
// Custom confirmation dialog
const confirmed = await dialog.confirm({
  title: 'Delete Item',
  text: 'This action cannot be undone. Are you sure?',
  confirmText: 'Delete',
  cancelText: 'Keep',
  confirmIcon: 'alert-triangle',
  variant: 'destructive'
})

// Destructive confirmation (shorthand)
const confirmed = await dialog.confirmDestructive({
  text: 'Delete all files?',
  confirmText: 'Delete All'
})
```

## API Reference

### useDialog()

Returns an object with the following methods:

#### `confirm(config: DialogConfig | string): Promise<boolean>`

Shows a confirmation dialog with confirm and cancel buttons.

**Parameters:**
- `config`: Dialog configuration object or simple text string
- Returns: `Promise<boolean>` - `true` if confirmed, `false` if cancelled

#### `alert(config: DialogConfig | string): Promise<void>`

Shows an alert dialog with only an OK button.

**Parameters:**
- `config`: Dialog configuration object or simple text string
- Returns: `Promise<void>` - Resolves when dialog is closed

#### `info(config: DialogConfig | string): Promise<void>`

Shows an info dialog with only an OK button and info styling.

**Parameters:**
- `config`: Dialog configuration object or simple text string
- Returns: `Promise<void>` - Resolves when dialog is closed

#### `confirmDestructive(config: DialogConfig | string): Promise<boolean>`

Shows a destructive confirmation dialog (red styling for dangerous actions).

**Parameters:**
- `config`: Dialog configuration object or simple text string
- Returns: `Promise<boolean>` - `true` if confirmed, `false` if cancelled

#### `close(): void`

Programmatically close the current dialog.

### DialogConfig Interface

```typescript
interface DialogConfig {
  title?: string           // Dialog title (uses i18n default if not provided)
  text: string            // Main dialog message (required)
  confirmText?: string    // Confirm button text (uses i18n default if not provided)
  cancelText?: string     // Cancel button text (uses i18n default if not provided)
  confirmIcon?: string    // Icon name for confirm button
  cancelIcon?: string     // Icon name for cancel button
  type?: 'confirm' | 'alert' | 'info'  // Dialog type
  variant?: 'default' | 'destructive' | 'secondary'  // Button variant
}
```

### Available Icons

The dialog system supports the following icon names:
- `check` - Check mark icon
- `x` - X/close icon
- `alert-triangle` - Warning triangle
- `info` - Information icon
- `alert-circle` - Alert circle

## Internationalization

The dialog system automatically uses translations from the i18n system. Default translations are provided in:

- `common.dialog.confirm.*` - Confirmation dialog defaults
- `common.dialog.alert.*` - Alert dialog defaults
- `common.dialog.info.*` - Info dialog defaults

### Custom Translations

You can override default text by providing custom `title`, `confirmText`, or `cancelText` in the config:

```typescript
await dialog.confirm({
  title: 'Custom Title',
  text: 'Custom message',
  confirmText: 'Yes, Do It',
  cancelText: 'No, Cancel'
})
```

## Examples

See `/app/dialog-examples` for interactive examples of all dialog types and configurations.

## Architecture

The dialog system consists of:

1. **Dialog Store** (`@/stores/dialog.ts`) - Pinia store managing global dialog state
2. **Global Dialog Component** (`@/components/GlobalDialog.vue`) - The actual dialog UI component
3. **Dialog Composable** (`@/composables/useDialog.ts`) - Easy-to-use API wrapper
4. **App Integration** - GlobalDialog component is registered in `App.vue`

The GlobalDialog component is automatically included in your app and listens to the dialog store state changes.
