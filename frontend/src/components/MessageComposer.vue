<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { sendMessage } from "../utils/messages";
import { encryptMsg } from "../utils/encryption";
import { useNotificationStore } from "../stores/notificationStore";
import { handleError } from "../utils/errorHandler";

const notificationStore = useNotificationStore();
const router = useRouter();
const message = ref("");
const password = ref("");
const expirationDays = ref(3);
const isLoading = ref(false);

/**
 * Encrypts the message and sends it to the API.
 */
const encrypt = async () => {
  isLoading.value = true;
  try {
    const encryptedMsg = await encryptMsg(message.value, password.value);
    encryptedMsg.expiration_days = expirationDays.value;
    const response = await sendMessage(encryptedMsg);
    notificationStore.add({
      message: "Message encrypted and saved succesfully",
      type: "success",
    });
    router.push({ name: "save", params: { id: response.msg_id } });
  } catch (error) {
    handleError(error, notificationStore, "MessageComposer.encrypt");
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="composer-container">
    <h3>Write a temporary message</h3>
    <p class="info-text">
      This message will be encrypted and can only be read once by someone with
      the password.
    </p>

    <textarea
      class="message-input"
      v-model="message"
      placeholder="Enter your message"
      :disabled="isLoading"
    ></textarea>

    <input
      class="text-input"
      type="password"
      v-model="password"
      placeholder="Enter a secure password"
      :disabled="isLoading"
    />

    <div class="expiration-container">
      <label for="expiration">Message expires after:</label>
      <select
        id="expiration"
        v-model.number="expirationDays"
        :disabled="isLoading"
      >
        <option v-for="day in [3, 5, 7, 14]" :key="day" :value="day">
          {{ day }} days
        </option>
      </select>
    </div>

    <button class="button" @click="encrypt" :disabled="isLoading">
      <span v-if="isLoading">Encrypting...</span>
      <span v-else>Encrypt & Save</span>
    </button>
  </div>
</template>
<style scoped>
.composer-container {
  display: flex;
  flex-direction: column;
  max-width: 600px;
  margin: 0 auto;
}

.info-text {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.87);
  margin-bottom: 16px;
}

.message-input {
  width: 100%;
  min-height: 150px;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.87);
  font-family: inherit;
  resize: vertical;
}

input,
select {
  width: 100%;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.87);
}

.expiration-container {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.expiration-container label {
  margin-right: 10px;
  flex-shrink: 0;
}

.expiration-container select {
  margin-bottom: 0;
  width: auto;
  flex-grow: 1;
}

button {
  padding: 12px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

button:hover:not(:disabled) {
  background-color: #3e8e41;
}

button:disabled {
  background-color: #525252;
  cursor: not-allowed;
  opacity: 0.7;
}
</style>
<!-- <style scoped>
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
select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}
</style> -->
