<template>
  <div class="chat-input">
    <textarea
      v-model="message"
      @keydown.enter.prevent="sendMessage"
      placeholder="Type your message..."
      rows="1"
    ></textarea>
    <button @click="sendMessage" :disabled="!message.trim()">Send</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'ChatInput',
  emits: ['send'],
  setup(_, { emit }) {
    const message = ref('')

    const sendMessage = () => {
      const trimmedMessage = message.value.trim()
      if (trimmedMessage) {
        emit('send', trimmedMessage)
        message.value = ''
      }
    }

    return {
      message,
      sendMessage
    }
  }
})
</script>

<style scoped>
.chat-input {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
  background-color: #fff;
}

textarea {
  flex: 1;
  resize: none;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  outline: none;
}

button {
  padding: 0.5rem 1rem;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>