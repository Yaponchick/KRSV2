<template>
    <div class="container py-5">
        <div class="card shadow-lg border-0 rounded-4 animate__animated animate__fadeIn">
            <div class="card-header text-center bg-primary text-white rounded-top-4">
                <h2 class="mb-0">Детали компьютера</h2>
            </div>
            <div class="card-body">
                <div class="row mb-3">
                    <div class="col-md-6">
                        <h4 class="text-secondary">Основная информация</h4>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">
                                <strong>Модель:</strong> {{ data.model }}
                            </li>
                            <li class="list-group-item">
                                <strong>Цена:</strong> {{ data.price }} ₽
                            </li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h4 class="text-secondary">Компоненты</h4>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">
                                <strong>Видеокарта:</strong> {{ data.videoCard }}
                            </li>
                            <li class="list-group-item">
                                <strong>Материнская плата:</strong> {{ data.motherboard }}
                            </li>
                            <li class="list-group-item">
                                <strong>Процессор:</strong> {{ data.processor }}
                            </li>
                            <li class="list-group-item">
                                <strong>Блок питания:</strong> {{ data.powerUnit }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="card-footer bg-light text-center rounded-bottom-4">
                <button class="btn btn-outline-primary animate__animated animate__pulse animate__infinite" @click="goBack">
                    <i class="bi bi-arrow-left"></i> Назад
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import 'animate.css';

export default {
    setup() {
        const data = ref({});

        onMounted(() => {
            const params = new URLSearchParams(window.location.search);
            data.value = {
                model: params.get('model'),
                price: params.get('price'),
                videoCard: params.get('videoCard'),
                motherboard: params.get('motherboard'),
                processor: params.get('processor'),
                powerUnit: params.get('powerUnit'),
            };
        });

        const goBack = () => {
            window.history.back();
        };

        return {
            data,
            goBack,
        };
    },
};
</script>

<style scoped>
.card-header {
    animation: slideDown 1s ease-in-out;
}

@keyframes slideDown {
    0% {
        transform: translateY(-20px);
        opacity: 0;
    }
    100% {
        transform: translateY(0);
        opacity: 1;
    }
}

.card {
    transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.btn {
    transition: transform 0.3s, background-color 0.3s;
}

.btn:hover {
    transform: scale(1.1);
    background-color: #007bff;
    color: white;
}
</style>
