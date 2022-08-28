<script>
    import NavBar from "../components/NavBar.svelte";

    import "../app.css";

    let year = new Date().getFullYear();
</script>

<NavBar />
<div>
    <div class="mt-20">
        <slot />
    </div>

    <p class="text-center text-gray-500 text-xs">
        &copy;{year} Joaquin. All rights reserved.
    </p>
</div>
