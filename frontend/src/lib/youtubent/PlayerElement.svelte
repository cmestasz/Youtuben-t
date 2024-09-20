<script lang="ts">
	export let audioURL: string;
</script>

<div>
	<p>Now playing:</p>
	<audio controls autoplay>
		<source src={audioURL} type="audio/mpeg" id="player" />
		Your browser does not support the audio element.
	</audio>
</div>