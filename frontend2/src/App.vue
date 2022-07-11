<template>
  <v-app>
    <v-main>
      <MainHeader />
      <RouterView />
    </v-main>
  </v-app>
</template>

<script>
import MainHeader from "./components/MainHeader.vue";
import { RouterView } from "vue-router";

export default {
  name: "App",

  components: {
    MainHeader,
    RouterView,
  },

  data: () => ({
    //
  }),
};
</script>
