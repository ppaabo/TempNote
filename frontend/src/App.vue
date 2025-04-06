<script setup>
import { createNotificationStore } from "./stores/notificationStore";
import NotificationContainer from "./components/NotificationContainer.vue";

createNotificationStore();
</script>

<template>
  <div class="app-container">
    <RouterView />
    <NotificationContainer />
  </div>
</template>

<style scoped>
.app-container {
  width: 70vh;
  display: flex;
  flex-direction: column;
}
</style>
