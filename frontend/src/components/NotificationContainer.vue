<script setup>
import { useNotificationStore } from "../stores/notificationStore";
import Notification from "./Notification.vue";

const { notifications, remove } = useNotificationStore();
</script>

<template>
  <div class="notification-container">
    <transition-group name="notification-list">
      <Notification
        v-for="notification in notifications"
        :key="notification.id"
        :id="notification.id"
        :message="notification.message"
        :type="notification.type"
        :timeout="notification.timeout"
        @close="remove"
      />
    </transition-group>
  </div>
</template>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  width: 400px;
  max-width: calc(100vw - 40px);
}

.notification-list-enter-active,
.notification-list-leave-active {
  transition: all 0.3s ease;
}

.notification-list-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.notification-list-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style>
