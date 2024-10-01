<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';

const computers = ref([]);
const videoCard = ref([]);
const motherboard = ref([]);
const processor = ref([]);
const powerUnit = ref([]);

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
        model: "123"
    });

}

onBeforeMount(async () => {
    await fetchComputers();
    await fetchVideocards();
    await fetchMotherboard();
    await fetchProcessor();
    await fetchPowerUnit();
});

</script>



<template>
    <div class="p-2">
        <div class="row">
            <div class="col-auto">
                <div class="form-floating">
                    <input type="text" class="form-control">
                    <label for="floatingInput">Model</label>
                </div>
            </div>


            <div class="col-auto">
                <div class="form-floating">
                    <input type="text" class="form-control">
                    <label for="floatingInput">Price</label>
                </div>
            </div>


            <div class="col-auto">
                <div class="form-floating">
                    <select name="" id="" class="form-select">
                        <option :value="g.id" v-for="g in videoCard">{{ g.model }}</option>
                    </select>
                    <label for="floatingInput">VideoCard</label>
                </div>
            </div>


            <div class="col-auto">
                <div class="form-floating">
                    <select name="" id="" class="form-select">
                        <option :value="g.id" v-for="g in motherboard">{{ g.model }}</option>
                    </select>
                    <label for="floatingInput">Motherboard</label>
                </div>
            </div>

            <div class="col-auto">
                <div class="form-floating">
                    <select name="" id="" class="form-select">
                        <option :value="g.id" v-for="g in processor">{{ g.model }}</option>
                    </select>
                    <label for="floatingInput">Processor</label>
                </div>
            </div>


            <div class="col-auto">
                <div class="form-floating">
                    <select name="" id="" class="form-select">
                        <option :value="g.id" v-for="g in powerUnit">{{ g.model }}</option>
                    </select>
                    <label for="floatingInput">PowerUnit</label>
                </div>
            </div>



            <div class="col-auto">
                <button class="btn btn-primary" @click="onComputerAdd">Добавить</button>
            </div>
        </div>

        <div>
            <div v-for="item in computers">
                <b>{{ item.model }}</b> <b>{{ item.price }}</b> <br><b>{{ item.computerV_FK.model }}</b>
            </div>

            <br>

            <div v-for="item in videoCard">
                <b>{{ item.model }}</b> <br> <b>{{ item.price }}</b>
            </div>
        </div>
    </div>
</template>



<style scoped></style>
