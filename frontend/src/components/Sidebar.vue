<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1>Instantly</h1>
    </div>
    <nav class="sidebar-nav">
      <router-link to="/" class="nav-item">Home</router-link>
      <router-link to="/chat" class="nav-item">Chat</router-link>
    </nav>
  </aside>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Sidebar'
})
</script>

<style scoped>
.sidebar {
  width: 250px;
  height: 100%;
  background-color: white;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.sidebar-header h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary);
}

.sidebar-nav {
  padding: 1rem;
}

.nav-item {
  display: block;
  padding: 0.75rem 1rem;
  margin: 0.5rem 0;
  color: var(--text);
  text-decoration: none;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}

.nav-item:hover {
  background-color: #f1f5f9;
}

.nav-item.router-link-active {
  background-color: var(--primary);
  color: white;
}
</style>