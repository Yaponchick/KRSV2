<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';

import Cookies from 'js-cookie';

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})


const motherboard = ref({});
const motherboardAdd = ref({});
const MotherboardAddToEdit = ref({});

async function fetchMotherboard() {
    const r = await axios.get("/api/Motherboard/");
    motherboard.value = r.data;
}

async function onMotherboardAdd() {
    await axios.post("/api/Motherboard/", {
        ...motherboardAdd.value,
    });
    await fetchMotherboard();
}

onBeforeMount(async () => {
    await fetchMotherboard();
});


async function onRemoveClick(motherboard) {
    await axios.delete(`/api/Motherboard/${motherboard.id}/`);
    await fetchMotherboard();
}

async function onMotherboardEditClick(motherboard) {
    MotherboardAddToEdit.value = { ...motherboard };
}

async function onUpdateMotherboard() {
    await axios.put(`/api/Motherboard/${MotherboardAddToEdit.value.id}/`, {
        ...MotherboardAddToEdit.value
    });
    await fetchMotherboard();
}


</script>



<template>
    <div class="container-fluid">

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
                </div>
            </form>
            <div>
                <div v-for="item in motherboard" class="motherboard-item">
                    <div>{{ item.model }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.compatibleKernels }}</div>
                    <div>{{ item.processorPowerConnector }}</div>
                    <div>{{ item.supportedMemory }}</div>


                    <button class="btn btn-success" @click="onMotherboardEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editMotherboardModal"> <i class="bi bi-pencil"> </i></button>
                    <button class="btn btn-danger" @click="onRemoveClick(item)"> <i class="bi bi-trash"> </i></button>
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
    grid-template-columns: 0.5fr 0.5fr 0.5fr 1fr 1fr 0.14fr auto;
    gap: 8px;
    text-align: center;
    align-items: center;
}
</style>