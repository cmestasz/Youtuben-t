<script lang="ts">
	import { getRequest } from '$lib/Fetcher.svelte';
	import { onMount } from 'svelte';
	import { VideoElementType, type VideoResult } from '$lib/youtubent/Models.svelte';
	import VideoElement from '$lib/youtubent/VideoElement.svelte';

	let results: VideoResult[] = [];

	onMount(async () => {
		let response = await getRequest<VideoResult[]>('youtubent/cached-list/');
		if (response == null) {
			return;
		}
		results = response;
	});

	function remove() {}
</script>


<div class="container m-auto flex flex-col items-start gap-5 p-5">
	{#each results as result}
		<VideoElement {result} type={VideoElementType.RESULT} {remove} />
	{/each}
</div>
