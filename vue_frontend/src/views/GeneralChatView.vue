<template>
<div>
    <h1 class="text-center font-bold text-3xl mb-10">General Chatroom</h1>
    <div class="max-w-screen mx-auto grid grid-cols-5 gap-5">
        <div class="main-left col-span-4">
            <div ref="chatContainer" class="chat-container w-full min-h-96 max-h-96 overflow-y-auto mb-3 p-2 bg-gray-300 rounded-xl">
                <div v-for="message in messages" :key="message.sender" class="flex flex-col">
                    <div v-if="message.sender === 'System' || message.sender === 'Very sad System'">
                        <p><strong>{{ message.sender }}:</strong> {{ message.body }}</p>
                    </div>
                    
                    <div v-else-if="message.sender === user.name" class="bg-emerald-300 p-5 w-2/4 rounded-xl my-2 self-end">
                        <p><strong>{{ message.sender }}:</strong></p>
                        <p class="text-xs"><i> {{ message.created_at_formatted }} ago</i></p>
                        <p class="mt-2"> {{ message.body }}</p>
                    </div>

                    <div v-else class="bg-sky-300 p-5 w-2/4 rounded-xl my-2">
                        <p><strong>{{ message.sender }}:</strong></p>
                        <p class="text-xs"><i> {{ message.created_at_formatted }} ago</i></p>
                        <p> {{ message.body }}</p>
                    </div>

                </div>
            </div>

            <form @submit.prevent="sendMessage" class=" w-full flex justify-center">
                <input
                    type="text"
                    v-model="newMessage"
                    placeholder="Enter your message"
                    class="chat-input p-2 w-4/5 mr-4 rounded-xl self-center"
                >
                <button type="submit" class="send-btn inline-block px-6 h-10 bg-emerald-400 text-white rounded-lg self-center">Send</button>
            </form>
        </div>

        <div class="main-left col-span-1 bg-gray-950 rounded-xl min-h-96 max-h-96 overflow-y-auto flex flex-col">
            <h1 class="m-4 mb-1 font-bold text-lg text-white self-center">Online:</h1>
            
            <div v-for="name in userList" :key="name" class="self-start w-full py-1 my-1 bg-slate-900 rounded-lg">
                <p class="font-semibold mx-4 mb-1 overflow-hidden text-xs text-white" >{{ name }}</p>  
            </div>
            

        </div>
    </div>
</div>
</template>

<script>
import { io } from "socket.io-client";
import { useUserStore } from '@/stores/user';
import axios from 'axios';

export default {
    setup() {
      const userStore = useUserStore()
      
      return {
        userStore
      }
    },
    data() {
        return {
            newMessage: "",
            messages: [],
            socket: null,
            user: null,
            userList: [],
            interval: null,
        };
    },
    created() {
        // connects to backend
        this.socket = io("http://127.0.0.1:8000");

        this.getAuthenticatedUser();

        // handle connection
        this.socket.on('connect', () => {
            console.log('Connected to the chat');
            this.socket.emit('join_room', { room: 'General', user_id: this.user.id, user_name: this.user.name });
        });

        // handle disconnection
        this.socket.on('disconnect', () => {
            console.log('Disconnected from the chat');
            this.socket.emit('leave_room', {room: 'General', user_id: this.user.id, user_name: this.user.name});
        });

        // Listen for incoming messages
        this.socket.on("chat_message", (msg) => {
            console.log("Message received from server", msg)
            this.messages.push(msg);

            this.$nextTick(() => {  // ensures that DOM updates are completed before executing
                const chatContainer = this.$refs.chatContainer;
                chatContainer.scrollTop = chatContainer.scrollHeight;   // Sets scroll position of container to it's max scroll height (to the bottom)
            })
        });
        
        // Listen for userList updates
        this.socket.on('user_list', (users) => {
            this.userList = users
        })
    },
    mounted() {
        this.interval = setInterval(this.updateTimePassed, 1000);
    },
    beforeDestroy() {
        clearInterval(this.interval);
    },
    methods : {
        getAuthenticatedUser() {
            this.user = this.userStore.user
            console.log("current user:", this.user)
        },

        sendMessage() {
            if (this.newMessage.trim() !== '' && this.user) {
                
                this.socket.emit('send_public_message', {
                    message: this.newMessage,
                    // sender: this.user.name,
                    user_id: this.user.id
                });

                this.newMessage = '';
            }
        },

        formatTimePassed(created_at) {
            const now = new Date();
            const timeDiff = Math.floor((now - new Date(created_at)) / 1000)

            if (timeDiff < 60) {
                return `${timeDiff} seconds` // Seconds
            } else if (timeDiff < 3600) {
                return `${Math.floor(timeDiff / 60)} min`  // minutes
            } else if (timeDiff < 86400) {
                return `${Math.floor(timeDiff / 3600)} hours`  // hours
            } else {
                return `${Math.floor(timeDiff / 3600)} days`  // days
            }
        },

        updateTimePassed() {
            this.messages.forEach(message => {
                message.created_at_formatted = this.formatTimePassed(message.created_at)
            })
        },
    },
    beforeUnmount() {
        this.socket.emit('leave_room', {room: 'General', user_id: this.user.id, user_name: this.user.name}); // Time diff in seconds
    },
}

</script>