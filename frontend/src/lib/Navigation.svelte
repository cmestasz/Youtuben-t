<script>
	import {
		Navbar,
		NavBrand,
		NavLi,
		NavUl,
		NavHamburger,
		Dropdown,
		DropdownItem,
		DropdownDivider
	} from 'flowbite-svelte';
	import { page } from '$app/stores';
	import NavContainer from 'flowbite-svelte/NavContainer.svelte';

	$: activeURL = $page.url.pathname;
</script>

<Navbar let:NavContainer color="primary">
	<NavContainer class="border, rounded-lg bg-white px-5 py-2 dark:bg-gray-600">
		<NavBrand href="/">
			<span class="self-center whitespace-nowrap text-xl font-semibold">Cricro's place</span>
		</NavBrand>
		<NavHamburger />
		<NavUl>
			<NavLi class="cursor-pointer">Toys</NavLi>
			<Dropdown>
				<DropdownItem href="/youtubent">Youtuben't</DropdownItem>
				<DropdownItem href="/">Test</DropdownItem>
				<DropdownItem href="/">Test</DropdownItem>
			</Dropdown>
		</NavUl>
	</NavContainer>
</Navbar>
