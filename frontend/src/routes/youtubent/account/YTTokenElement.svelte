<script lang="ts">
	import { onMount } from 'svelte';
	import { YT_TOKEN_NAME } from '$lib/Constants.svelte';
	import { checkForToken } from '$lib/youtubent/Utils.svelte';

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

<div class="flex w-max flex-col gap-2">
	{#if tokenSet}
		<p class="text-green-400">Token set</p>
	{:else}
		<p class="text-red-500">Make sure to set your token</p>
	{/if}

	<input bind:this={tokenElement} class="block" type="password" placeholder="Youtube API Token" />
	<button class="bg-gray-400 p-2" on:click={setYTToken}>Set Youtube API Token</button>
</div>
