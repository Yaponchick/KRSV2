import { onBeforeMount, ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";

const useUserStore = defineStore("UserStore", () => { 
    const isAuthenticated = ref(false); 
    const username = ref(""); 
    const userId = ref(null);

    async function fetchUser() { 
        try {
            const r = await axios.get("/api/User/info/");
            isAuthenticated.value = r.data.is_authenticated; 
            username.value = r.data.username; 
            userId.value = r.data.user_id; 
        } catch (error) {
            console.error("Ошибка при получении данных пользователя:", error);
            isAuthenticated.value = false;
            username.value = "";
            userId.value = null;
        }
    }

    // Функция авторизации
    async function login(credentials) {
        try {
            const response = await axios.post("/api/login/", credentials, {
                headers: {
                    "Content-Type": "application/json"
                }
            });
            isAuthenticated.value = true;
            username.value = response.data.username;
            userId.value = response.data.user_id;
            window.location.reload();
        } catch (error) {
            console.error("Ошибка авторизации:", error);
            throw new Error("Не удалось авторизоваться. Проверьте имя пользователя и пароль.");
        }
    }
    

    // Функция выхода из аккаунта
    async function logout() {
        try {
            await axios.post("/api/logout/"); 
            isAuthenticated.value = false;
            username.value = "";
            userId.value = null;
            window.location.reload();
        } catch (error) {
            console.error("Ошибка при выходе из аккаунта:", error);
        }
    }

    onBeforeMount(() => { 
        fetchUser(); 
    });

    return { 
        isAuthenticated, 
        username, 
        userId,
        fetchUser,
        login,
        logout 
    };
});

export default useUserStore;
