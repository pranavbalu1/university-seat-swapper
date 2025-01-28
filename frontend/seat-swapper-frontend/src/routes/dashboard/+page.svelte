<script lang="ts">
    import { writable } from 'svelte/store';
    import { getProfile, createOrUpdateProfile } from '$lib/api/profile';
    import FaEdit from 'svelte-fa';
    import FaTrash from 'svelte-fa';
    import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons'; // Import icon definitions
    import { getSchedule, add_class, remove_class } from '$lib/api/schedule';
    import { onMount } from 'svelte';

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

    // get class data from the backend
    async function loadSchedule() {
        try {
            const scheduleData = await getSchedule();
            schedule.set(scheduleData);
            console.log('schedule: ', schedule);
        } catch (error) {
            console.error('Error loading schedule:', error);
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
  async function removeClass(index: number) {
    const cls = $schedule[index];
    const classData = {
      course_number: cls.course_number,
      section_number: cls.section_number,
    };

    try {
      // Call the API to remove the class
      await remove_class(classData);

      // Update the schedule store to reflect the removed class
      schedule.update((current) => current.filter((_, i) => i !== index));
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
      schedule.update((current) => [...current, newClass]);
      classData.set({
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
      const cls = $schedule[index];
      classData.set({ ...cls });
      activeTab.set('schedule');
      removeClass(index);
    }

        // Add to existing interfaces
    interface ClassRequest {
        id: string;
        ownerId: string;
        offeredClass: ClassData;
        desiredClass: {
            course_number: string;
            section_number: string;
        };
        status: 'open' | 'closed' | 'pending';
        upvotedBy: string[];  // Changed from votes
        downvotedBy: string[]; // New property
        favorites: string[];
        createdAt: Date;
    }

    interface FilterCriteria {
        courseNumber?: string;
        className?: string;
        instructor?: string;
        status?: 'open' | 'closed' | 'pending';
    }

    // Add to existing stores
    let requests = writable<ClassRequest[]>([]);
    let newRequest = writable<{
        offeredClassId: number | null;
        desiredCourseNumber: string;
        desiredSectionNumber: string;
    }>({
        offeredClassId: null,
        desiredCourseNumber: '',
        desiredSectionNumber: '',
    });

    let filterCriteria = writable<FilterCriteria>({});
    
    onMount(() => {
        // Initialize mock requests
        requests.set([
            {
                id: '1',
                ownerId: 'user123',
                offeredClass: {
                    course_number: 'MATH101',
                    section_number: '01',
                    class_name: 'Calculus I',
                    instructor: 'Dr. Smith',
                    start_time: '10:00',
                    days: ['Mon', 'Wed']
                },
                desiredClass: { course_number: 'PHYS201', section_number: '02' },
                status: 'open',
                upvotedBy: ['user123'], // Example existing votes
                downvotedBy: [],
                favorites: [],
                createdAt: new Date()
            },
            // Add more mock requests as needed
        ]);
    });

    // Request actions
    function createRequest() {
        // Get the selected class using the index from the dropdown
        const offeredClass = $schedule[$newRequest.offeredClassId as number];
        
        if (offeredClass) {
            const newReq: ClassRequest = {
                id: Date.now().toString(),
                ownerId: $profile.student_id,
                offeredClass: { ...offeredClass },
                desiredClass: {
                    course_number: $newRequest.desiredCourseNumber,
                    section_number: $newRequest.desiredSectionNumber
                },
                status: 'open',
                upvotedBy: [],
                downvotedBy: [],
                favorites: [],
                createdAt: new Date()
            };
            
            requests.update(reqs => [...reqs, newReq]);
            newRequest.set({
                offeredClassId: null,
                desiredCourseNumber: '',
                desiredSectionNumber: '',
            });
        }
    }

    function voteRequest(requestId: string, upvote: boolean) {
        requests.update(reqs => reqs.map(req => {
            if (req.id === requestId) {
                const userId = $profile.student_id;
                const hasUpvoted = req.upvotedBy.includes(userId);
                const hasDownvoted = req.downvotedBy.includes(userId);
                
                if (upvote) {
                    return {
                        ...req,
                        upvotedBy: hasUpvoted 
                            ? req.upvotedBy.filter(id => id !== userId)
                            : [...req.upvotedBy, userId],
                        downvotedBy: hasDownvoted
                            ? req.downvotedBy.filter(id => id !== userId)
                            : req.downvotedBy
                    };
                } else {
                    return {
                        ...req,
                        downvotedBy: hasDownvoted
                            ? req.downvotedBy.filter(id => id !== userId)
                            : [...req.downvotedBy, userId],
                        upvotedBy: hasUpvoted
                            ? req.upvotedBy.filter(id => id !== userId)
                            : req.upvotedBy
                    };
                }
            }
            return req;
        }));
    }

    function toggleFavorite(requestId: string) {
        requests.update(reqs => reqs.map(req => {
            if (req.id === requestId) {
                const isFavorited = req.favorites.includes($profile.student_id);
                return {
                    ...req,
                    favorites: isFavorited 
                        ? req.favorites.filter(id => id !== $profile.student_id)
                        : [...req.favorites, $profile.student_id]
                };
            }
            return req;
        }));
    }

    function deleteRequest(requestId: string) {
        requests.update(reqs => reqs.filter(req => req.id !== requestId));
    }


    onMount(() => {
        loadProfile();
        loadSchedule();
    });
</script>

<div class="flex flex-col justify-center items-center p-1  h-[92%]">
  <!-- Tab navigation -->
  <div class="bg-background bg-opacity-80 flex justify-left gap-20 mb-2 mt-4 w-[80%] max-w-[80rem] px-8 py-4 rounded-2xl border-2 border-gray-400">
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

  <div class=" bg-background bg-opacity-80 flex flex-col justify-center items-center h-[45rem] w-[80%] max-w-[80rem] px-8 py-4 rounded-2xl border-2 border-gray-400">
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

          <button type="button" on:click={addClass}  class="px-4 py-2 bg-button text-primary rounded-md hover:bg-buttonHover">
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
    <div class="flex flex-row w-full gap-6">
        <!-- Create Request Panel -->
        <div class="flex flex-col gap-4 w-1/3 max-w-md border-r-2 border-gray-400 pr-12">
            <h2 class="text-xl font-semibold">Create Request</h2>
            
            <label class="flex flex-col">
                Offer Class:
                <select 
                    bind:value={$newRequest.offeredClassId}
                    class="border rounded-md px-2 py-1"
                >
                    <option value={null}>Select a class</option>
                    {#each $schedule as cls, index}
                        <option value={index}>{cls.class_name} - {cls.course_number}</option>
                    {/each}
                </select>
            </label>

            <label class="flex flex-col">
                Desired Course Number:
                <input 
                    type="text" 
                    bind:value={$newRequest.desiredCourseNumber}
                    class="border rounded-md px-2 py-1"
                />
            </label>

            <label class="flex flex-col">
                Desired Section Number:
                <input 
                    type="text" 
                    bind:value={$newRequest.desiredSectionNumber}
                    class="border rounded-md px-2 py-1"
                />
            </label>

            <button 
                on:click={createRequest}
                class="px-4 py-2 bg-button text-primary rounded-md hover:bg-buttonHover"
            >
                Create Request
            </button>

            <!-- Filter Section -->
            <div class="mt-8">
                <h2 class="text-xl font-semibold mb-4">Filters</h2>
                <div class="space-y-4">
                    <input 
                        type="text" 
                        placeholder="Course Number"
                        bind:value={$filterCriteria.courseNumber}
                        class="border rounded-md px-2 py-1 w-full"
                    />
                    <input 
                        type="text" 
                        placeholder="Class Name"
                        bind:value={$filterCriteria.className}
                        class="border rounded-md px-2 py-1 w-full"
                    />
                    <input 
                        type="text" 
                        placeholder="Instructor"
                        bind:value={$filterCriteria.instructor}
                        class="border rounded-md px-2 py-1 w-full"
                    />
                    <select 
                        bind:value={$filterCriteria.status}
                        class="border rounded-md px-2 py-1 w-full"
                    >
                        <option value={undefined}>All Statuses</option>
                        <option value="open">Open</option>
                        <option value="pending">Pending</option>
                        <option value="closed">Closed</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Requests List -->
        <div class="w-2/3 mx-auto rounded-lg">
            <div class="no-scrollbar overflow-y-auto h-[40rem] px-1">
                <ul class="grid grid-cols-1 gap-6">
                    {#each $requests.filter(req => 
                        (!$filterCriteria.courseNumber || req.desiredClass.course_number.includes($filterCriteria.courseNumber)) &&
                        (!$filterCriteria.className || req.offeredClass.class_name.includes($filterCriteria.className)) &&
                        (!$filterCriteria.instructor || req.offeredClass.instructor.includes($filterCriteria.instructor)) &&
                        (!$filterCriteria.status || req.status === $filterCriteria.status)
                    ) as req}
                        <li class="relative bg-gray-50 border-[#bbbbba] border-2 rounded-lg p-4 hover:shadow-lg transition-shadow">
                            <div class="absolute inset-0 bg-white opacity-30 blur-sm transition-all z-0"></div>
                            
                            <div class="relative">
                                <div class="flex justify-between items-start mb-2">
                                    <div>
                                        <p class="text-lg font-semibold">{req.offeredClass.class_name}</p>
                                        <p class="text-sm text-gray-600">Offered by {req.ownerId === $profile.student_id ? 'You' : 'User ' + req.ownerId.slice(-4)}</p>
                                    </div>
                                    <span class="px-2 py-1 text-sm rounded-full 
                                        {req.status === 'open' ? 'bg-green-100 text-green-800' :
                                        req.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                                        'bg-red-100 text-red-800'}">
                                        {req.status}
                                    </span>
                                </div>
                                
                                <div class="grid grid-cols-2 gap-4 text-sm">
                                    <div>
                                        <p class="font-semibold">Offering:</p>
                                        <p>{req.offeredClass.course_number} - Sec {req.offeredClass.section_number}</p>
                                        <p>Instructor: {req.offeredClass.instructor}</p>
                                        <p>Time: {req.offeredClass.start_time}</p>
                                    </div>
                                    <div>
                                        <p class="font-semibold">Desired:</p>
                                        <p>{req.desiredClass.course_number} - Sec {req.desiredClass.section_number}</p>
                                    </div>
                                </div>
                                
                                <div class="flex items-center gap-4 mt-4">
                                    <button 
                                        on:click={() => voteRequest(req.id, true)}
                                        class="flex items-center gap-1 {req.upvotedBy.includes($profile.student_id) ? 'text-green-600' : 'text-gray-600'} hover:text-green-700"
                                    >
                                        ▲ {req.upvotedBy.length - req.downvotedBy.length}
                                    </button>
                                    <button 
                                        on:click={() => voteRequest(req.id, false)}
                                        class="flex items-center gap-1 {req.downvotedBy.includes($profile.student_id) ? 'text-red-600' : 'text-gray-600'} hover:text-red-700"
                                    >
                                        ▼
                                    </button>
                                    <button 
                                        on:click={() => toggleFavorite(req.id)}
                                        class="flex items-center gap-1 text-yellow-600 hover:text-yellow-700"
                                    >
                                        {req.favorites.includes($profile.student_id) ? '★' : '☆'}
                                    </button>
                                    {#if req.ownerId === $profile.student_id}
                                        <button 
                                            on:click={() => deleteRequest(req.id)}
                                            class="ml-auto text-red-600 hover:text-red-700"
                                        >
                                            <FaTrash icon={faTrash} class="text-lg" />
                                        </button>
                                    {/if}
                                </div>
                            </div>
                        </li>
                    {/each}
                </ul>
            </div>
        </div>
    </div>
    {/if}
  </div>


</div>

<style>

</style>
