<template>
    <div class="main-div">
        <div class="mb-2 flex items-center justify-between">
            <div class="flex items-center space-x-6">
                <img src="../assets/surprised_pikachu.png" class="w-[40px] rounded-full">
                
                <p>
                    <strong>
                        <RouterLink :to="{name: 'profile', params: {'id': comment.created_by.id} }">{{ comment.created_by.name }}</RouterLink>
                    </strong>
                </p>
            </div>

            <p class="text-gray-600">{{ comment.created_at_formatted }} ago</p>
        </div>

        <p>{{ comment.body }} </p>
    </div>
    
</template>

<script>
import { RouterLink } from 'vue-router'

export default {
    props: {
        comment: Object
    },
    components: { RouterLink }

}
</script>