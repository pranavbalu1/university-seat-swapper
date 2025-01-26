import { writable } from 'svelte/store';

export const authStore = writable({
    token: null as string | null,
    user: null as any,
});

export function setAuth(token: string, user: any) {
    authStore.set({ token, user });
}

export function clearAuth() {
    authStore.set({ token: null, user: null });
}
