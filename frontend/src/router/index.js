import { createRouter, createWebHistory } from 'vue-router'
import PlaygroundView from "../views/PlaygroundView.vue";
import ListView from "../views/ListView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
    }
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
  ]
})

export default router
