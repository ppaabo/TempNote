<script setup>
import { defineProps, defineEmits, onMounted, ref } from "vue";

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  message: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    default: "info", // 'info', 'success', 'warning', 'error'
  },
  timeout: {
    type: Number,
    default: 5000,
  },
});

const emit = defineEmits(["close"]);
const isVisible = ref(false);

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true;
  }, 10);

  // Auto-dismiss if timeout is positive
  if (props.timeout > 0) {
    setTimeout(() => {
      close();
    }, props.timeout);
  }
});

const close = () => {
  isVisible.value = false;
  setTimeout(() => {
    emit("close", props.id);
  }, 300);
};
</script>

<template>
  <div
    class="notification"
    :class="[`notification-${type}`, { 'notification-visible': isVisible }]"
  >
    <div class="notification-content">{{ message }}</div>
    <button class="notification-close" @click="close">&times;</button>
  </div>
</template>

<style scoped>
.notification {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 10px;
  border-radius: 4px;
  background-color: #3a3a3a;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transform: translateX(100%);
  opacity: 0;
  transition: transform 0.3s ease, opacity 0.3s ease;
  max-width: 100%;
}

.notification-visible {
  transform: translateX(0);
  opacity: 1;
}

.notification-content {
  flex: 1;
}

.notification-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  margin-left: 12px;
}

/* Type-specific styles */
.notification-info {
  border-left: 4px solid #2196f3;
}

.notification-success {
  border-left: 4px solid #4caf50;
}

.notification-warning {
  border-left: 4px solid #ff9800;
}

.notification-error {
  border-left: 4px solid #f44336;
}
</style>
