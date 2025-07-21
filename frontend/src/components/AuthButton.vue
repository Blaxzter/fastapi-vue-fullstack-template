<template>
  <div class="auth-button">
    <button v-if="!isAuthenticated" @click="login" class="login-btn">Log In</button>
    <div v-else class="user-menu">
      <div class="user-info">
        <img
          v-if="user?.picture"
          :src="user.picture"
          :alt="user.name || user.email || 'User'"
          class="user-avatar"
        />
        <span class="user-name">{{ user?.name || user?.email || 'User' }}</span>
      </div>
      <button @click="logout" class="logout-btn">Log Out</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const { isAuthenticated, user, login, logout } = authStore
</script>

<style scoped>
.auth-button {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.login-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.login-btn:hover {
  background: #0056b3;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-weight: 500;
}

.logout-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.logout-btn:hover {
  background: #c82333;
}
</style>
