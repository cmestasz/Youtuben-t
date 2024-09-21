<script>
	import { page } from '$app/stores';
	import { Sidebar, SidebarGroup, SidebarItem, SidebarWrapper } from 'flowbite-svelte';
	import ShortAccountElement from './ShortAccountElement.svelte';
	$: activeUrl = $page.url.pathname;
</script>

<div class="container mx-auto p-2 w-min">
    <ShortAccountElement />
	<Sidebar {activeUrl}>
		<SidebarWrapper>
			<SidebarGroup>
				<SidebarItem label="Youtuben't" href="/youtubent/"></SidebarItem>
				<SidebarItem label="Account and tokens" href="/youtubent/account"></SidebarItem>
				<SidebarItem label="Playlist" href="/youtubent/playlist"></SidebarItem>
				<SidebarItem label="Saved songs" href="/youtubent/saved"></SidebarItem>
                <SidebarItem label="Cached songs" href="/youtubent/cached"></SidebarItem>
			</SidebarGroup>
		</SidebarWrapper>
	</Sidebar>
</div>
