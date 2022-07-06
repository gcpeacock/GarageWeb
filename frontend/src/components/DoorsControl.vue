<template>
  <div class="inputcode">
    <input
      v-model.number.trim="doorcode"
      class="doorcode"
      placeholder="Enter door code."
    />
  </div>
  <div class="row">
    <div class="col" v-for="(doorstate, index) in doors" :key="index">
      <div class="card text-center">
        <div v-if="index == 0" class="card-header">Christy's Door</div>
        <div v-else-if="index == 1" class="card-header">Gary's Door</div>
        <div class="card-body text-center">
          <img
            v-if="doorstate == 0"
            src="../assets/GarageQuestion.gif"
            class="card-img"
            @click="controlDoor(index)"
            alt="Opening/Closing"
          />
          <img
            v-else-if="doorstate == 1"
            src="../assets/GarageGreen.gif"
            class="card-img"
            @click="controlDoor(index)"
            alt="Close"
          />
          <img
            v-else-if="doorstate == 2"
            src="../assets/GarageRed.gif"
            class="card-img"
            @click="controlDoor(index)"
            alt="Open"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import axios from "axios";

const API_BASE_URL = "http://10.0.0.221:5000/api/"

export default defineComponent({
  data() {
    return {
      doors: [],
      doorcode: "",
      timer: 0,
    };
  },
  created() {
    this.timer = window.setInterval(this.getDoorsStatus, 300000);
    this.getDoorsStatus();
  },
  methods: {
    updatePollFrequency() {
      let interval = 300000;

      for (const door of this.doors) {
        if (door == 0) {
          interval = 3000;
        }
      }

      this.timer = window.setTimeout(this.getDoorsStatus, interval);
    },
    getDoorsStatus() {
      axios
        .get(`${API_BASE_URL}doors`)
        .then((res) => {
          this.doors = res.data.doorstates;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      this.updatePollFrequency();
    },
    controlDoor(index: number) {
      let whichdoor = ++index;
      const payload = { door: whichdoor, garagecode: this.doorcode };

      axios
        .post(`${API_BASE_URL}doors`, payload, {
          headers: { "content-type": "application/json" },
        })
        .then((res) => {
          if (res.status != 200) {
            this.doorcode = "Invalid Request";
          }
          this.doors = res.data.doorstates;
          this.updatePollFrequency();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.doorcode = "Invalid Request";
          this.getDoorsStatus();
        });
    },
    cancelAutoUpdate() {
      clearInterval(this.timer);
    },
  },
  unmounted() {
    this.cancelAutoUpdate();
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

input {
  text-align: center;
}
.col {
  /* font: 14px 'Helvetica Neue', Helvetica, Arial, sans-serif; */
  /* line-height: 1.4em; */
  /* background: #f5f5f5; */
  /* color: #111111; */
  /* min-width: 230px; */
  /* max-width: 550px; */
  /* margin: 0 auto; */
  /* -webkit-font-smoothing: antialiased; */
  /* -moz-osx-font-smoothing: grayscale; */
  /* font-weight: 300; */
}
.special-card {
  /* create a custom class so you 
   do not run into specificity issues 
   against bootstraps styles
   which tends to work better than using !important 
   (future you will thank you later)*/

  background-color: rgba(245, 245, 245, 1);
  opacity: 0.4;
}
</style>
