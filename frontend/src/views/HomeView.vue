<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="mx-auto max-w-7xl space-y-6">
    <div class="space-y-2">
      <h1 class="text-3xl font-bold">{{ $t('dashboard.home.title') }}</h1>
      <p class="text-muted-foreground">
        {{ $t('dashboard.home.subtitle') }}
      </p>
    </div>

    <!-- Stats Cards -->
    <div class="grid auto-rows-min gap-4 md:grid-cols-3">
      <div class="aspect-video rounded-xl bg-muted/50 p-6 flex flex-col justify-center">
        <h3 class="text-lg font-semibold mb-2">
          {{ $t('dashboard.home.stats.totalUsers.title') }}
        </h3>
        <p class="text-3xl font-bold">{{ $t('dashboard.home.stats.totalUsers.value') }}</p>
        <p class="text-sm text-muted-foreground">
          {{ $t('dashboard.home.stats.totalUsers.change') }}
        </p>
      </div>
      <div class="aspect-video rounded-xl bg-muted/50 p-6 flex flex-col justify-center">
        <h3 class="text-lg font-semibold mb-2">{{ $t('dashboard.home.stats.revenue.title') }}</h3>
        <p class="text-3xl font-bold">{{ $t('dashboard.home.stats.revenue.value') }}</p>
        <p class="text-sm text-muted-foreground">{{ $t('dashboard.home.stats.revenue.change') }}</p>
      </div>
      <div class="aspect-video rounded-xl bg-muted/50 p-6 flex flex-col justify-center">
        <h3 class="text-lg font-semibold mb-2">
          {{ $t('dashboard.home.stats.activeSessions.title') }}
        </h3>
        <p class="text-3xl font-bold">{{ $t('dashboard.home.stats.activeSessions.value') }}</p>
        <p class="text-sm text-muted-foreground">
          {{ $t('dashboard.home.stats.activeSessions.change') }}
        </p>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="min-h-[400px] flex-1 rounded-xl bg-muted/50 p-6">
      <h2 class="text-xl font-semibold mb-4">{{ $t('dashboard.home.recentActivity.title') }}</h2>
      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-background rounded-lg">
          <div>
            <p class="font-medium">{{ $t('dashboard.home.recentActivity.items.newUser.title') }}</p>
            <p class="text-sm text-muted-foreground">
              {{ $t('dashboard.home.recentActivity.items.newUser.email') }}
            </p>
          </div>
          <span class="text-sm text-muted-foreground">{{
            $t('dashboard.home.recentActivity.items.newUser.time')
          }}</span>
        </div>
        <div class="flex items-center justify-between p-3 bg-background rounded-lg">
          <div>
            <p class="font-medium">{{ $t('dashboard.home.recentActivity.items.payment.title') }}</p>
            <p class="text-sm text-muted-foreground">
              {{ $t('dashboard.home.recentActivity.items.payment.amount') }}
            </p>
          </div>
          <span class="text-sm text-muted-foreground">{{
            $t('dashboard.home.recentActivity.items.payment.time')
          }}</span>
        </div>
        <div class="flex items-center justify-between p-3 bg-background rounded-lg">
          <div>
            <p class="font-medium">{{ $t('dashboard.home.recentActivity.items.backup.title') }}</p>
            <p class="text-sm text-muted-foreground">
              {{ $t('dashboard.home.recentActivity.items.backup.description') }}
            </p>
          </div>
          <span class="text-sm text-muted-foreground">{{
            $t('dashboard.home.recentActivity.items.backup.time')
          }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
