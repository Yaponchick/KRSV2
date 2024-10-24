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

async function fetchPowerUnit() {
    const r = await axios.get("/api/PowerUnit/");
    powerUnit.value = r.data;
}

async function onPowerUnitAdd() {
    await axios.post("/api/PowerUnit/", {
        ...powerUnitdAdd.value,
    });
    await fetchPowerUnit();
}

onBeforeMount(async () => {
    await fetchPowerUnit();
});

function onRemoveClick(powerUnit) {
    powerUnitToDelete.value = powerUnit;
}
async function confirmDelete() {
    if (powerUnitToDelete.value) {
        await axios.delete(`/api/PowerUnit/${powerUnitToDelete.value.id}/`);
        await fetchPowerUnit();
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
            </form>
            <div>
                <div v-for="item in powerUnit" class="powerUnit-item">
                    <div>{{ item.model }}</div>
                    <div>{{ item.price }}</div>
                    <div>{{ item.networkVoltage }}</div>
                    <div>{{ item.coolingSystem }}</div>
                    <div>{{ item.power }}</div>


                    <button class="btn btn-success" @click="onPowerUnitEditClick(item)" data-bs-toggle="modal"
                        data-bs-target="#editPowerUnitModal"> <i class="bi bi-pencil"> </i></button>
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
</style>