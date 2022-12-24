<script>
    import { getUserTodos, createTodo } from "#services/TodoApi.js";
    import { loggedUser } from "#stores/UserStore.js";
    import { goto, afterNavigate } from "$app/navigation";
    import FormItem from "#components/FormItem.svelte";
    import StatusMessage from "#components/StatusMessage.svelte";

    let todos = [];

    let userId = "";
    let description = "";
    let dueDate = new Date().getDate().toString();
    $: form = {
        description: description,
        due_date: dueDate,
        owner_id: userId,
    };
    let createTodoMessage = "";
    let creationStatus = "";

    afterNavigate(async () => {
        loggedUser.subscribe(async (v) => {
            if (v === null) {
                goto("/login");
            }
            userId = v.id;

            todos = (await getUserTodos(userId)).response;
        });
    });

    async function createTodoItem() {
        createTodoMessage = "";
        let response = await createTodo(form);
        if (response.status != 200) {
            creationStatus = "ERROR";
            createTodoMessage = response.response;
            return;
        }
        creationStatus = "SUCCESS";
        createTodoMessage = "TODO created correctly";

        todos = (await getUserTodos(userId)).response;
    }
</script>

<h1>New Todo</h1>

<div class="flex justify-center mt-4">
    <div class="w-full max-w-xs">
        <form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            on:submit|preventDefault={createTodoItem}
        >
            <FormItem
                name="description"
                labelText="Description"
                placeholder="Description"
                type="text"
                bind:value={description}
            />

            <FormItem
                name=""
                labelText="Due Date"
                type="date"
                bind:value={dueDate}
            />

            <div class="flex justify-center">
                <div class="flex flex-col items-center">
                    <button
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                    >
                        Create
                    </button>
                    <StatusMessage
                        message={createTodoMessage}
                        type={creationStatus}
                    />
                </div>
            </div>
        </form>
    </div>
</div>

<h1>TODOS</h1>
<ul>
    {#each todos as todo, i}
        <li>{i} {JSON.stringify(todo)}</li>
    {/each}
</ul>
