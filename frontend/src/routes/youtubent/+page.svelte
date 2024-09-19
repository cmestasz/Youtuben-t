<script lang="ts">
	import { postRequest } from '$lib/Fetcher.svelte';
	import { onMount } from 'svelte';

	let queryElement: HTMLInputElement;
	let tokenElement: HTMLInputElement;
	let token: string;

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
	interface VideoResult {
		title: string;
		video_id: string;
		thumbnail: string;
		channel: string;
	}
	interface SearchResponse {
		results: VideoResult[];
	}

	let results: VideoResult[] = [];

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

	interface PlayRequest {
		video_id: string;
	}
	interface PlayResponse {
		url: string;
	}

	let audioURL: string;

	async function play(event: Event) {
		let videoId = (event.target as HTMLButtonElement).value;
		let request: PlayRequest = {
			video_id: videoId
		};

		let response = await postRequest<PlayRequest, PlayResponse>('youtubent/play/', request);
		if (response == null) {
			return;
		}

        audioURL = response.url;
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
	<div>
		<img src={result.thumbnail} alt="thumbnail" width="120" height="90" />
		<button on:click={play} value={result.video_id}>Play</button>
		<p>{result.channel}</p>
	</div>
{/each}

{#if audioURL}
	<footer>
        <p>Now playing:</p>
		<audio controls autoplay>
			<source src={audioURL} type="audio/mpeg" id="player" />
            Your browser does not support the audio element.
		</audio>
	</footer>
{/if}
