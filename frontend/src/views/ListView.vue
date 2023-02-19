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
    },
    leading_zero: function (data) {
      if(String(data).length === 1) return "0" + data
      return data
    }
  },
  computed: {
    game_list: function() {
      let result = [];

      let now = new Date(2023, 1, 16);
      let start = new Date(2022, 10, 13);
      let current = new Date(now);

      let storage = null;
      if(localStorage.games) {
         storage = JSON.parse(localStorage.games)
      }


      while(current > start) {
        let year = current.getFullYear()
        let month = this.leading_zero(current.getMonth() + 1)
        let day = this.leading_zero(current.getDate())

        let game_name = "" + year + "-" + month + "-" + day

        let solved = storage && storage[game_name] ? storage[game_name].solved : false

        result.push({
          name: game_name,
          solved: solved
        })

        current.setDate(current.getDate() - 1);
      }

      return result
    }
  },
  mounted() {

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