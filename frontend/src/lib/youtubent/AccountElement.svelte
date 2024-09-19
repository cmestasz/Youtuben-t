<script lang="ts">
	import { postRequest } from '$lib/Fetcher.svelte';
	import { onMount } from 'svelte';
    import { ACCOUNT_TOKEN_NAME } from '$lib/Constants.svelte';

	let userElement: HTMLInputElement;
	let passElement: HTMLInputElement;

	onMount(async () => {
		userElement = document.getElementById('user') as HTMLInputElement;
		passElement = document.getElementById('pass') as HTMLInputElement;
        await autoLogin();
	});

	interface TokenLoginRequest {
		type: string;
		token: string;
	}
	interface TokenLoginResponse {
		token: string;
	}
	async function autoLogin() {
		let token = localStorage.getItem(ACCOUNT_TOKEN_NAME);
		if (token == null) {
			return;
		}

		let request: TokenLoginRequest = {
			type: 'token',
			token: token
		};

		let response = await postRequest<TokenLoginRequest, TokenLoginResponse>(
			'youtubent/login/',
			request
		);
		if (response == null) {
			localStorage.removeItem(ACCOUNT_TOKEN_NAME);
			return;
		}

		localStorage.setItem(ACCOUNT_TOKEN_NAME, token);
	}

	interface CredLoginRequest {
		type: string;
		user: string;
		password: string;
	}
	interface CredLoginResponse {
		token: string;
	}
	async function manualLogin() {
		let user = userElement.value;
		let pass = passElement.value;

		let request: CredLoginRequest = {
			type: 'credentials',
			user: user,
			password: pass
		};

		let response = await postRequest<CredLoginRequest, CredLoginResponse>(
			'youtubent/login/',
			request
		);
		if (response == null) {
			localStorage.removeItem(ACCOUNT_TOKEN_NAME);
			return;
		}

		localStorage.setItem(ACCOUNT_TOKEN_NAME, response.token);
	}

	interface RegisterRequest {
		user: string;
		password: string;
	}
	interface RegisterReponse {
		token: string;
	}
	async function register() {
		let user = userElement.value;
		let pass = userElement.value;
		let request: RegisterRequest = {
			user: user,
			password: pass
		};

		let response = await postRequest<RegisterRequest, RegisterReponse>(
			'/youtubent/register/',
			request
		);
        if (response == null) {
            return;
        }

        localStorage.setItem(ACCOUNT_TOKEN_NAME, response.token);
	}
</script>

<input type="text" id="user" />
<input type="password" id="pass" />
<button on:click={manualLogin}>Login</button>
<button on:click={register}>Register</button>
