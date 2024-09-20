<script lang="ts">
	import { onMount } from 'svelte';
	import { YT_TOKEN_NAME } from '$lib/Constants.svelte';

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

<div class="flex w-max flex-col gap-2">
	{#if ytToken == null}
		<p class="text-red-500">Make sure to set your token</p>
	{:else}
		<p class="text-green-400">Token set</p>
	{/if}

	<input class="block" type="password" id="ytToken" placeholder="Youtube API Token" />
	<button class="bg-gray-400 p-2" on:click={setYTToken}>Set Youtube API Token</button>
</div>
