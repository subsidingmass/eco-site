<script lang="ts">
import Navbar from "../../components/Navbar.svelte";
</script>

<main>
    <Navbar />
    <div class="hero bg-base-200 min-h-screen">
        <div class="hero-content flex-col lg:flex-row">
            <div>
                <h1 class="text-5xl font-bold">Welcome to the about page</h1>
                <p class="py-6">
                    Here you can find information about the website and how it works
                </p>
            </div>
        </div>
    </div>
    <div class="bg-base-200 py-12">
        <div class="container mx-auto px-4">
            <div class="text-center mb-8">
                <h2 class="text-3xl font-bold">Frequently Asked Questions</h2>
            </div>
            <div class="accordion">
                <div class="collapse collapse-plus bg-base-100 mb-4">
                    <input type="radio" name="accordion" id="accordion1" />
                    <label for="accordion1" class="collapse-title text-xl font-medium cursor-pointer">Why was this site made?</label>
                    <div class="collapse-content">
                        <p>This website was developed to track records of the plants in the Immanuel College's forest. This can help sustain the forest and be used as a tool to teach about the environment.</p>
                    </div>
                </div>
                <div class="collapse collapse-plus bg-base-100 mb-4">
                    <input type="radio" name="accordion" id="accordion2" />
                    <label for="accordion2" class="collapse-title text-xl font-medium cursor-pointer">How long did it take to make?</label>
                    <div class="collapse-content">
                        <p>Using existing frameworks, the site was pretty straightforward to make. By using TailwindCSS utility classes and DaisyUI component library, it was easy to piece together.</p>
                    </div>
                </div>
                <div class="collapse collapse-plus bg-base-100 mb-4">
                    <input type="radio" name="accordion" id="accordion3" />
                    <label for="accordion3" class="collapse-title text-xl font-medium cursor-pointer">Who made it?</label>
                    <div class="collapse-content">
                        <p>I made the site alone, and that's about it.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="bg-base-100 py-12">
        <div class="container mx-auto px-4">
            <h2 class="text-2xl font-bold mb-6 text-center">How to Use the Site</h2>
            <ul class="steps steps-vertical max-w-lg mx-auto">
                <li class="step step-primary">Navigate to the creation page</li>
                <li class="step step-primary">Click "Create"</li>
                <li class="step step-primary">Fill in the form</li>
                <li class="step step-primary">Submit the form and you're done</li>
            </ul>
        </div>
    </div>
</main>
