<script lang="ts">
	import { Alert } from 'flowbite-svelte';
	import type { AlertMessage } from './Models.svelte';
	import { alerts } from './Stores.svelte';

	let activeAlerts: AlertMessage[] = [];
	const timeoutMap = new Map<string, number>();
	const ALERT_TIMEOUT = 5000;

	alerts.subscribe((value) => {
		activeAlerts = value;

		value.forEach((alert) => {
			if (timeoutMap.has(alert.message)) {
				clearTimeout(timeoutMap.get(alert.message));
				timeoutMap.delete(alert.message);
			}

			const timeoutID = setTimeout(() => {
				remove(alert);
				timeoutMap.delete(alert.message);
			}, ALERT_TIMEOUT);
			timeoutMap.set(alert.message, timeoutID);
		});
	});

	function remove(alert: AlertMessage) {
		alerts.update((value) => {
			return value.filter((item) => item !== alert);
		});
	}
</script>

<div class="fixed bottom-0 right-0 z-50 flex flex-col gap-2 p-5">
	{#each activeAlerts as alert (alert.message)}
		<Alert class="text-lg" color={alert.type} dismissable on:click={() => remove(alert)}>
			{alert.message}
		</Alert>
	{/each}
</div>
