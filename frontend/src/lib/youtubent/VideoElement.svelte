<script lang="ts">
	import type { VideoResult } from './Models.svelte';
    import { postRequest } from '$lib/Fetcher.svelte';

	export let result: VideoResult;
    export let audioURL: string;

    interface PlayRequest {
		video_id: string;
	}
	interface PlayResponse {
		url: string;
	}

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

<div>
	<img src={result.thumbnail} alt="thumbnail" width="120" height="90" />
	<button on:click={play} value={result.yt_id}>Play</button>
	<p>{result.title}</p>
	<p>{result.channel}</p>
</div>