import { PUBLIC_API_BASE_URL } from '$env/static/public';
import { get } from 'svelte/store';
import { authStore } from '../../stores/authstore';
// Fetch user schedule data
export async function getSchedule() {
    const { token } = get(authStore); // Get token from the store
    
    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/profile/get_classes/`, {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to fetch schedule.');
    }

    const data = await response.json();
    return data;
}

export async function add_class(classData: {course_number: '', section_number: '', class_name: '', instructor: '', start_time: '', days: []}){
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/profile/add_class/`, {
        method: 'POST',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(classData),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to add class.');
    }

    return response.json();
}

// Remove class from the user's schedule
export async function remove_class(classData: { course_number: string; section_number: string; }) {
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/profile/remove_class/`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(classData),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to remove class.');
    }

    return response.json();
}
