<template>
  <div class="home-page">
    <Sidebar />
    <main class="main-content">
      <div class="hero">
        <h1>Welcome to Instantly</h1>
        <p>Your AI-powered chat assistant with advanced tools and capabilities</p>
        <router-link to="/chat" class="cta-button">Start Chatting</router-link>
      </div>
      <div class="features">
        <div class="feature-card">
          <h2>Smart Search</h2>
          <p>Search the web and get relevant information instantly</p>
        </div>
        <div class="feature-card">
          <h2>Code Generation</h2>
          <p>Generate code snippets and get programming assistance</p>
        </div>
        <div class="feature-card">
          <h2>Tool Integration</h2>
          <p>Access various tools and APIs seamlessly</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Sidebar from '../components/Sidebar.vue'

export default defineComponent({
  name: 'HomePage',
  components: {
    Sidebar
  }
})
</script>

<style scoped>
.home-page {
  display: flex;
  height: 100%;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: var(--background);
}

.hero {
  text-align: center;
  margin-bottom: 4rem;
}

.hero h1 {
  font-size: 3rem;
  font-weight: bold;
  color: var(--primary);
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.25rem;
  color: var(--secondary);
  margin-bottom: 2rem;
}

.cta-button {
  display: inline-block;
  padding: 1rem 2rem;
  background-color: var(--primary);
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  font-weight: bold;
  transition: background-color 0.2s;
}

.cta-button:hover {
  background-color: #1d4ed8;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  padding: 2rem;
}

.feature-card {
  background-color: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

.feature-card h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: var(--primary);
}

.feature-card p {
  color: var(--secondary);
}
</style>