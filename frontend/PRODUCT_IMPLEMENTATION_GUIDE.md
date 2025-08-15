# Vue 3 Frontend - Product Implementation Guide

## Overview

This guide provides instructions for implementing new products/features in the Vue 3 frontend using Vue 3 composition API, TypeScript, Pinia, and shadcn-vue components.

## Architecture Overview

```
Frontend Architecture:
├── Views (Pages)          → Route components & page layouts
├── Components             → Reusable UI components
│   ├── ui/               → shadcn-vue base components
│   ├── feature/          → Feature-specific components
│   └── utils/            → Utility components
├── Stores (Pinia)        → State management
├── Composables           → Reusable logic
├── Router                → Navigation & route definitions
├── Client (API)          → Auto-generated API client
└── Types                 → TypeScript type definitions
```

## Tech Stack Reference

- **Vue 3** with Composition API
- **TypeScript** for type safety
- **Pinia** for state management
- **shadcn-vue** for UI components
- **Tailwind CSS v4** for styling
- **Auth0** for authentication
- **Zod** for validation (auto-generated)

## Implementation Steps

### 1. Generate API Client

```bash
# Ensure backend is running and generate TypeScript client
pnpm run generate-client
```

**Generated Files:**

- `src/client/types.gen.ts` - TypeScript interfaces for all API schemas
- `src/client/zod.gen.ts` - Zod validation schemas matching backend models
- `src/client/client.gen.ts` - HTTP client methods for all endpoints

**Development Workflow:**

1. **Backend First** - Implement backend schemas before frontend
2. **Generate Types** - Run `pnpm run generate-client` after backend changes
3. **No Manual Types** - Never manually create types that mirror backend schemas
4. **Use Generated Zod** - Always use generated schemas from `zod.gen.ts`

### 2. Define Types

**Location**: `src/types/`

```typescript
// src/types/product.ts
// ✅ ALWAYS import generated types - never redefine them
export type {
  Product,
  ProductCreate,
  ProductUpdate,
  ProductResponse,
  Category,
} from '@/client/types.gen'

// ✅ ONLY define frontend-specific types
export interface ProductFilters {
  search?: string
  categoryId?: string
  inStock?: boolean
}

export interface PaginationState {
  page: number
  perPage: number
  total: number
  totalPages: number
}

// ✅ Use auto-generated Zod schemas
export {
  zProductCreate as productCreateSchema,
  zProductUpdate as productUpdateSchema,
} from '@/client/zod.gen'
```

### 3. Create Pinia Store

**Location**: `src/stores/`

```typescript
// src/stores/product.ts
import { computed, ref } from 'vue'

import { defineStore } from 'pinia'

import { useAuthenticatedClient } from '@/composables/useAuthenticatedClient'

import type { Product, ProductCreate, ProductFilters } from '@/types/product'

export const useProductStore = defineStore('product', () => {
  // State
  const products = ref<Product[]>([])
  const categories = ref<Category[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref<PaginationState>({
    page: 1,
    perPage: 20,
    total: 0,
    totalPages: 0,
  })
  const filters = ref<ProductFilters>({})

  // API client
  const { get, post, patch, delete: del } = useAuthenticatedClient()

  // Getters
  const activeProducts = computed(() => products.value.filter((p) => p.is_active))

  // Actions
  const fetchProducts = async (page = 1, resetList = true) => {
    loading.value = true
    try {
      const params = new URLSearchParams({
        skip: ((page - 1) * pagination.value.perPage).toString(),
        limit: pagination.value.perPage.toString(),
        ...(filters.value.search && { search: filters.value.search }),
      })

      const response = await get({ url: `/api/v1/products/?${params}` })

      if (resetList) {
        products.value = response.items
      } else {
        products.value.push(...response.items)
      }

      pagination.value = {
        page: response.page,
        perPage: response.per_page,
        total: response.total,
        totalPages: response.pages,
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch products'
    } finally {
      loading.value = false
    }
  }

  const createProduct = async (productData: ProductCreate) => {
    try {
      const newProduct = await post({
        url: '/api/v1/products/',
        body: productData,
      })
      products.value.unshift(newProduct)
      return newProduct
    } catch (err: any) {
      error.value = err.message || 'Failed to create product'
      return null
    }
  }

  // ... other CRUD methods

  return {
    // State
    products,
    categories,
    loading,
    error,
    pagination,
    filters,
    // Getters
    activeProducts,
    // Actions
    fetchProducts,
    createProduct,
    // ... other actions
  }
})
```

### 4. Create Composables

**Location**: `src/composables/`

```typescript
// src/composables/useProductForm.ts
import { ref, computed } from 'vue'
import { z } from 'zod'
import { zProductCreate, zProductUpdate } from '@/client/zod.gen'
import type { Product, ProductCreate } from '@/client/types.gen'

export function useProductForm(initialData?: Partial<Product>) {
  const formData = ref<ProductCreate>({
    name: initialData?.name || '',
    description: initialData?.description || '',
    price: initialData?.price || 0,
    sku: initialData?.sku || '',
    stock_quantity: initialData?.stock_quantity || 0,
    is_active: initialData?.is_active ?? true,
    category_ids: []
  })

  const errors = ref<Record<string, string>>({})

  const validate = () => {
    errors.value = {}
    try {
      const schema = initialData ? zProductUpdate : zProductCreate
      schema.parse(formData.value)
      return true
    } catch (error) {
      if (error instanceof z.ZodError) {
        error.errors.forEach(err => {
          errors.value[err.path.join('.')] = err.message
        })
      }
      return false
    }
  }

  return { formData, errors, validate }
}

// src/composables/useProductFilters.ts
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { ProductFilters } from '@/types/product'

export function useProductFilters() {
  const route = useRoute()
  const router = useRouter()

  const filters = ref<ProductFilters>({
    search: route.query.search as string || '',
    categoryId: route.query.category as string || '',
  })

  const hasActiveFilters = computed(() =>
    Object.values(filters.value).some(value => value !== undefined && value !== '')
  )

  watch(filters, (newFilters) => {
    const query: Record<string, string> = {}
    if (newFilters.search) query.search = newFilters.search
    if (newFilters.categoryId) query.category = newFilters.categoryId
    router.replace({ query })
  }, { deep: true })

  return { filters, hasActiveFilters }
}
```

### 5. Create UI Components

**Location**: `src/components/`

#### Product List Component

```vue
<!-- src/components/product/ProductList.vue -->
<template>
  <div class="space-y-6">
    <!-- Filters -->
    <Card>
      <CardContent class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Input v-model="filters.search" placeholder="Search products..." />
          <Select v-model="filters.categoryId">
            <SelectTrigger>
              <SelectValue placeholder="All categories" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">All categories</SelectItem>
              <SelectItem v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </SelectItem>
            </SelectContent>
          </Select>
          <Button @click="clearFilters" variant="outline" v-if="hasActiveFilters">
            Clear Filters
          </Button>
        </div>
      </CardContent>
    </Card>

    <!-- Products Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
        @edit="$emit('edit', product)"
        @delete="$emit('delete', product.id)"
        @view="$emit('view', product)"
      />
    </div>

    <!-- Loading & Empty States -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Skeleton v-for="i in 6" :key="i" class="h-64" />
    </div>

    <Card v-if="!loading && products.length === 0">
      <CardContent class="text-center py-12">
        <h3 class="text-lg font-semibold mb-2">No products found</h3>
        <Button @click="$emit('create')">Create Product</Button>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useProductFilters } from '@/composables/useProductFilters'

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Skeleton } from '@/components/ui/skeleton'

import type { Category, Product } from '@/types/product'

interface Props {
  products: Product[]
  categories: Category[]
  loading: boolean
}

defineProps<Props>()
defineEmits<{
  edit: [product: Product]
  delete: [productId: string]
  view: [product: Product]
  create: []
}>()

const { filters, hasActiveFilters, clearFilters } = useProductFilters()
</script>
```

#### Product Card Component

```vue
<!-- src/components/product/ProductCard.vue -->
<template>
  <Card class="overflow-hidden hover:shadow-lg transition-shadow">
    <div class="aspect-square bg-muted flex items-center justify-center">
      <PackageIcon class="h-12 w-12 text-muted-foreground" />
    </div>

    <CardContent class="p-4">
      <h3 class="font-semibold text-lg">{{ product.name }}</h3>
      <p v-if="product.description" class="text-sm text-muted-foreground">
        {{ product.description }}
      </p>
      <div class="flex items-center justify-between mt-2">
        <span class="text-xl font-bold">${{ (product.price / 100).toFixed(2) }}</span>
        <Badge>{{ product.sku }}</Badge>
      </div>
      <div class="text-sm text-muted-foreground">Stock: {{ product.stock_quantity }} units</div>
    </CardContent>

    <CardFooter class="p-4 pt-0 flex gap-2">
      <Button variant="outline" size="sm" @click="$emit('view', product)">View</Button>
      <Button variant="outline" size="sm" @click="$emit('edit', product)">Edit</Button>
      <Button variant="destructive" size="sm" @click="$emit('delete', product.id)">Delete</Button>
    </CardFooter>
  </Card>
</template>

<script setup lang="ts">
import { PackageIcon } from 'lucide-vue-next'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardFooter } from '@/components/ui/card'

import type { Product } from '@/types/product'

defineProps<{ product: Product }>()
defineEmits<{
  view: [product: Product]
  edit: [product: Product]
  delete: [productId: string]
}>()
</script>
```

### 6. Create Views (Pages)

**Location**: `src/views/`

```vue
<!-- src/views/products/ProductsView.vue -->
<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold">Products</h1>
        <p class="text-muted-foreground">Manage your product catalog</p>
      </div>
      <Button @click="showCreateDialog = true">
        <PlusIcon class="h-4 w-4 mr-2" />
        Add Product
      </Button>
    </div>

    <!-- Stats Overview -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card>
        <CardContent class="p-4">
          <p class="text-sm text-muted-foreground">Total Products</p>
          <p class="text-2xl font-bold">{{ pagination.total }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-sm text-muted-foreground">Active Products</p>
          <p class="text-2xl font-bold">{{ activeProducts.length }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-sm text-muted-foreground">Categories</p>
          <p class="text-2xl font-bold">{{ categories.length }}</p>
        </CardContent>
      </Card>
    </div>

    <!-- Product List -->
    <ProductList
      :products="products"
      :categories="categories"
      :loading="loading"
      @edit="editProduct"
      @delete="deleteProduct"
      @view="viewProduct"
      @create="showCreateDialog = true"
    />

    <!-- Dialogs -->
    <ProductFormDialog
      v-model:open="showCreateDialog"
      :product="editingProduct"
      @success="handleProductSaved"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { PlusIcon } from 'lucide-vue-next'
import { storeToRefs } from 'pinia'

import { useProductStore } from '@/stores/product'

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

import ProductFormDialog from '@/components/product/ProductFormDialog.vue'
import ProductList from '@/components/product/ProductList.vue'

import type { Product } from '@/types/product'

const productStore = useProductStore()
const showCreateDialog = ref(false)
const editingProduct = ref<Product | null>(null)

const { products, categories, loading, pagination, activeProducts } = storeToRefs(productStore)

const editProduct = (product: Product) => {
  editingProduct.value = product
  showCreateDialog.value = true
}

const deleteProduct = async (productId: string) => {
  await productStore.deleteProduct(productId)
}

const viewProduct = (product: Product) => {
  // Navigate to product detail or show detail view
}

const handleProductSaved = () => {
  showCreateDialog.value = false
  editingProduct.value = null
  productStore.fetchProducts()
}

onMounted(async () => {
  await Promise.all([productStore.fetchProducts(), productStore.fetchCategories()])
})
</script>
```

### 7. Add Routes

**Location**: `src/router/index.ts`

```typescript
// Add to the postauth-layout children
{
  path: 'products',
  name: 'products',
  component: () => import('@/views/products/ProductsView.vue'),
  meta: {
    breadcrumbs: [
      { title: 'Home', to: { name: 'home' } },
      { title: 'Products' }
    ]
  }
},
{
  path: 'products/:id',
  name: 'product-detail',
  component: () => import('@/views/products/ProductDetailView.vue')
}
```

### 8. Update Navigation

**Location**: `src/components/navigation/NavMain.vue`

```typescript
const items = [
  {
    title: 'Dashboard',
    url: '/app/home',
    icon: Home,
  },
  {
    title: 'Products',
    url: '/app/products',
    icon: Package,
  },
  // ... other items
]
```

## Advanced Patterns

### Optimistic Updates

```typescript
// In store - optimistically update UI before API call
const updateProductOptimistic = async (id: string, update: ProductUpdate) => {
  const index = products.value.findIndex((p) => p.id === id)
  const original = products.value[index]

  // Update UI immediately
  if (index !== -1) products.value[index] = { ...original, ...update }

  try {
    const result = await patch({ url: `/api/v1/products/${id}`, body: update })
    products.value[index] = result
  } catch (error) {
    // Revert on error
    if (index !== -1) products.value[index] = original
    throw error
  }
}
```

### Real-time Updates

```typescript
// WebSocket composable for live updates
export function useProductUpdates() {
  const productStore = useProductStore()

  onMounted(() => {
    const ws = new WebSocket(`${import.meta.env.VITE_WS_URL}/products`)
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data)
      if (update.type === 'product_updated') {
        productStore.updateProductInList(update.product)
      }
    }
    onUnmounted(() => ws.close())
  })
}
```

## Testing

### Component Tests

```typescript
// tests/components/ProductCard.test.ts
import { mount } from '@vue/test-utils'

import { describe, expect, it } from 'vitest'

import ProductCard from '@/components/product/ProductCard.vue'

describe('ProductCard', () => {
  it('renders product information correctly', () => {
    const wrapper = mount(ProductCard, {
      props: { product: mockProduct },
    })
    expect(wrapper.text()).toContain('Test Product')
  })
})
```

### Store Tests

```typescript
// tests/stores/product.test.ts
import { createPinia, setActivePinia } from 'pinia'

import { useProductStore } from '@/stores/product'

describe('Product Store', () => {
  beforeEach(() => setActivePinia(createPinia()))

  it('filters active products correctly', () => {
    const store = useProductStore()
    store.products = [
      { id: '1', name: 'Active', is_active: true },
      { id: '2', name: 'Inactive', is_active: false },
    ]
    expect(store.activeProducts).toHaveLength(1)
  })
})
```

## Best Practices

### 1. Type Safety & Code Generation

- **Never duplicate backend types** - Always import from `@/client/types.gen`
- **Use generated Zod schemas** - Always import from `@/client/zod.gen`
- **Regenerate after changes** - Run `pnpm run generate-client` after backend updates
- **Frontend-only types** - Only define UI-specific types (filters, state)

### 2. State Management

- Use Pinia stores for global state
- Keep local state for UI-only concerns
- Implement proper error handling
- Use computed properties for derived state

### 3. Component Structure

- Follow single responsibility principle
- Use Composition API for reusability
- Implement proper TypeScript props
- Use emits for parent-child communication

### 4. Forms & Validation

- Use generated Zod schemas for validation
- Implement real-time validation feedback
- Handle server-side validation errors
- Provide clear error messages

### 5. Performance & Accessibility

- Implement pagination for large lists
- Use lazy loading for routes
- Use semantic HTML elements
- Ensure keyboard navigation works

This guide provides the foundation for implementing new features while maintaining consistency and best practices.
