<script lang="ts">
    import { onMount } from 'svelte';
    import { applyTheme } from '$lib/themeManager';
    import '../app.css'
    onMount(() => {
        applyTheme();
    })
</script>

<slot />