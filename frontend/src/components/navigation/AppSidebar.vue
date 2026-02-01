<script setup lang="ts">
import {
  AudioWaveform,
  BookOpen,
  Bot,
  Command,
  FolderKanban,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,
  Settings2,
  SquareTerminal,
} from 'lucide-vue-next'

import type { SidebarProps } from '@/components/ui/sidebar'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from '@/components/ui/sidebar'

import NavMain from '@/components/navigation/NavMain.vue'
import NavProjects from '@/components/navigation/NavProjects.vue'
import NavUser from '@/components/navigation/NavUser.vue'
import TeamSwitcher from '@/components/navigation/TeamSwitcher.vue'

interface AppSidebarProps extends SidebarProps {
  open?: boolean
}

const props = withDefaults(defineProps<AppSidebarProps>(), {
  collapsible: 'icon',
  open: true,
})

// This is sample data.
const data = {
  teams: [
    {
      name: 'Acme Inc',
      logo: GalleryVerticalEnd,
      plan: 'Enterprise',
    },
    {
      name: 'Acme Corp.',
      logo: AudioWaveform,
      plan: 'Startup',
    },
    {
      name: 'Evil Corp.',
      logo: Command,
      plan: 'Free',
    },
  ],
  navMain: [
    {
      title: 'Starter',
      routeName: 'projects',
      icon: FolderKanban,
      items: [
        {
          title: 'Projects',
          routeName: 'projects',
        },
      ],
    },
    {
      title: 'Playground',
      url: '#',
      icon: SquareTerminal,
      items: [
        {
          title: 'History',
          url: '#',
        },
        {
          title: 'Starred',
          url: '#',
        },
        {
          title: 'Settings',
          url: '#',
        },
      ],
    },
    {
      title: 'Examples',
      routeName: 'examples',
      icon: Bot,
      isActive: true,
      items: [
        {
          title: 'Api Example View',
          routeName: 'test',
        },
        {
          title: 'Breadcrumb Examples',
          routeName: 'breadcrumb-examples',
        },
        {
          title: 'Layout Demo',
          routeName: 'layout-demo',
        },
        {
          title: 'Dialog Examples',
          routeName: 'dialog-examples',
        },
      ],
    },
    {
      title: 'Documentation',
      url: '#',
      icon: BookOpen,
      items: [
        {
          title: 'Introduction',
          url: '#',
        },
        {
          title: 'Get Started',
          url: '#',
        },
        {
          title: 'Tutorials',
          url: '#',
        },
        {
          title: 'Changelog',
          url: '#',
        },
      ],
    },
    {
      title: 'Settings',
      url: '#',
      icon: Settings2,
      items: [
        {
          title: 'General',
          url: '#',
        },
        {
          title: 'Team',
          url: '#',
        },
        {
          title: 'Billing',
          url: '#',
        },
        {
          title: 'Limits',
          url: '#',
        },
      ],
    },
  ],
  projects: [
    {
      name: 'Design Engineering',
      url: '#',
      icon: Frame,
    },
    {
      name: 'Sales & Marketing',
      url: '#',
      icon: PieChart,
    },
    {
      name: 'Travel',
      url: '#',
      icon: Map,
    },
  ],
}
</script>

<template>
  <Sidebar v-bind="props">
    <SidebarHeader>
      <TeamSwitcher :teams="data.teams" />
    </SidebarHeader>
    <SidebarContent>
      <NavMain :items="data.navMain" :open="props.open" />
      <NavProjects :projects="data.projects" />
    </SidebarContent>
    <SidebarFooter>
      <NavUser />
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
</template>
