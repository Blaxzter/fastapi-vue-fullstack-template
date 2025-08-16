import { ref } from 'vue'
import { defineStore } from 'pinia'

export interface DialogConfig {
  title?: string
  text: string
  confirmText?: string
  cancelText?: string
  confirmIcon?: string
  cancelIcon?: string
  type?: 'confirm' | 'alert' | 'info'
  variant?: 'default' | 'destructive' | 'secondary'
}

export interface DialogState extends DialogConfig {
  isOpen: boolean
  onConfirm?: () => void | Promise<void>
  onCancel?: () => void | Promise<void>
}

export const useDialogStore = defineStore('dialog', () => {
  const dialog = ref<DialogState>({
    isOpen: false,
    title: '',
    text: '',
    type: 'confirm',
    variant: 'default'
  })

  const confirm = (config: DialogConfig): Promise<boolean> => {
    return new Promise((resolve) => {
      dialog.value = {
        ...config,
        isOpen: true,
        type: config.type || 'confirm',
        variant: config.variant || 'default',
        onConfirm: () => {
          close()
          resolve(true)
        },
        onCancel: () => {
          close()
          resolve(false)
        }
      }
    })
  }

  const alert = (config: Omit<DialogConfig, 'type'>): Promise<void> => {
    return new Promise((resolve) => {
      dialog.value = {
        ...config,
        isOpen: true,
        type: 'alert',
        variant: config.variant || 'default',
        onConfirm: () => {
          close()
          resolve()
        }
      }
    })
  }

  const close = () => {
    dialog.value.isOpen = false
  }

  return {
    dialog,
    confirm,
    alert,
    close
  }
})
