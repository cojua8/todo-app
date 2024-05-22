<script>
  import { faker } from "@faker-js/faker";
  import { validator } from "@felte/validator-yup";
  import { createForm } from "felte";
  import page from "page";
  import * as yup from "yup";
  import { createUser } from "../services/TodoApi";
  import { loggedUser } from "../stores/UserStores";
  import Form from "./formBase/Form.svelte";
  import FormButton from "./formBase/FormButton.svelte";
  import FormItem from "./formBase/FormItem.svelte";

  const { form, setErrors, errors } = createForm({
    initialValues: {
      email: faker.internet.email(),
      username: faker.internet.userName(),
      password: "1234",
      confirmPassword: "1234",
    },
    extend: validator({
      schema: yup.object().shape({
        email: yup.string().email().required("Email is required"),
        username: yup.string().required("Username is required"),
        password: yup.string().required("Password is required"),
        confirmPassword: yup
          .string()
          .required("Password confirmation is required")
          .equals([yup.ref("password")], "Passwords must match"),
      }),
    }),
    onSubmit: async (values) => {
      let response = await createUser(values);
      switch (response.status) {
        case 201:
          loggedUser.set(await response.json());
          return;
        case 400:
          throw await response.json();
        default:
          console.log("Unknown error");
          break;
      }
    },
    onSuccess: async () => {
      page.redirect("/dashboard");
    },
    onError: async ({ detail }) => {
      switch (detail) {
        case "USERNAME_ALREADY_EXISTS":
          setErrors({ username: "Username already exists" });
          break;
        case "EMAIL_ALREADY_EXISTS":
          setErrors({ email: "Email already exists" });
          break;
        case "PASSWORD_NOT_MATCHING":
          setErrors({ confirmPassword: "Passwords do not match" });
          break;
        default:
          console.log("Unknown error");
          break;
      }
    },
  });
</script>

<Form {form}>
  <FormItem
    name="email"
    labelText="Email"
    type="email"
    errors={$errors.email}
  />
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
  <FormItem
    name="confirmPassword"
    labelText="Confirm Password"
    type="password"
    errors={$errors.confirmPassword}
  />
  <br />
  <FormButton>Signup</FormButton>
</Form>
