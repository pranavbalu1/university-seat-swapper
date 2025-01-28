<script lang="ts">
    import { goto } from '$app/navigation';
    import { login } from '$lib/api/auth'; // Import the login API function

    let username = '';
    let password = '';
    let errorMessage = ''; // To display error messages

    const handleLogin = async () => {
        try {
            const { token, user } = await login(username, password); // Call the login API
            // Store the token and user info if needed (e.g., in a global store)
            console.log('Login successful:', user);
            goto('/dashboard'); // Navigate to the dashboard on successful login
        } catch (error: any) {
            errorMessage = error.message; // Display error message if login fails
        }
    };
</script>

<div class="min-h-screen bg-stacked-waves-2 bg-cover bg-no-repeat flex flex-col">
    <!-- Login Section -->
    <div class="flex-grow flex flex-col justify-center items-center px-4 ">
        <h1 class="text-5xl font-bold text-center text-title mb-6">Log In</h1>
        <form on:submit|preventDefault={handleLogin} class="w-full max-w-sm">
            <input
                type="username"
                placeholder="Username"
                bind:value={username}
                required
                class="w-full p-4 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary"
            />
            <input
                type="password"
                placeholder="Password"
                bind:value={password}
                required
                class="w-full p-4 mb-6 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary"
            />
            {#if errorMessage}
                <p class="text-red-500 mb-4">{errorMessage}</p>
            {/if}
            <button
                type="submit"
                class="w-full p-4 bg-navbar text-white font-semibold rounded-lg hover:bg-buttonHover transition duration-300"
            >
                Log In
            </button>
        </form>
        <p class="mt-4 text-sm text-center text-gray-600 text-body">
            Don't have an account? 
            <a href="/auth/register" class="text-primary hover:text-buttonHover">Register here</a>.
        </p>
    </div>
</div>
