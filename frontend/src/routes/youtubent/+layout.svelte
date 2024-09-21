<script lang="ts">
    import PlayerElement from '$lib/youtubent/PlayerElement.svelte';
import Sidebar from '$lib/youtubent/Sidebar.svelte';
</script>

<Sidebar />
<slot></slot>
<PlayerElement />