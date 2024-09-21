<script lang="ts">
	import { audioURL } from './Stores.svelte';
	import { Footer, FooterLinkGroup, FooterLink, ImagePlaceholder, TextPlaceholder, Skeleton, FooterCopyright } from 'flowbite-svelte';

	let audioElement: HTMLAudioElement;
	let audioSourceElement: HTMLSourceElement;

	audioURL.subscribe(updateAudio);

	function updateAudio(audioURL: string) {
		if (audioElement && audioURL !== '' && audioURL !== audioSourceElement.src) {
			audioSourceElement.src = audioURL;
			audioElement.load();
		}
	}
</script>



<Footer class="absolute bottom-0 start-0 z-20 w-full p-4 bg-white border-t border-gray-200 shadow md:flex md:items-center md:justify-between md:p-6 dark:bg-gray-800 dark:border-gray-600">
	<FooterCopyright href="/" by="Cricro" year={2024} />
	<div>
		<p>Now playing:</p>
		<audio bind:this={audioElement} controls autoplay volume=0.2>
			<source bind:this={audioSourceElement} type="audio/mpeg" />
			Your browser does not support the audio element.
		</audio>
	</div>
</Footer>