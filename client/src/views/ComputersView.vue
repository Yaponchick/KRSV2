<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import QRCode from 'qrcode';
import Cookies from 'js-cookie';
import Papa from 'papaparse';
onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})


const computers = ref({});
const videoCard = ref({});
const motherboard = ref({});
const processor = ref({});
const powerUnit = ref({});
const computersToDelete = ref(null);

const computersToAdd = ref({});
const computersToEdit = ref({});
const qrCodeDataUrl = ref('');
const authors = ref([]);
const isAuthenticated = ref(false);
const username = ref('');
const userId = ref(null);
const isLoading = ref(false);

const statistics = ref({
    totalComputer: 0,
    totalPrice: 0,
    averagePrice: 0,
    maxPrice: 0,
    minPrice: 0
});

async function fetchStatistics() {
    try {
        const r = await axios.get("/api/computers/stats/");
        statistics.value = {
            totalComputer: r.data.count,
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

async function fetchProcessor() {
    const r = await axios.get("/api/Processor/");
    processor.value = r.data;
}

async function fetchVideocards() {
    const r = await axios.get("/api/VideoCard/");
    videoCard.value = r.data;
}

async function fetchMotherboard() {
    const r = await axios.get("/api/Motherboard/");
    motherboard.value = r.data;
}

async function fetchComputers() {
    const r = await axios.get("/api/computers/");
    console.log(r.data)
    computers.value = r.data;
}


async function onComputerAdd() {
    await axios.post("/api/computers/", {
        ...computersToAdd.value,
    });
    await fetchComputers();
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
    await fetchComputers();
    await fetchVideocards();
    await fetchMotherboard();
    await fetchProcessor();
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

function onRemoveClick(computer) {
    computersToDelete.value = computer;
}
async function confirmDelete() {
    if (computersToDelete.value) {
        await axios.delete(`/api/computers/${computersToDelete.value.id}/`);
        await fetchComputers();
        await fetchStatistics();
        computersToDelete.value = null;
    }
}

async function onUpdateComputer() {
    await axios.put(`/api/computers/${computersToEdit.value.id}/`, {
        ...computersToEdit.value
    });
    await fetchComputers();
    await fetchStatistics();
}

function selectAuthor(authorId) {
    filters.value.user = authorId;
}

async function onComputerEditClick(computer) {
    computersToEdit.value = {
        id: computer.id,
        model: computer.model,
        price: computer.price,
        computerV_FK_1: computer.computerV_FK.id,
        computerM_FK_1: computer.computerM_FK.id,
        computerP_FK_1: computer.computerP_FK.id,
        computerPU_FK_1: computer.computerPU_FK.id,
    };
}
const filters = ref({
    model: '',
    minPrice: '',
    maxPrice: '',
    videoCardModel: '',
    motherboardModel: '',
    processorModel: '',
    powerUnitModel: '',
    user: ''
});

const computersFiltered = computed(() => {
    return Array.isArray(computers.value) ? computers.value.filter(item => {
        return (
            (!filters.value.model || item.model.includes(filters.value.model)) &&
            (!filters.value.minPrice || parseFloat(item.price) >= parseFloat(filters.value.minPrice)) &&
            (!filters.value.maxPrice || parseFloat(item.price) <= parseFloat(filters.value.maxPrice)) &&
            (!filters.value.videoCardModel || item.computerV_FK.model.includes(filters.value.videoCardModel)) &&
            (!filters.value.motherboardModel || item.computerM_FK.model.includes(filters.value.motherboardModel)) &&
            (!filters.value.processorModel || item.computerP_FK.model.includes(filters.value.processorModel)) &&
            (!filters.value.powerUnitModel || item.computerPU_FK.model.includes(filters.value.powerUnitModel)) &&
            (!filters.value.user || item.user === filters.value.user)
        );
    }) : [];
});

async function saveToFile() {
    const computersData = computersFiltered.value.map(item => ({
        model: item.model,
        price: item.price,
        videoCard: item.computerV_FK.model,
        motherboard: item.computerM_FK.model,
        processor: item.computerP_FK.model,
        powerUnit: item.computerPU_FK.model
    }));

    const csv = Papa.unparse(computersData);

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', 'computers_data.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

function onQRClick(computer) {
    computersToEdit.value = computer;
    generateQRCode();
}

function generateQRCode() {
    const data = computersToEdit.value;
    if (data && data.model) {
        const baseUrl = `${window.location.origin}/computer-details`;
        const queryParams = new URLSearchParams({
            model: data.model,
            price: data.price,
            videoCard: data.computerV_FK?.model || 'Не указана',
            motherboard: data.computerM_FK?.model || 'Не указана',
            processor: data.computerP_FK?.model || 'Не указан',
            powerUnit: data.computerPU_FK?.model || 'Не указан',
        });

        const qrUrl = `${baseUrl}?${queryParams.toString()}`;

        QRCode.toDataURL(qrUrl, { width: 200 }, (err, url) => {
            if (err) {
                console.error('Ошибка при генерации QR-кода:', err);
            } else {
                qrCodeDataUrl.value = url;
            }
        });
    }
}
const redirectUrl = computed(() => {
    const data = computersToEdit.value;
    if (data && data.model) {
        const baseUrl = `${window.location.origin}/computer-details`;
        return `${baseUrl}?${new URLSearchParams({
            model: data.model,
            price: data.price,
            videoCard: data.computerV_FK?.model || 'Не указана',
            motherboard: data.computerM_FK?.model || 'Не указана',
            processor: data.computerP_FK?.model || 'Не указан',
            powerUnit: data.computerPU_FK?.model || 'Не указан',
        }).toString()}`;
    }
    return '#';
});
</script>

<template>
    <div class="container-fluid">
        <!--Modal QR-->
        <div class="modal fade" id="QR" tabindex="-1" aria-labelledby="QR" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="QRLabel">Данные ПК</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Модель:</strong> {{ computersToEdit.model }}</p>
                        <p><strong>Цена:</strong> {{ computersToEdit.price }}</p>
                        <p><strong>Видеокарта:</strong> {{ computersToEdit.computerV_FK?.model || 'Не указана' }}</p>
                        <p><strong>Материнская плата:</strong> {{ computersToEdit.computerM_FK?.model || 'Не указана' }}
                        </p>
                        <p><strong>Процессор:</strong> {{ computersToEdit.computerP_FK?.model || 'Не указан' }}</p>
                        <p><strong>Блок питания:</strong> {{ computersToEdit.computerPU_FK?.model || 'Не указан' }}</p>

                        <div v-if="qrCodeDataUrl" class="text-center">
                            <img :src="qrCodeDataUrl" alt="QR-код" class="mb-3" />
                        </div>
                    </div>
                    <div class="modal-footer d-flex justify-content-center">
                        <a :href="redirectUrl" class="btn btn-primary w-100">ТЫК</a>
                    </div>
                </div>
            </div>
        </div>

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
                        Вы уверены, что хотите удалить этот компьютер?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-danger" @click="confirmDelete()"
                            data-bs-dismiss="modal">Удалить</button>
                    </div>
                </div>
            </div>
        </div>

        <form>
            <div class="modal fade" id="editComputerModal" tabindex="-1" aria-labelledby="exampleModalLabel"
                aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">Редактировать</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-12 col-md-2">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="computersToEdit.model" />
                                        <label for="floatingInput">Модель</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="computersToEdit.price" />
                                        <label for="floatingInput">Цена</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <select class="form-select" v-model="computersToEdit.computerV_FK_1">
                                            <option value="" disabled>Выберите видеокарту</option>
                                            <option :value="g.id" v-for="g in videoCard">{{ g.model }}</option>
                                        </select>
                                        <label for="floatingInput">Видеокарта</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <select class="form-select" v-model="computersToEdit.computerM_FK_1">
                                            <option value="" disabled>Выберите материнскую плату</option>
                                            <option :value="g.id" v-for="g in motherboard">{{ g.model }}</option>
                                        </select>
                                        <label for="floatingInput">Материнская плата</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <select class="form-select" v-model="computersToEdit.computerP_FK_1">
                                            <option value="" disabled>Выберите процессор</option>
                                            <option :value="g.id" v-for="g in processor">{{ g.model }}</option>
                                        </select>
                                        <label for="floatingInput">Процессор</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <select class="form-select" v-model="computersToEdit.computerPU_FK_1">
                                            <option value="" disabled>Выберите блок питания</option>
                                            <option :value="g.id" v-for="g in powerUnit">{{ g.model }}</option>
                                        </select>
                                        <label for="floatingInput">Блок питания</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button data-bs-dismiss="modal" type="button" class="btn btn-primary"
                                @click="onUpdateComputer">Сохранить</button>
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
                            <p>Общее количество компьютеров:</p>
                            <p class="stat-value">{{ statistics.totalComputer }} шт.</p>
                        </div>
                        <div class="stat-item">
                            <p>Общая цена компьютеров:</p>
                            <p class="stat-value">{{ statistics.totalPrice }} руб.</p>
                        </div>
                        <div class="stat-item">
                            <p>Средняя цена компьютеров:</p>
                            <p class="stat-value">{{ statistics.averagePrice }} руб.</p>
                        </div>
                        <div class="stat-item">
                            <p>Максимальная цена компьютера:</p>
                            <p class="stat-value">{{ statistics.maxPrice }} руб.</p>
                        </div>
                        <div class="stat-item">
                            <p>Минимальная цена компьютера:</p>
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
            <form @submit.prevent.stop="onComputerAdd">
                <div class="row">
                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="computersToAdd.model" required />
                            <label for="floatingInput">Модель</label>
                        </div>
                    </div>


                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="computersToAdd.price" required />
                            <label for="floatingInput">Цена</label>
                        </div>
                    </div>


                    <div class="col-md-2">
                        <div class="form-floating">
                            <select name="" id="" class="form-select" v-model="computersToAdd.computerV_FK_1" required>
                                <option :value="g.id" v-for="g in videoCard">{{ g.model }}</option>
                            </select>
                            <label for="floatingInput">Видеокарта</label>
                        </div>
                    </div>


                    <div class="col-md-2">
                        <div class="form-floating">
                            <select name="" id="" class="form-select" v-model="computersToAdd.computerM_FK_1" required>
                                <option :value="g.id" v-for="g in motherboard">{{ g.model }}</option>
                            </select>
                            <label for="floatingInput">Материнская плата</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <select name="" id="" class="form-select" v-model="computersToAdd.computerP_FK_1" required>
                                <option :value="g.id" v-for="g in processor">{{ g.model }}</option>
                            </select>
                            <label for="floatingInput">Процессор</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <select name="" id="" class="form-select" v-model="computersToAdd.computerPU_FK_1" required>
                                <option :value="g.id" v-for="g in powerUnit">{{ g.model }}</option>
                            </select>
                            <label for="floatingInput">Блок питания</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-primary mt-3 mb-2">Добавить</button>
                    </div>
                    <div class="col-auto">
                        <button type="button" class="btn btn-info mt-3 mb-2" data-bs-toggle="modal"
                            data-bs-target="#statisticsModal">
                            Статистика
                        </button>
                    </div>
                    <div class="col-auto">
                        <button type="button" class="btn btn-info mt-3 mb-2" @click="saveToFile">Сохранить в
                            exel</button>
                    </div>
                </div>
            </form>
            <form @submit.prevent>
                <div class="row mb-3 mt-3">
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
                        <input type="text" class="form-control" v-model="filters.videoCardModel"
                            placeholder="Видеокарта" />
                    </div>
                    <div class="col-md-2">
                        <input type="text" class="form-control" v-model="filters.motherboardModel"
                            placeholder="Материнская плата" />
                    </div>
                    <div class="col-md-2">
                        <input type="text" class="form-control" v-model="filters.processorModel"
                            placeholder="Процессор" />
                    </div>
                    <div class="col-md-2">
                        <input type="text" class="form-control mt-2" v-model="filters.powerUnitModel"
                            placeholder="Блок питания" />
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
                <div v-for="item in computersFiltered " :key="item.id" class="computers-item">

                    <div>{{ item.model }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.computerV_FK.model }}</div>
                    <div>{{ item.computerM_FK.model }}</div>
                    <div>{{ item.computerP_FK.model }}</div>
                    <div>{{ item.computerPU_FK.model }}</div>

                    <button class="btn btn-success" @click="onComputerEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editComputerModal"> <i class="bi bi-pencil"> </i></button>
                    <button class="btn btn-danger" @click="onRemoveClick(item)" data-bs-toggle="modal"
                        data-bs-target="#deleteConfirmationModal">
                        <i class="bi bi-trash"></i>
                    </button>
                    <button class="btn btn-primary" @click="onQRClick(item)" data-bs-toggle="modal"
                        data-bs-target="#QR">
                        <i class="bi bi-qr-code"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.computers-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    box-shadow: 0 0 4px silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 0.25fr 0.5fr 0.5fr 1fr 1fr 1fr 0.14fr 0.14fr auto;
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