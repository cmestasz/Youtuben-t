<script lang="ts" context="module">
	import { writable } from 'svelte/store';
	import type { AlertMessage, PlaylistVideoResult } from './Models.svelte';
	
    export const playlist = writable<PlaylistVideoResult[]>([]);
	export const user_name = writable<string>('');
	export const alerts = writable<AlertMessage[]>([]);
</script>
