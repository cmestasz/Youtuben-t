<script lang="ts">
	import { postRequest } from '$lib/Fetcher.svelte';
	import { onMount } from 'svelte';
	import { ACCOUNT_TOKEN_NAME, USER_NAME } from '$lib/Constants.svelte';

	let userElement: HTMLInputElement;
	let passElement: HTMLInputElement;
	let displayUser: string;

	onMount(async () => {
		await autoLogin();
	});

	interface TokenLoginRequest {
		type: string;
		token: string;
	}
	interface TokenLoginResponse {
		token: string;
		user: string;
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
		localStorage.setItem(USER_NAME, response.user);
		displayUser = response.user;
	}

	interface CredLoginRequest {
		type: string;
		user: string;
		password: string;
	}
	interface CredLoginResponse {
		token: string;
		user: string;
	}
	async function manualLogin() {
		console.log(userElement.value);

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
		localStorage.setItem(USER_NAME, response.user);
		displayUser = response.user;
	}

	interface RegisterRequest {
		user: string;
		password: string;
	}
	interface RegisterReponse {
		token: string;
		user: string;
	}
	async function register() {
		let user = userElement.value;
		let pass = passElement.value;
		let request: RegisterRequest = {
			user: user,
			password: pass
		};

		let response = await postRequest<RegisterRequest, RegisterReponse>(
			'youtubent/register/',
			request
		);
		if (response == null) {
			return;
		}

		localStorage.setItem(ACCOUNT_TOKEN_NAME, response.token);
		localStorage.setItem(USER_NAME, response.user);
		displayUser = response.user;
	}

	interface LogoutRequest {
		token: string;
	}
	async function logout() {
		let token = localStorage.getItem(ACCOUNT_TOKEN_NAME);
		if (token == null) {
			return;
		}

		let request: LogoutRequest = {
			token: token
		};

		let response = await postRequest<LogoutRequest, {}>('youtubent/logout/', request);
		if (response == null) {
			return;
		}

		localStorage.removeItem(ACCOUNT_TOKEN_NAME);
		localStorage.removeItem(USER_NAME);
		displayUser = '';
	}
</script>

<div class="container m-auto flex flex-col items-center gap-5 p-10">
	{#if displayUser}
		<p>Welcome, {displayUser}</p>
		<button on:click={logout}>Logout</button>
	{:else}
		<input bind:this={userElement} type="text" placeholder="User" />
		<input bind:this={passElement} type="password" placeholder="Password" />
		<button on:click={manualLogin}>Login</button>
		<button on:click={register}>Register</button>
	{/if}
</div>
