<script lang="ts" context="module">
    import { ACCOUNT_TOKEN_NAME, YT_TOKEN_NAME } from '$lib/Constants.svelte';
	import type { AlertType } from './Models.svelte';
	import { alerts } from './Stores.svelte';

    export function checkForYTToken() {
		let t = localStorage.getItem(YT_TOKEN_NAME);
		if (t == null) {
			return false;
		}
		return true;
	}

	export function checkForAccountToken() {
		let t = localStorage.getItem(ACCOUNT_TOKEN_NAME);
		if (t == null) {
			return false;
		}
		return true;
	}

	export function updateAlerts(message:string, type: AlertType) {
		alerts.update((list) => {
			let newValue = [];
			for (let alert of list) {
				if (alert.message !== message) {
					newValue.push(alert);
				}
			}
			newValue.push({ type: type, message: message });
			return newValue;
		});
	}
</script>