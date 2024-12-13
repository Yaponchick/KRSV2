import { createRouter, createWebHistory } from 'vue-router'
import ComputersView from '../views/ComputersView.vue';
import VideoCardView from '../views/VideoCardView.vue';
import MotherboardView from '../views/MotherboardView.vue';
import ProcessorView from '../views/ProcessorView.vue';
import PowerUnitView from '../views/PowerUnitView.vue';
import ComputerDetails from '../views/ComputerDetails.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      model: "ComputersView",
      component: ComputersView
    },
    {
      path: "/VideoCardView",
      model: "VideoCardView",
      component: VideoCardView
    },
    {
      path: "/MotherboardView",
      model: "MotherboardView",
      component: MotherboardView
    },
    {
      path: "/ProcessorView",
      model: "ProcessorView",
      component: ProcessorView
    },
    {
      path: "/PowerUnitView",
      model: "PowerUnitView",
      component: PowerUnitView
    },
    {
      path: '/computer-details',
      model: 'ComputerDetails',
      component: ComputerDetails
  }
  ]
})

export default router
