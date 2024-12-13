<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';

import Cookies from 'js-cookie';

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})


const processor = ref({});
const ProcessordAdd = ref({});
const ProcessorAddToEdit = ref({});
const processorToDelete = ref(null);
const authors = ref([]);
const isAuthenticated = ref(false);
const username = ref('');
const userId = ref(null);
const isLoading = ref(false);

const statistics = ref({
    totalProcessor: 0,
    totalPrice: 0,
    averagePrice: 0,
    maxPrice: 0,
    minPrice: 0
});

async function fetchStatistics() {
    try {
        const r = await axios.get("/api/Processor/stats/");
        statistics.value = {
            totalProcessor: r.data.count,
            totalPrice: r.data.totalPrice ? r.data.totalPrice.toFixed(2) : 0,
            averagePrice: r.data.avg ? r.data.avg.toFixed(2) : 0,
            maxPrice: r.data.max ? r.data.max : 0,
            minPrice: r.data.min ? r.data.min : 0
        };
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function fetchProcessor() {
    const r = await axios.get("/api/Processor/");
    processor.value = r.data;
}

async function onProcessorAdd() {
    await axios.post("/api/Processor/", {
        ...ProcessordAdd.value,
    });
    await fetchProcessor();
    await fetchStatistics();
}

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
    } finally {
        isLoading.value = false;
    }
}

async function fetchAuthors() {
    try {
        const response = await axios.get("/api/User/authors/");
        console.log("Список авторов:", response.data);
        authors.value = response.data;

        localStorage.setItem("authors", JSON.stringify(response.data));
    } catch (error) {
        console.error("Ошибка при получении списка авторов:", error);
        authors.value = [];
        localStorage.removeItem("authors");
    }
}

onBeforeMount(async () => {
    await fetchProcessor();
    await fetchStatistics();
    const storedAuthors = localStorage.getItem("authors");
    if (storedAuthors) {
        authors.value = JSON.parse(storedAuthors);
    }

    const storedIsAuthenticated = localStorage.getItem("isAuthenticated");
    const storedUsername = localStorage.getItem("username");
    const storedUserId = localStorage.getItem("userId");

    if (storedIsAuthenticated && storedUsername && storedUserId) {
        isAuthenticated.value = storedIsAuthenticated === "true";
        username.value = storedUsername;
        userId.value = storedUserId;
    }

    if (isAuthenticated.value && username.value === 'admin') {
        fetchAuthors();
    }

    fetchUser();
});

function onRemoveClick(processor) {
    processorToDelete.value = processor;
}
async function confirmDelete() {
    if (processorToDelete.value) {
        await axios.delete(`/api/Processor/${processorToDelete.value.id}/`);
        await fetchProcessor();
        await fetchStatistics();
        processorToDelete.value = null;
    }
}

async function onProcessorEditClick(processor) {
    ProcessorAddToEdit.value = { ...processor };
}

async function onUpdateProcessor() {
    await axios.put(`/api/Processor/${ProcessorAddToEdit.value.id}/`, {
        ...ProcessorAddToEdit.value
    });
    await fetchProcessor();
    await fetchStatistics();
}

function selectAuthor(authorId) {
    filters.value.user = authorId;
}

const filters = ref({
    model: '',
    socket: '',
    chipset: '',
    frequency: null,
    priceMin: null,
    priceMax: null,
    user: ''
});

// Функция для фильтрации процессоров
const filteredProcessors = computed(() => {
    if (!Array.isArray(processor.value)) return [];
    
    return processor.value.filter(item => {
        const matchModel = filters.value.model ? item.model.includes(filters.value.model) : true;
        const matchSocket = filters.value.socket ? item.socket.includes(filters.value.socket) : true;
        const matchChipset = filters.value.chipset ? item.chipset.includes(filters.value.chipset) : true;
        const matchFrequency = filters.value.frequency
            ? Number(item.frequency) === Number(filters.value.frequency)
            : true;
        const priceMin = filters.value.priceMin ? Number(filters.value.priceMin) : null;
        const priceMax = filters.value.priceMax ? Number(filters.value.priceMax) : null;
        const matchPriceMin = priceMin !== null ? item.price >= priceMin : true;
        const matchPriceMax = priceMax !== null ? item.price <= priceMax : true;
        const matchUser = !filters.value.user || item.user === filters.value.user;

        return matchModel && matchSocket && matchChipset && matchFrequency && matchPriceMin && matchPriceMax && matchUser;
    });
});


</script>



<template>
    <div class="container-fluid">

        <!--Modal delete-->
        <div class="modal fade" id="deleteConfirmationModal" tabindex="-1" aria-labelledby="deleteModalLabel"
            aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="deleteModalLabel">Подтверждение удаления</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        Вы уверены, что хотите удалить этот процессор?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-danger" @click="confirmDelete()"
                            data-bs-dismiss="modal">Удалить</button>
                    </div>
                </div>
            </div>
        </div>

        <!--Modal-->
        <form>
            <div class="modal fade" id="editProcessorModal" tabindex="-1" aria-labelledby="exampleModalLabel"
                aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">Редактировать</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="ProcessorAddToEdit.model" />
                                        <label for="floatingInput">Модель</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="ProcessorAddToEdit.price" />
                                        <label for="floatingInput">Цена</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="ProcessorAddToEdit.socket">
                                        <label for="floatingInput">Сокет</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="ProcessorAddToEdit.chipset">
                                        <label for="floatingInput">Чипсет</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="ProcessorAddToEdit.frequency">
                                        <label for="floatingInput">Частота</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button data-bs-dismiss="modal" type="button" class="btn btn-primary"
                                @click="onUpdateProcessor">Сохранить</button>
                        </div>
                    </div>
                </div>
            </div>
        </form>


        <!--Modal static-->
        <div class="modal fade" id="statisticsModal" tabindex="-1" aria-labelledby="statisticsModalLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="statisticsModalLabel">Статистика</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="stat-item">
                            <p>Общее количество процессоров:</p>
                            <p class="stat-value">{{ statistics.totalProcessor }} шт.</p>
                        </div>
                        <div class="stat-item">
                            <p>Общая цена процессоров:</p>
                            <p class="stat-value">{{ statistics.totalPrice }} руб.</p>
                        </div>
                        <div class="stat-item">
                            <p>Средняя цена процессоров:</p>
                            <p class="stat-value">{{ statistics.averagePrice }} руб.</p>
                        </div>
                        <div class="stat-item">
                            <p>Максимальная цена процессора:</p>
                            <p class="stat-value">{{ statistics.maxPrice }} руб.</p>
                        </div>
                        <div class="stat-item">
                            <p>Минимальная цена процессора:</p>
                            <p class="stat-value">{{ statistics.minPrice }} руб.</p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    </div>
                </div>
            </div>
        </div>





        <div class="p-2">
            <form @submit.prevent.stop="onProcessorAdd">
                <div class="row">
                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="ProcessordAdd.model" required />
                            <label for="floatingInput">Модель</label>
                        </div>
                    </div>


                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="ProcessordAdd.price" required />
                            <label for="floatingInput">Цена</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="ProcessordAdd.socket" required />
                            <label for="floatingInput">Сокет</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="ProcessordAdd.chipset" required />
                            <label for="floatingInput">Чипсет</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="ProcessordAdd.frequency" required />
                            <label for="floatingInput">Частота</label>
                        </div>
                    </div>


                    <div class="col-auto">
                        <button class="btn btn-primary mt-3">Добавить</button>
                    </div>
                </div>
                <div class="col-auto">
                    <button type="button" class="btn btn-info mt-3 mb-2" data-bs-toggle="modal"
                        data-bs-target="#statisticsModal">
                        Статистика
                    </button>
                </div>
            </form>
            <form class="filter-form">
                <div class="row">
                    <div class="col-md-2">
                        <input type="text" v-model="filters.model" class="form-control" placeholder="Модель" />
                    </div>
                    <div class="col-md-2">
                        <input type="text" v-model="filters.socket" class="form-control" placeholder="Сокет" />
                    </div>
                    <div class="col-md-2">
                        <input type="text" v-model="filters.chipset" class="form-control" placeholder="Чипсет" />
                    </div>
                    <div class="col-md-2">
                        <input type="number" v-model="filters.frequency" class="form-control" placeholder="Частота" />
                    </div>
                    <div class="col-md-2">
                        <input type="number" v-model="filters.priceMin" class="form-control" placeholder="Мин. цена" />
                    </div>
                    <div class="col-md-2">
                        <input type="number" v-model="filters.priceMax" class="form-control" placeholder="Макс. цена" />
                    </div>
                </div>
            </form>
            <div class="col-md-2">
                <ul class="nav">
                    <li v-if="isAuthenticated && username === 'admin'" class="nav-item dropdown"
                        style="list-style-type: none;">
                        <a class="nav-link dropdown-toggle" href="#" id="authorsDropdown" role="button"
                            data-bs-toggle="dropdown" aria-expanded="false" style="font-weight: bold; color: #ff9100;">
                            <i class="bi bi-person-circle"></i> Пользователи
                        </a>
                        <ul class="dropdown-menu shadow-lg p-3 rounded" aria-labelledby="authorsDropdown"
                            style="min-width: 200px; list-style-type: none;">
                            <li v-if="authors.length === 0" class="dropdown-item text-muted">Нет доступных авторов</li>
                            <li>
                                <a class="dropdown-item" href="#" @click.prevent="selectAuthor(null)">
                                    <i class="bi bi-person-lines-fill"></i> Все пользователи
                                </a>
                            </li>
                            <li v-for="author in authors" :key="author.id">
                                <a class="dropdown-item" href="#" @click.prevent="selectAuthor(author.id)">
                                    <i class="bi bi-person"></i> {{ author.username }}
                                </a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div>
                <div v-for="item in filteredProcessors" :key="item.id" class="processor-item">
                    <div>{{ item.model }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.socket }}</div>
                    <div>{{ item.chipset }}</div>
                    <div>{{ item.frequency }}</div>
                    <button class="btn btn-success" @click="onProcessorEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editProcessorModal"> <i class="bi bi-pencil"> </i></button>
                    <button class="btn btn-danger" @click="onRemoveClick(item)" data-bs-toggle="modal"
                        data-bs-target="#deleteConfirmationModal">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>



<style lang="scss" scoped>
.processor-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    box-shadow: 0 0 4px silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 0.5fr 0.5fr 0.5fr 1fr 1fr 0.14fr auto;
    gap: 8px;
    text-align: center;
    align-items: center;
}

.stat-card {
    margin-top: 20px;
    padding: 1.5rem;
    background-color: #ffffffe5;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgb(255, 140, 0);
    margin-bottom: 1rem;
    color: #000000;
}



.stat-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #ff9100;
}

.stat-item:last-child {
    border-bottom: none;
}

.stat-item p {
    margin: 0;
    font-size: 1.1rem;
}

.stat-value {
    font-size: 1.1rem;
    color: #000000;
}
</style>