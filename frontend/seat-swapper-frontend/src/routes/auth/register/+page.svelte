<script lang="ts">
    import { goto } from '$app/navigation';
    import { register } from '$lib/api/auth'; // Import the register API function

    let username = '';
    let password = '';
    let confirmPassword = '';
    let errorMessage = ''; // To display error messages

    const handleRegister = async () => {
        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        try {
            const { token, user } = await register(username, password); // Call the register API
            // Store the token and user info if needed (e.g., in a global store)
            console.log('Registration successful:', user);
            goto('/dashboard'); // Navigate to the dashboard on successful registration
        } catch (error: any) {
            errorMessage = error.message; // Display error message if registration fails
        }
    };
</script>

<div class=" bg-stacked-waves-2 bg-cover bg-no-repeat flex flex-col justify-center items-center h-[92%]  ">
    <!-- Registration Section -->
    <div class="flex-grow flex flex-col justify-center items-center px-4">
        <h1 class="text-5xl font-bold text-center text-title mb-6">Register</h1>
        <form on:submit|preventDefault={handleRegister} class="w-full max-w-sm">
            <input
                type="text"
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
                class="w-full p-4 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary"
            />
            <input
                type="password"
                placeholder="Confirm Password"
                bind:value={confirmPassword}
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
                Register
            </button>
        </form>
        <p class="mt-4 text-sm text-center text-gray-600 text-body">
            Already have an account? 
            <a href="/auth/login" class="text-primary hover:text-buttonHover">Login here</a>.
        </p>
    </div>
</div>
