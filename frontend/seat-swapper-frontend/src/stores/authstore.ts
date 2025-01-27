import { writable } from 'svelte/store';

// Initialize authStore based on whether we're in the browser or not
export const authStore = writable({
    token: (typeof window !== 'undefined' && localStorage.getItem('token')) || null, // Check if window exists (browser)
    user: (typeof window !== 'undefined' && JSON.parse(localStorage.getItem('user') || 'null')) || null, // Same for user
});

// Set auth data in both the store and localStorage (only in the browser)
export function setAuth(token: string, user: any) {
    authStore.set({ token, user });

    if (typeof window !== 'undefined') {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
    }
}

// Clear auth data in both the store and localStorage (only in the browser)
export function clearAuth() {
    authStore.set({ token: null, user: null });

    if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    }
}
