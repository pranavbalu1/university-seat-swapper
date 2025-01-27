<script lang="ts">
    import { writable } from 'svelte/store';
    import { getProfile, createOrUpdateProfile } from '$lib/api/profile';
    import FaEdit from 'svelte-fa';
    import FaTrash from 'svelte-fa';
    import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons'; // Import icon definitions

    

    interface Profile {
    student_id: string;
    full_name: string;
    email: string;
    }

    interface ClassData {
    course_number: string;
    section_number: string;
    class_name: string;
    instructor: string;
    start_time: string;
    days: string[];
    }

    // Tabs state
    let activeTab = writable<'profile' | 'schedule' | 'requests'>('profile');

    // Profile and class data stores
    let profile = writable<Profile>({
    student_id: '',
    full_name: '',
    email: '',
    });
    let schedule = writable<ClassData[]>([]);
    let classData = writable<ClassData>({
    course_number: '',
    section_number: '',
    class_name: '',
    instructor: '',
    start_time: '',
    days: [],
    });

    // Get profile data from the backend
    async function loadProfile() {
        try {
            const profileData = await getProfile();
            profile.set(profileData);
        } catch (error) {
            console.error('Error loading profile:', error);
        }
    }

    // Save profile data to the backend
    async function saveProfile() {
        try {
            await createOrUpdateProfile($profile);
        } catch (error) {
            console.error('Error saving profile:', error);
        }
    }

    // Function to remove a class
    function removeClass(index: number) {
    schedule.update((current) => current.filter((_, i) => i !== index));
    }

    // Function to edit a class
    function editClass(index: number) {
    const cls = $schedule[index];
    classData.set({ ...cls });
    activeTab.set('schedule');
    removeClass(index);
    }

    // Fetch initial data when the component mounts
    import { onMount } from 'svelte';
    onMount(() => {
    loadProfile();
    });
</script>

<div class="flex flex-col justify-center items-center p-1 h-screen">
  <!-- Tab navigation -->
  <div class="flex justify-left gap-20 mb-8 w-[80%] max-w-[80rem] px-8 py-4 rounded-2xl border-2 border-gray-400">
    <button class="text-2xl hover:underline underline-offset-2 decoration-2 text-primary" on:click={() => activeTab.set('profile')} class:underline={$activeTab === 'profile'}>
      Profile
    </button>
    <button class="text-2xl hover:underline underline-offset-2 decoration-2 text-primary" on:click={() => activeTab.set('schedule')} class:underline={$activeTab === 'schedule'}>
      Schedule
    </button>
    <button class="text-2xl hover:underline underline-offset-2 decoration-2 text-primary" on:click={() => activeTab.set('requests')} class:underline={$activeTab === 'requests'}>
      Requests
    </button>
  </div>

  <div class="flex flex-col justify-center items-center h-[45rem] w-[80%] max-w-[80rem] px-8 py-4 rounded-2xl border-2 border-gray-400">
    <!-- Profile tab -->
    {#if $activeTab === 'profile'}
      <form class="flex flex-col gap-4 w-full max-w-md" on:submit|preventDefault={saveProfile}>
        <label class="flex flex-col">
          Student ID:
          <input type="text" bind:value={$profile.student_id} class="border rounded-md px-2 py-1" />
        </label>

        <label class="flex flex-col">
          Full Name:
          <input type="text" bind:value={$profile.full_name} class="border rounded-md px-2 py-1" />
        </label>

        <label class="flex flex-col">
          Email:
          <input type="email" bind:value={$profile.email} class="border rounded-md px-2 py-1" />
        </label>

        <button type="submit" class="px-4 py-4 my-2 bg-button text-primary rounded-md hover:bg-buttonHover">
          Save
        </button>
      </form>
    {/if}

    <!-- Schedule tab -->
    {#if $activeTab === 'schedule'}
      <div class="flex flex-row w-full gap-6">
        <div class="flex flex-col gap-4 w-1/3 max-w-md border-r-2 border-gray-400 pr-12">
          <h2 class="text-xl font-semibold">Add Class</h2>
          <label class="flex flex-col">
            Course Number:
            <input type="text" bind:value={$classData.course_number} class="border rounded-md px-2 py-1" />
          </label>

          <label class="flex flex-col">
            Section Number:
            <input type="text" bind:value={$classData.section_number} class="border rounded-md px-2 py-1" />
          </label>

          <label class="flex flex-col">
            Class Name:
            <input type="text" bind:value={$classData.class_name} class="border rounded-md px-2 py-1" />
          </label>

          <label class="flex flex-col">
            Instructor:
            <input type="text" bind:value={$classData.instructor} class="border rounded-md px-2 py-1" />
          </label>

          <label class="flex flex-col">
            Start Time:
            <input type="time" bind:value={$classData.start_time} class="border rounded-md px-2 py-1" />
          </label>

          <label class="flex flex-col">
            Days:
            <div class="flex flex-col gap-1">
              {#each ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] as day}
                <label class="inline-flex items-center">
                  <input type="checkbox" value={day} bind:group={$classData.days} class="mr-2 border-gray-300 rounded focus:ring focus:ring-blue-300" />
                  {day}
                </label>
              {/each}
            </div>
          </label>

          <button type="button" class="px-4 py-2 bg-button text-primary rounded-md hover:bg-buttonHover">
            Add Class
          </button>
        </div>

        <div class="w-2/3 mx-aut rounded-lg">
          <div class="no-scrollbar overflow-y-auto h-[40rem] px-1">
            <ul class="grid grid-cols-1 sm:grid-cols-1 lg:grid-cols-2 gap-6">
              {#each $schedule as cls, index}
                <li class="relative bg-gray-50 border-[#bbbbba] border-2 rounded-lg p-4 hover:shadow-lg transition-shadow">
                  <div class="absolute inset-0 bg-white opacity-30 blur-sm transition-all z-0"></div>

                  <div class="relative ">
                    <p class="text-lg font-semibold mb-2">{cls.class_name}</p>
                    <div class="text-sm space-y-1">
                      <p><strong>Class Name:</strong> {cls.class_name}</p>
                      <p><strong>Course Number:</strong> {cls.course_number}</p>
                      <p><strong>Section Number:</strong> {cls.section_number}</p>
                      <p><strong>Instructor:</strong> {cls.instructor}</p>
                      <p><strong>Days:</strong> {cls.days.join(', ')}</p>
                      <p><strong>Start Time:</strong> {cls.start_time}</p>
                    </div>
                  </div>

                  <!-- Action buttons (always visible, above the blurred background) -->
                  <div class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity z-20">
                    <button on:click={() => editClass(index)} class="px-4 py-2 bg-yellow-500 text-white rounded-full hover:bg-yellow-600 mr-2">
                      <FaEdit icon={faEdit} class="text-xl" />
                    </button>
                    <button on:click={() => removeClass(index)} class="px-4 py-2 bg-red-500 text-white rounded-full hover:bg-red-600">
                      <FaTrash icon={faTrash} class="text-xl" />
                    </button>
                  </div>
                </li>
              {/each}
            </ul>
          </div>
        </div>
      </div>
    {/if}

    <!-- Requests tab -->
    {#if $activeTab === 'requests'}
      <div>
        <!-- Placeholder for future feature -->
        <p>Requests coming soon!</p>
      </div>
    {/if}
  </div>
</div>

<style>

</style>
