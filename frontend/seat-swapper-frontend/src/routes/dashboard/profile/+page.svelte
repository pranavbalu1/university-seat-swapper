<script lang="ts">
    import { writable } from 'svelte/store';
    import { profileStore, setProfile } from '../../../stores/profilestore';
    import { getProfile, createOrUpdateProfile } from '$lib/api/profile';
    import { onMount } from 'svelte';
	  import { goto } from '$app/navigation';



    // Tabs state
    let activeTab = writable<'profile' | 'schedule' | 'requests'>('profile');
    // Handle tab navigation
    function navigateTo(tab: 'profile' | 'schedule' | 'requests') {
        activeTab.set(tab);
        if (tab === 'schedule') {
            goto('/dashboard/schedule');
        } else if (tab === 'requests') {
            goto('/dashboard/requests');
        }
    }

    async function loadProfile() {
        try {
            const profileData = await getProfile();
            profileStore.set(profileData);
            console.log('Profile data:', profileData);
        } catch (error) {
            console.error('Error loading profile:', error);
        }
    }


    // Save profile data to the backend
    async function saveProfile() {
        try {
            await createOrUpdateProfile($profileStore);
            profileStore.set($profileStore);
            console.log('Profile saved:', $profileStore);
        } catch (error) {
            console.error('Error saving profile:', error);
        }
    }

    onMount(() => {
        loadProfile();
    });
</script>

<div class="flex flex-col justify-center items-center p-1  h-[92%]">
  <!-- Tab navigation -->
  <div class="bg-background bg-opacity-80 flex justify-left gap-20 mb-2 mt-4 w-[80%] max-w-[80rem] px-8 py-4 rounded-2xl border-2 border-gray-400">
    <button class="text-2xl hover:underline underline-offset-2 decoration-2 text-primary" on:click={() => navigateTo('profile')} class:underline={$activeTab === 'profile'}>
      Profile
    </button>
    <button class="text-2xl hover:underline underline-offset-2 decoration-2 text-primary" on:click={() => navigateTo('schedule')} class:underline={$activeTab === 'schedule'}>
      Schedule
    </button>
    <button class="text-2xl hover:underline underline-offset-2 decoration-2 text-primary" on:click={() => navigateTo('requests')} class:underline={$activeTab === 'requests'}>
      Requests
    </button>
  </div>

  <div class=" bg-background bg-opacity-80 flex flex-col justify-center items-center h-[45rem] w-[80%] max-w-[80rem] px-8 py-4 rounded-2xl border-2 border-gray-400">
    <!-- Profile tab -->
      <form class="flex flex-col gap-4 w-full max-w-md" on:submit|preventDefault={saveProfile}>
        <label class="flex flex-col">
          Student ID:
          <input type="text" bind:value={$profileStore.student_id} class="border rounded-md px-2 py-1" />
        </label>

        <label class="flex flex-col">
          Full Name:
          <input type="text" bind:value={$profileStore.full_name} class="border rounded-md px-2 py-1" />
        </label>

        <label class="flex flex-col">
          Email:
          <input type="email" bind:value={$profileStore.email} class="border rounded-md px-2 py-1" />
        </label>

        <button type="submit" class="px-4 py-4 my-2 bg-button text-primary rounded-md hover:bg-buttonHover">
          Save
        </button>
      </form>


  </div>


</div>

<style>

</style>

