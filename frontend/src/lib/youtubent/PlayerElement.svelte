<script lang="ts">
	import { onMount } from 'svelte';
	import { playlist } from './Stores.svelte';
	import { Footer, FooterCopyright } from 'flowbite-svelte';
	import { Toggle } from 'flowbite-svelte';

	let audioElement: HTMLAudioElement;
	let audioSourceElement: HTMLSourceElement;
	let currentName: string = '';
	let looping: boolean = false;

	onMount(() => {
		audioElement.addEventListener('ended', () => {
			playlist.update((value) => {
				value.shift();
				currentName = value[0]?.title || '';
				return value;
			});
		});
	});

	playlist.subscribe((value) => {
		currentName = value[0]?.title || '';
		let audioURL = value[0]?.url || '';
		updateAudio(audioURL);
	});

	function updateAudio(audioURL: string) {
		if (audioElement && audioURL !== audioSourceElement.src) {
			if (audioURL !== '') {
				audioSourceElement.src = audioURL;
				audioElement.load();
			} else {
				audioElement.pause();
				audioSourceElement.src = '';
				currentName = '';
				audioElement.load();
			}
		}
	}

	$: if (audioElement) {
		audioElement.loop = looping;
	}
</script>

<Footer
	class="fixed bottom-0 start-0 z-20 w-full border-t border-gray-200 bg-white p-4 shadow md:flex md:items-center md:justify-between md:p-6 dark:border-gray-600 dark:bg-gray-800"
>
	<FooterCopyright href="/" by="Cricro" year={2024} />
	<Toggle bind:checked={looping}>Loop</Toggle>
	<div>
		<p>Now playing: {currentName}</p>
		<audio bind:this={audioElement} controls autoplay>
			<source bind:this={audioSourceElement} type="audio/mpeg" />
			Your browser does not support the audio element.
		</audio>
	</div>
</Footer>
