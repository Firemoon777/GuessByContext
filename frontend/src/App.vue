<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="root">
    <nav class="navbar navbar-expand navbar-light bg-light">
     <router-link to="/"><a class="navbar-brand" href="#">Русо контексто</a></router-link>
      <ul class="navbar-nav">
        <li class="nav-item active">
          <router-link to="/list"><a class="nav-link" href="#">Игры</a></router-link>
        </li>
      </ul>
    </nav>

    <RouterView />
  </div>
</template>

<style scoped>
.root {
  max-width: 480px;
  margin: auto;
  padding-left: 10px;
  padding-right: 10px;
}
a {
  text-decoration: transparent;
  /*padding-left: 5px;*/
}
</style>
