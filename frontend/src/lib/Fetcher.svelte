<script lang="ts" context="module">
	import { API_URL } from '$lib/Constants.svelte';
	import { AlertType } from './youtubent/Models.svelte';
	import { updateAlerts } from './youtubent/Utils.svelte';

	export async function getRequest<Response>(url: string) {
		let dest: string = API_URL + url;
		const response = await fetch(dest);
		if (!response.ok) {
            let obj: Error = await response.json();
            updateAlerts(obj.error, AlertType.ERROR);
			console.log(obj.error);
            return null;
		}
		let obj: Response = await response.json();
		console.log(obj);
		return obj;
	}

    interface Error {
        error: string;
    }

	export async function postRequest<Request, Response>(url: string, data: Request) {
		let dest: string = API_URL + url;
		const response = await fetch(dest, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});
		if (!response.ok) {
            let obj: Error = await response.json();
            updateAlerts(obj.error, AlertType.ERROR);
			console.log(obj.error);
            return null;
        }
		let obj: Response = await response.json();
		console.log(obj);
		return obj;
	}
</script>