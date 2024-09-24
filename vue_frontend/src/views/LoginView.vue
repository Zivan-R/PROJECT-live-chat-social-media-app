<template>
    <div class="max-w-7xl mx-auto">
        <div class="main-right max-w-3xl mx-auto">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Log in</h1>
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Password</label>
                        <input type="password" v-model="form.password" placeholder="Your password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <template v-if = "errors.length > 0" >
                        <div class="bg-red-500 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error" > {{ error }}</p>
                        </div>
                    </template>

                    <div class="w-auto flex justify-center">
                        <button class="py-4 px-8 bg-purple-600 text-white rounded-lg">Log in</button>
                    </div>

                    <p class="font-bold text-center">
                        Don't have an account yet? <RouterLink :to="{'name': 'signup'}" class="underline">Click here</RouterLink> to Sign up!
                    </p>

                </form>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
      const userStore = useUserStore()
      
      return {
        userStore
      }
    },

    data() {
        return {
            form: {
                email: "",
                password: "",
            },
            errors: []
        }
    },
    methods: {
        async submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your email is missing')
            }

            if (this.form.password === '') {
                this.errors.push('Your password is missing')
            }

            if (this.errors.length === 0) {
                await axios
                    .post('api/login/', this.form)
                    .then(response => {
                        this.userStore.setToken(response.data)  // utiliser .userStore et non .store

                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
                    })
                    .catch(error => {
                        console.log("from api/login error")
                        console.log('error', error)
                        // if (error.response && error.response.data) {
                        //     console.error('Error logging user in', error.response.data.errors);
                        //     this.errors = error.response.data.errors
                        // } else {
                        //     console.error('Unexpected error', error)
                        // }
                    })
                
                await axios
                    .get('/api/me/')
                    .then(response => {
                        this.userStore.setUserInfo(response.data)   // utiliser .userStore et non .store

                        this.$router.push('/')
                    })
                    .catch(error => {
                        console.log('from loginview script')
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>