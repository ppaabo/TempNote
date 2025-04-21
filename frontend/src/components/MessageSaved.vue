<script setup>
import { ref, onMounted } from "vue";
import { useNotificationStore } from "../stores/notificationStore";
import RouterButton from "./RouterButton.vue";
const notificationStore = useNotificationStore();
const url = ref("");

const props = defineProps({
  id: String,
});

onMounted(() => {
  if (props.id) {
    url.value = `http://localhost:5173/read/${props.id}`;
  }
});

const copyToClipboard = () => {
  try {
    navigator.clipboard.writeText(url.value);
    notificationStore.add({ message: "URL copied to clipboard" });
  } catch (error) {
    console.error("Failed to copy: ", error);
    notificationStore.add({
      message: "Failed to copy URL to clipboard",
      type: "error",
    });
  }
};
</script>

<template>
  <div class="saved-container">
    <p>
      Your message has been created! <br />
      Copy the URL from below and send it to the recipient
    </p>
    <input class="text-input" v-model="url" readonly />
    <button class="btn btn-primary" @click="copyToClipboard">Copy URL</button>
    <RouterButton to="write" text="Write a new message" />
  </div>
</template>

<style scoped>
.saved-container {
  display: flex;
  flex-direction: column;
}

input {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}
</style>
