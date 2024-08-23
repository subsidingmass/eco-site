<script lang="ts">
	import '../app.css';
	import { setTheme, getTheme } from '$lib/themeManager';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let currentTheme: string = getTheme() || 'night';

	function changeTheme(event: Event) {
		const input = event.target as HTMLInputElement;
		const theme = input.value;
		setTheme(theme);
		currentTheme = theme; // Update local state if needed
	}

	onMount(() => {
		// Apply the saved theme when the component mounts
		const savedTheme = getTheme();
		if (savedTheme) {
			setTheme(savedTheme);
			currentTheme = savedTheme;
		}
	});

	function navigateToIndex() {
		goto('/');
	}

	//modal controller
	let modal: HTMLDialogElement;

	function openModal() {
		modal.showModal();
	}
</script>

<main>
	<div class="navbar bg-base-100 flex justify-between items-center">
		<div class="flex items-center">
			<button class="btn btn-primary m-3" on:click={() => goto('/')}>Home</button>
			<div class="dropdown flex-none">
				<div tabindex="0" role="button" class="btn m-1">
					Theme
					<svg
						width="12px"
						height="12px"
						class="inline-block h-2 w-2 fill-current opacity-60"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 2048 2048"
					>
						<path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z"></path>
					</svg>
				</div>
				<ul class="dropdown-content bg-base-300 rounded-box z-[1] w-52 p-2 shadow-2xl">
					<li>
						<input
							type="radio"
							name="theme-dropdown"
							class="theme-controller btn btn-sm btn-block btn-ghost justify-start"
							aria-label="Dark"
							value="night"
							checked={currentTheme === 'night'}
							on:change={changeTheme}
						/>
					</li>
					<li>
						<input
							type="radio"
							name="theme-dropdown"
							class="theme-controller btn btn-sm btn-block btn-ghost justify-start"
							aria-label="Light"
							value="emerald"
							checked={currentTheme === 'emerald'}
							on:change={changeTheme}
						/>
					</li>
					<li>
						<input
							type="radio"
							name="theme-dropdown"
							class="theme-controller btn btn-sm btn-block btn-ghost justify-start"
							aria-label="Pastel"
							value="pastel"
							checked={currentTheme === 'pastel'}
							on:change={changeTheme}
						/>
					</li>
					<li>
						<input
							type="radio"
							name="theme-dropdown"
							class="theme-controller btn btn-sm btn-block btn-ghost justify-start"
							aria-label="Forest"
							value="forest"
							checked={currentTheme === 'forest'}
							on:change={changeTheme}
						/>
					</li>
					<li>
						<input
							type="radio"
							name="theme-dropdown"
							class="theme-controller btn btn-sm btn-block btn-ghost justify-start"
							aria-label="Nord"
							value="nord"
							checked={currentTheme === 'nord'}
							on:change={changeTheme}
						/>
					</li>
					<li>
						<input
							type="radio"
							name="theme-dropdown"
							class="theme-controller btn btn-sm btn-block btn-ghost justify-start"
							aria-label="Retro"
							value="retro"
							checked={currentTheme === 'retro'}
							on:change={changeTheme}
						/>
					</li>
				</ul>
			</div>
		</div>
		<button class="btn btn-primary mr-3" on:click={openModal}>Navigation</button>
		<dialog bind:this={modal} class="modal">
			<div class="modal-box">
				<h3 class="text-lg font-bold mb-5">Where would you like to go?</h3>
				<div class="flex w-full flex-col">
					<button class="btn btn-primary" on:click={() => goto('/getPlants')}
						>Full Plant Index</button
					>
					<div class="divider"></div>
					<button class="btn btn-primary" on:click={() => goto('/createPlant')}
						>Create New Plant</button
					>
					<div class="divider"></div>
					<button class="btn btn-primary" on:click={() => goto('/about')}>About Us</button>
				</div>
				<p class="py-4">Press ESC key or click outside to close</p>
			</div>
			<form method="dialog" class="modal-backdrop">
				<button>close</button>
			</form>
		</dialog>
	</div>
</main>
