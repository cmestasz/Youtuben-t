<script lang="ts" context="module">
    export interface VideoResult {
        title: string;
        yt_id: string;
        thumbnail: string;
        channel: string;
    }

    export interface PlaylistVideoResult extends VideoResult {
        url: string;
    }

    export enum VideoElementType {
		RESULT = 'result',
		PLAYLIST = 'playlist',
		SAVED = 'saved'
	}
</script>