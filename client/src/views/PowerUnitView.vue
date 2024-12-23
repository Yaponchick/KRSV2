<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';

import Cookies from 'js-cookie';

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})


const powerUnit = ref({});
const powerUnitdAdd = ref({});
const PowerUnitAddToEdit = ref({});
const powerUnitToDelete = ref(null);
const authors = ref([]);
const isAuthenticated = ref(false);
const username = ref('');
const userId = ref(null);
const isLoading = ref(false);

const statistics = ref({
    totalPowerUnit: 0,
    totalPrice: 0,
    averagePrice: 0,
    maxPrice: 0,
    minPrice: 0
});

async function fetchStatistics() {
    try {
        const r = await axios.get("/api/PowerUnit/stats/");
        statistics.value = {
            totalPowerUnit: r.data.count,
            totalPrice: r.data.totalPrice ? r.data.totalPrice.toFixed(2) : 0,
            averagePrice: r.data.avg ? r.data.avg.toFixed(2) : 0,
            maxPrice: r.data.max ? r.data.max : 0,
            minPrice: r.data.min ? r.data.min : 0
        };
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function fetchPowerUnit() {
    const r = await axios.get("/api/PowerUnit/");
    powerUnit.value = r.data;
}

async function onPowerUnitAdd() {
    await axios.post("/api/PowerUnit/", {
        ...powerUnitdAdd.value,
    });
    await fetchPowerUnit();
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
    await fetchPowerUnit();
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

function onRemoveClick(powerUnit) {
    powerUnitToDelete.value = powerUnit;
}

async function confirmDelete() {
    if (powerUnitToDelete.value) {
        await axios.delete(`/api/PowerUnit/${powerUnitToDelete.value.id}/`);
        await fetchPowerUnit();
        await fetchStatistics();
        powerUnitToDelete.value = null;
    }
}

async function onPowerUnitEditClick(powerUnit) {
    PowerUnitAddToEdit.value = { ...powerUnit };
}

async function onUpdatePowerUnit() {
    await axios.put(`/api/PowerUnit/${PowerUnitAddToEdit.value.id}/`, {
        ...PowerUnitAddToEdit.value
    });
    await fetchPowerUnit();
    await fetchStatistics();
}
function selectAuthor(authorId) {
    filters.value.user = authorId;
}
const filters = ref({
    model: '',
    minPrice: '',
    maxPrice: '',
    networkVoltage: '',
    coolingSystem: '',
    power: '',
    user: ''
});

const powerUnitFiltered = computed(() => {
    if (!Array.isArray(powerUnit.value)) return [];
    return powerUnit.value.filter(item => {
        return (
            (!filters.value.model || item.model.includes(filters.value.model)) &&
            (!filters.value.minPrice || parseFloat(item.price) >= parseFloat(filters.value.minPrice)) &&
            (!filters.value.maxPrice || parseFloat(item.price) <= parseFloat(filters.value.maxPrice)) &&
            (!filters.value.networkVoltage || item.networkVoltage.includes(filters.value.networkVoltage)) &&
            (!filters.value.coolingSystem || item.coolingSystem.includes(filters.value.coolingSystem)) &&
            (!filters.value.power || parseFloat(item.power) === parseFloat(filters.value.power)) &&
            (!filters.value.user || item.user === filters.value.user)
        );
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
                        Вы уверены, что хотите удалить этот блок питания?
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
            <div class="modal fade" id="editPowerUnitModal" tabindex="-1" aria-labelledby="exampleModalLabel"
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
                                        <input type="text" class="form-control" v-model="PowerUnitAddToEdit.model" />
                                        <label for="floatingInput">Модель</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="PowerUnitAddToEdit.price" />
                                        <label for="floatingInput">Цена</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control"
                                            v-model="PowerUnitAddToEdit.networkVoltage">
                                        <label for="floatingInput">Напряжение</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control"
                                            v-model="PowerUnitAddToEdit.coolingSystem">
                                        <label for="floatingInput">Охлаждение</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="PowerUnitAddToEdit.power">
                                        <label for="floatingInput">Мощность</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button data-bs-dismiss="modal" type="button" class="btn btn-primary"
                                @click="onUpdatePowerUnit">Сохранить</button>
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
                            <p>Общее количество блоков питания:</p>
                            <p class="stat-value">{{ statistics.totalPowerUnit }} шт.</p>
                        </div>
                        <div class="stat-item">
                            <p>Общая цена блоков питания:</p>
                            <p class="stat-value">{{ statistics.totalPrice }} руб.</p>
                        </div>
                        <div class="stat-item">
                            <p>Средняя цена блоков питания:</p>
                            <p class="stat-value">{{ statistics.averagePrice }} руб.</p>
                        </div>
                        <div class="stat-item">
                            <p>Максимальная цена блока питания:</p>
                            <p class="stat-value">{{ statistics.maxPrice }} руб.</p>
                        </div>
                        <div class="stat-item">
                            <p>Минимальная цена блока питания:</p>
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
            <form @submit.prevent.stop="onPowerUnitAdd">
                <div class="row">
                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="powerUnitdAdd.model" required />
                            <label for="floatingInput">Модель</label>
                        </div>
                    </div>


                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="powerUnitdAdd.price" required />
                            <label for="floatingInput">Цена</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="powerUnitdAdd.networkVoltage" required />
                            <label for="floatingInput">Сетевое напряжение</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="powerUnitdAdd.coolingSystem" required />
                            <label for="floatingInput">Система охлаждения</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="powerUnitdAdd.power" required />
                            <label for="floatingInput">Мощность</label>
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
            <form @submit.prevent>
                <div class="row mb-3">
                    <div class="col-md-2">
                        <input type="text" class="form-control" v-model="filters.model" placeholder="Модель" />
                    </div>
                    <div class="col-md-2">
                        <input type="number" class="form-control" v-model="filters.minPrice" placeholder="Мин. цена" />
                    </div>
                    <div class="col-md-2">
                        <input type="number" class="form-control" v-model="filters.maxPrice" placeholder="Макс. цена" />
                    </div>
                    <div class="col-md-2">
                        <input type="text" class="form-control" v-model="filters.networkVoltage"
                            placeholder="Напряжение" />
                    </div>
                    <div class="col-md-2">
                        <input type="text" class="form-control" v-model="filters.coolingSystem"
                            placeholder="Охлаждение" />
                    </div>
                    <div class="col-md-2">
                        <input type="number" class="form-control" v-model="filters.power" placeholder="Мощность" />
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
                <div v-for="item in powerUnitFiltered" :key="item.id" class="powerUnit-item">
                    <div>{{ item.model }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.networkVoltage }}</div>
                    <div>{{ item.coolingSystem }}</div>
                    <div>{{ item.power }}</div>

                    <button class="btn btn-success" @click="onPowerUnitEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editPowerUnitModal">
                        <i class="bi bi-pencil"></i>
                    </button>
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
.powerUnit-item {
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