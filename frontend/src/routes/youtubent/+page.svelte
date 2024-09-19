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

    interface Request {
        query: string;
        token: string;
    }
    interface Results {
        title: string;
        videoId: string;
        thumbnail: string;
        channel: string;
    }
    interface Response {
        results: Results[];
    }

    let results: Results[] = [];

    async function search() {
        if (!checkForToken()) {
            return;
        }

        let query = queryElement.value;
        let token = localStorage.getItem('token')!;
        let request: Request = {
            query: query,
            token: token
        };

        let response = await postRequest<Request, Response>('youtubent/search/', request);
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
<input type="text" id="token">
<button on:click={setToken}>Set Token</button>

<input type="text" id="query" />
<button on:click={search}>Search</button>

{#each results as result}
    <div>
        <img src={result.thumbnail} alt="thumbnail" width="120" height="90" />
        <a href={"https://www.youtube.com/watch?v=" + result.videoId}>{result.title}</a>
        <p>{result.channel}</p>
    </div>
{/each}