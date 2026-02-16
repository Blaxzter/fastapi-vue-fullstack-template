import { expect, test } from '@playwright/test'

test.describe('authenticated routes', () => {
  test('can open dashboard home', async ({ page }) => {
    await page.goto('/app/home')
    await expect(page).toHaveURL(/\/app\/home/)
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()
  })

  test('can open settings page', async ({ page }) => {
    await page.goto('/app/settings')
    await expect(page).toHaveURL(/\/app\/settings/)
  })
})
