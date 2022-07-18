<script setup lang="ts">
import { RouterView, RouterLink } from "vue-router";
import HelloWorld from "@/components/HelloWorld.vue";
import NavBar from "@/components/NavBar.vue";
</script>

<template>
  <div>
    <NavBar/>
  </div>
  <div class="wrapper">
    <HelloWorld msg="Peacock's" />
  </div>

  <RouterView />
</template>

<style>
html {
  background-color: aliceblue;
}

#app {
  background-color: aliceblue;
}
</style>
