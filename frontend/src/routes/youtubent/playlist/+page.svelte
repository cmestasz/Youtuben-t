<script lang="ts">
	import { get } from 'svelte/store';
	import { playlist } from '$lib/youtubent/Stores.svelte';
	import type { VideoResult } from '$lib/youtubent/Models.svelte';
	import { onMount } from 'svelte';
	import PlaylistVideoElement from './PlaylistVideoElement.svelte';

	let list: VideoResult[] = [];

	onMount(() => {
		list = get(playlist);
		console.log(list);
	});

	playlist.subscribe((value) => {
		list = value;
	});

	function remove(result: VideoResult) {
		playlist.update((value) => {
			return value.filter((item) => item.yt_id !== result.yt_id);
		});
	}
</script>

<div class="container m-auto flex flex-col items-start gap-5 p-5">
	{#each list as item}
		<PlaylistVideoElement result={item} {remove} />
	{/each}
</div>
