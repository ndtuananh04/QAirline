import { writable } from 'svelte/store';

export const quantity = writable(1);
export const tripType = writable('round-trip');
