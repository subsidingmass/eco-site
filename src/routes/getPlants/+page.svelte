<script lang="ts">
	import Navbar from '../../components/Navbar.svelte';
	import { onMount } from 'svelte';

	// Modal controller
	let modal: HTMLDialogElement;

	function openModal(plantData: Plant) {
		selectedPlant = plantData;
		isChecked = selectedPlant.conservation_status === 'Endangered';
		modal.showModal();
	}

	function closeModal() {
		modal.close();
	}

	interface Plant {
		id: number;
		common_name: string;
		first_nations_name: string;
		scientific_name: string;
		first_nations_uses: string;
		description: string;
		latitude: number;
		longitude: number;
		conservation_status: string;
		kml_file: string | null;
		image: string | null;
	}

	let plants: Plant[] = [];
	let filteredPlants: Plant[] = [];
	let selectedPlant: Plant | null = null;
	let loading: boolean = true;
	let error: string | null = null;
	let searchQuery: string = '';
	let isChecked: boolean = false;

	let kmlFile: File | null = null;
	let imageFile: File | null = null;
	let keepExistingKml: boolean = true;
	let keepExistingImage: boolean = true;

	onMount(async () => {
		try {
			const res = await fetch('http://localhost:5000/api/plants');
			if (res.ok) {
				plants = await res.json();
				filteredPlants = plants;
			} else {
				error = 'Failed to fetch plants data';
			}
		} catch (e) {
			if (e instanceof Error) {
				error = 'Error: ' + e.message;
			} else {
				error = 'An unknown error occurred';
			}
		} finally {
			loading = false;
		}
	});

	function handleSearch(event: Event) {
		const input = event.target as HTMLInputElement;
		searchQuery = input.value.toLowerCase();
		filteredPlants = plants.filter(
			(plant) =>
				plant.id.toString().toLowerCase().includes(searchQuery) ||
				plant.common_name.toLowerCase().includes(searchQuery) ||
				plant.first_nations_name.toLowerCase().includes(searchQuery) ||
				plant.scientific_name.toLowerCase().includes(searchQuery) ||
				plant.first_nations_uses.toLowerCase().includes(searchQuery) ||
				plant.description.toLowerCase().includes(searchQuery) ||
				plant.conservation_status.toLowerCase().includes(searchQuery)
		);
	}

	async function handleSubmit(event: Event) {
		event.preventDefault();
		if (!selectedPlant) return;

		const formData = new FormData();
		formData.append('common_name', selectedPlant.common_name);
		formData.append('first_nations_name', selectedPlant.first_nations_name || '');
		formData.append('scientific_name', selectedPlant.scientific_name);
		formData.append('first_nations_uses', selectedPlant.first_nations_uses || '');
		formData.append('description', selectedPlant.description || '');
		formData.append('latitude', String(selectedPlant.latitude));
		formData.append('longitude', String(selectedPlant.longitude));
		formData.append('conservation_status', isChecked ? 'Endangered' : 'Normal');

		if (!keepExistingKml && kmlFile) {
			formData.append('kml_file', kmlFile);
		}

		if (!keepExistingImage && imageFile) {
			formData.append('image', imageFile);
		}

		try {
			const response = await fetch(`http://localhost:5000/api/plants/${selectedPlant.id}`, {
				method: 'PUT',
				body: formData
			});

			if (response.ok) {
				const updatedPlant = await response.json();

				// Update the plant in the list
				plants = plants.map((plant) => (plant.id === updatedPlant.id ? updatedPlant : plant));
				filteredPlants = filteredPlants.map((plant) =>
					plant.id === updatedPlant.id ? updatedPlant : plant
				);

				closeModal();
			} else {
				error = `Failed to update plant data: ${response.statusText}`;
				console.error('Update error:', response.statusText);
			}
		} catch (e) {
			error = e instanceof Error ? `Error: ${e.message}` : 'An unknown error occurred';
			console.error('Request error:', e);
		}
	}

	function handleKmlFileChange(event: Event) {
		const input = event.target as HTMLInputElement | null;
		if (input?.files) {
			kmlFile = input.files[0];
		}
	}

	function handleImageFileChange(event: Event) {
		const input = event.target as HTMLInputElement | null;
		if (input?.files) {
			imageFile = input.files[0];
		}
	}
</script>

<main class="bg-base-200">
	<Navbar />
	<div class="hero bg-base-200 min-h-screen">
		<div class="hero-content flex-col lg:flex-row">
			<div>
				<h1 class="text-8xl font-bold">Welcome to the Full Plant Index</h1>
				<p class="py-9">Here you can view all the plants in the database.</p>
				<button class="btn btn-primary">Get Started</button>
			</div>
		</div>
	</div>

	<div class="bg-base-200 py-4">
		<div class="divider divider-primary"></div>
		<input
			type="text"
			placeholder="Search"
			class="input input-bordered w-full"
			on:input={handleSearch}
		/>

		<div class="divider divider-primary"></div>
	</div>

	{#if loading}
		<div class="flex justify-center items-center h-screen bg-base-200">
			<span class="loading loading-ring loading-lg"></span>
		</div>
	{:else if error}
		<div class="flex justify-center items-center h-screen bg-base-200 flex-col">
			<h1 class="text-4xl font-bold">Oops. An error has occurred</h1>
			<h2 class="text-2xl">Error: {error}</h2>
			<button class="btn btn-primary mt-4" on:click={() => openModal(null)}
				>Contact Developer</button
			>
			<dialog bind:this={modal} class="modal">
				<div class="modal-box">
					<h3 class="text-lg font-bold mb-5">Please Fill Form</h3>
					<textarea class="textarea textarea-primary textarea-lg" placeholder="Message"></textarea>
					<form method="dialog" class="modal-backdrop">
						<button>close</button>
					</form>
				</div>
			</dialog>
		</div>
	{:else}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4 bg-base-200">
			{#each filteredPlants as plant}
				<div class="card card-bordered lg:card-side bg-base-100 shadow-xl">
					{#if plant.image}
						<figure>
							<img src={`data:image/png;base64,${plant.image}`} alt={plant.common_name} />
						</figure>
					{/if}
					<div class="card-body">
						<h2 class="card-title">{plant.common_name}</h2>
						<p><strong>Plant ID:</strong> {plant.id}</p>
						<p><strong>First Nations Name:</strong> {plant.first_nations_name}</p>
						<p><strong>Scientific Name:</strong> {plant.scientific_name}</p>
						<p><strong>Uses:</strong> {plant.first_nations_uses}</p>
						<p><strong>Description:</strong> {plant.description}</p>
						<p><strong>Latitude:</strong> {plant.latitude}</p>
						<p><strong>Longitude:</strong> {plant.longitude}</p>
						<p><strong>Conservation Status:</strong> {plant.conservation_status}</p>
						<button class="btn btn-primary" on:click={() => openModal(plant)}>Edit</button>
					</div>
				</div>
			{/each}
		</div>
	{/if}
	<dialog bind:this={modal} class="modal">
		{#if selectedPlant}
			<div class="modal-box">
				<h3 class="font-bold text-lg">Edit Plant: {selectedPlant.common_name}</h3>
				<form on:submit={handleSubmit} class="form-control">
					<div class="grid grid-cols-2 gap-4">
						<div class="form-control">
							<label for="common_name" class="label">Common Name</label>
							<input
								id="common_name"
								type="text"
								bind:value={selectedPlant.common_name}
								class="input input-bordered"
							/>
						</div>
						<div class="form-control">
							<label for="first_nations_name" class="label">First Nations Name</label>
							<input
								id="first_nations_name"
								type="text"
								bind:value={selectedPlant.first_nations_name}
								class="input input-bordered"
							/>
						</div>
						<div class="form-control">
							<label for="scientific_name" class="label">Scientific Name</label>
							<input
								id="scientific_name"
								type="text"
								bind:value={selectedPlant.scientific_name}
								class="input input-bordered"
							/>
						</div>
						<div class="form-control">
							<label for="first_nations_uses" class="label">First Nations Uses</label>
							<input
								id="first_nations_uses"
								type="text"
								bind:value={selectedPlant.first_nations_uses}
								class="input input-bordered"
							/>
						</div>
						<div class="form-control col-span-2">
							<label for="description" class="label">Description</label>
							<textarea
								id="description"
								bind:value={selectedPlant.description}
								class="textarea textarea-bordered"
							></textarea>
						</div>
						<div class="form-control">
							<label for="latitude" class="label">Latitude</label>
							<input
								id="latitude"
								type="number"
								step="any"
								bind:value={selectedPlant.latitude}
								class="input input-bordered"
							/>
						</div>
						<div class="form-control">
							<label for="longitude" class="label">Longitude</label>
							<input
								id="longitude"
								type="number"
								step="any"
								bind:value={selectedPlant.longitude}
								class="input input-bordered"
							/>
						</div>
						<div class="form-control col-span-2 flex items-center">
							<label for="conservation_status" class="label cursor-pointer">
								<span class="label-text">Endangered</span>
								<input
									id="conservation_status"
									type="checkbox"
									bind:checked={isChecked}
									class="checkbox checkbox-primary ml-2"
								/>
							</label>
						</div>
						<div class="form-control col-span-2">
							<label for="kml_file" class="label">KML File</label>
							<input
								id="kml_file"
								type="file"
								on:change={handleKmlFileChange}
								class="file-input file-input-bordered"
							/>
							<div class="flex items-center mt-2">
								<input
									type="checkbox"
									id="keep_existing_kml"
									bind:checked={keepExistingKml}
									class="checkbox checkbox-primary ml-2"
								/>
								<label for="keep_existing_kml" class="ml-2">Keep existing KML file</label>
							</div>
						</div>
						<div class="form-control col-span-2">
							<label for="image" class="label">Image</label>
							<input
								id="image"
								type="file"
								on:change={handleImageFileChange}
								class="file-input file-input-bordered"
							/>
							<div class="flex items-center mt-2">
								<input
									type="checkbox"
									id="keep_existing_image"
									bind:checked={keepExistingImage}
									class="checkbox checkbox-primary ml-2"
								/>
								<label for="keep_existing_image" class="ml-2">Keep existing image</label>
							</div>
						</div>
					</div>
					<div class="modal-action">
						<button type="submit" class="btn btn-primary">Save Changes</button>
						<button type="button" class="btn" on:click={closeModal}>Cancel</button>
					</div>
				</form>
			</div>
			<form method="dialog" class="modal-backdrop">
				<button>close</button>
			</form>
			<div class="toast">
				<div class="alert alert-secondary">
					<span>Click off the modal or press <kbd class="kbd kbd-sm">Esc</kbd> to close.</span>
				</div>
			</div>
		{/if}
	</dialog>
</main>
