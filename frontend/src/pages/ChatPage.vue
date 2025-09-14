<template>
  <div class="chat-page">
    <Sidebar />
    <div class="chat-container">
      <div class="chat-messages" ref="messagesContainer">
        <ChatMessage
          v-for="(message, index) in messages"
          :key="index"
          :message="message"
          :is-user="message.isUser"
        />
      </div>
      <ChatInput @send="sendMessage" />
    </div>
    <ToolPanel :tools="availableTools" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, nextTick } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import ChatMessage from '../components/ChatMessage.vue'
import ChatInput from '../components/ChatInput.vue'
import ToolPanel from '../components/ToolPanel.vue'

interface Message {
  content: string
  timestamp: Date
  isUser: boolean
}

export default defineComponent({
  name: 'ChatPage',
  components: {
    Sidebar,
    ChatMessage,
    ChatInput,
    ToolPanel
  },
  setup() {
    const messages = ref<Message[]>([])
    const messagesContainer = ref<HTMLElement | null>(null)

    const availableTools = [
      {
        name: 'Web Search',
        description: 'Search the web using DuckDuckGo'
      },
      {
        name: 'Code Generation',
        description: 'Generate code using AI models'
      }
    ]

    const scrollToBottom = async () => {
      await nextTick()
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    const sendMessage = async (content: string) => {
      // Add user message
      messages.value.push({
        content,
        timestamp: new Date(),
        isUser: true
      })

      await scrollToBottom()

      // TODO: Implement actual message sending logic
      // For now, just add a mock response
      setTimeout(() => {
        messages.value.push({
          content: 'This is a mock response from the AI',
          timestamp: new Date(),
          isUser: false
        })
        scrollToBottom()
      }, 1000)
    }

    return {
      messages,
      messagesContainer,
      availableTools,
      sendMessage
    }
  }
})
</script>

<style scoped>
.chat-page {
  display: flex;
  height: 100%;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}
</style>