<script setup>

const message = ref("")
const messages = ref([])

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
    <div>
        <div v-for="msg in messages">
            {{  msg.role }}: {{ msg.content }}
        </div>

        <input v-model="message">

        <button @click="sendMessage">
            Send
        </button>
    </div>
</template>