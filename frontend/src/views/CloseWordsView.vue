<template>
  <div>
    <ProgressBar v-for="payload in this.word_list" :payload="payload"/>
    <div
      class="progress progress-bar progress-bar-striped progress-bar-animated loading"
      role="progressbar"
      v-if="this.loading"
    ></div>
  </div>
</template>

<script>
import axios from 'axios';
import ProgressBar from "../components/ProgressBar.vue";
export default {
  name: "CloseWordsView",
  components: {ProgressBar},
  props: ["id"],
  data() {
    return {
      word_list: [],
      loading: true
    }
  },
  created() {
    let self = this
    axios.get("/game/" + this.id + ".json").then(function (response) {
      let top = 500
      let top_dict = {}
      for(let word in response.data) {
        let distance = response.data[word]
        if(distance <= top) {
          top_dict[distance] = word
        }
      }

      let result = [];
      for(let i = 1; i <= top; i++) {
        result.push({
          "word": top_dict[i],
          "lemma": top_dict[i],
          "distance": i
        })
      }
      self.word_list = result
    }).finally(function () {
      self.loading = false;
    })
  }
}
</script>

<style scoped>

</style>