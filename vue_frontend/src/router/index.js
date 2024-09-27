import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import FriendsView from '../views/FriendsView.vue'
import PostView from '../views/PostView.vue'
import GeneralChatView from '../views/GeneralChatView.vue'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/chat/general',
      name: 'general-chat',
      component: GeneralChatView,
      // meta: { requiresAuth: true }
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/profile/:id', // :id expects custom id => can see other people's profiles as well
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/profile/:id/friends', // :id expects custom id => can see other people's profiles as well
      name: 'friends',
      component: FriendsView
    },
    {
      path: '/:id', 
      name: 'postview',
      component: PostView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

// router.beforeEach((to, from, next) => {
//   const userStore = useUserStore();
//   const isAuthenticated = userStore.isAuthenticated;

//   if (to.meta.requiresAuth && !isAuthenticated) {
//     next({ name: 'login'});
//   } else {
//     next();
//   }
// });

export default router
