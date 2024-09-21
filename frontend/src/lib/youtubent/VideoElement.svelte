<script lang="ts">
	import type { PlaylistVideoResult, VideoResult } from './Models.svelte';
	import { postRequest } from '$lib/Fetcher.svelte';
	import { playlist } from './Stores.svelte';
	import { Button } from 'flowbite-svelte';
	import { VideoElementType } from './Models.svelte';
	import { checkForToken } from './Utils.svelte';
	import { ACCOUNT_TOKEN_NAME } from '$lib/Constants.svelte';

	export let result: VideoResult;
	export let type: VideoElementType;
	export let remove: (result: VideoResult) => void;

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

	interface ForgetRequest {
		video_id: string;
		token: string;
	}
	async function forget() {
		if (!checkForToken()) {
			alert('You need an account to forget videos!');
			return;
		}
		
		let token = localStorage.getItem(ACCOUNT_TOKEN_NAME)!;
		let request: ForgetRequest = {
			video_id: result.yt_id,
			token: token
		};

		let response = await postRequest<ForgetRequest, {}>('youtubent/forget/', request);
		if (response == null) {
			return;
		}

		remove(result);
	}

	interface SaveRequest {
		video_id: string;
		token: string;
	}
	async function save(event: Event) {
		if (!checkForToken()) {
			alert('You need an account to save videos!');
			return;
		}

		let videoId = (event.target as HTMLButtonElement).value;
		let token = localStorage.getItem(ACCOUNT_TOKEN_NAME)!;
		let request: SaveRequest = {
			video_id: videoId,
			token: token
		};

		await postRequest<SaveRequest, {}>('youtubent/save/', request);
	}
</script>

<div class="flex w-full flex-row gap-5 rounded-xl bg-gray-100 p-4">
	<img src={result.thumbnail} alt="thumbnail" />
	<div class="flex flex-col gap-3">
		<p class="text-lg font-bold">{result.title}</p>
		<p class="text-sm">{result.channel}</p>
		{#if type == VideoElementType.RESULT}
			<Button class="w-64" color="green" pill on:click={play} value={result.yt_id}
				>Add to playlist</Button
			>
			<Button class="w-64" color="blue" pill on:click={save} value={result.yt_id}>Save to account storage</Button>
		{:else if type == VideoElementType.PLAYLIST}
			<Button class="w-64" color="blue" pill on:click={save} value={result.yt_id}>Save to account storage</Button>
			<Button class="w-64" color="red" pill on:click={() => remove(result)}>Remove from playlist</Button>
		{:else if type == VideoElementType.SAVED}
			<Button class="w-64" color="green" pill on:click={play} value={result.yt_id}
				>Add to playlist</Button
			>
			<Button class="w-64" color="red" pill on:click={forget}>Forget from account storage</Button>
		{/if}
	</div>
</div>
