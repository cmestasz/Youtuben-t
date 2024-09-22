<script lang="ts">
	import Alerts from '$lib/youtubent/Alerts.svelte';
	import PlayerElement from '$lib/youtubent/PlayerElement.svelte';
	import Sidebar from '$lib/youtubent/Sidebar.svelte';
</script>

<div class="container flex flex-row content-around w-full m-auto">
	<Sidebar />
	<div class="container flex flex-col items-center gap-5 pt-5 flex-1">
		<p class="font-bold text-4xl">Not Quite Youtube</p>
		<slot></slot>
	</div>
</div>

<div class="h-40"></div>
<Alerts />
<PlayerElement />
