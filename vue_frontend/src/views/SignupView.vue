<template>
    <div class="max-w-7xl mx-auto">
        <div class="main-right max-w-3xl mx-auto">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Sign Up</h1>
                <form class="space-y-6 mx-auto" v-on:submit.prevent="submitForm">
                    <div>
                        <label>Name</label><br>
                        <input type="text" v-model="form.name" placeholder="Your nickname" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Password</label>
                        <input type="password" v-model="form.password1" placeholder="Your password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Repeat password</label>
                        <input type="password" v-model="form.password2"  placeholder="Repeat your password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <!-- To Show the errors in this.errors list -->
                    <template v-if = "errors.length > 0" >
                        <div class="bg-red-500 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error" > {{ error }}</p>
                        </div>
                    </template>

                    <div class="w-auto flex justify-center">
                        <button class="mx-auto py-4 px-8 bg-purple-600 text-white rounded-lg">Sign up</button>
                    </div>

                    <p class="font-bold text-center">
                        Already have an account? <RouterLink :to="{'name': 'login'}" class="underline">Click here</RouterLink> to Log in! <!-- to="/login" -->
                    </p>

                </form>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios'

import { useToastStore } from '@/stores/toast'

export default {
    setup() {
        const toastStore = useToastStore()

        return {
            toastStore
        }
    },

    data() {
        return {
            form: {
                email: '',
                name: '',
                password1: '',
                password2: '',
            },
            errors: [],
        }
    },

    methods: {
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your email is missing')
            }

            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }

            if (this.form.password1 === '') {
                this.errors.push('Your password is missing')
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('The passwords does not match!')
            }

            if (this.errors.length === 0) {
                axios
                    .post('api/signup/', this.form)
                    .then(response => {
                        if (response.data.message === 'user created successfully') {
                            this.toastStore.showToast(5000, 'The user is registered. Please log in', 'bg-emerald-500')

                            this.form.email = ''
                            this.form.name = ''
                            this.form.password1 = ''
                            this.form.password2 = ''
                        } else {
                            this.toastStore.showToast(5000, 'Something went wrong, please try again', 'bg-red-300')
                        }
                        // console.log('User created successfully', response.data);
                        this.successMessage = response.data.message;
                    })
                    .catch(error => {
                        // console.log('error', error)
                        if (error.response && error.response.data) {
                            console.error('Error creating user', error.response.data.errors);
                            this.errors = error.response.data.errors
                        } else {
                            console.error('Unexpected error', error)
                        }
                    })
            }
        }
    }
}
</script>