<script lang="ts">
  import { onMount, beforeUpdate } from 'svelte';
  import { page } from '$app/stores';
  import Navbar from '../../../components/Navbar.svelte';
  import { goto } from '$app/navigation';

  let plantId: number;
  $: plantId = +$page.params.id;

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
  let plants: Plant[] = [];
  let plantIds: number[] = [];
  let currentIndex: number = 0;

  async function fetchPlantData() {
    try {
      const res = await fetch('http://localhost:5000/api/plants');
      if (res.ok) {
        plants = await res.json();
        plantIds = plants.map(p => p.id);
        currentIndex = plantIds.indexOf(plantId);
        if (currentIndex === -1) {
          error = 'Plant not found';
          plant = null;
        } else {
          plant = plants[currentIndex];
        }
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
  }

  onMount(fetchPlantData);

  $: {
    if (plantId) {
      loading = true;
      fetchPlantData();
    }
  }

  function navigateToUpdatePage() {
    goto(`/editPlant/${plantId}`);
  }

  function goToNextPlant() {
    if (currentIndex < plantIds.length - 1) {
      currentIndex++;
      goto(`/getPlants/${plantIds[currentIndex]}`);
    }
  }

  function goToPreviousPlant() {
    if (currentIndex > 0) {
      currentIndex--;
      goto(`/getPlants/${plantIds[currentIndex]}`);
    }
  }
</script>

<main class="bg-base-200 min-h-screen">
  <Navbar />
  <div class="container mx-auto p-4">
    <button class="btn btn-primary block mb-4" on:click={() => goto('/plants')}>Go Back</button>
    {#if loading}
      <div class="flex justify-center items-center h-screen bg-base-200">
        <span class="loading loading-ring loading-lg"></span>
      </div>
    {:else if error}
      <div class="flex justify-center items-center h-screen bg-base-200 flex-col">
        <h1 class="text-4xl font-bold">Oops. An error has occurred</h1>
        <h2 class="text-2xl">Error: {error}</h2>
      </div>
    {:else if plant}
      <div class="card bg-base-200 shadow-xl">
        {#if plant.image}
          <figure>
            <img src={`data:image/png;base64,${plant.image}`} alt={plant.common_name} />
          </figure>
        {/if}
        <div class="card-body">
          <h2 class="card-title">{plant.common_name}</h2>
          <p><strong>First Nations Name:</strong> {plant.first_nations_name}</p>
          <p><strong>Scientific Name:</strong> {plant.scientific_name}</p>
          <p><strong>Uses:</strong> {plant.first_nations_uses}</p>
          <p><strong>Description:</strong> {plant.description}</p>
          <p><strong>Latitude:</strong> {plant.latitude}</p>
          <p><strong>Longitude:</strong> {plant.longitude}</p>
          <p><strong>Conservation Status:</strong> {plant.conservation_status}</p>
          <button class="btn btn-primary" on:click={navigateToUpdatePage}>Edit</button>
          <div class="flex justify-between mt-4">
            <button class="btn btn-secondary" on:click={goToPreviousPlant} disabled={currentIndex === 0}>Previous</button>
            <button class="btn btn-secondary" on:click={goToNextPlant} disabled={currentIndex === plantIds.length - 1}>Next</button>
          </div>
        </div>
      </div>
    {/if}
  </div>
</main>
