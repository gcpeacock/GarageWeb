<template>
  <v-toolbar color="primary" prominent>
    <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer">
    </v-app-bar-nav-icon>
    <v-toolbar-title>Peacock's Garage Monitor</v-toolbar-title>
    <v-navigation-drawer v-model="drawer" bottom temporary>
      <v-list>
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
          :to="item.path"
          :prepend-icon="item.icon"
          :title="item.title"
        >
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-toolbar>
</template>

<script>
import logo from "../assets/logo.svg";

export default {
  name: "MainHeader",
  data() {
    return {
      drawer: false,
      group: null,
      logo,
      items: [
        {
          title: "Home",
          icon: "mdi-garage",
          path: "/",
        },
        {
          title: "Log",
          icon: "mdi-file-document",
          path: "/log",
        },
      ],
    };
  },
};
</script>
