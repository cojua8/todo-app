<script>
  import { validator } from "@felte/validator-yup";
  import { createForm } from "felte";
  import * as yup from "yup";
  import { updateTodoItem } from "../services/TodoApi";
  import Form from "./formBase/Form.svelte";
  import FormButton from "./formBase/FormButton.svelte";
  import FormItem from "./formBase/FormItem.svelte";

  export let handleSubmit;
  export let todo;

  const { form, errors } = createForm({
    initialValues: {
      description: todo.description,
      dueDate: todo.dueDate,
    },
    extend: validator({
      schema: yup.object().shape({
        description: yup.string().required("Must have a description"),
        dueDate: yup.string().required("Must have a finish date"),
      }),
    }),
    onSubmit: async (values) => {
      let updatedTodo = { ...todo, ...values };
      let response = await updateTodoItem(updatedTodo);
      switch (response.status) {
        case 200:
          return await response.json();
        case 404:
          throw await response.json();
        default:
          throw response;
      }
    },
    onSuccess: () => {
      handleSubmit();
    },
    onError: async (values) => {
      alert(JSON.stringify(values));
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
