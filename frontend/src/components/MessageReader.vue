<script setup>
import { ref, onMounted } from "vue";
import { decryptMsg } from "../utils/encryption";
import { fetchMessage, consumeMessage } from "../utils/messages";
import { useNotificationStore } from "../stores/notificationStore";

const props = defineProps({
  id: String,
});

const message = ref(null);
const password = ref("");
const decrypted = ref(null);
const notificationStore = useNotificationStore();
onMounted(async () => {
  if (props.id) {
    message.value = await fetchMessage(props.id);
    if (!message.value) {
      decrypted.value = "Message not found";
    } else {
      console.log("Message fetched", message.value);
      notificationStore.add({ message: "Message retrieved", type: "success" });
    }
  }
});

const decrypt = async () => {
  if (message.value && password.value) {
    const { ciphertext, iv, salt } = message.value;
    const decryptedMessage = await decryptMsg(
      ciphertext,
      iv,
      salt,
      password.value
    );
    if (decryptedMessage) {
      decrypted.value = decryptedMessage;
      consumeMessage(props.id);
    } else {
      decrypted.value = "Decryption failed!";
    }
  }
};
</script>

<template>
  <div class="reader-container">
    <h3>Enter password to decrypt message</h3>
    <p class="info-text">
      Once a message is decrypted, it will be automatically destroyed.
    </p>
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

.info-text {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.87);
  margin-bottom: 8px;
}
</style>
