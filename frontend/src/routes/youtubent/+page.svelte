<script lang="ts">
	import PlayerElement from '$lib/youtubent/PlayerElement.svelte';
	import Navigation from '../../lib/Navigation.svelte';
	import Sidebar from '$lib/youtubent/Sidebar.svelte';
	import SearchElement from './SearchElement.svelte';
</script>

<div class="container m-auto flex flex-col items-center gap-5 p-10">
	<p class="text-xl font-bold">Not Quite Youtube</p>

	<SearchElement />
</div>