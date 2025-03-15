<script setup>
// For testing decryption of messages
import { ref } from "vue";
import { decryptMsg } from "../utils/encryption";
import { fetchMessage } from "../utils/messages";

const msg_id = ref("");
const password = ref("");
const decrypted = ref(null);

const decrypt = async () => {
  const message = await fetchMessage(msg_id.value);
  if (message) {
    const { ciphertext, iv, salt } = message;
    decrypted.value =
      (await decryptMsg(ciphertext, iv, salt, password.value)) ||
      "Decryption failed";
  } else {
    decrypted.value = "Message not found";
  }
};
</script>

<template>
  <div class="reader-container">
    <input class="text-input" v-model="msg_id" placeholder="Enter msg_id" />
    <input
      class="text-input"
      type="password"
      v-model="password"
      placeholder="Enter password"
    />
    <button class="button" @click="decrypt">Decrypt</button>
    <pre>{{ decrypted }}</pre>
  </div>
</template>

<style scoped>
.reader-container {
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
