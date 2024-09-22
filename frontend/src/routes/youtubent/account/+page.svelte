<script lang="ts">
	import AccountElement from './AccountElement.svelte';
	import YtTokenElement from './YTTokenElement.svelte';
</script>

<div class="container flex flex-col items-center gap-10">
	<p>Check out or create your account and set your Youtube API token</p>
	<AccountElement />
	<YtTokenElement />
</div>
