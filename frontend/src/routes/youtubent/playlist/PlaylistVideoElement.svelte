<script lang="ts">
	import type { VideoResult } from '$lib/youtubent/Models.svelte';
	import { Button } from 'flowbite-svelte';

	export let result: VideoResult;
	export let remove: (result: VideoResult) => void;
</script>

<div class="flex w-full flex-row gap-5 bg-gray-100 p-4 rounded-xl">
	<img src={result.thumbnail} alt="thumbnail" />
	<div class="flex flex-col gap-3">
		<p class="text-lg font-bold">{result.title}</p>
		<p class="text-sm">{result.channel}</p>
		<Button color="red" class="w-64" pill on:click={() => remove(result)}>Remove</Button>
	</div>
</div>
