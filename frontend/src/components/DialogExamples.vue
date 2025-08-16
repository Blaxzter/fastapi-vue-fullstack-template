<template>
  <div class="p-6 space-y-4">
    <h2 class="text-2xl font-bold">Dialog Examples</h2>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Basic Confirm Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>Basic Confirm</CardTitle>
          <CardDescription>Simple confirmation dialog</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showBasicConfirm">Show Confirm Dialog</Button>
        </CardContent>
      </Card>

      <!-- Custom Confirm Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>Custom Confirm</CardTitle>
          <CardDescription>Confirmation with custom text and icons</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showCustomConfirm">Show Custom Confirm</Button>
        </CardContent>
      </Card>

      <!-- Destructive Confirm Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>Destructive Confirm</CardTitle>
          <CardDescription>Dangerous action confirmation</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showDestructiveConfirm" variant="destructive">
            Delete Item
          </Button>
        </CardContent>
      </Card>

      <!-- Alert Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>Alert Dialog</CardTitle>
          <CardDescription>Simple alert message</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showAlert" variant="secondary">Show Alert</Button>
        </CardContent>
      </Card>

      <!-- Info Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>Info Dialog</CardTitle>
          <CardDescription>Informational dialog</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showInfo" variant="outline">Show Info</Button>
        </CardContent>
      </Card>

      <!-- String Only Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>Quick Confirm</CardTitle>
          <CardDescription>Using string-only syntax</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showQuickConfirm">Quick Confirm</Button>
        </CardContent>
      </Card>
    </div>

    <!-- Result Display -->
    <div v-if="lastResult !== null" class="mt-6 p-4 border rounded-lg">
      <h3 class="text-lg font-semibold mb-2">Last Result:</h3>
      <p class="text-sm text-muted-foreground">
        {{ lastResult ? 'User confirmed' : 'User cancelled' }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useDialog } from '@/composables/useDialog'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const dialog = useDialog()
const lastResult = ref<boolean | null>(null)

const showBasicConfirm = async () => {
  const result = await dialog.confirm({
    text: 'Are you sure you want to proceed with this action?'
  })
  lastResult.value = result
}

const showCustomConfirm = async () => {
  const result = await dialog.confirm({
    title: 'Custom Confirmation',
    text: 'This action will save your changes. Do you want to continue?',
    confirmText: 'Save Changes',
    cancelText: 'Keep Editing',
    confirmIcon: 'check',
    cancelIcon: 'x'
  })
  lastResult.value = result
}

const showDestructiveConfirm = async () => {
  const result = await dialog.confirmDestructive({
    title: 'Delete Item',
    text: 'This action cannot be undone. Are you sure you want to delete this item?',
    confirmText: 'Delete',
    confirmIcon: 'alert-triangle'
  })
  lastResult.value = result

  if (result) {
    // Simulate deletion
    await dialog.alert('Item has been deleted successfully!')
  }
}

const showAlert = async () => {
  await dialog.alert({
    title: 'Important Notice',
    text: 'Your changes have been saved successfully.',
    variant: 'default'
  })
  lastResult.value = null
}

const showInfo = async () => {
  await dialog.info('This is some useful information for the user.')
  lastResult.value = null
}

const showQuickConfirm = async () => {
  const result = await dialog.confirm('Do you want to continue?')
  lastResult.value = result
}
</script>
