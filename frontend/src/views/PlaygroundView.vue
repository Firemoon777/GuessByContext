<template>
  <div>
    <div class="row stats-panel">
      <div class="d-flex align-bottom col-5">
        <span class="label">Игра:</span>
        <span>{{this.game_id}}</span>&nbsp;&nbsp;
      </div>
      <div class="d-flex col-2">
        <span class="label">Всего:</span>
        <span>{{this.attempt}}</span>&nbsp;&nbsp;
      </div>
      <div class="d-flex col-3">
        <span class="label" v-if="hint">Подсказок:</span>
        <span v-if="hint">{{this.hint}}</span>
      </div>
      <div class="d-flex col-2 justify-content-end">
        <img class="img-hint" src="tip.png"  :disabled="this.loading" v-on:click="tip">
      </div>

    </div>

    <input class="form-control form-control-lg" type="text" placeholder="Введите слово" aria-label=".form-control-lg example" v-on:keyup.enter="guess" v-model="text">

    <div class="message-panel">
      <div class="alert alert-primary" role="alert" v-if="solved">
        <h1>Поздравлямба!</h1>
        Вы угадали слово за {{this.attempt}} попыток и {{this.hint}} подсказок.
      </div>
      <div class="alert alert-primary" role="alert" v-if="lastWordNotFound">
        Кажется, слова {{lastPayload.word}} нет в словаре или оно слишком далеко!
      </div>
      <div class="alert alert-danger" v-if="dup">
        Слово {{this.lastPayload.lemma}} уже отгадано!
      </div>
<!--      <div-->
<!--          class="progress progress-bar progress-bar-striped progress-bar-animated loading"-->
<!--          role="progressbar"-->
<!--          v-if="this.loading"-->
<!--      ></div>-->
      <ProgressBar :payload="this.lastPayload" v-if="lastWordCorrect" :strip="true"/>

      <div class="alert alert-dark" role="alert" v-if="this.words.length === 0 && !this.id">
        <span class="title">Как играть?</span><br><br>
        <p>Угадайте загаданное слово. У вас бесконечное количество попыток.</p>
        <p>Слова отсортированы искуственным интеллектом по смыслу в порядке убывания.</p>
        <p>После отправки слова отобразится его позиция в списке. Загаданное слово имеет номер 0.</p>
        <p>Перед тем как попасть сюда, искуственный интеллект работал над миллионами текстов. Он использует полученный опыт и понимание контекста для определения смысловой близости слов.</p>
      </div>
    </div>

    <div class="col mt-4">
      <ProgressBar v-for="payload in this.sortedWords" :payload="payload" :dup="dup" :last="lastPayload"/>
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
      lastPayload: {},
      dup: false,
      solved: false,
      hint: 0,
      loading: false
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
      return this.lastPayload.distance !== -1 && !this.dup;
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
      this.dup = false;
      this.loading = true;
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
        for(let i in self.words) {
          data = self.words[i]
          if(data.lemma === response.data.lemma) {
            self.dup = true;
            break
          }
        }
        if(!self.dup) {
          self.words.push(response.data)
          if (!self.solved) self.attempt++;
        }
        if(response.data.distance === 0) {
          self.solved = true;
        }

        self.saveState()
      }).finally(function () {
        self.loading = false;
        console.warn(self.$refs.input)
        self.$refs.input.focus()
      })
      this.text = ""
    },
    tip: function () {
      this.dup = false;
      this.loading = true;
      let self = this;

      let min_distance = 50_000;
      for(let i in this.words) {
        if(this.words[i].distance < min_distance) min_distance = this.words[i].distance;
      }
      min_distance = ~~(min_distance / 2);
      if(min_distance < 1) min_distance = 1;

      let found = true;
      while(found) {
        found = false;
        for(let i in this.words) {
          console.log("" + this.words[i].distance + " === " + min_distance + "(" + this.words[i].lemma + ")")
          if(this.words[i].distance === min_distance) {
            found = true;
            min_distance += 1;
            break;
          }
        }
      }

      let data = {
        game_id: this.game_id,
        distance: min_distance
      };
      axios.post("/tip", data).then(function (response) {
        self.lastPayload = response.data
        if ("error" in response.data) {
          return
        }
        if(response.data.distance === -1) {
          return;
        }

        self.words.push(response.data)
        if (!self.solved) self.hint++;

        self.saveState()
      }).finally(function () {
        self.loading = false;
      })
    },
    loadState: function() {
      console.log("loading " + this.game_id)
      if(!localStorage.games) return;

      let games_data = JSON.parse(localStorage.games)
      if(!(this.game_id in games_data)) return;

      this.attempt = games_data[this.game_id].attempt
      this.words = games_data[this.game_id].words
      this.solved = games_data[this.game_id].solved
    },
    saveState: function () {
      if(!localStorage.games) {
        localStorage.games = "{}"
      }

      let games_data = JSON.parse(localStorage.games)
      games_data[this.game_id] = {
        'attempt': this.attempt,
        'words': this.words,
        'solved': this.solved
      }
      console.warn(typeof(games_data))
      localStorage.setItem("games", JSON.stringify(games_data))
    }
  },
  created() {
    if (!this.id) {
      let self = this
      axios.get("/game").then(function (response) {
        localStorage.list = JSON.stringify(response.data)
        self.game_id = response.data[0]
        self.loadState()
      })
    } else {
      this.game_id = this.id
      this.loadState()
    }
  }
}
</script>

<style scoped>
.label {
  font-size: 12px;
  text-transform: uppercase;
  margin-right: 6px;
  font-weight: 700;
  margin-top: 6px;
}

span {
  font-size: 18px;
  font-weight: 900;
}

.stats-panel {
  padding: 10px 10px 0;
}

input {
  margin-top: 10px;
  margin-bottom: 10px;
}

.loading {
  width: 100%;
  background-color: #cccccc;
  border: 5px solid #000000;
  height: 47px;
}

p {
  font-weight: 550;
}

.help-button {
  width: 36px;
  height: 36px;
  border-radius: 19px;
}

.img-hint {
  width: 27px;
}
</style>