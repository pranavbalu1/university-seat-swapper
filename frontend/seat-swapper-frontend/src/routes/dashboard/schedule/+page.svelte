<script lang="ts">
    import { writable } from 'svelte/store';

    import FaEdit from 'svelte-fa';
    import FaTrash from 'svelte-fa';
    import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons'; // Import icon definitions
    import { getSchedule, add_class, remove_class } from '$lib/api/schedule';
    import { onMount } from 'svelte';
	  import { goto } from '$app/navigation';
    import { profileStore } from '../../../stores/profilestore';
    import { type ClassData, scheduleStore } from '../../../stores/schedulestore';
    


    let activeTab = writable<'profile' | 'schedule' | 'requests'>('schedule');
    let classData = writable<ClassData>({
        id: 0,
        course_number: '',
        section_number: '',
        class_name: '',
        instructor: '',
        start_time: '',
        days: [],
    });
    function navigateTo(tab: 'profile' | 'schedule' | 'requests') {
        activeTab.set(tab);
        if (tab === 'profile') {
            goto('/dashboard/profile');
        } else
        if (tab === 'schedule') {
            goto('/dashboard/schedule');
        } else if (tab === 'requests') {
            goto('/dashboard/requests');
        }
    }

    // get class data from the backend
    async function loadSchedule() {
        try {
            const scheduleData = await getSchedule();
            scheduleStore.set(scheduleData);

        } catch (error) {
            console.error('Error loading schedule:', error);
        }
    }


  // Function to remove a class
  async function removeClass(index: number) {
    const cls = $scheduleStore[index];
    const classData = {
      course_number: cls.course_number,
      section_number: cls.section_number,
    };

    try {
      // Call the API to remove the class
      await remove_class(classData);

      // Update the schedule store to reflect the removed class
      scheduleStore.update((current) => current.filter((_, i) => i !== index));
    } catch (error) {
      console.error('Error removing class:', error);
    }
  }


  // Add a new class and send it to the backend
  async function addClass() {
    try {
      const newClass: any = { ...$classData };
      console.log('newClass: ', newClass);
      await add_class(newClass);
      scheduleStore.update((current) => [...current, newClass]);
      classData.set({
        id: 0 ,
        course_number: '',
        section_number: '',
        class_name: '',
        instructor: '',
        start_time: '',
        days: [],
      });
    } catch (error) {
      console.error('Error adding class:', error);
    }
  }



    // Function to edit a class
    function editClass(index: number) {
      const cls = $scheduleStore[index];
      classData.set({ ...cls });
      activeTab.set('schedule');
      removeClass(index);
    }





    onMount(() => {
       
        loadSchedule();
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

          <button type="button" on:click={addClass}  class="px-4 py-2 bg-button text-primary rounded-md hover:bg-buttonHover">
            Add Class
          </button>
        </div>

        <div class="w-2/3 mx-aut rounded-lg">
          <div class="no-scrollbar overflow-y-auto h-[40rem] px-1">
            {#if $scheduleStore.length === 0}
              <!-- Render a message if the schedule is empty -->
              <div class="flex justify-center items-center text-xl font-semibold text-gray-500">
                <p>Make sure your profile details are right, and you have added classes.</p>
              </div>
            {:else}
              <!-- Render the schedule list if there are classes -->
              <ul class="grid grid-cols-1 sm:grid-cols-1 lg:grid-cols-2 gap-6">
                {#each $scheduleStore as cls, index}
                  <li class="relative bg-gray-50 border-[#bbbbba] border-2 rounded-lg p-4 hover:shadow-lg transition-shadow">
                    <div class="absolute inset-0 bg-white opacity-30 blur-sm transition-all z-0"></div>

                    <div class="relative">
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
            {/if}
          </div>

        </div>
      </div>
    {/if}


  </div>


</div>

<style>

</style>
