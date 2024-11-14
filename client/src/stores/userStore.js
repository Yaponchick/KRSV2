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
        logout 
    };
});

export default useUserStore;
