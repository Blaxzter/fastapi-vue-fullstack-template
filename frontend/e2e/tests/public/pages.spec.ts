import { test, expect } from '@playwright/test';

test.describe('Public Pages', () => {
  test('landing page loads correctly', async ({ page }) => {
    await page.goto('/');
    
    // Test that the page loads
    await expect(page).toHaveTitle(/.*/)
    
    // Add specific assertions for your landing page
    // For example:
    // await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible()
    // await expect(page.getByText('Get started')).toBeVisible()
  });

  test('about page is accessible', async ({ page }) => {
    await page.goto('/about');
    
    // Test that the about page loads
    await expect(page).toHaveURL(/.*\/about/)
    
    // Add specific assertions for your about page
    // For example:
    // await expect(page.getByRole('heading', { name: 'About Us' })).toBeVisible()
  });

  test('navigation works between public pages', async ({ page }) => {
    await page.goto('/');
    
    // Test navigation to about page
    await page.getByRole('link', { name: /about/i }).click();
    await expect(page).toHaveURL(/.*\/about/);
    
    // Test navigation back to home
    await page.getByRole('link', { name: /home/i }).click();
    await expect(page).toHaveURL('/');
  });
});
