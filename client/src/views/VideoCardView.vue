<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';

import Cookies from 'js-cookie';

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})


const videoCard = ref({});
const videoCardAdd = ref({});
const VideoCardToEdit = ref({});

async function fetchVideocards() {
    const r = await axios.get("/api/VideoCard/");
    videoCard.value = r.data;
}

async function onVideoCardAdd() {
    await axios.post("/api/VideoCard/", {
        ...videoCardAdd.value,
    });
    await fetchVideocards();
}

onBeforeMount(async () => {
    await fetchVideocards();
});


async function onRemoveClick(videoCard) {
    await axios.delete(`/api/VideoCard/${videoCard.id}/`);
    await fetchVideocards();
}

async function onVideoCardEditClick(videocard) {
    VideoCardToEdit.value = { ...videocard };
}

async function onUpdateVideoCard() {
    await axios.put(`/api/VideoCard/${VideoCardToEdit.value.id}/`, {
        ...VideoCardToEdit.value
    });
    await fetchVideocards();
}


</script>



<template>
    <div class="container-fluid">

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
                </div>
            </form>
            <div>
                <div v-for="item in videoCard" class="videocard-item">
                    <div>{{ item.model }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.numberFans }}</div>
                    <div>{{ item.turboFrequency }}</div>
                    <div>{{ item.memory_size }}</div>


                    <button class="btn btn-success" @click="onVideoCardEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editVideoCardModal"> <i class="bi bi-pencil"> </i></button>
                    <button class="btn btn-danger" @click="onRemoveClick(item)"> <i class="bi bi-trash"> </i></button>
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
    grid-template-columns: 0.5fr 0.5fr 0.5fr 1fr 1fr 0.14fr auto;
    gap: 8px;
    text-align: center;
    align-items: center;
}
</style>