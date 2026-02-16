import { expect, test } from '@playwright/test'

test.describe('public pages', () => {
  test('about page is accessible', async ({ page }) => {
    await page.goto('/about')
    await expect(page).toHaveURL(/\/about/)
    await expect(page.getByRole('heading', { name: 'About' })).toBeVisible()
  })

  test('navigation works between landing and about', async ({ page }) => {
    await page.goto('/')
    await page.getByRole('button', { name: 'About' }).click()
    await expect(page).toHaveURL(/\/about/)

    await page.getByRole('button', { name: 'Back to Home' }).click()
    await expect(page).toHaveURL('/')
  })
})
