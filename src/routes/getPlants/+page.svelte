<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let modal: HTMLDialogElement;
	let addModal: HTMLDialogElement;

	// Plant interface
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

	// Plant data variables
	let plants: Plant[] = [];
	let filteredPlants: Plant[] = [];
	let selectedPlant: Plant | null = null;
	let newPlant: Plant = {
		id: 0,
		common_name: '',
		first_nations_name: '',
		scientific_name: '',
		first_nations_uses: '',
		description: '',
		latitude: 0,
		longitude: 0,
		conservation_status: 'Normal',
		kml_file: null,
		image: null
	};

	// UI state variables
	let loading: boolean = true;
	let error: string | null = null;
	let searchQuery: string = '';
	let isChecked: boolean = false;

	// File upload variables
	let kmlFile: File | null = null;
	let imageFile: File | null = null;
	let keepExistingKml: boolean = true;
	let keepExistingImage: boolean = true;

	// Fetch plants data on mount
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

	// Search function
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

	// Open and close edit modal
	function openModal(plantData: Plant) {
		selectedPlant = plantData;
		isChecked = selectedPlant.conservation_status === 'Endangered';
		modal.showModal();
	}

	function closeModal() {
		modal.close();
	}

	// Open and close add plant modal
	function openAddModal() {
		newPlant = {
			id: 0,
			common_name: '',
			first_nations_name: '',
			scientific_name: '',
			first_nations_uses: '',
			description: '',
			latitude: 0,
			longitude: 0,
			conservation_status: 'Normal',
			kml_file: null,
			image: null
		};
		addModal.showModal();
	}

	function closeAddModal() {
		addModal.close();
	}

	async function handleDelete(plantId: number) {
    if (confirm("Are you sure you want to delete this plant?")) {
        try {
            const response = await fetch(`http://localhost:5000/api/plants/${plantId}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                // Remove the deleted plant from the local state
                plants = plants.filter((plant) => plant.id !== plantId);
                filteredPlants = filteredPlants.filter((plant) => plant.id !== plantId);
            } else {
                error = `Failed to delete plant: ${response.statusText}`;
                console.error('Delete error:', response.statusText);
            }
        } catch (e) {
            error = e instanceof Error ? `Error: ${e.message}` : 'An unknown error occurred';
            console.error('Request error:', e);
        }
    }
}
	// Handle editing a plant submission
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

	// Handle adding a new plant submission
	async function handleSubmitNewPlant(event: Event) {
		event.preventDefault();

		const formData = new FormData();
		formData.append('common_name', newPlant.common_name);
		formData.append('first_nations_name', newPlant.first_nations_name || '');
		formData.append('scientific_name', newPlant.scientific_name);
		formData.append('first_nations_uses', newPlant.first_nations_uses || '');
		formData.append('description', newPlant.description || '');
		formData.append('latitude', String(newPlant.latitude));
		formData.append('longitude', String(newPlant.longitude));
		formData.append('conservation_status', newPlant.conservation_status);

		if (kmlFile) formData.append('kml_file', kmlFile);
		if (imageFile) formData.append('image', imageFile);

		try {
			const response = await fetch('http://localhost:5000/api/plants', {
				method: 'POST',
				body: formData
			});

			if (response.ok) {
				const addedPlant = await response.json();

				// Add the new plant to the list
				plants = [...plants, addedPlant];
				filteredPlants = [...filteredPlants, addedPlant];

				closeAddModal();
			} else {
				error = `Failed to add new plant: ${response.statusText}`;
				console.error('Add error:', response.statusText);
			}
		} catch (e) {
			error = e instanceof Error ? `Error: ${e.message}` : 'An unknown error occurred';
			console.error('Request error:', e);
		}
	}

	// Handle file changes for editing plant
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

	// Handle file changes for adding new plant
	function handleNewKmlFileChange(event: Event) {
		const input = event.target as HTMLInputElement | null;
		if (input?.files) {
			kmlFile = input.files[0];
		}
	}

	function handleNewImageFileChange(event: Event) {
		const input = event.target as HTMLInputElement | null;
		if (input?.files) {
			imageFile = input.files[0];
		}
	}
</script>

<main class="bg-base-200">
	<div class="hero bg-base-200 min-h-screen">
		<div class="hero-content flex-col lg:flex-row">
			<div>
				<h1 class="text-8xl font-bold">Plant Index</h1>
			</div>
		</div>
	</div>

	<div class="bg-base-200 py-4 flex justify-center">
		<div class="flex w-3/4 space-x-4">
			<input
				type="text"
				placeholder="Search"
				class="input input-bordered flex-grow"
				on:input={handleSearch}
			/>
			<button class="btn btn-primary" on:click={openAddModal}>Add New Plant</button>
		</div>
	</div>

	{#if loading}
		<div class="flex justify-center items-center h-screen bg-base-200">
			<span class="loading loading-ring loading-lg"></span>
		</div>
	{:else if error}
		<div>
			<h1>error</h1>
		</div>
	{:else}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4 bg-base-200">
			{#each filteredPlants as plant}
				<div class="card card-bordered lg:card-side bg-base-100 shadow-xl">
					{#if plant.image}
    <figure class="w-full h-48 bg-base-300 overflow-hidden flex items-center justify-center">
        <img 
            src={`data:image/png;base64,${plant.image}`} 
            alt={plant.common_name} 
            class="object-cover w-full h-full"
        />
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
						<button class="btn btn-errror" on:click={() => handleDelete(plant.id)}>Delete</button>
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
		<dialog bind:this={addModal} class="modal">
		<div class="modal-box">
			<h3 class="font-bold text-lg">Add New Plant</h3>
			<form on:submit={handleSubmitNewPlant} class="form-control">
				<div class="grid grid-cols-2 gap-4">
					<div class="form-control">
						<label for="new_common_name" class="label">Common Name</label>
						<input
							id="new_common_name"
							type="text"
							bind:value={newPlant.common_name}
							class="input input-bordered"
						/>
					</div>
					<div class="form-control">
						<label for="new_first_nations_name" class="label">First Nations Name</label>
						<input
							id="new_first_nations_name"
							type="text"
							bind:value={newPlant.first_nations_name}
							class="input input-bordered"
						/>
					</div>
					<div class="form-control">
						<label for="new_scientific_name" class="label">Scientific Name</label>
						<input
							id="new_scientific_name"
							type="text"
							bind:value={newPlant.scientific_name}
							class="input input-bordered"
						/>
					</div>
					<div class="form-control">
						<label for="new_first_nations_uses" class="label">First Nations Uses</label>
						<input
							id="new_first_nations_uses"
							type="text"
							bind:value={newPlant.first_nations_uses}
							class="input input-bordered"
						/>
					</div>
					<div class="form-control col-span-2">
						<label for="new_description" class="label">Description</label>
						<textarea
							id="new_description"
							bind:value={newPlant.description}
							class="textarea textarea-bordered"
						></textarea>
					</div>
					<div class="form-control">
						<label for="new_latitude" class="label">Latitude</label>
						<input
							id="new_latitude"
							type="number"
							step="any"
							bind:value={newPlant.latitude}
							class="input input-bordered"
						/>
					</div>
					<div class="form-control">
						<label for="new_longitude" class="label">Longitude</label>
						<input
							id="new_longitude"
							type="number"
							step="any"
							bind:value={newPlant.longitude}
							class="input input-bordered"
						/>
					</div>
					<div class="form-control col-span-2 flex items-center">
						<label for="new_conservation_status" class="label cursor-pointer">
							<span class="label-text">Endangered</span>
							<input
								id="new_conservation_status"
								type="checkbox"
								bind:checked={isChecked}
								class="checkbox checkbox-primary ml-2"
							/>
						</label>
					</div>
					<div class="form-control col-span-2">
						<label for="new_kml_file" class="label">KML File</label>
						<input
							id="new_kml_file"
							type="file"
							on:change={handleKmlFileChange}
							class="file-input file-input-bordered"
						/>
					</div>
					<div class="form-control col-span-2">
						<label for="new_image" class="label">Image</label>
						<input
							id="new_image"
							type="file"
							on:change={handleImageFileChange}
							class="file-input file-input-bordered"
						/>
					</div>
				</div>
				<div class="modal-action">
					<button type="submit" class="btn btn-primary">Add Plant</button>
					<button type="button" class="btn" on:click={closeAddModal}>Cancel</button>
				</div>
			</form>
		</div>
	</dialog>
		<div class="btm-nav">
  <button on:click={() => {goto('/')}}>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
    </svg>
  </button>
  <button>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  </button>
  <button class="active">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
    </svg>
  </button>
</div>
</main>
