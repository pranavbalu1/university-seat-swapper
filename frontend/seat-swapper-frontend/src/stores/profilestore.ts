import { writable } from 'svelte/store';

export const profileStore = writable({
    student_id: '',
    full_name: '',
    email: '',
});

// Set the profile data
export function setProfile(profileData: { student_id: string; full_name: string; email: string }) {
    profileStore.set(profileData);
}

// Clear the profile data
export function clearProfile() {
    profileStore.set({
        student_id: '',
        full_name: '',
        email: '',
    });
}
