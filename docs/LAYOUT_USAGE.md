# Layout System (Nested Router Approach)

This document explains how layouts are organized using Vue Router's nested routes. Each layout is a parent route that wraps its child routes.

## Available Layouts

### 1. PostAuth Layout (`/app/*`)

- **Path Prefix**: `/app/`
- **Component**: `PostAuth.vue`
- **Includes**: Sidebar navigation, breadcrumbs, header with user controls
- **Use for**: Main dashboard, settings, user management, etc.
- **Authentication**: Protected with `authGuard`

### 2. PreAuth Layout (`/`)

- **Path Prefix**: `/`
- **Component**: `PreAuth.vue`
- **Includes**: Simple header with login button
- **Use for**: Landing pages, marketing pages, public documentation
- **Authentication**: Public access

### 3. Minimal Layout (`/minimal/*`)

- **Path Prefix**: `/minimal/`
- **Component**: `Minimal.vue`
- **Includes**: Just the page content, no header or navigation
- **Use for**: Error pages, full-screen experiences, focused tasks

## Route Structure

### PostAuth Routes (Authenticated)

```
/app/
├── /app (redirects to /app/home)
├── /app/home (dashboard)
├── /app/settings (user settings)
├── /app/breadcrumb-examples (examples)
└── /app/users/:id (user detail)
```

### PreAuth Routes (Public)

```
/
└── / (landing page)
```

### Minimal Routes

```
/minimal/
├── /minimal/about (about page)
└── /minimal/404 (not found)
```

## How to Add New Routes

### Adding a PostAuth Route (With Navigation)

Add to the `postauth-layout` children array:

```typescript
{
  path: '/app',
  name: 'postauth-layout',
  component: () => import('@/layout/PostAuth.vue'),
  beforeEnter: authGuard,
  children: [
    // Add your new route here
    {
      path: 'your-new-page',
      name: 'your-new-page',
      component: () => import('@/views/YourView.vue'),
      meta: {
        breadcrumbs: [
          { title: 'Home', to: { name: 'home' } },
          { title: 'Your New Page' }
        ],
      },
    },
```

### Adding a PreAuth Route (Public)

Add to the `preauth-layout` children array:

````typescript
{
  path: '/',
  name: 'preauth-layout',
  component: () => import('@/layout/PreAuth.vue'),
  children: [
    {
      path: 'your-public-page',
      name: 'your-public-page',
      component: () => import('@/views/YourPublicPageView.vue'),
    },
  ]

### Adding a Minimal Route (Clean Layout)

Add to the `minimal-layout` children array:

```typescript
{: '/minimal',
  name: 'minimal-layout',
  component: () => import('@/layout/Minimal.vue'),
  children: [
    {
      path: 'your-clean-page',
      name: 'your-clean-page',
      component: () => import('@/views/YourCleanPageView.vue'),
    },
  ]

## Benefits of Nested Approach

1. **Cleaner App.vue**: No layout logic in the main App component
2. **Explicit URLs**: Layout is reflected in the URL structure
3. **Better SEO**: Clear URL hierarchy
4. r Navigation**: Users can understand where they are by the URL
5. **Layout Isolation**: Each layout is self-contained with its own children

## URL Examples

- `/` - Landing page (PreAuth layout)
- `/app/home` - Dashboard (PostAuth layout)
- `/app/settings` - Settings (PostAuth layout)
- `/minimal/about` - About page (Minimal layout)
- `/minimal/404` - Not found (Minimal layout)

## Navigation Between Layouts

To navigate from one layout to another:

```typescript
// From landing page to dashboard
router.push({ name: 'home' }) // Goes to /app/home

// From dashboard to about page
router.push({ name: 'about' }) // Goes to /minimal/about

// From any page back to landing
router.push({ name: 'landing' }) // Goes to /
````

This approach provides a clean, maintainable layout system where the URL structure reflects the layout hierarchy.
