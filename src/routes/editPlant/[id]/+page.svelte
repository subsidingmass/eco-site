<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';

  let modal: HTMLDialogElement;

  function openModal() {
    if (modal) {
      modal.showModal();
    }
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

  let plant: Plant | null = null;
  let loading: boolean = true;
  let error: string | null = null;
  let kmlFile: File | null = null;
  let imageFile: File | null = null;
  let keepExistingKml: boolean = true;
  let keepExistingImage: boolean = true;
  let isChecked: boolean = false;

  const { id } = $page.params;

  // Fetch plant data on component mount
  onMount(async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/plants/${id}`);
      if (response.ok) {
        plant = await response.json();
        isChecked = plant.conservation_status === 'Endangered';
      } else {
        error = 'Failed to fetch plant data';
      }
    } catch (e) {
      error = e instanceof Error ? 'Error: ' + e.message : 'An unknown error occurred';
    } finally {
      loading = false;
    }
  });

  // Handle form submission
  async function handleSubmit(event: Event) {
    event.preventDefault();
    if (!plant) return;

    const formData = new FormData();
    formData.append('common_name', plant.common_name);
    formData.append('first_nations_name', plant.first_nations_name || '');
    formData.append('scientific_name', plant.scientific_name);
    formData.append('first_nations_uses', plant.first_nations_uses || '');
    formData.append('description', plant.description || '');
    formData.append('latitude', String(plant.latitude));
    formData.append('longitude', String(plant.longitude));
    formData.append('conservation_status', isChecked ? 'Endangered' : 'Normal');

    if (!keepExistingKml && kmlFile) {
      formData.append('kml_file', kmlFile);
    }

    if (!keepExistingImage && imageFile) {
      formData.append('image', imageFile);
    }

    try {
      const response = await fetch(`http://localhost:5000/api/plants/${id}`, {
        method: 'PUT',
        body: formData,
      });

      if (response.ok) {
        goto(`/getPlants`);
      } else {
        error = `Failed to update plant data: ${response.statusText}`;
        console.error('Update error:', response.statusText);
      }
    } catch (e) {
      error = e instanceof Error ? `Error: ${e.message}` : 'An unknown error occurred';
      console.error('Request error:', e);
    }
  }

  // Handle KML file input change
  function handleKmlFileChange(event: Event) {
    const input = event.target as HTMLInputElement | null;
    if (input?.files) {
      kmlFile = input.files[0];
    }
  }

  // Handle image file input change
  function handleImageFileChange(event: Event) {
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
        <h1 class="text-5xl font-bold">Edit Plant</h1>
        <p class="py-6">
          Modify the details of the selected plant.
        </p>
      </div>
    </div>
  </div>

  <div class="bg-base-200 py-4">
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
      <button class="btn btn-primary mt-4" on:click={openModal}>Contact Developer</button>
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
    {#if plant}
      <form on:submit={handleSubmit} class="p-4">
        <div class="grid grid-cols-1 gap-4">
          <div>
            <label for="common_name" class="label">Common Name</label>
            <input id="common_name" type="text" bind:value={plant?.common_name} class="input input-primary w-full" />
          </div>
          <div>
            <label for="first_nations_name" class="label">First Nations Name</label>
            <input id="first_nations_name" type="text" bind:value={plant.first_nations_name} class="input input-primary w-full" />
          </div>
          <div>
            <label for="scientific_name" class="label">Scientific Name</label>
            <input id="scientific_name" type="text" bind:value={plant.scientific_name} class="input input-primary w-full" />
          </div>
          <div>
            <label for="first_nations_uses" class="label">Uses</label>
            <input id="first_nations_uses" type="text" bind:value={plant.first_nations_uses} class="input input-primary w-full" />
          </div>
          <div>
            <label for="description" class="label">Description</label>
            <textarea id="description" bind:value={plant.description} class="textarea textarea-primary w-full"></textarea>
          </div>
          <div>
            <label for="latitude" class="label">Latitude</label>
            <input id="latitude" type="number" bind:value={plant.latitude} class="input input-primary w-full" />
          </div>
          <div>
            <label for="longitude" class="label">Longitude</label>
            <input id="longitude" type="number" bind:value={plant.longitude} class="input input-primary w-full" />
          </div>
          <div>
            <label for="conservation_status" class="label">Conservation Status</label>
            <div class="form-control">
              <label class="label cursor-pointer">
                <span class="font-medium">Endangered?</span>
                <input id="conservation_status" type="checkbox" bind:checked={isChecked} class="checkbox checkbox-primary" />
              </label>
            </div>
          </div>
          <div>
            <label for="kml_file" class="label">KML File</label>
            <div class="flex items-center">
              <input
                id="keep_existing_kml"
                type="checkbox"
                bind:checked={keepExistingKml}
                class="checkbox checkbox-primary mr-2"
              />
              <label for="keep_existing_kml" class="label mr-4">Keep existing KML file</label>

              {#if keepExistingKml}
                <input
                  type="file"
                  placeholder="You can't touch this"
                  class="file-input file-input-bordered w-full max-w-xs"
                  disabled
                />
              {:else}
                <input
                  id="kml_file_input"
                  type="file"
                  accept=".kml"
                  on:change={handleKmlFileChange}
                  class="file-input file-input-primary"
                />
              {/if}
            </div>
          </div>

          <div>
            <label for="image" class="label">Image (base64)</label>
            <div class="flex items-center">
              <input
                id="keep_existing_image"
                type="checkbox"
                bind:checked={keepExistingImage}
                class="checkbox checkbox-primary mr-2"
              />
              <label for="keep_existing_image" class="label mr-4">Keep existing image</label>

              {#if keepExistingImage}
                <input
                  type="file"
                  placeholder="You can't touch this"
                  class="file-input file-input-bordered w-full max-w-xs"
                  disabled
                />
              {:else}
                <input
                  id="image_file_input"
                  type="file"
                  accept="image/*"
                  on:change={handleImageFileChange}
                  class="file-input file-input-primary"
                />
              {/if}
            </div>
          </div>
        </div>

        <button type="submit" class="btn btn-primary mt-4">Save Changes</button>
      </form>
    {/if}
  {/if}
</main>
