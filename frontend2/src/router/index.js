import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
// import LogView from "../views/LogView.vue";

const About = { template: "<div>About</div>" };

const routes = [
  {
    path: "/",
    name: "home",
    title: "Home",
    icon: "mdi-view-dashboard",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    title: "About",
    icon: "mdi-cog",
    component: About,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
