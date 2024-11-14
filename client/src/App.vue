<script setup>
import { ref } from 'vue';
import useUserStore from './stores/userStore'; // Подключаем userStore
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const { username } = storeToRefs(userStore);

const showModal = ref(false); // Контролирует отображение модального окна
const loginUsername = ref('');
const loginPassword = ref('');

// Открытие и закрытие модального окна
function openModal() {
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
}

// Отправка данных для авторизации
async function submitLogin() {
  try {
    await userStore.login({ username: loginUsername.value, password: loginPassword.value });
    closeModal(); // Закрываем модальное окно после успешной авторизации
  } catch (error) {
    console.error('Ошибка авторизации:', error);
    alert('Не удалось авторизоваться. Проверьте имя пользователя и пароль.');
  }
}
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Сборщик</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Компьютеры</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/VideoCardView">Видеокарты</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/MotherboardView">Материнские платы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/ProcessorView">Процессоры</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/PowerUnitView">Блоки питания</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-item dropdown-toggle link" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                {{ username }}
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/admin">Админка</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="openModal">Авторизация</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="userStore.logout()">Выйти</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  
  <!-- Модальное окно для авторизации -->
  <div class="modal fade" :class="{ show: showModal }" tabindex="-1" v-if="showModal" style="display: block;" role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Авторизация</h5>
          <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitLogin">
            <div class="mb-3">
              <label for="username" class="form-label">Имя пользователя</label>
              <input type="text" class="form-control" id="username" v-model="loginUsername" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Пароль</label>
              <input type="password" class="form-control" id="password" v-model="loginPassword" required>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">Закрыть</button>
          <button type="button" class="btn btn-primary" @click="submitLogin">Войти</button>
        </div>
      </div>
    </div>
  </div>

  <div>
    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.modal.show {
  display: block;
  opacity: 1;
}
</style>
