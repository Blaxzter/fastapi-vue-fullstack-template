<template>
  <Card>
    <CardHeader>
      <CardTitle class="flex items-center gap-2">
        <EditIcon class="h-5 w-5" />
        Update Profile
      </CardTitle>
      <CardDescription>
        Update your profile information. Changes will be processed through Auth0.
      </CardDescription>
    </CardHeader>
    <CardContent>
      <form @submit="onSubmit" class="space-y-6">
        <!-- Name Field -->
        <FormField v-slot="{ componentField }" name="name">
          <FormItem>
            <FormLabel>Display Name</FormLabel>
            <FormControl>
              <Input type="text" placeholder="Enter your display name" v-bind="componentField" />
            </FormControl>
            <FormDescription> This is your display name that others will see. </FormDescription>
            <FormMessage />
          </FormItem>
        </FormField>

        <!-- Nickname Field -->
        <FormField v-slot="{ componentField }" name="nickname">
          <FormItem>
            <FormLabel>Nickname</FormLabel>
            <FormControl>
              <Input type="text" placeholder="Enter your nickname" v-bind="componentField" />
            </FormControl>
            <FormDescription> A shorter name or alias for your profile. </FormDescription>
            <FormMessage />
          </FormItem>
        </FormField>

        <!-- Picture URL Field -->
        <FormField v-if="canEditProfilePicture" v-slot="{ componentField }" name="picture">
          <FormItem>
            <FormLabel>Profile Picture URL</FormLabel>
            <FormControl>
              <Input
                type="url"
                placeholder="https://example.com/your-picture.jpg"
                v-bind="componentField"
              />
            </FormControl>
            <FormDescription>
              URL to your profile picture. Must be a valid image URL.
            </FormDescription>
            <FormMessage />
          </FormItem>
        </FormField>

        <!-- Bio/Description Field -->
        <FormField v-slot="{ componentField }" name="bio">
          <FormItem>
            <FormLabel>Bio</FormLabel>
            <FormControl>
              <Textarea
                placeholder="Tell us a little about yourself"
                class="min-h-[100px]"
                v-bind="componentField"
              />
            </FormControl>
            <FormDescription>
              A short biography or description about yourself (optional).
            </FormDescription>
            <FormMessage />
          </FormItem>
        </FormField>

        <!-- Provider Limitation Notice -->
        <div v-if="!canEditProfilePicture" class="p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <p class="text-sm text-blue-700">
            <InfoIcon class="h-4 w-4 inline mr-1" />
            Profile picture changes are not available for {{ authProviderName }} accounts. Please
            update your profile picture through your {{ authProviderName }} account settings.
          </p>
        </div>

        <!-- Form Actions -->
        <div class="flex items-center gap-4 pt-4">
          <Button type="submit" :disabled="isSubmitting" class="flex items-center gap-2">
            <LoaderIcon v-if="isSubmitting" class="h-4 w-4 animate-spin" />
            <SaveIcon v-else class="h-4 w-4" />
            {{ isSubmitting ? 'Updating...' : 'Update Profile' }}
          </Button>
          <Button type="button" variant="outline" @click="resetForm" :disabled="isSubmitting">
            Reset
          </Button>
        </div>
      </form>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { toTypedSchema } from '@vee-validate/zod'
import { EditIcon, InfoIcon, LoaderIcon, SaveIcon } from 'lucide-vue-next'
import { useForm } from 'vee-validate'
import { toast } from 'vue-sonner'

import { useAuthenticatedClient } from '@/composables/useAuthenticatedClient'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

import { zUserProfileUpdate } from '@/client/zod.gen'

interface Props {
  user: any // You might want to type this properly based on your user interface
  canEditProfilePicture: boolean
  authProviderName: string
}

interface Emits {
  (e: 'profile-updated', values: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Validation schema
const profileSchema = toTypedSchema(zUserProfileUpdate)

// Composables
const { patch } = useAuthenticatedClient()

// Reactive data
const isSubmitting = ref(false)

// Form setup
const form = useForm({
  validationSchema: profileSchema,
  initialValues: {
    name: '',
    nickname: '',
    picture: '',
    bio: '',
  },
})

// Initialize form with current user data
onMounted(() => {
  if (props.user) {
    const formValues: any = {
      name: props.user.name || '',
      nickname: props.user.nickname || '',
      bio: props.user.bio || '',
    }

    // Only include picture if it can be edited
    if (props.canEditProfilePicture) {
      formValues.picture = props.user.picture || ''
    }

    form.setValues(formValues)
  }
})

// Form submission
const onSubmit = form.handleSubmit(async (values) => {
  if (!props.user) {
    showError('User not authenticated')
    return
  }

  isSubmitting.value = true
  try {
    await updateUserProfile(values)
    showSuccess()
    emit('profile-updated', values)
  } catch (error) {
    console.error('Error updating profile:', error)
    showError('Failed to update profile. Please try again.')
  } finally {
    isSubmitting.value = false
  }
})

// Update user profile via API
const updateUserProfile = async (values: any) => {
  try {
    const updateData: any = {
      name: values.name,
      nickname: values.nickname,
      bio: values.bio,
    }

    // Only include picture if it can be edited
    if (props.canEditProfilePicture && values.picture !== undefined) {
      updateData.picture = values.picture || undefined
    }

    await patch({
      url: '/users/me',
      body: updateData,
    })
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}

// Reset form to current user values
const resetForm = () => {
  if (props.user) {
    const formValues: any = {
      name: props.user.name || '',
      nickname: props.user.nickname || '',
      bio: props.user.bio || '',
    }

    // Only include picture if it can be edited
    if (props.canEditProfilePicture) {
      formValues.picture = props.user.picture || ''
    }

    form.setValues(formValues)
  }
}

// Toast functions
const showSuccess = () => {
  toast.success('Profile updated successfully!')
}

const showError = (message: string) => {
  toast.error(message)
}
</script>
