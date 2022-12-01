<template>
  <div class="row">
    <router-link class="w-100 mt-2" :to="'/' + game.name" v-for="game in this.game_list">
      <button  type="button" class="btn w-100" :class="button_class(game)">{{ game.name }}</button>
    </router-link>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ListView",
  data() {
    return {
      raw_list: []
    }
  },
  methods: {
    button_class: function (payload) {
      if(payload.solved) return 'btn-success'
      return 'btn-light'
    }
  },
  computed: {
    game_list: function() {
      let result = [];

      let storage = {}
      if(localStorage.games) storage = JSON.parse(localStorage.games)

      for(let i in this.raw_list) {
        let game_name = this.raw_list[i];
        let game = {
          'name': game_name,
          'solved': storage[game_name] ? (!!storage[game_name].solved) : false
        }
        result.push(game)
      }
      return result
    }
  },
  mounted() {
    if(!localStorage.list) return;

    if(localStorage.list) this.raw_list = JSON.parse(localStorage.list)

    let self = this
    axios.get("/game").then(function (response) {
      localStorage.list = JSON.stringify(response.data)
      self.raw_list = response.data
    })
  }
}
</script>

<style scoped>
.btn {
  max-width: 100%;
}
.row {
  margin: 0;
}
</style>