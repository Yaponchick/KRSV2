<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';

import Cookies from 'js-cookie';

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})
const selectedImageUrl = ref('');
const motherboardToDelete = ref(null);

const motherboard = ref({});
const motherboardAdd = ref({});
const MotherboardAddToEdit = ref({});

const computersPictureRef = ref();
const computersAddImageUrl = ref();
const computersEditImageUrl = ref();
const computersEditPictureRef = ref();

const statistics = ref({
    totalMotherboard: 0,
    totalPrice: 0,
    averagePrice: 0,
    maxPrice: 0,
    minPrice: 0
});

async function fetchStatistics() {
    try {
        const r = await axios.get("/api/Motherboard/stats/");
        statistics.value = {
            totalMotherboard: r.data.count,
            totalPrice: r.data.totalPrice ? r.data.totalPrice.toFixed(2) : 0,
            averagePrice: r.data.avg ? r.data.avg.toFixed(2) : 0,
            maxPrice: r.data.max ? r.data.max : 0,
            minPrice: r.data.min ? r.data.min : 0
        };
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function computersAddPictureChange() {
    computersAddImageUrl.value = URL.createObjectURL(computersPictureRef.value.files[0])

}

async function computersEditPicture() {
    computersEditImageUrl.value = URL.createObjectURL(computersEditPictureRef.value.files[0])
}

function openImageModal(imageUrl) {
    selectedImageUrl.value = imageUrl;
    const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
    imageModal.show();
}

function onRemoveClick(motherboard) {
    motherboardToDelete.value = motherboard;
}
async function confirmDelete() {
    if (motherboardToDelete.value) {
        await axios.delete(`/api/Motherboard/${motherboardToDelete.value.id}/`);
        await fetchMotherboard();
        await fetchStatistics();
        motherboardToDelete.value = null;
    }
}


async function fetchMotherboard() {
    const r = await axios.get("/api/Motherboard/");
    motherboard.value = r.data;
}

async function onMotherboardAdd() {
    const formData = new FormData();

    formData.append('picture', computersPictureRef.value.files[0]);

    formData.set('model', motherboardAdd.value.model)
    formData.set('price', motherboardAdd.value.price)
    formData.set('compatibleKernels', motherboardAdd.value.compatibleKernels)
    formData.set('processorPowerConnector', motherboardAdd.value.processorPowerConnector)
    formData.set('supportedMemory', motherboardAdd.value.supportedMemory)

    await axios.post("/api/Motherboard/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchMotherboard();
    await fetchStatistics();
}

onBeforeMount(async () => {
    await fetchMotherboard();
    await fetchStatistics();
});




async function onMotherboardEditClick(motherboard) {
    MotherboardAddToEdit.value = { ...motherboard };
    computersEditImageUrl.value = motherboard.picture;

    computersEditPictureRef.value.value = null;
}


async function onUpdateMotherboard() {
    const formData = new FormData();
    if (computersEditPictureRef.value.files.length > 0) {
        formData.append('picture', computersEditPictureRef.value.files[0]);
    }
    formData.set('model', MotherboardAddToEdit.value.model);
    formData.set('price', MotherboardAddToEdit.value.price);
    formData.set('compatibleKernels', MotherboardAddToEdit.value.compatibleKernels);
    formData.set('processorPowerConnector', MotherboardAddToEdit.value.processorPowerConnector);
    formData.set('supportedMemory', MotherboardAddToEdit.value.supportedMemory);

    await axios.put(`/api/Motherboard/${MotherboardAddToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchMotherboard();
    await fetchStatistics();
}

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
                        Вы уверены, что хотите удалить эту материнскую плату?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-danger" @click="confirmDelete()"
                            data-bs-dismiss="modal">Удалить</button>
                    </div>
                </div>
            </div>
        </div>

        <!--Modal picture-->
        <div class="modal fade" id="imageModal" tabindex="-1" aria-labelledby="imageModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="imageModalLabel">Изображение</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <img :src="selectedImageUrl" class="img-fluid" alt="Изображение">
                    </div>
                </div>
            </div>
        </div>

        <!--Modal-->
        <form>
            <div class="modal fade" id="editMotherboardModal" tabindex="-1" aria-labelledby="exampleModalLabel"
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
                                        <input type="text" class="form-control" v-model="MotherboardAddToEdit.model" />
                                        <label for="floatingInput">Модель</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="MotherboardAddToEdit.price" />
                                        <label for="floatingInput">Цена</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control"
                                            v-model="MotherboardAddToEdit.compatibleKernels">
                                        <label for="floatingInput">Совместимые ядра</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control"
                                            v-model="MotherboardAddToEdit.processorPowerConnector">
                                        <label for="floatingInput">Разъем питания</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control"
                                            v-model="MotherboardAddToEdit.supportedMemory">
                                        <label for="floatingInput">Память</label>
                                    </div>
                                </div>
                                <div class="col-auto">
                                    <input class="form-control" type="file" ref="computersEditPictureRef"
                                        @change="computersEditPicture" required>

                                </div>
                                <div class="col-auto">
                                    <img :src="computersEditImageUrl || MotherboardAddToEdit.picture"
                                        style="max-height: 60px;" alt="">
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button data-bs-dismiss="modal" type="button" class="btn btn-primary"
                                @click="onUpdateMotherboard">Сохранить</button>
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
                            <p class="stat-value">{{ statistics.totalMotherboard }} шт.</p>
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
            <form @submit.prevent.stop="onMotherboardAdd">
                <div class="row">
                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="motherboardAdd.model" required />
                            <label for="floatingInput">Модель</label>
                        </div>
                    </div>


                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="motherboardAdd.price" required />
                            <label for="floatingInput">Цена</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="motherboardAdd.compatibleKernels"
                                required />
                            <label for="floatingInput">Совместимые ядра</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="motherboardAdd.processorPowerConnector"
                                required />
                            <label for="floatingInput">Разъем питания процессора</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="motherboardAdd.supportedMemory" required />
                            <label for="floatingInput">Поддерживаемая память</label>
                        </div>
                    </div>


                    <div class="col-auto">
                        <button class="btn btn-primary mt-3">Добавить</button>
                    </div>
                    <div class="col-auto mt-3">
                        <input class="form-control" type="file" ref="computersPictureRef"
                            @change="computersAddPictureChange" required>
                    </div>
                    <div class="col-auto">
                        <img :src="computersAddImageUrl" style="max-height: 60px;" alt="">
                    </div>
                </div>
                <div class="col-auto">
                    <button type="button" class="btn btn-info mt-3 mb-2" data-bs-toggle="modal"
                        data-bs-target="#statisticsModal">
                        Статистика
                    </button>
                </div>
            </form>
            <div>
                <div v-for="item in motherboard" class="motherboard-item">
                    <div>{{ item.model }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.compatibleKernels }}</div>
                    <div>{{ item.processorPowerConnector }}</div>
                    <div>{{ item.supportedMemory }}</div>

                    <div v-show="item.picture">
                        <img :src="item.picture" style="max-height: 60px;" @click="openImageModal(item.picture)" alt=""
                            data-bs-toggle="modal" data-bs-target="#imageModal">
                    </div>

                    <button class="btn btn-success" @click="onMotherboardEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editMotherboardModal"> <i class="bi bi-pencil"> </i></button>
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
.motherboard-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    box-shadow: 0 0 4px silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 0.5fr 0.5fr 0.5fr 1fr 1fr 0.14fr 0.2fr auto;
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