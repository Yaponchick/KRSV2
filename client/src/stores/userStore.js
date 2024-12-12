import { onBeforeMount, ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";

const useUserStore = defineStore("UserStore", () => { 
    const isAuthenticated = ref(false); 
    const username = ref(""); 
    const userId = ref(null);
    const authors = ref([]); // Состояние для авторов
    const userStore = useUserStore();
    // Функция для получения данных пользователя
    async function fetchUser() { 
        try {
          const r = await axios.get("/api/User/info/");
          isAuthenticated.value = r.data.is_authenticated; 
          username.value = r.data.username; 
          userId.value = r.data.user_id;
          
          // Сохраняем данные в localStorage
          localStorage.setItem("isAuthenticated", isAuthenticated.value);
          localStorage.setItem("username", username.value);
          localStorage.setItem("userId", userId.value);
        } catch (error) {
          console.error("Ошибка при получении данных пользователя:", error);
          isAuthenticated.value = false;
          username.value = "";
          userId.value = null;
          
          // Очистить localStorage при ошибке
          localStorage.removeItem("isAuthenticated");
          localStorage.removeItem("username");
          localStorage.removeItem("userId");
        }
      }
      

    // Функция для получения списка авторов
    async function fetchAuthors() {
        try {
            const response = await axios.get("/api/User/authors/");
            authors.value = response.data;
        } catch (error) {
            console.error("Ошибка при получении списка авторов:", error);
            authors.value = [];
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
      
          // Очистка localStorage при выходе
          localStorage.removeItem("isAuthenticated");
          localStorage.removeItem("username");
          localStorage.removeItem("userId");
      
          window.location.reload();
        } catch (error) {
          console.error("Ошибка при выходе из аккаунта:", error);
        }
      }
      

    // Загружаем данные пользователя и авторов при монтировании
    onBeforeMount(() => {
        // Проверяем, есть ли данные в localStorage
        const storedIsAuthenticated = localStorage.getItem("isAuthenticated");
        const storedUsername = localStorage.getItem("username");
        const storedUserId = localStorage.getItem("userId");
      
        if (storedIsAuthenticated && storedUsername && storedUserId) {
          isAuthenticated.value = storedIsAuthenticated === "true";  // Преобразуем строку в boolean
          username.value = storedUsername;
          userId.value = storedUserId;
        }
        
        // Загружаем авторов, если пользователь авторизован
        if (isAuthenticated.value && username.value === 'admin') {
          fetchAuthors();
        }
      });
      

    return { 
        isAuthenticated, 
        username, 
        userId,
        authors, // Добавляем список авторов в return
        fetchUser,
        fetchAuthors, // Возвращаем функцию получения авторов
        login,
        logout 
    };
});

export default useUserStore;
