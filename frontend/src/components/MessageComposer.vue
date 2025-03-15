<script setup>
import { ref } from "vue";
import { sendMessage } from "../utils/messages";
import { encryptMsg } from "../utils/encryption";

const message = ref("");
const password = ref("");
const encrypted = ref(null);

const encrypt = async () => {
  const encryptedMsg = await encryptMsg(message.value, password.value);
  const response = await sendMessage(encryptedMsg);
  if (response) {
    encrypted.value = response;
  } else {
    console.error("Sending message failed");
  }
};
</script>

<template>
  <div class="composer-container">
    <input class="text-input" v-model="message" placeholder="Enter message" />
    <input
      class="text-input"
      type="password"
      v-model="password"
      placeholder="Enter password"
    />
    <button class="button" @click="encrypt">Encrypt</button>
    <pre>{{ encrypted }}</pre>
  </div>
</template>

<style scoped>
.composer-container {
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
