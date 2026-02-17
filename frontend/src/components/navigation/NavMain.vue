<script setup lang="ts">
import { ChevronRight, type LucideIcon } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { RouterLink, useRouter } from 'vue-router'

import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from '@/components/ui/sidebar'

const router = useRouter()
const { t } = useI18n()

const props = defineProps<{
  open: boolean
  items: {
    title: string
    titleKey?: string
    url?: string
    routeName?: string
    icon?: LucideIcon
    isActive?: boolean
    items?: {
      title: string
      titleKey?: string
      url?: string
      routeName?: string
    }[]
  }[]
}>()

const resolveTitle = (item: { title: string; titleKey?: string }) =>
  item.titleKey ? t(item.titleKey) : item.title

const handleSidebarToggle = (item: { isActive?: boolean; routeName?: string; url?: string }) => {
  if (props.open) {
    item.isActive = !item.isActive
  } else {
    // in the closed state the button itself is a router link if it has url or routeName
    if (item.routeName) {
      router.push({ name: item.routeName })
    } else if (item.url) {
      window.location.href = item.url
    }
  }
}
</script>

<template>
  <SidebarGroup>
    <SidebarGroupLabel>{{ $t('navigation.sidebar.platform') }}</SidebarGroupLabel>
    <SidebarMenu>
      <Collapsible
        v-for="item in items"
        :key="item.routeName ?? item.titleKey ?? item.title"
        as-child
        :default-open="item.isActive"
        class="group/collapsible"
      >
        <SidebarMenuItem>
          <CollapsibleTrigger as-child>
            <SidebarMenuButton :tooltip="resolveTitle(item)" @click="handleSidebarToggle(item)">
              <component :is="item.icon" v-if="item.icon" />
              <span>{{ resolveTitle(item) }}</span>
              <ChevronRight
                class="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90"
              />
            </SidebarMenuButton>
          </CollapsibleTrigger>
          <CollapsibleContent>
            <SidebarMenuSub>
              <SidebarMenuSubItem
                v-for="subItem in item.items"
                :key="subItem.routeName ?? subItem.titleKey ?? subItem.title"
              >
                <SidebarMenuSubButton as-child>
                  <RouterLink v-if="subItem.routeName" :to="{ name: subItem.routeName }">
                    <span>{{ resolveTitle(subItem) }}</span>
                  </RouterLink>
                  <a v-else :href="subItem.url">
                    <span>{{ resolveTitle(subItem) }}</span>
                  </a>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>
            </SidebarMenuSub>
          </CollapsibleContent>
        </SidebarMenuItem>
      </Collapsible>
    </SidebarMenu>
  </SidebarGroup>
</template>
