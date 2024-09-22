<script lang="ts">
	import { ACCOUNT_TOKEN_NAME } from "$lib/Constants.svelte";
	import { postRequest } from "$lib/Fetcher.svelte";
	import { AlertType, VideoElementType, type PlaylistVideoResult, type VideoResult } from "$lib/youtubent/Models.svelte";
	import { checkForAccountToken, updateAlerts } from "$lib/youtubent/Utils.svelte";
	import VideoElement from "$lib/youtubent/VideoElement.svelte";
	import { Button } from "flowbite-svelte";
	import { onMount } from "svelte";
    import { playlist } from "$lib/youtubent/Stores.svelte";

    let results: PlaylistVideoResult[] = [];
    let savedAmount = 0;
    let maxAmount = 100;

    interface SavedListRequest {
        token: string;
    }
    interface SavedListResponse {
        results: PlaylistVideoResult[];
        saved_amount: number;
        max_amount: number;
    }
    onMount(async () => {
        if (!checkForAccountToken()) {
            updateAlerts("You need an account to view saved songs", AlertType.WARNING);
            return;
        }

        let token = localStorage.getItem(ACCOUNT_TOKEN_NAME)!;
        let request: SavedListRequest = {
            token: token,
        };

        let response = await postRequest<SavedListRequest, SavedListResponse>("youtubent/saved-list/", request);
        if (response == null) {
            return;
        }
        results = response.results;
        savedAmount = response.saved_amount;
        maxAmount = response.max_amount;
    });

    function remove(result: VideoResult) {
        results = results.filter((item) => item.yt_id !== result.yt_id);
        savedAmount -= 1;
    }

    function addAll() {
        playlist.update((value) => {
            let newValue = value;
            for (let result of results) {
                if (newValue.some((item) => item.yt_id === result.yt_id)) {
                    continue;
                }
                newValue.push(result);
            }
            return newValue;
        });
    }

</script>

<div class="container flex flex-col items-center gap-5">
    <p>Your saved songs, you can add these to your playlist</p>
    <p class="text-xl font-bold">You have saved {savedAmount} out of {maxAmount} songs</p>
    <Button class="w-64" pill color="blue" on:click={addAll}>Add all to playlist</Button>
    {#each results as result}
        <VideoElement {result} type={VideoElementType.SAVED} {remove} />
    {/each}
</div>