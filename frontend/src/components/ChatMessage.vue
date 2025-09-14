<template>
  <div :class="['chat-message', { 'user-message': isUser }]">
    <div class="avatar">
      {{ isUser ? 'U' : 'A' }}
    </div>
    <div class="message-content">
      <div class="message-text">{{ message.content }}</div>
      <div class="message-time">{{ formattedTime }}</div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'

interface Message {
  content: string
  timestamp: Date
  isUser: boolean
}

export default defineComponent({
  name: 'ChatMessage',
  props: {
    message: {
      type: Object as () => Message,
      required: true
    },
    isUser: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const formattedTime = computed(() => {
      return new Date(props.message.timestamp).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
      })
    })

    return {
      formattedTime
    }
  }
})
</script>

<style scoped>
.chat-message {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  margin: 0.5rem;
  border-radius: 0.5rem;
}

.user-message {
  background-color: #f1f5f9;
}

.avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background-color: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.message-content {
  flex: 1;
}

.message-text {
  margin-bottom: 0.25rem;
}

.message-time {
  font-size: 0.75rem;
  color: var(--secondary);
}
</style>