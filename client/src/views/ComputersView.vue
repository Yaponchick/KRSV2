<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';

import Cookies from 'js-cookie';

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
}

onBeforeMount(async () => {
    await fetchComputers();
    await fetchVideocards();
    await fetchMotherboard();
    await fetchProcessor();
    await fetchPowerUnit();
});


function onRemoveClick(computer) {
    computersToDelete.value = computer;
}
async function confirmDelete() {
    if (computersToDelete.value) {
        await axios.delete(`/api/computers/${computersToDelete.value.id}/`);
        await fetchComputers();
        computersToDelete.value = null;
    }
}

async function onUpdateComputer() {
    await axios.put(`/api/computers/${computersToEdit.value.id}/`, {
        ...computersToEdit.value
    });
    await fetchComputers();
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

        <!--Modal-->
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
                                <div class="col-12 col-md-4">
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
                        <button class="btn btn-primary mt-3">Добавить</button>
                    </div>
                </div>
            </form>
            <div>
                <div v-for="item in computers" class="computers-item">
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
    grid-template-columns: 0.25fr 0.5fr 0.5fr 1fr 1fr 1fr 0.14fr auto;
    gap: 8px;
    text-align: center;
    align-items: center;
}
</style>