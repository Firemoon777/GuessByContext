import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { BootstrapVue } from 'bootstrap-vue'
import './assets/main.css'
// import 'bootstrap/dist/css/bootstrap.css'
const app = createApp(App)

import axios from "axios";

// axios.defaults.baseURL = "http://127.0.0.1:8000";
// axios.defaults.baseURL = "https://words.f1remoon.com/";

app.use(router)
// app.use(BootstrapVue)

app.mount('#app')
