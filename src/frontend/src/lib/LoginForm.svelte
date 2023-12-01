<script>
  import page from "page";
  import { createForm } from "felte";
  import { validator } from "@felte/validator-yup";
  import * as yup from "yup";
  import { loginUser } from "../services/TodoApi";
  import { loggedUser } from "../stores/UserStore";
  import FormItem from "./formBase/FormItem.svelte";
  import Form from "./formBase/Form.svelte";
  import FormButton from "./formBase/FormButton.svelte";

  const { form, errors } = createForm({
    initialValues: {
      username: "theusername3",
      password: "password",
    },
    extend: validator({
      schema: yup.object().shape({
        username: yup.string().required("Username is required"),
        password: yup.string().required("Password is required"),
      }),
    }),
    onSubmit: async (values) => {
      let response = await loginUser(values);
      switch (response.status) {
        case 200:
          loggedUser.set(await response.json());
          return;
        case 400:
          throw await response.json();
        default:
          console.log("Unknown error");
      }
    },
    onSuccess: () => {
      page.redirect("/dashboard");
    },
    onError: async ({ result }) => {
      alert(result);
    },
  });
</script>

<Form {form}>
  <FormItem
    name="username"
    labelText="Username"
    type="text"
    errors={$errors.username}
  />
  <FormItem
    name="password"
    labelText="Password"
    type="password"
    errors={$errors.password}
  />
  <br />
  <FormButton>Login</FormButton>
</Form>
