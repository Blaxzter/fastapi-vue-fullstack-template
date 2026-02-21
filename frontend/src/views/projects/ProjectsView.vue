<template>
  <div class="mx-auto max-w-6xl space-y-6">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="space-y-1">
        <h1 class="text-3xl font-bold tracking-tight">Projects</h1>
        <p class="text-muted-foreground">Create, track, and organize your project work.</p>
      </div>
      <div class="flex items-center gap-2">
        <Dialog v-model:open="createDialogOpen">
          <DialogTrigger as-child>
            <Button>
              <PlusIcon class="h-4 w-4 mr-2" />
              New project
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle class="flex items-center gap-2">
                <PlusIcon class="h-5 w-5" />
                New project
              </DialogTitle>
              <DialogDescription>Start a project and add tasks as you go.</DialogDescription>
            </DialogHeader>
            <form class="grid gap-4" @submit.prevent="createProject">
              <div>
                <Label for="project-name">Name</Label>
                <Input
                  id="project-name"
                  v-model="newProject.name"
                  placeholder="Project name"
                  class="mt-2"
                />
              </div>
              <div>
                <Label for="project-description">Description</Label>
                <Textarea
                  id="project-description"
                  v-model="newProject.description"
                  placeholder="Short description"
                  class="mt-2 min-h-[64px]"
                />
              </div>
              <div>
                <Label for="project-status">Status</Label>
                <Select v-model="newProject.status">
                  <SelectTrigger id="project-status" class="mt-2 w-full">
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="archived">Archived</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div class="flex flex-wrap items-center gap-3">
                <Button type="submit" :disabled="creating || !newProject.name.trim()">
                  <PlusIcon class="h-4 w-4 mr-2" />
                  Create project
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  @click="resetNewProject"
                  :disabled="creating"
                >
                  Reset
                </Button>
                <!-- spacer component -->
                <div class="flex-1" />
                <Button
                  type="button"
                  variant="ghost"
                  @click="createDialogOpen = false"
                  :disabled="creating"
                >
                  Cancel
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
        <Button variant="outline" @click="loadProjects" :disabled="loading">
          <RefreshCwIcon class="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>
    </div>

    <Card>
      <CardHeader class="space-y-3">
        <CardTitle>Project list</CardTitle>
        <div class="grid gap-3 md:grid-cols-3">
          <div class="md:col-span-2">
            <Label for="project-search">Search</Label>
            <Input
              id="project-search"
              v-model="filters.search"
              placeholder="Search by name or description"
              class="mt-2"
            />
          </div>
          <div>
            <Label for="project-filter-status">Status</Label>
            <Select v-model="filters.status">
              <SelectTrigger id="project-filter-status" class="mt-2">
                <SelectValue placeholder="All statuses" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="archived">Archived</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div class="flex items-center justify-between text-sm text-muted-foreground">
          <span>{{ totalLabel }}</span>
          <Button variant="ghost" @click="loadProjects" :disabled="loading">Apply filters</Button>
        </div>
        <div class="mt-4 grid gap-4">
          <div
            v-for="project in projects"
            :key="project.id"
            class="rounded-lg border bg-background p-4"
          >
            <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div class="space-y-2">
                <div class="flex flex-wrap items-center gap-2">
                  <h3 class="text-lg font-semibold">{{ project.name }}</h3>
                  <Badge :variant="project.status === 'archived' ? 'secondary' : 'default'">
                    {{ project.status }}
                  </Badge>
                </div>
                <p class="text-sm text-muted-foreground">
                  {{ project.description || 'No description yet.' }}
                </p>
              </div>
              <div class="flex items-center gap-2">
                <Button variant="outline" @click="goToProject(project)">
                  <ArrowRightIcon class="h-4 w-4 mr-2" />
                  View
                </Button>
                <Button variant="ghost" @click="startEdit(project)">
                  <PencilIcon class="h-4 w-4 mr-2" />
                  Edit
                </Button>
                <Button variant="destructive" @click="removeProject(project)">
                  <Trash2Icon class="h-4 w-4 mr-2" />
                  Delete
                </Button>
              </div>
            </div>
          </div>

          <div
            v-if="!projects.length && !loading"
            class="text-center text-sm text-muted-foreground"
          >
            No projects found. Create your first project with the New project button.
          </div>
        </div>
      </CardContent>
    </Card>

    <Dialog v-model:open="editDialogOpen">
      <DialogContent>
        <DialogHeader>
          <DialogTitle class="flex items-center gap-2">
            <PencilIcon class="h-5 w-5" />
            Edit project
          </DialogTitle>
          <DialogDescription>Update details and save changes.</DialogDescription>
        </DialogHeader>
        <form class="grid gap-4" @submit.prevent="updateProject">
          <div>
            <Label for="edit-project-name">Name</Label>
            <Input id="edit-project-name" v-model="editForm.name" class="mt-2" />
          </div>
          <div>
            <Label for="edit-project-description">Description</Label>
            <Textarea
              id="edit-project-description"
              v-model="editForm.description"
              class="mt-2 min-h-[64px]"
            />
          </div>
          <div>
            <Label for="edit-project-status">Status</Label>
            <Select v-model="editForm.status">
              <SelectTrigger id="edit-project-status" class="mt-2 w-full">
                <SelectValue placeholder="Select status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="archived">Archived</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="flex items-center gap-3">
            <Button type="submit" :disabled="updating"> Save changes </Button>
            <Button type="button" variant="ghost" @click="cancelEdit" :disabled="updating">
              Cancel
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'

import { ArrowRightIcon, PencilIcon, PlusIcon, RefreshCwIcon, Trash2Icon } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

import { useAuthenticatedClient } from '@/composables/useAuthenticatedClient'
import { useDialog } from '@/composables/useDialog'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'

import type {
  ProjectCreate,
  ProjectListResponse,
  ProjectRead,
  ProjectUpdate,
} from '@/client/types.gen'
import { toastApiError } from '@/lib/api-errors'

const router = useRouter()
const dialog = useDialog()
const { t } = useI18n()
const { get, post, patch, delete: del } = useAuthenticatedClient()

const projects = ref<ProjectRead[]>([])
const loading = ref(false)
const creating = ref(false)
const updating = ref(false)
const total = ref(0)
const createDialogOpen = ref(false)
const editDialogOpen = ref(false)

const filters = ref({
  search: '',
  status: 'all',
})

type ProjectFormState = {
  name: string
  description: string
  status: ProjectCreate['status']
}

type ProjectEditFormState = {
  name: string
  description: string
  status: ProjectUpdate['status']
}

const newProject = ref<ProjectFormState>({
  name: '',
  description: '',
  status: 'active',
})

const editingProject = ref<ProjectRead | null>(null)
const editForm = ref<ProjectEditFormState>({
  name: '',
  description: '',
  status: 'active',
})

const totalLabel = computed(() => `${total.value} project${total.value === 1 ? '' : 's'}`)

const loadProjects = async () => {
  loading.value = true
  try {
    const query: Record<string, unknown> = {
      skip: 0,
      limit: 50,
      sort_by: 'created_at',
      sort_dir: 'desc',
    }
    if (filters.value.search.trim()) {
      query.search = filters.value.search.trim()
    }
    if (filters.value.status !== 'all') {
      query.status = filters.value.status
    }

    const response = (await get({
      url: '/projects/me',
      query,
    })) as { data: ProjectListResponse }

    projects.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    toastApiError(error, t('common.errors.api.loadProjects'))
  } finally {
    loading.value = false
  }
}

const resetNewProject = () => {
  newProject.value = { name: '', description: '', status: 'active' }
}

watch(createDialogOpen, (isOpen) => {
  if (!isOpen) {
    resetNewProject()
  }
})

watch(editDialogOpen, (isOpen) => {
  if (!isOpen) {
    editingProject.value = null
  }
})

const createProject = async () => {
  if (!newProject.value.name.trim()) {
    toast.error(t('common.errors.api.projectNameRequired'))
    return
  }

  creating.value = true
  try {
    await post({
      url: '/projects',
      body: {
        name: newProject.value.name.trim(),
        description: newProject.value.description.trim() || null,
        status: newProject.value.status,
      },
    })
    toast.success('Project created')
    createDialogOpen.value = false
    await loadProjects()
  } catch (error) {
    toastApiError(error, t('common.errors.api.createProject'))
  } finally {
    creating.value = false
  }
}

const startEdit = (project: ProjectRead) => {
  editingProject.value = project
  editForm.value = {
    name: project.name,
    description: project.description || '',
    status: project.status,
  }
  editDialogOpen.value = true
}

const cancelEdit = () => {
  editDialogOpen.value = false
}

const updateProject = async () => {
  if (!editingProject.value) return
  updating.value = true
  try {
    await patch({
      url: `/projects/${editingProject.value.id}`,
      body: {
        name: editForm.value.name.trim(),
        description: editForm.value.description.trim() || null,
        status: editForm.value.status,
      },
    })
    toast.success('Project updated')
    editDialogOpen.value = false
    await loadProjects()
  } catch (error) {
    toastApiError(error, t('common.errors.api.updateProject'))
  } finally {
    updating.value = false
  }
}

const removeProject = async (project: ProjectRead) => {
  const confirmed = await dialog.confirmDestructive({
    title: 'Delete project',
    text: `Delete "${project.name}" and its tasks? This cannot be undone.`,
    confirmText: 'Delete',
  })
  if (!confirmed) return

  try {
    await del({ url: `/projects/${project.id}` })
    toast.success('Project deleted')
    await loadProjects()
  } catch (error) {
    toastApiError(error, t('common.errors.api.deleteProject'))
  }
}

const goToProject = (project: ProjectRead) => {
  router.push({ name: 'project-detail', params: { projectId: project.id } })
}

onMounted(() => {
  loadProjects()
})
</script>
