import API from "./API";

export const getUsers = async () => {
    try {
        const response = await API.get("/users");
        return response;
    } catch (error) {
        console.error(error);
    }
};

export const newUser = async (registration_data) => {
    try {
        const response = await API.post("/register", registration_data);
        return response;
    } catch (error) {
        console.error(error);
    }
}