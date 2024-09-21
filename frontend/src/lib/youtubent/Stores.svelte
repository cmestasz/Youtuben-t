<script lang="ts" context="module">
	import { writable } from 'svelte/store';
	import type { PlaylistVideoResult } from './Models.svelte';
	
    export const playlist = writable<PlaylistVideoResult[]>([]);
</script>
