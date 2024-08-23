<script lang="ts">
    import '../../app.css';
    import Navbar from '../../components/Navbar.svelte';

    let common_name = '';
    let first_nations_name = '';
    let scientific_name = '';
    let first_nations_uses = '';
    let description = '';
    let latitude = '';
    let longitude = '';
    let conservation_status = 'Normal';
    let isChecked: boolean = false;
    $: conservation_status = isChecked ? 'Endangered' : 'Normal';
    let kml_file: File | null = null;
    let image: File | null = null;

    let modal: HTMLDialogElement;

    function openModal() {
        if (modal) {
            modal.showModal();
        }
    }

    const submitForm = async () => {
        const formData = new FormData();
        formData.append('common_name', common_name);
        formData.append('first_nations_name', first_nations_name);
        formData.append('scientific_name', scientific_name);
        formData.append('first_nations_uses', first_nations_uses);
        formData.append('description', description);
        formData.append('latitude', latitude);
        formData.append('longitude', longitude);
        formData.append('conservation_status', conservation_status);

        if (kml_file) formData.append('kml_file', kml_file);
        if (image) formData.append('image', image);

        try {
            const response = await fetch('http://127.0.0.1:5000/api/plants', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            // Check if the response content type is JSON
            const contentType = response.headers.get('Content-Type');
            if (contentType && contentType.includes('application/json')) {
                const result = await response.json();
                console.log(result);
            } else {
                const text = await response.text(); // Read as text if not JSON
                console.log('Response is not JSON:', text);
            }

            modal.close();
        } catch (error) {
            console.error('Error:', error);
        }
    };

    function handleFileInput(event: Event, type: 'kml' | 'image') {
        const input = event.target as HTMLInputElement;
        if (input?.files?.length) {
            if (type === 'kml') {
                kml_file = input.files[0];
            } else if (type === 'image') {
                image = input.files[0];
            }
        }
    }
</script>

<main>
    <Navbar />
    <div class="hero bg-base-200 min-h-screen">
        <div class="hero-content flex-col lg:flex-row-reverse">
            <img
                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvE2_vg9_KXDrT4r5d96yjW2LSOmF5OXyvDQ&s"
                class="max-w-sm rounded-lg shadow-2xl" alt=""/>
            <div>
                <h1 class="text-5xl font-bold">Welcome to the image creation page</h1>
                <p class="py-3">
                    Here you can add a new 🌱plant🌱 to the database.
                </p>
                <button class="btn btn-primary" on:click={openModal}>Create New Plant</button>
            </div>
        </div>
    </div>

    <dialog id="my_modal_2" class="modal" bind:this={modal}>
        <div class="modal-box">
            <h3 class="text-lg font-bold">Fill out the form below</h3>
            <input type="text" placeholder="Common Name" bind:value={common_name} class="input input-bordered w-full max-w-xs my-2" />
            <input type="text" placeholder="First Nations Name" bind:value={first_nations_name} class="input input-bordered w-full max-w-xs my-2" />
            <input type="text" placeholder="Scientific Name" bind:value={scientific_name} class="input input-bordered w-full max-w-xs my-2" />
            <input type="text" placeholder="First Nations Uses" bind:value={first_nations_uses} class="input input-bordered w-full max-w-xs my-2" />
            <input type="text" placeholder="Description" bind:value={description} class="input input-bordered w-full max-w-xs my-2" />
            <input type="text" placeholder="Latitude" bind:value={latitude} class="input input-bordered w-full max-w-xs my-2" />
            <input type="text" placeholder="Longitude" bind:value={longitude} class="input input-bordered w-full max-w-xs my-2" />
            <div class="form-control">
                <label class="label cursor-pointer">
                    <span class="font-medium">Endangered?</span>
                    <input type="checkbox" bind:checked={isChecked} class="checkbox" />
                </label>
            </div>
            <input type="file" accept=".kml" on:change={(e) => handleFileInput(e, 'kml')} class="file-input file-input-bordered w-full max-w-xs my-2" />
            <input type="file" accept="image/*" on:change={(e) => handleFileInput(e, 'image')} class="file-input file-input-bordered w-full max-w-xs my-2" />
            <button class="btn btn-primary mt-4" on:click={submitForm}>Submit</button>
        </div>
        <form method="dialog" class="modal-backdrop">
            <button>Close</button>
        </form>
    </dialog>
</main>
