<template>
  <v-toolbar color="primary" prominent>
    <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer">
    </v-app-bar-nav-icon>
    <v-toolbar-title>Peacock's Garage Monitor</v-toolbar-title>
    <v-navigation-drawer v-model="drawer" bottom temporary>
      <v-list v-for="route in router.routes" :key="route.title">
        <v-list-item
          prepend-icon="{{ route.icon }}"
          title="{{ route.title }}"
          @click="navigateTo(route.path)"
        >
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-toolbar>
</template>

<script>
import router from "../router";

export default {
  name: "MainHeader",
  data() {
    return {
      drawer: false,
      group: null,
      router,
      items: [
        {
          title: "Home",
          value: "home",
        },
        {
          title: "Log",
          value: "log",
        },
      ],
    };
  },
};
</script>
