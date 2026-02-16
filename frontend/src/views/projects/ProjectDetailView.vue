<template>
  <div class="mx-auto max-w-6xl space-y-6">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="space-y-1">
        <div class="flex items-center gap-2 text-sm text-muted-foreground">
          <Button variant="ghost" size="sm" @click="goBack">Back to projects</Button>
        </div>
        <h1 class="text-3xl font-bold tracking-tight">
          {{ project?.name || 'Project' }}
        </h1>
        <p class="text-muted-foreground">
          {{ project?.description || 'Track tasks and progress for this project.' }}
        </p>
      </div>
      <div class="flex items-center gap-2">
        <Badge v-if="project" :variant="project.status === 'archived' ? 'secondary' : 'default'">
          {{ project.status }}
        </Badge>
        <Dialog v-model:open="createDialogOpen">
          <DialogTrigger as-child>
            <Button>
              <PlusIcon class="h-4 w-4 mr-2" />
              New task
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle class="flex items-center gap-2">
                <PlusIcon class="h-5 w-5" />
                New task
              </DialogTitle>
              <DialogDescription>Add a task to keep the work moving.</DialogDescription>
            </DialogHeader>
            <form class="grid gap-4 md:grid-cols-3" @submit.prevent="createTask">
              <div class="md:col-span-1">
                <Label for="task-title">Title</Label>
                <Input id="task-title" v-model="newTask.title" class="mt-2" />
              </div>
              <div class="md:col-span-1">
                <Label for="task-status">Status</Label>
                <Select v-model="newTask.status">
                  <SelectTrigger id="task-status" class="mt-2">
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="todo">Todo</SelectItem>
                    <SelectItem value="in_progress">In progress</SelectItem>
                    <SelectItem value="done">Done</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div class="md:col-span-1">
                <Label for="task-priority">Priority</Label>
                <Select v-model="newTask.priority">
                  <SelectTrigger id="task-priority" class="mt-2">
                    <SelectValue placeholder="Priority" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">1</SelectItem>
                    <SelectItem value="2">2</SelectItem>
                    <SelectItem value="3">3</SelectItem>
                    <SelectItem value="4">4</SelectItem>
                    <SelectItem value="5">5</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div class="md:col-span-2">
                <Label for="task-description">Description</Label>
                <Textarea id="task-description" v-model="newTask.description" class="mt-2" />
              </div>
              <div class="md:col-span-1">
                <Label for="task-due-date">Due date</Label>
                <Input id="task-due-date" type="date" v-model="newTask.due_date" class="mt-2" />
              </div>
              <div class="md:col-span-3 flex flex-wrap items-center gap-3">
                <Button type="submit" :disabled="creating || !newTask.title.trim()">
                  <PlusIcon class="h-4 w-4 mr-2" />
                  Add task
                </Button>
                <Button type="button" variant="outline" @click="resetNewTask" :disabled="creating">
                  Reset
                </Button>
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
      </div>
    </div>

    <Card>
      <CardHeader class="space-y-3">
        <CardTitle>Tasks</CardTitle>
        <div class="grid gap-3 md:grid-cols-3">
          <div class="md:col-span-2">
            <Label for="task-search">Search</Label>
            <Input
              id="task-search"
              v-model="filters.search"
              placeholder="Search tasks"
              class="mt-2"
            />
          </div>
          <div>
            <Label for="task-filter-status">Status</Label>
            <Select v-model="filters.status">
              <SelectTrigger id="task-filter-status" class="mt-2">
                <SelectValue placeholder="All statuses" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="todo">Todo</SelectItem>
                <SelectItem value="in_progress">In progress</SelectItem>
                <SelectItem value="done">Done</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div class="flex items-center justify-between text-sm text-muted-foreground">
          <span>{{ totalLabel }}</span>
          <Button variant="ghost" @click="loadTasks" :disabled="loading">Apply filters</Button>
        </div>
        <div class="mt-4 grid gap-4">
          <div v-for="task in tasks" :key="task.id" class="rounded-lg border bg-background p-4">
            <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div class="space-y-2">
                <div class="flex flex-wrap items-center gap-2">
                  <h3 class="text-lg font-semibold">{{ task.title }}</h3>
                  <Badge :variant="statusVariant(task.status)">{{ task.status }}</Badge>
                  <Badge variant="outline">Priority {{ task.priority }}</Badge>
                </div>
                <p class="text-sm text-muted-foreground">
                  {{ task.description || 'No description yet.' }}
                </p>
                <p v-if="task.due_date" class="text-xs text-muted-foreground">
                  Due: {{ task.due_date }}
                </p>
              </div>
              <div class="flex items-center gap-2">
                <Button variant="ghost" @click="startEdit(task)">
                  <PencilIcon class="h-4 w-4 mr-2" />
                  Edit
                </Button>
                <Button variant="destructive" @click="removeTask(task)">
                  <Trash2Icon class="h-4 w-4 mr-2" />
                  Delete
                </Button>
              </div>
            </div>
          </div>

          <div v-if="!tasks.length && !loading" class="text-center text-sm text-muted-foreground">
            No tasks yet. Add one with the New task button.
          </div>
        </div>
      </CardContent>
    </Card>

    <Dialog v-model:open="editDialogOpen">
      <DialogContent>
        <DialogHeader>
          <DialogTitle class="flex items-center gap-2">
            <PencilIcon class="h-5 w-5" />
            Edit task
          </DialogTitle>
          <DialogDescription>Update task details and progress.</DialogDescription>
        </DialogHeader>
        <form class="grid gap-4 md:grid-cols-3" @submit.prevent="updateTask">
          <div class="md:col-span-1">
            <Label for="edit-task-title">Title</Label>
            <Input id="edit-task-title" v-model="editForm.title" class="mt-2" />
          </div>
          <div class="md:col-span-1">
            <Label for="edit-task-status">Status</Label>
            <Select v-model="editForm.status">
              <SelectTrigger id="edit-task-status" class="mt-2">
                <SelectValue placeholder="Select status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="todo">Todo</SelectItem>
                <SelectItem value="in_progress">In progress</SelectItem>
                <SelectItem value="done">Done</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="md:col-span-1">
            <Label for="edit-task-priority">Priority</Label>
            <Select v-model="editForm.priority">
              <SelectTrigger id="edit-task-priority" class="mt-2">
                <SelectValue placeholder="Priority" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1">1</SelectItem>
                <SelectItem value="2">2</SelectItem>
                <SelectItem value="3">3</SelectItem>
                <SelectItem value="4">4</SelectItem>
                <SelectItem value="5">5</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="md:col-span-2">
            <Label for="edit-task-description">Description</Label>
            <Textarea id="edit-task-description" v-model="editForm.description" class="mt-2" />
          </div>
          <div class="md:col-span-1">
            <Label for="edit-task-due">Due date</Label>
            <Input id="edit-task-due" type="date" v-model="editForm.due_date" class="mt-2" />
          </div>
          <div class="md:col-span-3 flex items-center gap-3">
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

import { PencilIcon, PlusIcon, Trash2Icon } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

import { useAuthenticatedClient } from '@/composables/useAuthenticatedClient'
import { useDialog } from '@/composables/useDialog'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
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
  ProjectRead,
  TaskCreate,
  TaskListResponse,
  TaskRead,
  TaskUpdate,
} from '@/client/types.gen'
import { toastApiError } from '@/lib/api-errors'

const route = useRoute()
const router = useRouter()
const dialog = useDialog()
const { t } = useI18n()
const { get, post, patch, delete: del } = useAuthenticatedClient()

const project = ref<ProjectRead | null>(null)
const tasks = ref<TaskRead[]>([])
const loading = ref(false)
const creating = ref(false)
const updating = ref(false)
const total = ref(0)
const createDialogOpen = ref(false)
const editDialogOpen = ref(false)

const projectId = computed(() => route.params.projectId as string)

const filters = ref({
  search: '',
  status: 'all',
})

type TaskFormState = Pick<TaskCreate, 'title' | 'description' | 'status' | 'due_date'> & {
  priority: string
}

const newTask = ref<TaskFormState>({
  title: '',
  description: '',
  status: 'todo',
  priority: '3',
  due_date: '',
})

const editingTask = ref<TaskRead | null>(null)
const editForm = ref<TaskUpdate>({
  title: '',
  description: '',
  status: 'todo',
  priority: 3,
  due_date: '',
})

const totalLabel = computed(() => `${total.value} task${total.value === 1 ? '' : 's'}`)

const statusVariant = (status?: TaskRead['status']) => {
  if (status === 'done') return 'secondary'
  if (status === 'in_progress') return 'default'
  return 'outline'
}

const goBack = () => {
  router.push({ name: 'projects' })
}

const loadProject = async () => {
  try {
    const response = (await get({
      url: `/projects/${projectId.value}`,
    })) as { data: ProjectRead }
    project.value = response.data
  } catch (error) {
    toastApiError(error, t('common.errors.api.loadProject'))
  }
}

const loadTasks = async () => {
  loading.value = true
  try {
    const query: Record<string, unknown> = {
      project_id: projectId.value,
      skip: 0,
      limit: 100,
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
      url: '/tasks',
      query,
    })) as { data: TaskListResponse }

    tasks.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    toastApiError(error, t('common.errors.api.loadTasks'))
  } finally {
    loading.value = false
  }
}

const resetNewTask = () => {
  newTask.value = {
    title: '',
    description: '',
    status: 'todo',
    priority: '3',
    due_date: '',
  }
}

watch(createDialogOpen, (isOpen) => {
  if (!isOpen) {
    resetNewTask()
  }
})

watch(editDialogOpen, (isOpen) => {
  if (!isOpen) {
    editingTask.value = null
  }
})

const createTask = async () => {
  if (!newTask.value.title.trim()) {
    toast.error(t('common.errors.api.taskTitleRequired'))
    return
  }
  creating.value = true
  try {
    await post({
      url: '/tasks',
      body: {
        project_id: projectId.value,
        title: newTask.value.title.trim(),
        description: newTask.value.description.trim() || null,
        status: newTask.value.status,
        priority: Number(newTask.value.priority) || 3,
        due_date: newTask.value.due_date || null,
      },
    })
    toast.success('Task created')
    createDialogOpen.value = false
    await loadTasks()
  } catch (error) {
    toastApiError(error, t('common.errors.api.createTask'))
  } finally {
    creating.value = false
  }
}

const startEdit = (task: TaskRead) => {
  editingTask.value = task
  editForm.value = {
    title: task.title,
    description: task.description || '',
    status: task.status ?? 'todo',
    priority: String(task.priority ?? 3),
    due_date: task.due_date || '',
  }
  editDialogOpen.value = true
}

const cancelEdit = () => {
  editDialogOpen.value = false
}

const updateTask = async () => {
  if (!editingTask.value) return
  updating.value = true
  try {
    await patch({
      url: `/tasks/${editingTask.value.id}`,
      body: {
        title: editForm.value.title.trim(),
        description: editForm.value.description.trim() || null,
        status: editForm.value.status,
        priority: Number(editForm.value.priority) || 3,
        due_date: editForm.value.due_date || null,
      },
    })
    toast.success('Task updated')
    editDialogOpen.value = false
    await loadTasks()
  } catch (error) {
    toastApiError(error, t('common.errors.api.updateTask'))
  } finally {
    updating.value = false
  }
}

const removeTask = async (task: TaskRead) => {
  const confirmed = await dialog.confirmDestructive({
    title: 'Delete task',
    text: `Delete "${task.title}"? This cannot be undone.`,
    confirmText: 'Delete',
  })
  if (!confirmed) return

  try {
    await del({ url: `/tasks/${task.id}` })
    toast.success('Task deleted')
    await loadTasks()
  } catch (error) {
    toastApiError(error, t('common.errors.api.deleteTask'))
  }
}

onMounted(async () => {
  await loadProject()
  await loadTasks()
})

watch(projectId, async () => {
  await loadProject()
  await loadTasks()
})
</script>
