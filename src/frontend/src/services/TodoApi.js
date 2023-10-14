const baseURL = "http://localhost:5000";

const fetchFromApi = async (method, endpoint, body) => {
  const raw = await fetch(baseURL + endpoint, {
    method: method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    mode: "cors",
  });
  const response = await raw.text();

  return JSON.parse(response);
};

export const createUser = async (body) => {
  return await fetchFromApi("POST", "/register", body);
};

export const loginUser = async (body) => {
  return await fetchFromApi("POST", "/login", body);
};

export const getUserTodos = async (user_id) => {
  return await fetchFromApi("GET", `/todos?user_id=${user_id}`);
};

export const createTodo = async (body) => {
  return await fetchFromApi("POST", "/todo", body);
};
