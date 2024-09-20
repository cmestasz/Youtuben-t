<script lang="ts">
	import { postRequest } from '$lib/Fetcher.svelte';
	import { onMount } from 'svelte';
	import type { VideoResult } from '$lib/youtubent/Models.svelte';
	import { YT_TOKEN_NAME } from '$lib/Constants.svelte';
	import VideoElement from '$lib/youtubent/VideoElement.svelte';
	import PlayerElement from '$lib/youtubent/PlayerElement.svelte';
	import YtTokenElement from '$lib/youtubent/YTTokenElement.svelte';
	import AccountElement from '$lib/youtubent/AccountElement.svelte';
	import Navigation from '$lib/Navigation.svelte';

	let queryElement: HTMLInputElement;
	let token: string;
	let results: VideoResult[] = [];
	let audioURL: string;

	onMount(() => {
		queryElement = document.getElementById('query') as HTMLInputElement;
		checkForToken();
	});

	function checkForToken() {
		let t = localStorage.getItem(YT_TOKEN_NAME);
		if (t == null) {
			return false;
		}
		token = t;
		return true;
	}

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

<Navigation />
<div class="m-auto container flex flex-col gap-5 p-10 items-center">
	<p class="text-xl font-bold">Not Quite Youtube</p>

	<YtTokenElement bind:ytToken={token} {checkForToken} />

	<div class="flex w-max flex-col gap-2">
		<input class="block" type="text" id="query" placeholder="Search query" />
		<button class="bg-gray-400 p-2" on:click={search}>Search</button>
	</div>

	{#each results as result}
		<div>
			<VideoElement {result} bind:audioURL={audioURL} />
		</div>
	{/each}
</div>

{#if audioURL}
	<footer>
		<PlayerElement {audioURL} />
	</footer>
{/if}
