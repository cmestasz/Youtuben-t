<script lang="ts">
    import { onMount } from "svelte";
    import { YT_TOKEN_NAME } from "$lib/Constants.svelte";
    
    let tokenElement: HTMLInputElement;
    export let ytToken: string;
    export let checkForToken: () => boolean;

    onMount(() => {
        tokenElement = document.getElementById('ytToken') as HTMLInputElement;
        checkForToken();
    });

    function setYTToken() {
		let token = tokenElement.value;
		localStorage.setItem(YT_TOKEN_NAME, token);
        tokenElement.value = '';
	}
</script>

{#if ytToken == null}
	<p>Make sure to set your token</p>
{:else}
	<p>Token set</p>
{/if}
<input type="password" id="ytToken" placeholder="Youtube API Token" />
<button on:click={setYTToken}>Set Youtube API Token</button>
