<template>
  <div>
    <div class="row stats-panel">
      <div class="d-flex align-bottom col-6">
<!--        <span class="label">Игра:</span>-->
        <span>{{this.game_id}}</span>&nbsp;&nbsp;
      </div>
      <div class="d-flex col-5">
        <span class="label">Попыток:</span>
        <span>{{this.attempt}}</span>&nbsp;&nbsp;
      </div>
      <div class="d-flex col-1 justify-content-end">
        <img class="img-hint" src="/tip.png" :disabled="this.loading" v-on:click="tip">
      </div>
    </div>

    <div class="row stats-panel">
      <div class="d-flex col-3" v-if="hint">
        <span class="label">Подсказок:</span>
        <span>{{this.hint}}</span>
      </div>
    </div>

    <input class="form-control form-control-lg" type="text" placeholder="Введите слово" aria-label=".form-control-lg example" v-on:keyup.enter="guess" v-model="text" :disabled="this.loading">

    <div class="message-panel">
      <div class="alert alert-primary" role="alert" v-if="solved">
        <h1>Поздравлямба!</h1>
        Вы угадали слово за {{this.attempt}} попыток и {{this.hint}} подсказок.

        <router-link :to="closeWordsLink"><button type="button" class="btn mt-3 btn-light w-100">Ближайшие слова</button></router-link>
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
        <p>Сделано под впечатлением от <a href="https://contexto.me/">contexto.me</a> </p>
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
      loading: false,
      dict: {}
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
    closeWordsLink: function () {
      return '/' + this.game_id + '/words'
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
    leading_zero: function (data) {
      if(String(data).length === 1) return "0" + data
      return data
    },
    guess: function () {
      let clean_word = this.text.trim().toLowerCase().replace("ё", "е")

      let result = this.dict[clean_word]
      if(result === undefined) result = -1

      this.lastPayload = {
        "word": this.text,
        "lemma": clean_word,
        "distance": result
      }

      this.dup = false;
      for(let i in this.words) {
        let data = this.words[i]
        if(data.lemma === clean_word) {
          this.dup = true;
        }
      }

      if(!this.dup) {
        if(this.lastPayload.distance !== -1) this.words.push(this.lastPayload)
        if(!this.solved) this.attempt++;
      }

      if (this.lastPayload.distance === 0) {
        this.solved = true;
      }
      this.saveState()
      this.text = ""
    },
    tip: function () {
      this.dup = false;
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
          if(this.words[i].distance === min_distance) {
            found = true;
            min_distance += 1;
            break;
          }
        }
      }

      if (!self.solved) this.hint++;

      for(let i in self.dict) {
        if(self.dict[i] === min_distance) {
          this.lastPayload = {
            "word": i,
            "lemma": i,
            "distance": min_distance
          }
          break
        }
      }

      this.words.push(this.lastPayload)
      self.saveState()
    },
    loadState: function() {
      console.log("loading " + this.game_id)

      let self = this;
      axios.get("/game/" + this.game_id + ".json").then(function (response) {
        self.dict = response.data
        self.loading = false
      })
      if(!localStorage.games) return;

      let games_data = JSON.parse(localStorage.games)
      if(!(self.game_id in games_data)) return;

      self.attempt = games_data[self.game_id].attempt
      self.words = games_data[self.game_id].words
      self.solved = games_data[self.game_id].solved
      self.hint = games_data[self.game_id].hint
    },
    saveState: function () {
      if(!localStorage.games) {
        localStorage.games = "{}"
      }

      let games_data = JSON.parse(localStorage.games)
      games_data[this.game_id] = {
        'attempt': this.attempt,
        'words': this.words,
        'solved': this.solved,
        'hint': this.hint
      }
      localStorage.setItem("games", JSON.stringify(games_data))
    }
  },
  mounted() {
    this.loading = true;
    if (!this.id) {
      let now = new Date();
      let year = now.getFullYear()
      let month = this.leading_zero(now.getMonth() + 1)
      let day = this.leading_zero(now.getDate())
      this.game_id = "" + year + "-" + month + "-" + day;
    } else {
      this.game_id = this.id
    }
    this.loadState()
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
  height: 27px;
}
</style>