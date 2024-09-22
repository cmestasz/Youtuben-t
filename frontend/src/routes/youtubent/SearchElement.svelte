<script lang="ts">
	import { YT_TOKEN_NAME } from '$lib/Constants.svelte';
	import { postRequest } from '$lib/Fetcher.svelte';
	import { Button } from 'flowbite-svelte';
	import { AlertType, VideoElementType, type VideoResult } from '$lib/youtubent/Models.svelte';
	import { checkForYTToken, updateAlerts } from '$lib/youtubent/Utils.svelte';
	import VideoElement from '$lib/youtubent/VideoElement.svelte';

	let queryElement: HTMLInputElement;
	let results: VideoResult[] = [];

	interface SearchRequest {
		query: string;
		token: string;
	}
	interface SearchResponse {
		results: VideoResult[];
	}
	async function search() {
		if (!checkForYTToken()) {
			updateAlerts('You need a YouTube token to search', AlertType.WARNING);
			return;
		}

		let query = queryElement.value;
		let token = localStorage.getItem(YT_TOKEN_NAME)!;
		let request: SearchRequest = {
			query: query,
			token: token
		};

		let response = await postRequest<SearchRequest, SearchResponse>('youtubent/search/', request);
		if (response == null) {
			return;
		}

		results = response.results;
	}

	function remove() {}
</script>

<div class="flex w-full flex-col gap-8">
	<div class="m-auto flex w-full flex-col items-center gap-6">
		<input bind:this={queryElement} class="block w-full" type="text" placeholder="Search query" />
		<Button class="w-64" color="green" pill on:click={search}>Search</Button>
	</div>

	<div class="container m-auto flex flex-col items-start gap-5 p-5">
		{#each results as result}
			<VideoElement {result} type={VideoElementType.RESULT} {remove} />
		{/each}
	</div>
</div>
