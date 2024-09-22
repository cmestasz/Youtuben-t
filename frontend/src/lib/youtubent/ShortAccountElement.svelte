<script lang="ts">
	import { USER_NAME } from '$lib/Constants.svelte';
	import { user_name } from '$lib/youtubent/Stores.svelte';
	import { onMount } from 'svelte';

	let displayUser = '';

	onMount(() => {
		displayUser = localStorage.getItem(USER_NAME) || '';
	});

	user_name.subscribe((value) => {
		displayUser = value;
	});

</script>

{#if displayUser != ''}
	<div>
		<p class="m-auto p-2 text-center text-xl">Welcome, {displayUser}</p>
	</div>
{/if}
