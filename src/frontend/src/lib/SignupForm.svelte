<script>
  import page from "page";
  import { createForm } from "felte";
  import { validator } from "@felte/validator-yup";
  import * as yup from "yup";
  import { createUser } from "../services/TodoApi";
  import { faker } from "@faker-js/faker";
  import { loggedUser } from "../stores/UserStore";

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
    onError: async ({ result, user }) => {
      console.log(result, user);
      switch (result) {
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

<form use:form>
  <label for="email">email</label>
  <input name="email" type="email" />
  {#if $errors.email}
    <p>{$errors.email}</p>
  {/if}

  <label for="username">username</label>
  <input name="username" />
  {#if $errors.username}
    <p>{$errors.username}</p>
  {/if}

  <label for="password">password</label>
  <input name="password" type="password" />
  {#if $errors.password}
    <p>{$errors.password}</p>
  {/if}

  <label for="confirmPassword">confirm password</label>
  <input name="confirmPassword" type="password" />
  {#if $errors.confirmPassword}
    <p>{$errors.confirmPassword}</p>
  {/if}

  <button type="submit">Submit</button>
</form>
