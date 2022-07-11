<template>
  <v-container>
    <v-text-field
      v-model="doorcode"
      :append-icon="showcode ? 'mdi-eye' : 'mdi-eye-off'"
      placeholder="Enter door code."
      :rules="[rules.required, rules.numeric, rules.min]"
      :type="showcode ? 'text' : 'password'"
      hide-details="auto"
      clearable
      density="compact"
      @click:append="showcode = !showcode"
    ></v-text-field>
  </v-container>
  <v-container>
    <v-row>
      <v-col v-for="(card, index) in cards" :key="index" :cols="card.flex">
        <v-card>
          <v-card-title class="text-center">{{ card.title }}</v-card-title>
          <v-img
            :src="garagequestion"
            @click="controlDoor(index)"
            alt="Opening/Closing"
          />
        </v-card>
        <!-- <v-img
          v-else-if="doors[index].doorstate == 1"
          src="../assets/GarageGreen.gif"
          @click="controlDoor(index)"
          alt="Close"
        />
        <v-img
          v-else-if="doors[index].doorstate == 2"
          src="../assets/GarageRed.gif"
          @click="controlDoor(index)"
          alt="Open"
        /> -->
      </v-col>
    </v-row>
  </v-container>
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

<script>
import axios from "axios";

import garagequestion from "../assets/GarageQuestion.gif";

const API_BASE_URL = "http://10.0.0.221:5000/api/";

export default {
  name: "DoorsControl",
  data() {
    return {
      showcode: false,
      doors: [],
      doorcode: "",
      timer: 0,
      rules: {
        required: (value) => !!value || "Required.",
        min: (value) => (value || "").length <= 8 || "Max 8 characters",
        numeric: (value) => {
          const pattern = /^[0-9]+$/;
          return pattern.test(value) || "Numbers only.";
        },
      },
      cards: [
        { title: "Christy's Door", flex: 6 },
        { title: "Gary's Door", flex: 6 },
      ],
      garagequestion,
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
    controlDoor(index) {
      let whichdoor = ++index;
      const payload = { door: whichdoor, garagecode: this.doorcode };

      axios
        .post(`${API_BASE_URL}doors`, payload, {
          headers: { "content-type": "application/json" },
        })
        .then((res) => {
          if (res.status != 200) {
            this.doorcode = "";
          }
          this.doorcode = "";
          this.doors = res.data.doorstates;
          this.updatePollFrequency();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.doorcode = "";
          this.isVisible = true;
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
};
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
</style>
