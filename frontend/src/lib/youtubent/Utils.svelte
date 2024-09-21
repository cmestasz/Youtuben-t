<script lang="ts" context="module">
    import { YT_TOKEN_NAME } from '$lib/Constants.svelte';

    export function checkForToken() {
		let t = localStorage.getItem(YT_TOKEN_NAME);
		if (t == null) {
			return false;
		}
		return true;
	}
</script>