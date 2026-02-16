import { expect, test } from '@playwright/test'

test.describe('projects and tasks views', () => {
  test('supports project and task CRUD flows against real backend', async ({ page }) => {
    const stamp = Date.now()
    const projectName = `E2E Project ${stamp}`
    const updatedProjectName = `${projectName} Updated`
    const taskTitle = `E2E Task ${stamp}`
    const updatedTaskTitle = `${taskTitle} Updated`

    await page.goto('/app/projects')

    await expect(page.getByRole('heading', { name: 'Projects' })).toBeVisible()

    await page.getByRole('button', { name: 'New project' }).click()
    await page.locator('#project-name').fill(projectName)
    await page.locator('#project-description').fill('Created by Playwright E2E test.')
    await page.getByRole('button', { name: 'Create project' }).click()

    const createdProjectCard = page
      .locator('div.rounded-lg.border.bg-background.p-4')
      .filter({ hasText: projectName })

    await expect(createdProjectCard).toBeVisible()

    await createdProjectCard.getByRole('button', { name: 'Edit' }).click()
    await page.locator('#edit-project-name').fill(updatedProjectName)
    await page.getByRole('button', { name: 'Save changes' }).click()

    const updatedProjectCard = page
      .locator('div.rounded-lg.border.bg-background.p-4')
      .filter({ hasText: updatedProjectName })
    await expect(updatedProjectCard).toBeVisible()

    await updatedProjectCard.getByRole('button', { name: 'View' }).click()
    await expect(page).toHaveURL(/\/app\/projects\/[^/]+$/)
    await expect(page.getByRole('heading', { name: updatedProjectName })).toBeVisible()

    await page.getByRole('button', { name: 'New task' }).click()
    await page.locator('#task-title').fill(taskTitle)
    await page.locator('#task-description').fill('Created by Playwright E2E test.')
    await page.locator('#task-due-date').fill('2026-03-21')
    await page.getByRole('button', { name: 'Add task' }).click()

    const createdTaskCard = page
      .locator('div.rounded-lg.border.bg-background.p-4')
      .filter({ hasText: taskTitle })

    await expect(createdTaskCard).toBeVisible()

    await createdTaskCard.getByRole('button', { name: 'Edit' }).click()
    await page.locator('#edit-task-title').fill(updatedTaskTitle)
    await page.getByRole('button', { name: 'Save changes' }).click()

    const updatedTaskCard = page
      .locator('div.rounded-lg.border.bg-background.p-4')
      .filter({ hasText: updatedTaskTitle })
    await expect(updatedTaskCard).toBeVisible()

    await updatedTaskCard.getByRole('button', { name: 'Delete' }).click()
    await page.getByRole('dialog').getByRole('button', { name: 'Delete' }).click()
    await expect(updatedTaskCard).toHaveCount(0)

    await page.getByRole('button', { name: 'Back to projects' }).click()
    await expect(page).toHaveURL(/\/app\/projects$/)
    await expect(page.getByRole('heading', { name: 'Projects' })).toBeVisible()

    await page.locator('#project-search').fill(updatedProjectName)
    await page.getByRole('button', { name: 'Apply filters' }).click()

    const projectCardForCleanup = page
      .locator('div.rounded-lg.border.bg-background.p-4')
      .filter({ hasText: updatedProjectName })
      .first()

    await expect(projectCardForCleanup).toBeVisible()
    await projectCardForCleanup.getByRole('button', { name: 'Delete' }).click()
    await page.getByRole('dialog').getByRole('button', { name: 'Delete' }).click()
    await expect(projectCardForCleanup).toHaveCount(0)
  })
})
