import { writable } from 'svelte/store';

// Define the structure of a class request
export interface ClassRequest {
    id: string;
    ownerId: string;
    offeredClass: {
        id: string;
        course_number: string;
        section_number: string;
        class_name: string;
        instructor: string;
        start_time: string;
        days: string[];
    };
    desiredClassNumber: string;
    desiredSectionNumber: string;
    status: 'open' | 'closed' | 'pending';
    upvotedBy: string[];
    downvotedBy: string[];
    favorites: string[];
    createdAt: Date;
}

// Create a writable store to hold the requests
export const requests = writable<ClassRequest[]>([]);

