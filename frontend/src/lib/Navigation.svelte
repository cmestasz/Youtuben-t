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
</script>

<Navbar let:NavContainer color="primary">
	<NavContainer class="border, rounded-lg bg-white px-5 py-2 dark:bg-gray-600">
		<NavBrand href="/">
			<span class="self-center whitespace-nowrap text-xl font-semibold">Toys!</span>
		</NavBrand>
		<NavHamburger />
		<NavUl>
			<NavLi class="cursor-pointer">Tiny toys</NavLi>
			<Dropdown>
				<DropdownItem href="/youtubent">Youtuben't</DropdownItem>
			</Dropdown>
		</NavUl>
	</NavContainer>
</Navbar>
