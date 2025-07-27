<script setup lang="ts"></script>

<template>
  <div class="mx-auto max-w-7xl space-y-6">
    <div class="space-y-2">
      <h1 class="text-3xl font-bold">Dashboard</h1>
      <p class="text-muted-foreground">
        Welcome back! Here's what's happening with your application.
      </p>
    </div>

    <!-- Stats Cards -->
    <div class="grid auto-rows-min gap-4 md:grid-cols-3">
      <div class="aspect-video rounded-xl bg-muted/50 p-6 flex flex-col justify-center">
        <h3 class="text-lg font-semibold mb-2">Total Users</h3>
        <p class="text-3xl font-bold">1,234</p>
        <p class="text-sm text-muted-foreground">+12% from last month</p>
      </div>
      <div class="aspect-video rounded-xl bg-muted/50 p-6 flex flex-col justify-center">
        <h3 class="text-lg font-semibold mb-2">Revenue</h3>
        <p class="text-3xl font-bold">$45,678</p>
        <p class="text-sm text-muted-foreground">+8% from last month</p>
      </div>
      <div class="aspect-video rounded-xl bg-muted/50 p-6 flex flex-col justify-center">
        <h3 class="text-lg font-semibold mb-2">Active Sessions</h3>
        <p class="text-3xl font-bold">892</p>
        <p class="text-sm text-muted-foreground">+5% from last hour</p>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="min-h-[400px] flex-1 rounded-xl bg-muted/50 p-6">
      <h2 class="text-xl font-semibold mb-4">Recent Activity</h2>
      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-background rounded-lg">
          <div>
            <p class="font-medium">New user registered</p>
            <p class="text-sm text-muted-foreground">john@example.com</p>
          </div>
          <span class="text-sm text-muted-foreground">2 minutes ago</span>
        </div>
        <div class="flex items-center justify-between p-3 bg-background rounded-lg">
          <div>
            <p class="font-medium">Payment received</p>
            <p class="text-sm text-muted-foreground">$299.00 from Premium plan</p>
          </div>
          <span class="text-sm text-muted-foreground">15 minutes ago</span>
        </div>
        <div class="flex items-center justify-between p-3 bg-background rounded-lg">
          <div>
            <p class="font-medium">System backup completed</p>
            <p class="text-sm text-muted-foreground">All data backed up successfully</p>
          </div>
          <span class="text-sm text-muted-foreground">1 hour ago</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
