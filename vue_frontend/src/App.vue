<template>
    <div class="main-div">
        <nav class="py-10 px-8 border-b border-gray-200">
            <div class="max-w-7xl mx-auto">
                <div class="flex items-center justify-between">
                    <div class="menu-left flex justify-center">
                        <img src="./assets/logo-r3.png" class="max-w-20 self-center">
                        <RouterLink to="/" class="text-xl self-center">R3 Messenger</RouterLink>
                    </div>

                    <div class="menu-center flex space-x-12" v-if="userStore.user.isAuthenticated" >
                        <RouterLink to="/" class="text-purple-700">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                            </svg>
                        </RouterLink>

                        <RouterLink to="/chat/general">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 9.75a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 01.778-.332 48.294 48.294 0 005.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z"></path>
                            </svg>                              
                        </RouterLink>

                        <RouterLink to="/search">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                            </svg>                                                         
                        </RouterLink>
                    </div>

                    <div class="menu-right">
                        <template v-if="userStore.user.isAuthenticated">
                            <RouterLink :to="{name: 'profile', params: {'id': userStore.user.id} }">
                                <img src="./assets/surprised_pikachu.png" class="rounded-full max-w-20 maw-h-20">
                            </RouterLink>
                        </template>

                        <template v-else>
                            <RouterLink to="/login" class=" mr-4 py-4 px-6 bg-gray-600 text-white rounded-lg">Log In</RouterLink>
                            <RouterLink to="/signup" class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign Up</RouterLink>
                        </template>
                    </div>
                </div>
            </div>
        </nav>
        
        <main class="px-8 py-6 bg-gray-100">
            <RouterView />
        </main>
        
        <Toast />
    </div>
</template>

<script>
import axios from 'axios'
import Toast from '@/components/Toast.vue'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
      const userStore = useUserStore()
      
      return {
        userStore
      }
    },
    components: {
        Toast
    },

    mounted() {     // Use mounted() instead of beforeCreate(). Now profile menu element loads bc mounted() runs after components fully created and inserted into DOM
        this.userStore.initStore()

        const token = this.userStore.user.access

        if (token) {
           axios.defaults.headers.common["Authorization"] = "Bearer " + token; 
        } else {
            axios.defaults.headers.common["Authorization"] = "";
        }
    }
}
</script>