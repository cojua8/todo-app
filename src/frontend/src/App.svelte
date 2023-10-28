<script>
  import page from "page";

  import Home from "./pages/Home.svelte";
  import Login from "./pages/Login.svelte";
  import Signup from "./pages/Signup.svelte";
  import NavBar from "./components/NavBar.svelte";

  let currentPage = Home;
  page("/", () => (currentPage = Home));
  page("/login", () => (currentPage = Login));
  page("/signup", () => (currentPage = Signup));
  page();

  let year = new Date().getFullYear();
</script>

<main>
  <NavBar />
  <div>
    <div class="mt-20">
      <svelte:component this={currentPage} />
    </div>

    <p class="text-center text-gray-500 text-xs">
      &copy;{year} Joaquin. All rights reserved.
    </p>
  </div>
</main>
