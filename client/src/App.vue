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


async function onRemoveClick(computer) {
    await axios.delete(`/api/computers/${computer.id}/`);
    await fetchComputers();
}

// async function onComputerEditClick(computer) {
//     computersToEdit.value = {...computer};
// }

async function onUpdateComputer() {
    await axios.put(`/api/computers/${computersToEdit.value.id}/`,{
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
    <!--Modal-->
    <div class="modal fade" id="editComputerModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Редактировать</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-2">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="computersToEdit.model" />
                                <label for="floatingInput">Model</label>
                            </div>
                        </div>


                        <div class="col-md-2">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="computersToEdit.price" />
                                <label for="floatingInput">Price</label>
                            </div>
                        </div>


                        <div class="col-md-2">
                            <div class="form-floating">
                                <select name="" id="" class="form-select" v-model="computersToEdit.computerV_FK_1">
                                    <option :value="g.id" v-for="g in videoCard">{{ g.model }}</option>
                                </select>
                                <label for="floatingInput">VideoCard</label>
                            </div>
                        </div>


                        <div class="col-md-2">
                            <div class="form-floating">
                                <select name="" id="" class="form-select" v-model="computersToEdit.computerM_FK_1">
                                    <option :value="g.id" v-for="g in motherboard">{{ g.model }}</option>
                                </select>
                                <label for="floatingInput">Motherboard</label>
                            </div>
                        </div>

                        <div class="col-md-2">
                            <div class="form-floating">
                                <select name="" id="" class="form-select" v-model="computersToEdit.computerP_FK_1">
                                    <option :value="g.id" v-for="g in processor">{{ g.model }}</option>
                                </select>
                                <label for="floatingInput">Processor</label>
                            </div>
                        </div>


                        <div class="col-md-2">
                            <div class="form-floating">
                                <select name="" id="" class="form-select" v-model="computersToEdit.computerPU_FK_1">
                                    <option :value="g.id" v-for="g in powerUnit">{{ g.model }}</option>
                                </select>
                                <label for="floatingInput">PowerUnit</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateComputer">Сохранить</button>
                </div>
            </div>
        </div>
    </div>



    <div class="p-2">
        <div class="row">
            <div class="col-md-2">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="computersToAdd.model" />
                    <label for="floatingInput">Model</label>
                </div>
            </div>


            <div class="col-md-2">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="computersToAdd.price" />
                    <label for="floatingInput">Price</label>
                </div>
            </div>


            <div class="col-md-2">
                <div class="form-floating">
                    <select name="" id="" class="form-select" v-model="computersToAdd.computerV_FK_1">
                        <option :value="g.id" v-for="g in videoCard">{{ g.model }}</option>
                    </select>
                    <label for="floatingInput">VideoCard</label>
                </div>
            </div>


            <div class="col-md-2">
                <div class="form-floating">
                    <select name="" id="" class="form-select" v-model="computersToAdd.computerM_FK_1">
                        <option :value="g.id" v-for="g in motherboard">{{ g.model }}</option>
                    </select>
                    <label for="floatingInput">Motherboard</label>
                </div>
            </div>

            <div class="col-md-2">
                <div class="form-floating">
                    <select name="" id="" class="form-select" v-model="computersToAdd.computerP_FK_1">
                        <option :value="g.id" v-for="g in processor">{{ g.model }}</option>
                    </select>
                    <label for="floatingInput">Processor</label>
                </div>
            </div>


            <div class="col-md-2">
                <div class="form-floating">
                    <select name="" id="" class="form-select" v-model="computersToAdd.computerPU_FK_1">
                        <option :value="g.id" v-for="g in powerUnit">{{ g.model }}</option>
                    </select>
                    <label for="floatingInput">PowerUnit</label>
                </div>
            </div>



            <div class="col-auto">
                <button class="btn btn-primary mt-3" @click="onComputerAdd">Добавить</button>
            </div>
        </div>

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
                <button class="btn btn-danger" @click="onRemoveClick(item)"> <i class="bi bi-trash"> </i></button>
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