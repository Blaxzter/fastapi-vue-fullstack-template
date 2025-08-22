import { test, expect } from '@playwright/test';

test.describe('User Dashboard - Authenticated', () => {
  test('shows user dashboard after login', async ({ page }) => {
    // This test will automatically use the authenticated state
    await page.goto('/dashboard');
    
    // Test authenticated content
    // await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()
    // await expect(page.getByText('Welcome back')).toBeVisible()
    // await expect(page.getByRole('button', { name: 'User Menu' })).toBeVisible()
  });

  test('can access user settings', async ({ page }) => {
    await page.goto('/settings');
    
    // Test authenticated settings page
    // await expect(page.getByRole('heading', { name: 'User Settings' })).toBeVisible()
    // await expect(page.getByRole('textbox', { name: 'Email' })).toBeVisible()
  });
});
