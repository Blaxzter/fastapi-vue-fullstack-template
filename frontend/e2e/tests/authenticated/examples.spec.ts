import { expect, test } from '@playwright/test'

const examplesOverviewHeading = /Examples Overview|Beispiele/i
const breadcrumbHeading = /Dynamic Breadcrumb Examples|Dynamische Breadcrumb Beispiele/i
const dialogHeading = /Dialog Examples|Dialog Beispiele/i
const layoutHeading = /Layout System Demo/i
const errorHandlingHeading = /Error Handling Demo|Fehlerbehandlung Demo/i

test.describe('examples views', () => {
  test('sidebar navigation includes all example pages', async ({ page }) => {
    await page.goto('/app/home')

    const breadcrumbLink = page.getByRole('link', { name: 'Breadcrumb Examples' })
    const layoutLink = page.getByRole('link', { name: 'Layout Demo' })
    const dialogLink = page.getByRole('link', { name: 'Dialog Examples' })
    const errorHandlingLink = page.getByRole('link', { name: 'Error Handling Demo' })

    await expect(breadcrumbLink).toBeVisible()
    await expect(layoutLink).toBeVisible()
    await expect(dialogLink).toBeVisible()
    await expect(errorHandlingLink).toBeVisible()

    await breadcrumbLink.click()
    await expect(page).toHaveURL(/\/app\/breadcrumb-examples$/)
    await expect(page.getByRole('heading', { name: breadcrumbHeading })).toBeVisible()

    await layoutLink.click()
    await expect(page).toHaveURL(/\/app\/layout-demo$/)
    await expect(page.getByRole('heading', { name: layoutHeading })).toBeVisible()

    await dialogLink.click()
    await expect(page).toHaveURL(/\/app\/dialog-examples$/)
    await expect(page.getByRole('heading', { name: dialogHeading })).toBeVisible()

    await errorHandlingLink.click()
    await expect(page).toHaveURL(/\/app\/error-handling-demo$/)
    await expect(page.getByRole('heading', { name: errorHandlingHeading })).toBeVisible()
  })

  test('examples overview cards route to each demo', async ({ page }) => {
    await page.goto('/app/examples')

    await expect(page.getByRole('heading', { name: examplesOverviewHeading })).toBeVisible()

    const examplesCards = page.locator('div.cursor-pointer').filter({ has: page.locator('h3') })
    await expect(examplesCards).toHaveCount(4)

    await examplesCards
      .filter({ has: page.getByRole('heading', { name: /Layout Demo/i }) })
      .click()
    await expect(page).toHaveURL(/\/app\/layout-demo$/)

    await page.goto('/app/examples')
    await examplesCards
      .filter({ has: page.getByRole('heading', { name: dialogHeading }) })
      .click()
    await expect(page).toHaveURL(/\/app\/dialog-examples$/)

    await page.goto('/app/examples')
    await examplesCards
      .filter({ has: page.getByRole('heading', { name: errorHandlingHeading }) })
      .click()
    await expect(page).toHaveURL(/\/app\/error-handling-demo$/)
  })

  test('example views expose interactive features', async ({ page }) => {
    await page.goto('/app/breadcrumb-examples')
    await expect(page.getByRole('heading', { name: breadcrumbHeading })).toBeVisible()
    await page.getByRole('button', { name: /Set Static Breadcrumb|Statische Breadcrumb setzen/i }).click()
    await expect(page.getByText(/Static Example|Statisches Beispiel/i)).toBeVisible()

    await page.goto('/app/dialog-examples')
    await expect(page.getByRole('heading', { name: dialogHeading })).toBeVisible()
    await page
      .getByRole('button', { name: /Show Confirm Dialog|Best.tigungsdialog zeigen/i })
      .click()
    await page.getByRole('dialog').getByRole('button', { name: /Confirm|Best.tigen/i }).click()
    await expect(page.getByText(/User confirmed|Benutzer hat best.tigt/i)).toBeVisible()

    await page.goto('/app/error-handling-demo')
    await expect(page.getByRole('heading', { name: errorHandlingHeading })).toBeVisible()
    await page.getByRole('button', { name: /Not Found Error/i }).click()
    await page.getByRole('button', { name: 'Get Message' }).first().click()
    await expect(page.getByRole('heading', { name: 'Results' })).toBeVisible()
    await expect(page.getByText('Project with ID 123 not found')).toBeVisible()
  })
})
