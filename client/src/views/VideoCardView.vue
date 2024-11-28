<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';

import Cookies from 'js-cookie';

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const selectedImageUrl = ref('');
const videoCardToDelete = ref(null);

const videoCard = ref({});
const videoCardAdd = ref({});
const VideoCardToEdit = ref({});

const computersPictureRef = ref();
const computersAddImageUrl = ref();
const computersEditImageUrl = ref();
const computersEditPictureRef = ref();

const statistics = ref({
    totalVideoCards: 0,
    totalPrice: 0,
    averagePrice: 0,
    maxPrice: 0,
    minPrice: 0
});

async function fetchStatistics() {
    try {
        const r = await axios.get("/api/VideoCard/stats/");
        statistics.value = {
            totalVideoCards: r.data.count,
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

async function fetchVideocards() {
    const r = await axios.get("/api/VideoCard/");
    videoCard.value = r.data;
    await fetchStatistics();
}

async function onVideoCardAdd() {
    const formData = new FormData();

    formData.append('picture', computersPictureRef.value.files[0]);

    formData.set('model', videoCardAdd.value.model)
    formData.set('price', videoCardAdd.value.price)
    formData.set('numberFans', videoCardAdd.value.numberFans)
    formData.set('turboFrequency', videoCardAdd.value.turboFrequency)
    formData.set('memory_size', videoCardAdd.value.memory_size)

    await axios.post("/api/VideoCard/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchVideocards();
    await fetchStatistics();
}

onBeforeMount(async () => {
    await fetchVideocards();
    await fetchStatistics();

});
function onRemoveClick(videoCard) {
    videoCardToDelete.value = videoCard;
}
async function confirmDelete() {
    if (videoCardToDelete.value) {
        await axios.delete(`/api/VideoCard/${videoCardToDelete.value.id}/`);
        await fetchVideocards();
        await fetchStatistics();
        videoCardToDelete.value = null;
    }
}


async function onVideoCardEditClick(videocard) {
    VideoCardToEdit.value = { ...videocard };
    computersEditImageUrl.value = videocard.picture;

    computersEditPictureRef.value.value = null;
}


async function onUpdateVideoCard() {
    const formData = new FormData();
    if (computersEditPictureRef.value.files.length > 0) {
        formData.append('picture', computersEditPictureRef.value.files[0]);
    }
    formData.set('model', VideoCardToEdit.value.model);
    formData.set('price', VideoCardToEdit.value.price);
    formData.set('numberFans', VideoCardToEdit.value.numberFans);
    formData.set('turboFrequency', VideoCardToEdit.value.turboFrequency);
    formData.set('memory_size', VideoCardToEdit.value.memory_size);

    await axios.put(`/api/VideoCard/${VideoCardToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchVideocards();
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
                        Вы уверены, что хотите удалить эту видеокарту?
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
            <div class="modal fade" id="editVideoCardModal" tabindex="-1" aria-labelledby="exampleModalLabel"
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
                                        <input type="text" class="form-control" v-model="VideoCardToEdit.model" />
                                        <label for="floatingInput">Модель</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="VideoCardToEdit.price" />
                                        <label for="floatingInput">Цена</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="VideoCardToEdit.numberFans">
                                        <label for="floatingInput">Кол. вентиляторов</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control"
                                            v-model="VideoCardToEdit.turboFrequency">
                                        <label for="floatingInput">Турбочастота</label>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="VideoCardToEdit.memory_size">
                                        <label for="floatingInput">Размер памяти</label>
                                    </div>
                                </div>
                                <div class="col-auto">
                                    <input class="form-control" type="file" ref="computersEditPictureRef"
                                        @change="computersEditPicture" required>
                                </div>
                                <div class="col-auto">
                                    <img :src="computersEditImageUrl || VideoCardToEdit.picture"
                                        style="max-height: 60px;" alt="">
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button data-bs-dismiss="modal" type="button" class="btn btn-primary"
                                @click="onUpdateVideoCard">Сохранить</button>
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
                            <p class="stat-value">{{ statistics.totalVideoCards }} шт.</p>
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
            <form @submit.prevent.stop="onVideoCardAdd">
                <div class="row">
                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="videoCardAdd.model" required />
                            <label for="floatingInput">Модель</label>
                        </div>
                    </div>


                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="videoCardAdd.price" required />
                            <label for="floatingInput">Цена</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="videoCardAdd.numberFans" required />
                            <label for="floatingInput">Количество вентиляторов</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="videoCardAdd.turboFrequency" required />
                            <label for="floatingInput">Турбочастота</label>
                        </div>
                    </div>

                    <div class="col-md-2">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="videoCardAdd.memory_size" required />
                            <label for="floatingInput">Размер памяти</label>
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
                <div v-for="item in videoCard" class="videocard-item">
                    <div>{{ item.model }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.numberFans }}</div>
                    <div>{{ item.turboFrequency }}</div>
                    <div>{{ item.memory_size }}</div>

                    <div v-show="item.picture">
                        <img :src="item.picture" style="max-height: 60px;" @click="openImageModal(item.picture)" alt=""
                            data-bs-toggle="modal" data-bs-target="#imageModal">
                    </div>

                    <button class="btn btn-success" @click="onVideoCardEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editVideoCardModal"> <i class="bi bi-pencil"> </i></button>
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
.videocard-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    box-shadow: 0 0 4px silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 0.5fr 0.5fr 0.5fr 1fr 1fr 0.14fr 0.1fr auto;
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
