<script>
    import UserRegisterForm from "../components/UserRegisterForm.svelte";

    let year = new Date().getFullYear();
</script>

<UserRegisterForm />

<p class="text-center text-gray-500 text-xs">
    &copy;{year} Joaquin. All rights reserved.
</p>
