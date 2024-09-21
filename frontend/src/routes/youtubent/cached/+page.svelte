<script lang="ts">
	import { getRequest } from '$lib/Fetcher.svelte';
	import { onMount } from 'svelte';
	import type { VideoResult } from '$lib/youtubent/Models.svelte';
	import VideoElement from '$lib/youtubent/VideoElement.svelte';
	import PlayerElement from '$lib/youtubent/PlayerElement.svelte';

	let results: VideoResult[] = [];
	let audioURL: string;

	onMount(async () => {
		let response = await getRequest<VideoResult[]>('youtubent/cached-list/');
		if (response == null) {
			return;
		}
		results = response;
	});
</script>


<div class="container m-auto flex flex-col items-start gap-5 p-5">
	{#each results as result}
		<VideoElement {result} />
	{/each}
</div>
