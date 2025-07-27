<template>
  <Card>
    <CardHeader>
      <CardTitle class="flex items-center gap-2">
        <UserIcon class="h-5 w-5" />
        Current Profile
      </CardTitle>
      <CardDescription> Your current profile information from Auth0 </CardDescription>
    </CardHeader>
    <CardContent>
      <div class="flex items-start gap-6">
        <!-- Avatar -->
        <div class="flex flex-col items-center gap-4">
          <Avatar class="h-24 w-24">
            <AvatarImage v-if="user?.picture" :src="user.picture" :alt="displayName" />
            <AvatarFallback class="text-xl">
              {{ initials }}
            </AvatarFallback>
          </Avatar>
        </div>

        <!-- User Info -->
        <div class="flex-1 grid gap-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label class="text-sm font-medium text-muted-foreground">Name</Label>
              <p class="text-sm">{{ user?.name || 'Not provided' }}</p>
            </div>
            <div>
              <div class="flex items-center gap-2">
                <Label class="text-sm font-medium text-muted-foreground">Email</Label>
                <Badge variant="outline">
                  {{ user?.email_verified ? 'Verified' : 'Unverified' }}
                </Badge>
              </div>
              <p class="text-sm">{{ user?.email || 'Not provided' }}</p>
            </div>
            <div>
              <Label class="text-sm font-medium text-muted-foreground">Nickname</Label>
              <p class="text-sm">{{ user?.nickname || 'Not provided' }}</p>
            </div>
            <div>
              <Label class="text-sm font-medium text-muted-foreground">Auth Provider</Label>
              <Badge
                :variant="authProvider.variant"
                class="text-xs flex items-center gap-2 w-fit mt-1"
              >
                <SimpleIcon :iconData="authProvider.icon" />
                {{ authProvider.name }}
              </Badge>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import { UserIcon } from 'lucide-vue-next'

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'

import SimpleIcon from '@/components/utils/SimpleIcon.vue'

import { useAuthProvider } from './useAuthProvider'

interface Props {
  user: any // You might want to type this properly based on your user interface
}

const props = defineProps<Props>()

// Computed properties
const displayName = computed(
  () => props.user?.name || props.user?.nickname || props.user?.email || 'User',
)

const initials = computed(() => {
  if (props.user?.name) {
    return props.user.name
      .split(' ')
      .map((n: string) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }
  if (props.user?.email) {
    return props.user.email[0].toUpperCase()
  }
  return 'U'
})

// Determine auth provider from sub field
const authProvider = useAuthProvider(props.user)
</script>
