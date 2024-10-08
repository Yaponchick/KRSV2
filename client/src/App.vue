<script setup>

</script>



<template>

    <div class="container">
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Сборщик</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <router-link class="nav-link" to="/"> Компьютеры </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/VideoCardView"> Видеокарты </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/MotherboardView"> Материнские платы </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/ProcessorView"> Процессоры </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/PowerUnitView"> Блоки питания </router-link>
                        </li>

                    </ul>
					<ul class="navbar-nav">
						<li class="nav-item dropdown">
							<a class="nav-item dropdown-toggle link" href="#" role="button" data-bs-toggle="dropdown"
								aria-expanded="false" >
								Пользователь
							</a>
							<ul class="dropdown-menu">
								<li><a class="dropdown-item" href="/admin">Админка</a></li>
							</ul>
						</li>
					</ul>
                </div>
            </div>
        </nav>
    </div>
    <div>
        <div class="container">
            <router-view />
        </div>
    </div>

</template>



<style scoped></style>