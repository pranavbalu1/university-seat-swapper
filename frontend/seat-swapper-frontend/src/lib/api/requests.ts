import { PUBLIC_API_BASE_URL } from '$env/static/public';
import { get } from 'svelte/store';
import { authStore } from '../../stores/authstore'; // Import the authStore

// Fetch all class trade requests
export async function getAllClassTradeRequests() {
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/class_trade_requests/all/`, {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to fetch class trade requests.');
    }

    return response.json();
}

// Create a new class trade request
export async function createClassTradeRequest(offeredClassId: number, desiredClassNumber: string, desiredSectionNumber: string) {
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/class_trade_requests/create_class_trade_request`, {
        method: 'POST',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            offered_class_id: offeredClassId,
            desired_class_number: desiredClassNumber,
            desired_section_number: desiredSectionNumber,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create class trade request.');
    }

    return response.json();
}

// Vote on a class trade request
export async function voteOnRequest(requestId: number, upvote: boolean) {
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/class_trade_requests/${requestId}/vote/`, {
        method: 'POST',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ upvote }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to vote on request.');
    }

    return response.json();
}

// Toggle favorite on a class trade request
export async function toggleFavoriteRequest(requestId: number) {
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/class_trade_requests/${requestId}/favorite/`, {
        method: 'POST',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to toggle favorite on request.');
    }

    return response.json();
}

// Delete a class trade request
export async function deleteClassTradeRequest(requestId: number) {
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/class_trade_requests/${requestId}/delete/`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to delete class trade request.');
    }

    return response.json();
}

// Filter class trade requests
export async function filterClassTradeRequests(filters: { course_number?: string; class_name?: string; instructor?: string; status?: string }) {
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const queryParams = new URLSearchParams(filters).toString();
    const response = await fetch(`${PUBLIC_API_BASE_URL}/class_trade_requests/filtered?${queryParams}`, {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to filter class trade requests.');
    }

    return response.json();
}

// Fetch favorite class trade requests
export async function getFavoriteClassTradeRequests() {
    const { token } = get(authStore); // Get token from the store

    if (!token) {
        throw new Error('User is not authenticated');
    }

    const response = await fetch(`${PUBLIC_API_BASE_URL}/class_trade_requests/favorites/`, {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to fetch favorite class trade requests.');
    }

    return response.json();
}