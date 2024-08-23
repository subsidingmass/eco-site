import { setTheme as setThemeChanger } from 'theme-changer';

export function setTheme(theme: string): void {
  if (typeof window !== 'undefined') { // Ensure this runs only in the browser
    localStorage.setItem('theme', theme);
    setThemeChanger(theme);
  }
}

export function getTheme(): string | null {
  if (typeof window !== 'undefined') { // Ensure this runs only in the browser
    return localStorage.getItem('theme');
  }
  return null;
}

export function applyTheme(): void {
  const theme = getTheme();
  if (theme) {
    setThemeChanger(theme);
  }
}