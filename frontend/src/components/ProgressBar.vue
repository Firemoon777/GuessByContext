<template>
  <div class="progress position-relative mt-3" style="height: 64px">
    <div class="progress-bar" :class="color" role="progressbar" :style="this.width"></div>
    <div class="row position-absolute w-100">
      <div class="col-6 justify-content-start d-flex">
        <h1>{{payload.word}}</h1>
      </div>
      <div class="col-6 justify-content-end d-flex">
        <h1>{{payload.distance}}</h1>
      </div>
    </div>
<!--    <small class="justify-content-center">60% complete</small>-->
  </div>
</template>

<script>
export default {
  name: "ProgressBar",
  props: ["payload", "strip"],
  computed: {
    color: function () {
      let result = this.strip === true ? "progress-bar-striped " : "";
      if(this.payload.distance < 300) return result + "bg-success"
      if(this.payload.distance < 1500) return result + "bg-warning"
      return result + "bg-danger"
    },
    width: function () {
      let result;
      if(this.payload.distance < 300) {
        result = (300 - this.payload.distance) / 300 * 100 + 66;
      } else if(this.payload.distance < 1500) {
        result = (1500 - this.payload.distance) / 1500 / 3 * 100 + 33;
      } else {
        result = (50000 - this.payload.distance) / 50000 / 3 * 100;
      }
      return {
        width: result.toString() + "%"
      }
    }
  }
}
</script>

<style scoped>

</style>