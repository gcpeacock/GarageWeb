<template>
  <v-toolbar color="primary" prominent>
    <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer">
    </v-app-bar-nav-icon>
    <v-toolbar-title>Peacock's Garage Monitor</v-toolbar-title>
    <v-navigation-drawer v-model="drawer" bottom temporary>
      <v-list :items="items"></v-list>
    </v-navigation-drawer>
  </v-toolbar>
</template>

<script>
export default {
  name: "MainHeader",
  data() {
    return {
      drawer: false,
      group: null,
      items: [
        {
          title: "Foo",
          value: "foo",
        },
        {
          title: "Bar",
          value: "bar",
        },
        {
          title: "Fizz",
          value: "fizz",
        },
        {
          title: "Buzz",
          value: "buzz",
        },
      ],
    };
  },
};
</script>
