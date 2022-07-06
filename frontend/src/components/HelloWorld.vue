<script setup lang="ts">
defineProps<{
  msg: string;
}>();
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>Garage Doors Monitor</h3>
  </div>
</template>

<style scoped>
div {
  background-color: lightsteelblue;
}
h1 {
  padding: 10px;
  font-size: 2.6rem;
  font-weight: 200;
  text-align: center;
  color: #b83f45;
  -webkit-text-rendering: optimizeLegibility;
  -moz-text-rendering: optimizeLegibility;
  text-rendering: optimizeLegibility;
}

h3 {
  padding-bottom: 10px;
  margin: auto;
  text-align: center;
  font-size: 1.2rem;
  font-weight: 200;
}
</style>
