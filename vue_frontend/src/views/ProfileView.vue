<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <!-- left -->
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img src="../assets/surprised_pikachu.png" class="mb-6 rounded-full">
                
                <p><strong>{{ user?.name }}</strong></p>

                

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{name: 'friends', params: {id: user.id} }" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink>
                    <p class="text-xs text-gray-500">120 posts</p>
                </div>

                <div class="mt-6">      <!-- v-if Won't show the send friend request button if profile is yours -->
                    <button
                        v-if="userStore.user.id !== user.id"
                        class="inline-block py-4 px-3 bg-purple-600 
                        text-white text-xs rounded-lg"
                        @click="sendFriendshipRequest">Send friend request</button>

                    <button
                        v-if="userStore.user.id === user.id"
                        class="inline-block py-4 px-3 bg-red-600 
                        text-white text-xs rounded-lg"
                        @click="logout">Log out</button>
                </div>
            </div>
        </div>

        <!-- center -->
        <div class="main-center col-span-3 space-y-4">
            <div 
                v-if="userStore.user.id === user.id"
                class="bg-white border border-gray-200 rounded-lg"
            >
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>

                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>
                </form>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post" @post-deleted="handlePostDelete" />  
            </div>
        </div>

        <!-- right -->
        <!-- <div class="main-right col-span-1 space-y-4">
            
        </div> -->

    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import FeedItem from "../components/FeedItem.vue"
import { useToastStore } from '@/stores/toast'

export default {
    name: 'ProfileView',

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()
      
        return {
            userStore,
            toastStore
        }
    },

    components: {
        FeedItem,
    },

    data() {
        return {
            user: {},
            posts: [],
            body: '',
        }
    },

    mounted() {
        this.getFeed()
    },

    watch: {
        "$route.params.id": {   // originally had userId, replaced with .id and works
            handler() {
                this.getFeed();
            },
            immediate: true
        }
    },

    // beforeRouteUpdate(to, from, next) { ==> Did not work
    //     if (from.name === to.name) {
    //         this.getFeed();
    //     }
    // },

    // updated() {
    //     // this.getFeed()
    // },

    methods: {
        sendFriendshipRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`)
                .then(response => {
                    console.log('data_sendfriendshiprequest', response.data)

                    this.user = response.data.user
                    if (response.data.message === 'request already sent') {
                        this.toastStore.showToast(5000, 'Request already sent', 'bg-red-300')
                    } else {
                        this.toastStore.showToast(5000, 'Request was sent successfuly', 'bg-emerald-300')
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}`)     // gets from the endpoint set in post.urls
                .then(response => {
                    console.log('datagetFeed', response.data)

                    this.posts = response.data.posts
                    this.user = response.data.user

                    console.log("data2", this.posts)
                })
                .catch(error => {
                    console.log('error', error)
                })
                
        },

        submitForm() {
            console.log('submitForm', this.body)

            axios
                .post("/api/posts/create/", {
                    "body": this.body
                })
                .then(response => {
                    console.log('datasubmitForm', response.data)

                    this.posts.unshift(response.data)   // Use unshift and not push to add to beginning of array
                    this.body = ''
                })
                .catch(error => {
                    console.log("error", error)
                })
        },

        logout() {
            console.log('Logging out...')

            this.userStore.removeToken()

            this.$router.push('/login')     // Send to login page
        },

        handlePostDelete(id) {
            this.posts = this.posts.filter(post => post.id !== id)
        },
    }
}
</script>