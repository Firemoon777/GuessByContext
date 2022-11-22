<template>
  <div>
    <div class="row">
      <h1>Игра: {{this.game_id}} Попыток: {{this.attempt}}</h1>
    </div>
    <input class="form-control form-control-lg" type="text" placeholder="Введите слово" aria-label=".form-control-lg example" v-on:keyup.enter="guess" v-model="text">
    <div class="alert alert-primary mt-3" role="alert" v-if="lastWordNotFound">
      Кажется, слова {{lastPayload.word}} нет в словаре!
    </div>
    <div class="alert alert-primary mt-3" role="alert" v-if="lastWordGuessed">
      <h1>Поздравлямба!</h1>
      Вы угадали слово за {{this.attempt}} попыток.
    </div>
    <ProgressBar :payload="this.lastPayload" v-if="lastWordCorrect" :strip="true"/>
    <div class="col mt-5">
      <ProgressBar v-for="payload in this.sortedWords" :payload="payload"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ProgressBar from "../components/ProgressBar.vue";
export default {
  name: "PlaygroundView",
  components: {ProgressBar},
  props: ["id"],
  data() {
    return {
      game_id: "0",
      text: "",
      attempt: 0,
      words: [],
      lastPayload: {}
    }
  },
  computed: {
    sortedWords: function () {
      return this.words.sort(function (a, b) {
          if(a.distance < b.distance) return -1;
          if(a.distance > b.distance) return 1;
          return 0
      })
    },
    lastWordCorrect: function () {
      if ("error" in this.lastPayload) return false;
      if (!("distance" in this.lastPayload)) return false;
      return this.lastPayload.distance !== -1;
    },
    lastWordNotFound: function () {
      if("error" in this.lastPayload) return false;
      if(!("distance" in this.lastPayload)) return false;
      return this.lastPayload.distance === -1;
    },
    lastWordGuessed: function () {
      if("error" in this.lastPayload) return false;
      if(!("distance" in this.lastPayload)) return false;
      return this.lastPayload.distance === 0;
    }
  },
  methods: {
    guess: function () {
      this.attempt++;
      let self = this;
      let data = {
        game_id: this.game_id,
        word: this.text
      };
      axios.post("/guess", data).then(function (response) {
        self.lastPayload = response.data
        if ("error" in response.data) {
          return
        }
        if(response.data.distance === -1) {
          return;
        }
        self.words.push(response.data)
      })
      this.text = ""
    }
  },
  created() {
    if (!this.id) {
      let self = this
      axios.get("/game").then(function (response) {
        console.log(response.data[0])
        self.game_id = response.data[0]
      })
    } else {
      this.game_id = this.id
    }
  }
}
</script>

<style scoped>

</style>