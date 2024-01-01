<script>
  import { createForm } from "felte";
  import { validator } from "@felte/validator-yup";
  import * as yup from "yup";
  import Form from "./formBase/Form.svelte";
  import FormItem from "./formBase/FormItem.svelte";
  import FormButton from "./formBase/FormButton.svelte";
  import { createTodo } from "../services/TodoApi";
  import { selectedTodo } from "../stores/TodoStore";
  import { loggedUser } from "../stores/UserStore";

  const { form, errors } = createForm({
    initialValues: {
      description: "",
      dueDate: new Date().toISOString(),
    },
    extend: validator({
      schema: yup.object().shape({
        description: yup.string().required("Must have a description"),
        dueDate: yup.string().required("Must have a finish date"),
      }),
    }),
    onSubmit: async (values) => {
      let newTodo = { ownerId: $loggedUser.id, ...values };
      let response = await createTodo(newTodo);
      switch (response.status) {
        case 201:
          return await response.json();
        case 404:
          throw await response.json();
        default:
          console.log("Unknown error");
          console.log(response);
          break;
      }
    },
    onSuccess: () => {
      selectedTodo.set(null);
    },
    onError: async (values) => {
      console.log(values);
    },
  });
</script>

<Form {form} class="w-auto">
  <FormItem
    name="description"
    labelText="Description"
    type="text"
    errors={$errors.description}
  />

  <FormItem
    name="dueDate"
    labelText="Due Date"
    type="date"
    errors={$errors.dueDate}
  />

  <FormButton>Save</FormButton>
</Form>
