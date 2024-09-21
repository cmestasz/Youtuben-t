<script lang="ts">
	import { onMount } from 'svelte';
	import { YT_TOKEN_NAME } from '$lib/Constants.svelte';
	import { checkForToken } from '$lib/youtubent/Utils.svelte';
	import { Button } from 'flowbite-svelte';

	let tokenElement: HTMLInputElement;
	let tokenSet: boolean = false;

	onMount(() => {
		tokenSet = checkForToken();
	});

	function setYTToken() {
		let token = tokenElement.value;
		localStorage.setItem(YT_TOKEN_NAME, token);
		tokenElement.value = '';
		tokenSet = true;
	}
</script>

<div class="flex w-full flex-col items-center gap-6">
	{#if tokenSet}
		<p class="text-green-400 text-center text-xl">Token set</p>
	{:else}
		<p class="text-red-500 text-center text-xl">Make sure to set your token</p>
	{/if}

	<input bind:this={tokenElement} class="block w-1/2" type="password" placeholder="Youtube API Token" />
	<Button class="w-64" pill color="green" on:click={setYTToken}>Set Youtube API Token</Button>
</div>
