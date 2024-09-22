<script lang="ts">
	import { postRequest } from '$lib/Fetcher.svelte';
	import { onMount } from 'svelte';
	import { ACCOUNT_TOKEN_NAME, USER_NAME } from '$lib/Constants.svelte';
	import { Button } from 'flowbite-svelte';
	import { user_name } from '$lib/youtubent/Stores.svelte';
	import { updateAlerts } from '$lib/youtubent/Utils.svelte';
	import { AlertType } from '$lib/youtubent/Models.svelte';

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
		user_name.set(response.user);
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
		user_name.set(response.user);
		displayUser = response.user;
		updateAlerts('Logged in successfully', AlertType.SUCCESS);
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
		user_name.set(response.user);
		displayUser = response.user;
		updateAlerts('Registered successfully', AlertType.SUCCESS);
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
		user_name.set('');
		displayUser = '';
		updateAlerts('Logged out successfully', AlertType.SUCCESS);
	}
</script>

<div class="container m-auto flex w-full flex-col items-center gap-6">
	{#if displayUser}
		<p class="text-2xl">Welcome, {displayUser}!</p>
		<Button class="w-64" pill color="red" on:click={logout}>Logout</Button>
	{:else}
		<input class="block w-1/2" bind:this={userElement} type="text" placeholder="User" />
		<input class="block w-1/2" bind:this={passElement} type="password" placeholder="Password" />
		<div class="flex flex-row gap-5">
			<Button class="w-64" pill on:click={manualLogin}>Login</Button>
			<Button class="w-64" pill on:click={register}>Register</Button>
		</div>
	{/if}
</div>
