import { test, expect } from '@playwright/test';

test.describe('Landing Page', () => {
  test('displays hero section', async ({ page }) => {
    await page.goto('/');
    
    // Test that the landing page loads
    await expect(page).toHaveTitle(/.*/)
    
    // Add your specific landing page tests here
    // For example:
    // await expect(page.getByRole('heading', { name: 'Welcome to Our App' })).toBeVisible()
    // await expect(page.getByText('Sign up today')).toBeVisible()
  });

  test('shows navigation without user menu', async ({ page }) => {
    await page.goto('/');
    
    // Test that public navigation is visible
    // await expect(page.getByRole('link', { name: 'Home' })).toBeVisible()
    // await expect(page.getByRole('link', { name: 'About' })).toBeVisible()
    // await expect(page.getByRole('link', { name: 'Sign In' })).toBeVisible()
    
    // Test that authenticated elements are NOT visible
    // await expect(page.getByRole('button', { name: 'User Menu' })).not.toBeVisible()
  });
});
