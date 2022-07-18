<template>
  <v-container>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field
        v-model="doorcode"
        :append-icon="showcode ? 'mdi-eye' : 'mdi-eye-off'"
        placeholder="Enter door code."
        :rules="[rules.required, rules.numeric]"
        :type="showcode ? 'text' : 'password'"
        hide-details="auto"
        clearable
        @click:append="showcode = !showcode"
      ></v-text-field>
    </v-form>
  </v-container>
  <v-container>
    <v-row>
      <v-col
        v-for="(doorstate, index) in doors"
        :key="index"
        :cols="cards[index].flex"
      >
        <v-card>
          <v-card-title class="text-center">{{
            cards[index].title
          }}</v-card-title>
          <v-img
            v-if="doorstate == 0"
            :src="garagequestion"
            @click="controlDoor(index)"
            alt="Opening/Closing"
          />
          <v-img
            v-else-if="doorstate == 1"
            :src="garageopen"
            @click="controlDoor(index)"
            alt="Close"
          />
          <v-img
            v-else-if="doorstate == 2"
            :src="garageclosed"
            @click="controlDoor(index)"
            alt="Open"
          />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

import garagequestion from "../assets/GarageQuestion.gif";
import garageopen from "../assets/GarageGreen.gif";
import garageclosed from "../assets/GarageRed.gif";

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
      garageopen,
      garageclosed,
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
            this.resetInput();
          }
          this.doors = res.data.doorstates;
          this.updatePollFrequency();
          this.resetInput();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getDoorsStatus();
          this.resetInput();
        });
    },
    cancelAutoUpdate() {
      clearInterval(this.timer);
    },
    resetInput() {
      this.$refs.form.reset();
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
