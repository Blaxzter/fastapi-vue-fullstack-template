<template>
  <div class="mx-auto max-w-6xl space-y-6">
    <div class="space-y-4">
      <h1 class="text-2xl font-bold">Dynamic Breadcrumb Examples</h1>
      <p class="text-muted-foreground">
        This page demonstrates different ways to use dynamic breadcrumbs.
      </p>
    </div>

    <div class="grid gap-6 md:grid-cols-2">
      <!-- Example 1: Static override -->
      <Card>
        <CardHeader>
          <CardTitle>Static Override</CardTitle>
          <CardDescription>
            Breadcrumb is set statically when the component mounts.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="setStaticBreadcrumb">Set Static Breadcrumb</Button>
        </CardContent>
      </Card>

      <!-- Example 2: Dynamic based on data -->
      <Card>
        <CardHeader>
          <CardTitle>Dynamic from Data</CardTitle>
          <CardDescription> Breadcrumb changes based on user selection. </CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="space-y-2">
            <Label>Select a category:</Label>
            <select
              v-model="selectedCategory"
              @change="updateBreadcrumbFromData"
              class="w-full p-2 border rounded"
            >
              <option value="">Choose...</option>
              <option value="electronics">Electronics</option>
              <option value="clothing">Clothing</option>
              <option value="books">Books</option>
            </select>
          </div>
          <div v-if="selectedCategory" class="space-y-2">
            <Label>Select an item:</Label>
            <select
              v-model="selectedItem"
              @change="updateBreadcrumbFromData"
              class="w-full p-2 border rounded"
            >
              <option value="">Choose...</option>
              <option v-for="item in availableItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </option>
            </select>
          </div>
        </CardContent>
      </Card>

      <!-- Example 3: Reset to route default -->
      <Card>
        <CardHeader>
          <CardTitle>Reset to Default</CardTitle>
          <CardDescription> Reset breadcrumb back to route meta definition. </CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="resetBreadcrumb" variant="outline">Reset to Route Default</Button>
        </CardContent>
      </Card>

      <!-- Example 4: Add breadcrumb dynamically -->
      <Card>
        <CardHeader>
          <CardTitle>Add Breadcrumb</CardTitle>
          <CardDescription> Add additional breadcrumb items dynamically. </CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="flex gap-2">
            <Input v-model="newBreadcrumbTitle" placeholder="Breadcrumb title" />
            <Button @click="addNewBreadcrumb">Add</Button>
          </div>
        </CardContent>
      </Card>
    </div>

    <div class="h-[500px]"></div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { type BreadcrumbItem, useBreadcrumbStore } from '@/stores/breadcrumb'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

// Breadcrumb store
const breadcrumbStore = useBreadcrumbStore()

// Component state
const selectedCategory = ref('')
const selectedItem = ref('')
const newBreadcrumbTitle = ref('')

// Mock data for demonstration
const categories = {
  electronics: [
    { id: 'laptop', name: 'Laptop' },
    { id: 'phone', name: 'Smartphone' },
    { id: 'tablet', name: 'Tablet' },
  ],
  clothing: [
    { id: 'shirt', name: 'T-Shirt' },
    { id: 'jeans', name: 'Jeans' },
    { id: 'jacket', name: 'Jacket' },
  ],
  books: [
    { id: 'fiction', name: 'Fiction' },
    { id: 'technical', name: 'Technical' },
    { id: 'biography', name: 'Biography' },
  ],
}

const availableItems = computed(() => {
  if (!selectedCategory.value) return []
  return categories[selectedCategory.value as keyof typeof categories] || []
})

// Breadcrumb functions
const setStaticBreadcrumb = () => {
  breadcrumbStore.setBreadcrumbs([
    { title: 'Home', to: { name: 'home' } },
    { title: 'Examples', to: '/breadcrumb-examples' },
    { title: 'Static Example' },
  ])
}

const updateBreadcrumbFromData = () => {
  const breadcrumbs: BreadcrumbItem[] = [
    { title: 'Home', to: { name: 'home' } },
    { title: 'Examples', to: { name: 'breadcrumb-examples' } },
  ]

  if (selectedCategory.value) {
    breadcrumbs.push({
      title: selectedCategory.value.charAt(0).toUpperCase() + selectedCategory.value.slice(1),
      to: `/examples/${selectedCategory.value}`,
    })

    if (selectedItem.value) {
      const item = availableItems.value.find((i) => i.id === selectedItem.value)
      if (item) {
        breadcrumbs.push({
          title: item.name,
        })
      }
    }
  }

  breadcrumbStore.setBreadcrumbs(breadcrumbs)
}

const resetBreadcrumb = () => {
  breadcrumbStore.clearBreadcrumbs()
  selectedCategory.value = ''
  selectedItem.value = ''
  newBreadcrumbTitle.value = ''
}

const addNewBreadcrumb = () => {
  if (newBreadcrumbTitle.value.trim()) {
    breadcrumbStore.addBreadcrumb({ title: newBreadcrumbTitle.value.trim() })
    newBreadcrumbTitle.value = ''
  }
}

// Set initial breadcrumb when component mounts
onMounted(() => {
  breadcrumbStore.setBreadcrumbs([
    { title: 'Home', to: { name: 'home' } },
    { title: 'Breadcrumb Examples' },
  ])
})
</script>
