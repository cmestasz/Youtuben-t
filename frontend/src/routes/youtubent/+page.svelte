<script lang="ts">
	import { postRequest } from '$lib/Fetcher.svelte';
	import { onMount } from 'svelte';
	import type { VideoResult } from '$lib/youtubent/Models.svelte';
	import VideoElement from '$lib/youtubent/VideoElement.svelte';
	import PlayerElement from '$lib/youtubent/PlayerElement.svelte';

	let queryElement: HTMLInputElement;
	let tokenElement: HTMLInputElement;
	let token: string;
	let results: VideoResult[] = [];
	let audioURL: string;

	onMount(() => {
		queryElement = document.getElementById('query') as HTMLInputElement;
		tokenElement = document.getElementById('token') as HTMLInputElement;
		checkForToken();
	});

	function checkForToken(): boolean {
		let t = localStorage.getItem('token');
		if (t == null) {
			alert('Make sure to set your token (ill someday make this a separate page)');
			return false;
		}
		token = t;
		return true;
	}

	function setToken() {
		let token = tokenElement.value;
		localStorage.setItem('token', token);
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
		let token = localStorage.getItem('token')!;
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

<h1>Not quite Youtube</h1>

{#if token == null}
	<p>Make sure to set your token</p>
{:else}
	<p>Token set</p>
{/if}
<input type="text" id="token" />
<button on:click={setToken}>Set Token</button>

<input type="text" id="query" />
<button on:click={search}>Search</button>

{#each results as result}
	<VideoElement {result} bind:audioURL={audioURL} />
{/each}

{#if audioURL}
	<footer>
		<PlayerElement {audioURL} />
	</footer>
{/if}
