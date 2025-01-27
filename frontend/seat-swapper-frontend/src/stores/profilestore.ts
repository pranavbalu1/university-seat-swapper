import { writable } from 'svelte/store';

export type Course = {
  course_number: string;
  section_number: string;
  class_name: string;
  instructor: string;
  start_time: string;
  days: string[];
};

export type Profile = {
  name: string;
  email: string;
  courses: Course[];
};

export const profile = writable<Profile>({
  name: '',
  email: '',
  courses: []
});

export const addCourse = (course: Course) => {
  profile.update((profileData) => {
    profileData.courses.push(course);
    return profileData;
  });
};

export const updateProfile = (newProfileData: Profile) => {
  profile.set(newProfileData);
};
