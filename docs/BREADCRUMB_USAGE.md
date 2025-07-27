# Dynamic Breadcrumb System (Store-based)

This project includes a flexible dynamic breadcrumb system using Pinia store that automatically updates breadcrumbs based on route changes and allows manual overrides from components.

## 🚀 Features

-   **Automatic route-based breadcrumbs**: Automatically generates breadcrumbs from route meta or route path
-   **Dynamic breadcrumbs**: Override breadcrumbs from components using the store
-   **Parameter-based breadcrumbs**: Create breadcrumbs based on route parameters and data
-   **Additive breadcrumbs**: Add breadcrumb items to existing ones
-   **Reactive updates**: Breadcrumbs automatically update when route changes or data changes
-   **Router integration**: Breadcrumb store automatically updates on route navigation

## 🏗️ Architecture

The system consists of:

-   **Pinia Store** (`stores/breadcrumb.ts`): Manages breadcrumb state reactively
-   **Router Plugin** (`plugins/breadcrumb.ts`): Automatically updates store on route changes
-   **Layout Integration** (`PostAuth.vue`): Renders breadcrumbs from store

## 📖 Usage

### 1. Automatic Route-based Breadcrumbs

**Route Meta Breadcrumbs** - Define static breadcrumbs in your route configuration:

```typescript
// router/index.ts
{
  path: '/settings',
  name: 'settings',
  component: () => import('../views/UserSettingsView.vue'),
  meta: {
    breadcrumbs: [
      { title: 'Home', to: '/' },
      { title: 'Settings' }
    ]
  }
}
```

**Auto-generated from Path** - When no route meta is provided, breadcrumbs are automatically generated from the route path:

-   `/users/profile` → Home > Users > Profile

### 2. Component-based Dynamic Breadcrumbs

Override breadcrumbs from within your Vue components using the store:

```vue
<script setup lang="ts">
import { useBreadcrumbStore } from "@/stores/breadcrumb";

const breadcrumbStore = useBreadcrumbStore();

// Set breadcrumbs when component mounts
breadcrumbStore.setBreadcrumbs([
    { title: "Home", to: "/" },
    { title: "Custom Page" },
]);
</script>
```

### 3. Data-driven Dynamic Breadcrumbs

Create breadcrumbs based on fetched data:

```vue
<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useBreadcrumbStore } from "@/stores/breadcrumb";

const route = useRoute();
const breadcrumbStore = useBreadcrumbStore();
const user = ref(null);

const loadUser = async () => {
    // Fetch user data
    const userData = await fetchUser(route.params.id);
    user.value = userData;

    // Update breadcrumbs with user name
    breadcrumbStore.setBreadcrumbs([
        { title: "Home", to: "/" },
        { title: "Users", to: "/users" },
        { title: userData.name },
    ]);
};

watch(() => route.params.id, loadUser, { immediate: true });
</script>
```

### 4. Adding Breadcrumb Items

Add additional breadcrumb items to existing ones:

```vue
<script setup lang="ts">
const breadcrumbStore = useBreadcrumbStore();

const navigateToSubSection = (sectionName: string) => {
    breadcrumbStore.addBreadcrumb({ title: sectionName });
};
</script>
```

### 5. Resetting Breadcrumbs

Clear dynamic breadcrumbs to fall back to route meta or auto-generated:

```vue
<script setup lang="ts">
const breadcrumbStore = useBreadcrumbStore();

const resetToDefault = () => {
    breadcrumbStore.clearBreadcrumbs(); // Will show route meta or auto-generated breadcrumbs
};
</script>
```

## 🔧 Store API

```typescript
// Available store methods
const breadcrumbStore = useBreadcrumbStore()

breadcrumbStore.setBreadcrumbs(items: BreadcrumbItem[])    // Set complete breadcrumb array
breadcrumbStore.clearBreadcrumbs()                        // Clear dynamic breadcrumbs
breadcrumbStore.addBreadcrumb(item: BreadcrumbItem)       // Add single breadcrumb item
breadcrumbStore.breadcrumbs                               // Computed breadcrumbs (readonly)
```

## 📄 Breadcrumb Item Interface

```typescript
interface BreadcrumbItem {
    title: string; // Display text
    to?: string | { name: string; params?: Record<string, any> }; // Vue Router route location
    disabled?: boolean; // Optional disabled state
}
```

## ⚡ Automatic Behavior

The breadcrumb system automatically:

1. **Updates on route change**: Router plugin updates store with new route
2. **Clears dynamic breadcrumbs**: When navigating to a route with its own meta breadcrumbs
3. **Generates fallback breadcrumbs**: From route path when no meta is defined
4. **Maintains reactivity**: All components using the store update automatically

## 🎯 Best Practices

1. **Use route meta for static breadcrumbs** - When breadcrumbs don't change based on data
2. **Use store.setBreadcrumbs for dynamic content** - When breadcrumbs depend on loaded data
3. **Include proper navigation links** - Add `to` for all items except the last one
4. **Clear breadcrumbs when appropriate** - Reset to defaults when navigating away
5. **Handle loading states** - Set appropriate breadcrumbs while data is loading

## 📁 Examples in the Codebase

-   **TestView.vue**: Simple static override
-   **BreadcrumbExamplesView.vue**: Comprehensive examples of all approaches
-   **UserDetailView.vue**: Parameter-based dynamic breadcrumbs

## 🎉 Priority Order

1. Dynamic breadcrumbs (set via store methods)
2. Route meta breadcrumbs (defined in router configuration)
3. Auto-generated breadcrumbs (from route path)

Dynamic breadcrumbs always take precedence over route meta and auto-generated breadcrumbs when they are set.
