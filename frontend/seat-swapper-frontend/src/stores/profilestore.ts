import { writable } from 'svelte/store';

export const profileStore = writable({
    user: -1,
    student_id: '',
    full_name: '',
    email: '',
});

// Set the profile data
export function setProfile(profileData: {user: number; student_id: string; full_name: string; email: string }) {
    profileStore.set(profileData);
}

// Clear the profile data
export function clearProfile() {
    profileStore.set({
        user: -1,
        student_id: '',
        full_name: '',
        email: '',
    });
}
