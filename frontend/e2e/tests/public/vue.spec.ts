import { expect, test } from '@playwright/test'

test('root path renders preauth layout', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('button', { name: 'About' })).toBeVisible()
  await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible()
})
