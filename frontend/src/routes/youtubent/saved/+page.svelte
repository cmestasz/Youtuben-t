<script lang="ts">
	import { ACCOUNT_TOKEN_NAME } from "$lib/Constants.svelte";
	import { postRequest } from "$lib/Fetcher.svelte";
	import { VideoElementType, type VideoResult } from "$lib/youtubent/Models.svelte";
	import { playlist } from "$lib/youtubent/Stores.svelte";
	import { checkForToken } from "$lib/youtubent/Utils.svelte";
	import VideoElement from "$lib/youtubent/VideoElement.svelte";
	import { onMount } from "svelte";

    let results: VideoResult[] = [];
    let savedAmount = 0;
    let maxAmount = 100;

    interface SavedListRequest {
        token: string;
    }
    interface SavedListResponse {
        results: VideoResult[];
        saved_amount: number;
        max_amount: number;
    }
    onMount(async () => {
        if (!checkForToken()) {
            alert("You need an account to save videos!");
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
</script>

<div class="container m-auto flex flex-col items-start gap-5 p-5">
    <p class="text-xl font-bold">You have saved {savedAmount} out of {maxAmount} videos</p>
    {#each results as result}
        <VideoElement {result} type={VideoElementType.SAVED} {remove} />
    {/each}
</div>