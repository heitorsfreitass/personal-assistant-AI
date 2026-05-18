<script setup>

import { onMounted } from 'vue'

const message = ref("")
const messages = ref([])

async function loadMessages() {
    const response = await $fetch("http://localhost:8000/messages")
    console.log(response)
    messages.value = response
}

onMounted(() => {
    loadMessages()
})

async function sendMessage() {
    if (!message.value) return

    messages.value.push({
        role: "user",
        content: message.value
    })

    const userMessage = message.value
    message.value = ""

    const response = await $fetch("http://localhost:8000/chat", {
        method: "POST",
        body: {
            message: userMessage
        }
    })

    messages.value.push({
        role: "assistant",
        content: response.reply
    })
}

</script>

<template>
    <div class="min-h-screen bg-zinc-900 text-white p-6">
        <h1 class="text-4xl font-bold mb-6 text-center">Assitente Pessoal de IA</h1>
        <div class="chat">
            <div class="message" :class="msg.role === 'user' ? 'bg-blue-600 ml-auto max-w-[70%]' : 'bg-zinc-800 max-w-[70%]'" v-for="msg in messages" :key="msg.id">
                <strong>{{  msg.role }}</strong>
                <p>{{ msg.content }}</p>
            </div>

            <div class="flex gap-2 mt-4">
                <input 
                    v-model="message" 
                    @keyup.enter="sendMessage" 
                    placeholder="Digite uma mensagem..."
                    class="
                        flex-1
                        bg-zinc-800
                        text-white
                        px-4
                        py-3
                        rounded-xl
                        outline-none
                        border
                        border-zinc-700
                        focus:border-blue-500
                    "
                >

                <button 
                    @click="sendMessage"
                    class="
                        bg-blue-600
                        hover>bg-blue-700
                        transition
                        px-5
                        py-3
                        rounded-xl
                        font-medium
                    "
                >
                    Enviar
                </button>
            </div>


            
        </div>
    </div>
    
</template>

<style scoped>
.chat {
    max-width: 700px;
    margin: 0 auto;
    padding: 20px;
}

.message {
    margin-bottom: 16px;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
}

.input-area {
    display: flex;
    gap: 8px;
}

input {
    flex: 1;
}
</style>