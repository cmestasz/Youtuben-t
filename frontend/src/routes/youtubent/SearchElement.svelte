<script lang="ts">
	import { YT_TOKEN_NAME } from '$lib/Constants.svelte';
	import { postRequest } from '$lib/Fetcher.svelte';
	import type { VideoResult } from '../../lib/youtubent/Models.svelte';
	import { checkForToken } from '../../lib/youtubent/Utils.svelte';
    import VideoElement from '../../lib/youtubent/VideoElement.svelte';

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
		if (!checkForToken()) {
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
</script>

<div>
	<div class="flex w-max flex-col gap-2">
		<input bind:this={queryElement} class="block" type="text" placeholder="Search query" />
		<button class="bg-gray-400 p-2" on:click={search}>Search</button>
	</div>

	{#each results as result}
		<div class="flex flex-col gap-2 align-middle">
			<VideoElement {result} />
		</div>
	{/each}
</div>
