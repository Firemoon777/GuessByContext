import { createRouter, createWebHashHistory } from 'vue-router'
import PlaygroundView from "../views/PlaygroundView.vue";
import ListView from "../views/ListView.vue";
import CloseWordsView from "../views/CloseWordsView.vue";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/:id',
      name: 'home2',
      component: PlaygroundView,
      props: true
    },
    {
      path: '/',
      name: 'home',
      component: PlaygroundView,
    },
    {
      path: '/list',
      name: 'list',
      component: ListView,
    },
    {
      path: '/:id/words',
      name: 'close_words',
      component: CloseWordsView,
      props: true
    }
  ]
})

export default router
