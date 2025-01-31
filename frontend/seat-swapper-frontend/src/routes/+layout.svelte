<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';  // Import the Navbar component
  import { onMount } from 'svelte';  // Import onMount from Svelte
  import '../app.css';  // Import the global styles
  
  let { children } = $props();  // This will render the content of the pages

  let isPageActive = true;

  // Handle switching the favicon based on visibility
  function updateFavicon() {
    const favicon = document.querySelector("link[rel='icon']") as HTMLLinkElement;
    const newIcon = isPageActive ? "/cool.ico" : "/smirk.ico";
    if (favicon) {
        favicon.href = newIcon;
    }
  }

  // Listen to visibility change events
  const handleVisibilityChange = () => {
    isPageActive = !document.hidden;
    updateFavicon();
  };

  // Set up event listener when the component is mounted
  onMount(() => {
    updateFavicon(); // Set initial favicon
    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  });
</script>



<main 
  class="h-svh bg-stacked-waves bg-cover bg-no-repeat">
  <Navbar />  <!-- Add the Navbar at the top -->
  {@render children()}  <!-- This renders the content of each page -->
</main>

<style>


</style>