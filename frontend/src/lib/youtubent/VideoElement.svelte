<script lang="ts">
	import type { PlaylistVideoResult, VideoResult } from './Models.svelte';
    import { postRequest } from '$lib/Fetcher.svelte';
	import { playlist } from './Stores.svelte';
	import { Button } from 'flowbite-svelte';

	export let result: VideoResult;

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

		let playlistResult: PlaylistVideoResult = {
			...result,
			url: response.url
		};

		playlist.update((list) => {
			if (list.some((item) => item.yt_id === playlistResult.yt_id)) {
				return list;
			}
			list.push(playlistResult);
			return list;
		});
	}
</script>

<div class="flex w-full flex-row gap-5 bg-gray-100 p-4 rounded-xl">
	<img src={result.thumbnail} alt="thumbnail" />
	<div class="flex flex-col gap-3">
		<p class="text-lg font-bold">{result.title}</p>
		<p class="text-sm">{result.channel}</p>
		<Button class="w-64" color="green" pill on:click={play} value={result.yt_id}>Add to playlist</Button>
	</div>
</div>