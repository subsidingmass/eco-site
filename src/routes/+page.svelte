<script lang="ts">
  import '../app.css';
  import Navbar from '../components/Navbar.svelte';
  import { goto } from '$app/navigation';
  import { setTheme, getTheme } from '$lib/themeManager';

  // Modal Logic
  let modal: HTMLDialogElement;

  function openModal() {
    modal.showModal();
  }
</script>

<main>
  <Navbar />
  <div class="hero bg-base-200 min-h-screen flex">
    <div class="hero-content text-center flex-1">
      <div class="max-w-md">
        <h1 class="text-3xl font-bold">Hello there,</h1>
        <h1 class="text-5xl font-bold">Welcome to the Immanuel Plant Index</h1>
        <button class="btn btn-primary mt-5" on:click={openModal}>Get Started</button>

        <dialog bind:this={modal} class="modal">
          <div class="modal-box">
            <h3 class="text-lg font-bold mb-5">Where would you like to go?</h3>
            <div class="flex w-full flex-col">
              <button class="btn btn-primary" on:click={() => goto('/getPlants')}>Full Plant Index</button>
              <div class="divider"></div>
              <button class="btn btn-primary" on:click={() => goto('/createPlant')}>Create New Plant</button>
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
    </div>

    <div class="flex-1 flex justify-center items-center">
      <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.21/build/spline-viewer.js"></script>
      <spline-viewer url="https://prod.spline.design/ICNLp77qWff0iRhC/scene.splinecode" class="w-full h-full"></spline-viewer>
    </div>
  </div>
</main>
                               