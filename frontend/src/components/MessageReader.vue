<script setup>
import { ref, onMounted } from "vue";
import { decryptMsg } from "../utils/encryption";
import { fetchMessage, consumeMessage } from "../utils/messages";
import { useNotificationStore } from "../stores/notificationStore";
import { handleError, ErrorTypes } from "../utils/errorHandler";

const props = defineProps({
  id: String,
});
const message = ref(null);
const password = ref("");
const decrypted = ref(null);
const isLoading = ref(false);
const notificationStore = useNotificationStore();

// Retrieve the message when component is mounted
onMounted(async () => {
  if (!props.id) {
    notificationStore.add({
      message: "No message ID provided",
      type: "warning",
    });
    return;
  }
  isLoading.value = true;

  try {
    message.value = await fetchMessage(props.id);
    notificationStore.add({
      message: "Message retrieved successfully",
      type: "success",
    });
  } catch (error) {
    handleError(error, notificationStore, "MessageReader.onMounted", true);
  } finally {
    isLoading.value = false;
  }
});
/**
 * Decrypts the message and displays the contents. Sends a request to delete the message
 * from API if decryption is succesful
 */
const readMessage = async () => {
  isLoading.value = true;
  try {
    const { ciphertext, iv, salt } = message.value;
    const decryptedMessage = await decryptMsg(
      ciphertext,
      iv,
      salt,
      password.value
    );
    decrypted.value = decryptedMessage;
    notificationStore.add({
      message: "Message decrypted successfully",
      type: "success",
    });
    try {
      await consumeMessage(props.id);
      notificationStore.add({
        message: "Message has been destroyed",
        type: "info",
      });
    } catch (consumeError) {
      handleError(
        consumeError,
        notificationStore,
        "MessageReader.consumeMessage",
        true
      );
    }
  } catch (error) {
    handleError(error, notificationStore, "MessageReader.decrypt");
    if (error.type === ErrorTypes.PASSWORD_ERROR) {
      password.value = "";
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="reader-container">
    <h3>Enter password to decrypt message</h3>
    <p class="info-text">
      Once a message is decrypted, it will be automatically destroyed.
    </p>
    <div v-if="isLoading" class="loading">Decrypting...</div>
    <template v-if="!decrypted">
      <input
        class="text-input"
        type="password"
        v-model="password"
        placeholder="Password"
        :disabled="isLoading || !message"
        @keyup.enter="decrypt"
      />
      <button
        class="button"
        @click="readMessage"
        :disabled="isLoading || !message"
      >
        Decrypt
      </button>
    </template>

    <pre v-if="decrypted" class="decrypted-content">{{ decrypted }}</pre>
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

.loading {
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  margin: 10px 0;
}

.decrypted-content {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 16px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-word;
  margin-top: 16px;
}
</style>
