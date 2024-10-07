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

async function fetchProcessor() {
    const r = await axios.get("/api/Processor/");
    processor.value = r.data;
}

async function onProcessorAdd() {
    await axios.post("/api/Processor/", {
        ...ProcessordAdd.value,
    });
    await fetchProcessor();
}

onBeforeMount(async () => {
    await fetchProcessor();
});


async function onRemoveClick(processor) {
    await axios.delete(`/api/Processor/${processor.id}/`);
    await fetchProcessor();
}

async function onProcessorEditClick(processor) {
    ProcessorAddToEdit.value = { ...processor };
}

async function onUpdateProcessor() {
    await axios.put(`/api/Processor/${ProcessorAddToEdit.value.id}/`, {
        ...ProcessorAddToEdit.value
    });
    await fetchProcessor();
}


</script>



<template>
    <div class="container-fluid">

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
            </form>
            <div>
                <div v-for="item in processor" class="processor-item">
                    <div>{{ item.model }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.socket }}</div>
                    <div>{{ item.chipset }}</div>
                    <div>{{ item.frequency }}</div>


                    <button class="btn btn-success" @click="onProcessorEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editProcessorModal"> <i class="bi bi-pencil"> </i></button>
                    <button class="btn btn-danger" @click="onRemoveClick(item)"> <i class="bi bi-trash"> </i></button>
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
</style>