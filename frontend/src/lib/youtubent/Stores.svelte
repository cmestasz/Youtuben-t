<script lang="ts" context="module">
	import { writable } from 'svelte/store';
	
    export const audioURL = writable<string>('');
</script>
