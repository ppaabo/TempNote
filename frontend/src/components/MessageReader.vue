<script setup>
import { ref, onMounted } from "vue";
import { decryptMsg } from "../utils/encryption";
import { fetchMessage } from "../utils/messages";

const props = defineProps({
  id: String,
});

const message = ref(null);
const password = ref("");
const decrypted = ref(null);

onMounted(async () => {
  if (props.id) {
    message.value = await fetchMessage(props.id);
    console.log("Message fetched", message.value);
  }
});

const decrypt = async () => {
  if (message.value && password.value) {
    const { ciphertext, iv, salt } = message.value;
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
    <h3>Enter password to decrypt message</h3>
    <input
      class="text-input"
      type="password"
      v-model="password"
      placeholder="Password"
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
