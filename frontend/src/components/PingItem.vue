<template>
  <div>
    <p>{{ msg }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import axios from "axios";

export default defineComponent({
  data() {
    return {
      msg: "",
    };
  },
  methods: {
    getMessage() {
      const path = "http://127.0.0.1:5000/health";
      axios
        .get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
});
</script>
