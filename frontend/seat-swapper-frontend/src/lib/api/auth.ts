import { PUBLIC_API_BASE_URL } from '$env/static/public';

export async function login(email: string, password: string) {
    const response = await fetch(`${PUBLIC_API_BASE_URL}/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email, password }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to log in.');
    }

    return response.json();
}

export async function register(email: string, password: string) {
    const response = await fetch(`${PUBLIC_API_BASE_URL}/auth/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email, password }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to register.');
    }

    return response.json();
}

export async function testToken(token: string) {
    const response = await fetch(`${PUBLIC_API_BASE_URL}/auth/test_token/`, {
        method: 'GET',
        headers: { Authorization: `Token ${token}` },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Token validation failed.');
    }

    return response.text();
}
