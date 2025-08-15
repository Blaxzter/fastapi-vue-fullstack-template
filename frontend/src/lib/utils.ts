import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Converts numbered translation keys to an array of translated strings.
 * Useful for handling i18n lists that are stored as numbered object keys.
 *
 * @param translationFn - The translation function from vue-i18n (usually `t`)
 * @param baseKey - The base translation key (e.g., 'preauth.about.sections.techStack.frontend.items')
 * @returns Array of translated strings
 *
 * @example
 * // Given translations like:
 * // "items": { "0": "Vue.js", "1": "TypeScript", "2": "Tailwind" }
 * const items = getTranslationList(t, 'preauth.about.sections.techStack.frontend.items')
 * // Returns: ["Vue.js", "TypeScript", "Tailwind"]
 */
export function getTranslationList(
  translationFn: (key: string) => string,
  baseKey: string,
): string[] {
  const items: string[] = []
  let index = 0

  while (true) {
    const key = `${baseKey}.${index}`
    const item = translationFn(key)

    // If translation doesn't exist, t() returns the key itself
    if (item === key) break

    items.push(item)
    index++
  }

  return items
}
