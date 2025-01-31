<script lang="ts">
    import { writable, derived } from 'svelte/store';
    import { getProfile, createOrUpdateProfile } from '$lib/api/profile';
    import FaEdit from 'svelte-fa';
    import FaTrash from 'svelte-fa';
    import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';
    import { getSchedule, add_class, remove_class } from '$lib/api/schedule';
    import { onMount } from 'svelte';
    import { 
        getAllClassTradeRequests, 
        createClassTradeRequest, 
        voteOnRequest, 
        toggleFavoriteRequest, 
        deleteClassTradeRequest
    } from '$lib/api/requests';
    import { goto } from '$app/navigation';
    import { profileStore as profile } from '../../../stores/profilestore';
    import { type ClassData } from '../../../stores/schedulestore';
    import { scheduleStore as schedule } from '../../../stores/schedulestore';

    interface ClassTradeRequest {
        id: number;
        owner: number;
        owner_student_id: string;
        offered_class: ClassData;
        desired_class_number: string;
        desired_section_number: string;
        status: string;
        upvoted_by: string[];
        downvoted_by: string[];
        favorites: string[];
        created_at: string;
    }

    let favorite = writable(false);
    let activeTab = writable<'profile' | 'schedule' | 'requests'>('requests');
    let requests = writable<ClassTradeRequest[]>([]);

    let newRequest = writable<{
        offeredClassId: number | null;
        desiredClassNumber: string;
        desiredSectionNumber: string;
    }>({
        offeredClassId: null,
        desiredClassNumber: '',
        desiredSectionNumber: '',
    });

    let filterCriteria = writable<{
        course_number?: string;
        class_name?: string;
        instructor?: string;
        status?: string;
    }>({});

    const filteredRequests = derived(
        [requests, filterCriteria, favorite, profile],
        ([$requests, $filterCriteria, $favorite, $profile]) => {
            if (!$profile) return [];
            
            return $requests.filter(req => {
                const courseMatch = !$filterCriteria.course_number || 
                    req.offered_class.course_number.includes($filterCriteria.course_number);
                
                const classNameMatch = !$filterCriteria.class_name || 
                    req.offered_class.class_name.toLowerCase().includes($filterCriteria.class_name.toLowerCase());
                
                const instructorMatch = !$filterCriteria.instructor || 
                    req.offered_class.instructor.toLowerCase().includes($filterCriteria.instructor.toLowerCase());
                
                const statusMatch = !$filterCriteria.status || 
                    req.status === $filterCriteria.status;
                
                const favoriteMatch = !$favorite || req.favorites.includes($profile.student_id);

                return courseMatch && classNameMatch && instructorMatch && statusMatch && favoriteMatch;
            });
        }
    );

    function navigateTo(tab: 'profile' | 'schedule' | 'requests') {
        activeTab.set(tab);
        if (tab === 'profile') {
            goto('/dashboard/profile');
        } else if (tab === 'schedule') {
            goto('/dashboard/schedule');
        } else if (tab === 'requests') {
            goto('/dashboard/requests');
        }
    }

    async function loadProfile() {
        try {
            const profileData = await getProfile();
            profile.set(profileData);
        } catch (error) {
            console.error('Error loading profile:', error);
        }
    }

    async function loadSchedule() {
        try {
            const scheduleData = await getSchedule();
            schedule.set(scheduleData);
        } catch (error) {
            console.error('Error loading schedule:', error);
        }
    }

    async function loadRequests() {
        try {
            const reqs = await getAllClassTradeRequests();
            requests.set(reqs);
        } catch (error) {
            console.error('Error loading requests:', error);
        }
    }

    async function createRequest() {
        try {
            if (!$newRequest.offeredClassId) throw new Error('Please select a class to offer');
            
            await createClassTradeRequest(
                $newRequest.offeredClassId,
                $newRequest.desiredClassNumber,
                $newRequest.desiredSectionNumber
            );
            
            newRequest.set({ offeredClassId: null, desiredClassNumber: '', desiredSectionNumber: '' });
            await loadRequests();
        } catch (error) {
            console.error('Error creating request:', error);
        }
    }

    async function voteRequest(requestId: number, upvote: boolean) {
        try {
            await voteOnRequest(requestId, upvote);
            await loadRequests();
        } catch (error) {
            console.error('Error voting:', error);
        }
    }

    async function toggleFavorite(requestId: number) {
        try {
            await toggleFavoriteRequest(requestId);
            await loadRequests();
        } catch (error) {
            console.error('Error toggling favorite:', error);
        }
    }

    async function deleteRequest(requestId: number) {
        try {
            await deleteClassTradeRequest(requestId);
            await loadRequests();
        } catch (error) {
            console.error('Error deleting request:', error);
        }
    }

    onMount(() => {
        loadProfile();
        loadSchedule();
        loadRequests();
    });
</script>

<div class="flex flex-col justify-center items-center p-1 h-[92%]">
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

    <div class="bg-background bg-opacity-80 flex flex-col justify-center items-center h-[45rem] w-[80%] max-w-[80rem] px-8 py-4 rounded-2xl border-2 border-gray-400">
        {#if $activeTab === 'requests'}
        <div class="flex flex-row w-full gap-6">
            <div class="flex flex-col gap-4 w-1/3 max-w-md border-r-2 border-gray-400 pr-12">
                <h2 class="text-xl font-semibold">Create Request</h2>
                
                <label class="flex flex-col">
                    Offer Class:
                    <select bind:value={$newRequest.offeredClassId} class="border rounded-md px-2 py-1">
                        <option value={null}>Select a class</option>
                        {#each $schedule as cls}
                            <option value={cls.id}>{cls.class_name}</option>
                        {/each}
                    </select>
                </label>

                <label class="flex flex-col">
                    Desired Course Number:
                    <input type="text" bind:value={$newRequest.desiredClassNumber} class="border rounded-md px-2 py-1" />
                </label>

                <label class="flex flex-col">
                    Desired Section Number:
                    <input type="text" bind:value={$newRequest.desiredSectionNumber} class="border rounded-md px-2 py-1" />
                </label>

                <button on:click={createRequest} class="px-4 py-2 bg-button text-primary rounded-md hover:bg-buttonHover">
                    Create Request
                </button>

                <div class="mt-8">
                </div>
            </div>

            <div class="w-2/3 mx-auto rounded-lg">
                <div class="no-scrollbar overflow-y-auto h-[40rem] px-1">
                    <ul class="grid grid-cols-1 gap-6">
                        {#each $filteredRequests as req}
                            <li class="relative bg-gray-50 border-[#bbbbba] border-2 rounded-lg p-4 hover:shadow-lg transition-shadow">
                                <div class="absolute inset-0 bg-white opacity-30 blur-sm transition-all z-0"></div>
                                
                                <div class="relative">
                                    <div class="flex justify-between items-start mb-2">
                                        <div>
                                            <p class="text-lg font-semibold">{req.offered_class.class_name}</p>
                                            <p class="text-sm text-gray-600">Offered by {req.owner_student_id === $profile.student_id ? 'You' : req.owner_student_id}</p>
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
                                            <p>{req.offered_class.course_number} - Sec {req.offered_class.section_number}</p>
                                            <p>Instructor: {req.offered_class.instructor}</p>
                                            <p>Time: {req.offered_class.start_time}</p>
                                        </div>
                                        <div>
                                            <p class="font-semibold">Desired:</p>
                                            <p>{req.desired_class_number} - Sec {req.desired_section_number}</p>
                                        </div>
                                    </div>
                                    
                                    <div class="flex items-center gap-4 mt-4">
                                        <button on:click={() => voteRequest(req.id, true)} class="flex items-center gap-1 {req.upvoted_by.includes($profile.student_id) ? 'text-green-600' : 'text-gray-600'} hover:text-green-700">
                                            ▲ 
                                        </button>
                                        <p>{req.upvoted_by.length - req.downvoted_by.length}</p>
                                        <button on:click={() => voteRequest(req.id, false)} class="flex items-center gap-1 {req.downvoted_by.includes($profile.student_id) ? 'text-red-600' : 'text-gray-600'} hover:text-red-700">
                                            ▼
                                        </button>
                                        <button on:click={() => toggleFavorite(req.id)} class="flex items-center gap-1 {req.favorites.includes($profile.student_id) ? 'text-yellow-600' : 'text-gray-600'} hover:text-yellow-700">
                                            {req.favorites.includes($profile.student_id) ? '★' : '☆'}
                                        </button>
                                        {#if req.owner_student_id === $profile.student_id}
                                            <button on:click={() => deleteRequest(req.id)} class="ml-auto text-red-600 hover:text-red-700">
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
    .no-scrollbar::-webkit-scrollbar {
        display: none;
    }
    .no-scrollbar {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
</style>