<script setup lang="ts">
import { ref } from 'vue'

import { RouterView } from 'vue-router'

import { useBreadcrumbStore } from '@/stores/breadcrumb'

import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import { SidebarInset, SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'

import AppSidebar from '@/components/navigation/AppSidebar.vue'

const breadcrumbStore = useBreadcrumbStore()
const open = ref(true)
</script>

<template>
  <SidebarProvider v-model:open="open">
    <AppSidebar :open="open" />
    <SidebarInset>
      <header
        class="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12"
      >
        <div class="flex items-center gap-2 px-4">
          <SidebarTrigger class="-ml-1" />
          <Separator orientation="vertical" class="mr-2 h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <template v-for="(item, index) in breadcrumbStore.breadcrumbs" :key="index">
                <BreadcrumbItem>
                  <BreadcrumbLink
                    v-if="item.to && index < breadcrumbStore.breadcrumbs.length - 1"
                    @click="$router.push(item.to)"
                  >
                    {{ item.title }}
                  </BreadcrumbLink>
                  <BreadcrumbPage v-else>
                    {{ item.title }}
                  </BreadcrumbPage>
                </BreadcrumbItem>
                <BreadcrumbSeparator v-if="index < breadcrumbStore.breadcrumbs.length - 1" />
              </template>
            </BreadcrumbList>
          </Breadcrumb>
        </div>
      </header>

      <!-- Main content area where router views will be rendered -->
      <div class="flex-1 p-4 pt-0">
        <RouterView />
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>

<style scoped></style>
