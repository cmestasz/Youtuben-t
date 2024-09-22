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

<div class="container flex flex-col items-center gap-5">
	<div class="text-center">
		<p>Your playlist, these songs will play from top to bottom.</p>
		<p class="text-xs">
			(I had a short argument with a teacher about whether this is a list or a queue but i can't
			remember it)
		</p>
	</div>
	{#each list as item}
		<VideoElement result={item} type={VideoElementType.PLAYLIST} {remove} />
	{/each}
</div>
