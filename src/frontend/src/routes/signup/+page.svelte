<script>
    import FormItem from "#components/FormItem.svelte";
    import StatusMessage from "#components/StatusMessage.svelte";
    import { createUser } from "#services/TodoApi";

    let form = {};
    let errors = {};
    let registerMessage = "";
    let registerStatus = "";

    function isEmptyOrNull(value) {
        return value != null && value !== "";
    }

    function validateForm() {
        errors = {};

        if (!isEmptyOrNull(form.username)) {
            errors.username = "Username is required";
        }

        if (!isEmptyOrNull(form.email)) {
            errors.email = "Email is required";
        }

        if (!isEmptyOrNull(form.password)) {
            errors.password = "Password is required";
        }

        if (!isEmptyOrNull(form.confirm_password)) {
            errors.confirm_password = "Password confirmation is required";
        }

        if (
            form.password != form.confirm_password &&
            !errors.confirm_password
        ) {
            errors.confirm_password = "Passwords do not match";
        }

        return Object.keys(errors).length === 0;
    }

    async function submit() {
        registerMessage = "";

        if (!validateForm()) {
            return;
        }

        let response = await createUser(form);

        if (response.status != 200) {
            registerStatus = "ERROR";
            console.log(response.response);
            registerMessage = "Registration failed";
            return;
        }

        switch (response.response) {
            case "SUCCESS":
                registerStatus = "SUCCESS";
                registerMessage = "Registration successful";
                break;
            case "PASSWORD_NOT_MATCHING":
                errors.confirm_password = "Passwords do not match";
                break;
            case "USERNAME_ALREADY_EXISTS":
                errors.username = "Username already exists";
                break;
            case "EMAIL_ALREADY_EXISTS":
                errors.email = "Email already exists";
                break;
        }
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
                name="email"
                labelText="Email"
                type="email"
                placeholder="Email"
                bind:value={form.email}
                bind:message={errors.email}
            />
            <FormItem
                name="password"
                labelText="Password"
                type="password"
                placeholder="***********"
                bind:value={form.password}
                bind:message={errors.password}
            />
            <FormItem
                name="confirm_password"
                labelText="Confirm password"
                type="password"
                placeholder="***********"
                bind:value={form.confirm_password}
                bind:message={errors.confirm_password}
            />

            <div class="flex justify-center">
                <div class="flex flex-col items-center">
                    <button
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                    >
                        Sign Up
                    </button>
                    <StatusMessage
                        message={registerMessage}
                        type={registerStatus}
                    />
                </div>
            </div>
        </form>
    </div>
</div>
