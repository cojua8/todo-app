<script>
    import { loggedUser } from "#stores/UserStore.js";
    import { loginUser } from "#services/TodoApi.js";
    import FormItem from "#components/FormItem.svelte";
    import StatusMessage from "#components/StatusMessage.svelte";
    import { goto } from "$app/navigation";

    let form = { username: "Joaco92", password: "1234" };
    let errors = {};
    let loginMessage = "";
    let loginStatus = "";

    function isEmptyOrNull(value) {
        return value != null && value !== "";
    }

    function validateForm() {
        errors = {};

        if (!isEmptyOrNull(form.username)) {
            errors.username = "Username is required";
        }

        if (!isEmptyOrNull(form.password)) {
            errors.password = "Password is required";
        }

        return Object.keys(errors).length === 0;
    }

    async function submit() {
        loginMessage = "";

        if (!validateForm()) {
            return;
        }

        let response = await loginUser(form);

        if (response.status != 200) {
            loginStatus = "ERROR";
            loginMessage = response.response;
            return;
        }

        loggedUser.set(response.response);

        loggedUser.subscribe((v) => {
            if (v !== null) {
                goto("/dashboard");
            }
        });
    }
</script>

<div class="flex justify-center mt-4">
    <div class="w-full max-w-xs">
        <form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            on:submit|preventDefault={submit}
        >
            <FormItem
                name="username"
                labelText="Username"
                placeholder="Username"
                type="text"
                bind:value={form.username}
                bind:message={errors.username}
            />

            <FormItem
                name="password"
                labelText="Password"
                type="password"
                placeholder="***********"
                bind:value={form.password}
                bind:message={errors.password}
            />

            <div class="flex justify-center">
                <div class="flex flex-col items-center">
                    <button
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                    >
                        Login
                    </button>
                    <StatusMessage message={loginMessage} type={loginStatus} />

                    <a
                        href="/signup"
                        class="text-xs hover:underline text-blue-700 mt-1"
                    >
                        Signup
                    </a>
                </div>
            </div>
        </form>
    </div>
</div>
