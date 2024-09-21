<script lang="ts">
	import { onMount } from 'svelte';
	import { USER_NAME } from '$lib/Constants.svelte';

	let displayUser: string | null;

	onMount(() => {
		displayUser = localStorage.getItem(USER_NAME);
	});
</script>

{#if displayUser}
	<div>
		<p class="m-auto p-2 text-xl text-center">Welcome, {displayUser}</p>
	</div>
{/if}
