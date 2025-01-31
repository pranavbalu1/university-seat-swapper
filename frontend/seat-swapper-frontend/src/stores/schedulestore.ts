import { writable } from 'svelte/store';

export interface ClassData {
  id: number;
  course_number: string;
  section_number: string;
  class_name: string;
  instructor: string;
  start_time: string;
  days: string[];
}

const scheduleStore = writable<ClassData[]>([]);


export { scheduleStore };
