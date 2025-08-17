import { useDialogStore } from '@/stores/dialog'
import type { DialogConfig } from '@/stores/dialog'

/**
 * Composable for easy dialog usage
 */
export function useDialog() {
  const dialogStore = useDialogStore()

  /**
   * Show a confirmation dialog
   */
  const confirm = (config: DialogConfig | string): Promise<boolean> => {
    const dialogConfig = typeof config === 'string' ? { text: config } : config
    return dialogStore.confirm(dialogConfig)
  }

  /**
   * Show an alert dialog
   */
  const alert = (config: Omit<DialogConfig, 'type'> | string): Promise<void> => {
    const dialogConfig = typeof config === 'string' ? { text: config } : config
    return dialogStore.alert(dialogConfig)
  }

  /**
   * Show an info dialog
   */
  const info = (config: Omit<DialogConfig, 'type'> | string): Promise<void> => {
    const dialogConfig =
      typeof config === 'string'
        ? { text: config, type: 'info' }
        : { ...config, type: 'info' as const }
    return dialogStore.alert(dialogConfig)
  }

  /**
   * Show a destructive confirmation dialog (for dangerous actions)
   */
  const confirmDestructive = (config: DialogConfig | string): Promise<boolean> => {
    const dialogConfig =
      typeof config === 'string'
        ? { text: config, variant: 'destructive' as const }
        : { ...config, variant: 'destructive' as const }
    return dialogStore.confirm(dialogConfig)
  }

  return {
    confirm,
    alert,
    info,
    confirmDestructive,
    close: dialogStore.close,
  }
}
