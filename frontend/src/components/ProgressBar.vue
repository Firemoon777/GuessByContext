<template>
  <div class="progress position-relative mt-3" :class="bordered">
    <div class="progress-bar" :class="color" role="progressbar" :style="this.width"></div>
    <div class="row position-absolute w-100 h-100">
      <div class="col-6 justify-content-start d-flex">
        <span>{{payload.lemma}}</span>
      </div>
      <div class="col-6 justify-content-end d-flex">
        <span>{{payload.distance}}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProgressBar",
  props: ["payload", "strip", "dup", "last"],
  computed: {
    color: function () {
      if(this.payload.distance < 300) return "progress-bar-green"
      if(this.payload.distance < 1500) return "progress-bar-yellow"
      return "progress-bar-red"
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
    },
    bordered: function() {
      if(this.strip) {
        return "panel-border"
      }
      if(this.last.lemma === this.payload.lemma) {
        return "panel-border"
      }
      return "panel-no-border"
    }
  }
}
</script>

<style scoped>
.row>* {
  padding: 0 !important;
}
.row {
  margin: 0 !important;
  padding: 7px;
}
span {
  vertical-align: middle;
  padding-top: 0px;
  text-transform: lowercase;
  /*padding-left: 7px;*/
  /*padding-right: 7px;*/
}

.panel-border {
  border: 5px solid #000000;
  height: 47px;
  /*border-width: 5px;*/
}

.panel-no-border {
  height: 38px;
  border: 1px solid transparent;
}

.progress-bar-green {
  background-color: var(--green);
}

.progress-bar-yellow {
  background-color: var(--yellow);
}

.progress-bar-red {
  background-color: var(--red);
}
</style>