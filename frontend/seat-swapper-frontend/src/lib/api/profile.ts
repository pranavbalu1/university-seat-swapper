import { PUBLIC_API_BASE_URL } from '$env/static/public';
import { get } from 'svelte/store';
import { authStore } from '../../stores/authstore'; // Import the authStore

// Fetch user profile data
export async function getProfile() {
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/profile/get_profile/`, {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to fetch profile.');
    }

    return response.json();
}

// Create or update user profile data
export async function createOrUpdateProfile(profileData: { student_id: string; full_name: string; email: string }) {
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/profile/create_or_update_profile/`, {
        method: 'POST',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to save profile.');
    }

    return response.json();
}
