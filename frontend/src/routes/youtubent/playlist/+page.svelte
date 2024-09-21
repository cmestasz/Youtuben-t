<script lang="ts">
	import { get } from 'svelte/store';
	import { playlist } from '$lib/youtubent/Stores.svelte';
	import { VideoElementType, type VideoResult } from '$lib/youtubent/Models.svelte';
	import { onMount } from 'svelte';
	import VideoElement from '$lib/youtubent/VideoElement.svelte';

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
		<VideoElement result={item} type={VideoElementType.PLAYLIST} {remove} />
	{/each}
</div>
