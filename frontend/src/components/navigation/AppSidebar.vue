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
      titleKey: 'navigation.sidebar.sections.starter',
      routeName: 'projects',
      icon: FolderKanban,
      items: [
        {
          title: 'Projects',
          titleKey: 'navigation.sidebar.items.projects',
          routeName: 'projects',
        },
      ],
    },
    {
      title: 'Playground',
      titleKey: 'navigation.sidebar.sections.playground',
      url: '#',
      icon: SquareTerminal,
      items: [
        {
          title: 'History',
          titleKey: 'navigation.sidebar.items.history',
          url: '#',
        },
        {
          title: 'Starred',
          titleKey: 'navigation.sidebar.items.starred',
          url: '#',
        },
        {
          title: 'Settings',
          titleKey: 'navigation.sidebar.items.settings',
          url: '#',
        },
      ],
    },
    {
      title: 'Examples',
      titleKey: 'navigation.sidebar.sections.examples',
      routeName: 'examples',
      icon: Bot,
      isActive: true,
      items: [
        {
          title: 'Breadcrumb Examples',
          titleKey: 'navigation.sidebar.items.breadcrumbExamples',
          routeName: 'breadcrumb-examples',
        },
        {
          title: 'Layout Demo',
          titleKey: 'navigation.sidebar.items.layoutDemo',
          routeName: 'layout-demo',
        },
        {
          title: 'Dialog Examples',
          titleKey: 'navigation.sidebar.items.dialogExamples',
          routeName: 'dialog-examples',
        },
        {
          title: 'Error Handling Demo',
          titleKey: 'navigation.sidebar.items.errorHandlingDemo',
          routeName: 'error-handling-demo',
        },
      ],
    },
    {
      title: 'Documentation',
      titleKey: 'navigation.sidebar.sections.documentation',
      url: '#',
      icon: BookOpen,
      items: [
        {
          title: 'Introduction',
          titleKey: 'navigation.sidebar.items.introduction',
          url: '#',
        },
        {
          title: 'Get Started',
          titleKey: 'navigation.sidebar.items.getStarted',
          url: '#',
        },
        {
          title: 'Tutorials',
          titleKey: 'navigation.sidebar.items.tutorials',
          url: '#',
        },
        {
          title: 'Changelog',
          titleKey: 'navigation.sidebar.items.changelog',
          url: '#',
        },
      ],
    },
    {
      title: 'Settings',
      titleKey: 'navigation.sidebar.sections.settings',
      url: '#',
      icon: Settings2,
      items: [
        {
          title: 'General',
          titleKey: 'navigation.sidebar.items.general',
          url: '#',
        },
        {
          title: 'Team',
          titleKey: 'navigation.sidebar.items.team',
          url: '#',
        },
        {
          title: 'Billing',
          titleKey: 'navigation.sidebar.items.billing',
          url: '#',
        },
        {
          title: 'Limits',
          titleKey: 'navigation.sidebar.items.limits',
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
