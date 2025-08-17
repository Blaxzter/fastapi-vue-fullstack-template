<template>
  <div class="p-6 space-y-4">
    <h2 class="text-2xl font-bold">{{ $t('example.dialogExamples.title') }}</h2>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Basic Confirm Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>{{ $t('example.dialogExamples.cards.basicConfirm.title') }}</CardTitle>
          <CardDescription>{{
            $t('example.dialogExamples.cards.basicConfirm.description')
          }}</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showBasicConfirm">{{
            $t('example.dialogExamples.cards.basicConfirm.button')
          }}</Button>
        </CardContent>
      </Card>

      <!-- Custom Confirm Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>{{ $t('example.dialogExamples.cards.customConfirm.title') }}</CardTitle>
          <CardDescription>{{
            $t('example.dialogExamples.cards.customConfirm.description')
          }}</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showCustomConfirm">{{
            $t('example.dialogExamples.cards.customConfirm.button')
          }}</Button>
        </CardContent>
      </Card>

      <!-- Destructive Confirm Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>{{ $t('example.dialogExamples.cards.destructiveConfirm.title') }}</CardTitle>
          <CardDescription>{{
            $t('example.dialogExamples.cards.destructiveConfirm.description')
          }}</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showDestructiveConfirm" variant="destructive">
            {{ $t('example.dialogExamples.cards.destructiveConfirm.button') }}
          </Button>
        </CardContent>
      </Card>

      <!-- Alert Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>{{ $t('example.dialogExamples.cards.alert.title') }}</CardTitle>
          <CardDescription>{{
            $t('example.dialogExamples.cards.alert.description')
          }}</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showAlert" variant="secondary">{{
            $t('example.dialogExamples.cards.alert.button')
          }}</Button>
        </CardContent>
      </Card>

      <!-- Info Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>{{ $t('example.dialogExamples.cards.info.title') }}</CardTitle>
          <CardDescription>{{
            $t('example.dialogExamples.cards.info.description')
          }}</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showInfo" variant="outline">{{
            $t('example.dialogExamples.cards.info.button')
          }}</Button>
        </CardContent>
      </Card>

      <!-- String Only Dialog -->
      <Card>
        <CardHeader>
          <CardTitle>{{ $t('example.dialogExamples.cards.quickConfirm.title') }}</CardTitle>
          <CardDescription>{{
            $t('example.dialogExamples.cards.quickConfirm.description')
          }}</CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="showQuickConfirm">{{
            $t('example.dialogExamples.cards.quickConfirm.button')
          }}</Button>
        </CardContent>
      </Card>
    </div>

    <!-- Result Display -->
    <div v-if="lastResult !== null" class="mt-6 p-4 border rounded-lg">
      <h3 class="text-lg font-semibold mb-2">{{ $t('example.dialogExamples.result.title') }}</h3>
      <p class="text-sm text-muted-foreground">
        {{
          lastResult
            ? $t('example.dialogExamples.result.confirmed')
            : $t('example.dialogExamples.result.cancelled')
        }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import { useI18n } from 'vue-i18n'

import { useDialog } from '@/composables/useDialog'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const { t } = useI18n()
const dialog = useDialog()
const lastResult = ref<boolean | null>(null)

const showBasicConfirm = async () => {
  const result = await dialog.confirm({
    text: t('example.dialogExamples.dialogs.basicConfirm.text'),
  })
  lastResult.value = result
}

const showCustomConfirm = async () => {
  const result = await dialog.confirm({
    title: t('example.dialogExamples.dialogs.customConfirm.title'),
    text: t('example.dialogExamples.dialogs.customConfirm.text'),
    confirmText: t('example.dialogExamples.dialogs.customConfirm.confirmText'),
    cancelText: t('example.dialogExamples.dialogs.customConfirm.cancelText'),
    confirmIcon: 'check',
    cancelIcon: 'x',
  })
  lastResult.value = result
}

const showDestructiveConfirm = async () => {
  const result = await dialog.confirmDestructive({
    title: t('example.dialogExamples.dialogs.destructiveConfirm.title'),
    text: t('example.dialogExamples.dialogs.destructiveConfirm.text'),
    confirmText: t('example.dialogExamples.dialogs.destructiveConfirm.confirmText'),
    confirmIcon: 'alert-triangle',
  })
  lastResult.value = result

  if (result) {
    // Simulate deletion
    await dialog.alert(t('example.dialogExamples.dialogs.destructiveConfirm.successMessage'))
  }
}

const showAlert = async () => {
  await dialog.alert({
    title: t('example.dialogExamples.dialogs.alert.title'),
    text: t('example.dialogExamples.dialogs.alert.text'),
    variant: 'default',
  })
  lastResult.value = null
}

const showInfo = async () => {
  await dialog.info(t('example.dialogExamples.dialogs.info.text'))
  lastResult.value = null
}

const showQuickConfirm = async () => {
  const result = await dialog.confirm(t('example.dialogExamples.dialogs.quickConfirm.text'))
  lastResult.value = result
}
</script>
