<script>
    import { loggedUser } from "#stores/UserStore.js";
    import { goto, afterNavigate } from "$app/navigation";

    afterNavigate(async () => {
        loggedUser.subscribe((v) => {
            if (v === null) {
                goto("/login");
            }
        });
    });
</script>

<div>LOGGED INTO DASHBOARD</div>
