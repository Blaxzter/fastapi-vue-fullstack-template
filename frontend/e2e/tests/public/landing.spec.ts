import { expect, test } from '@playwright/test'

test.describe('landing page', () => {
  test('renders main hero and auth actions', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('heading', { name: 'Welcome to Your App' })).toBeVisible()
    await expect(page.getByRole('button', { name: 'Get Started' })).toBeVisible()
    await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible()
  })
})
