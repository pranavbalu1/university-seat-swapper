import { PUBLIC_API_BASE_URL } from '$env/static/public';
import { setAuth } from '../../stores/authstore';

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

    const data = await response.json();

    // Store token and user information in authStore
    setAuth(data.token, data.user);

    return data;
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

    const data = await response.json();

    // Store token and user information in authStore
    setAuth(data.token, data.user);

    return data;
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
