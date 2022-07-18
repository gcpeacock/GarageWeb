<template>
  <div class="logdata">
    <pre>{{logtext}}</pre>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import axios from "axios";

const API_BASE_URL = "http://10.0.0.221:5000/api"

export default defineComponent({
  data() {
    return {
      logtext: "",
    };
  },
  created() {
    this.getLogText();
  },
  methods: {
    getLogText() {
      axios
        .get(`${API_BASE_URL}/log`)
        .then((res) => {
          this.logtext = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
});
</script>

<style scoped>
.inputcode {
  margin: auto;
  margin-top: 20px;
  margin-bottom: 20px;
  text-align: center;
}

</style>
