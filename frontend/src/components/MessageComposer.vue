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
const expirationHours = ref(24);
const isLoading = ref(false);

const expirationOptions = [
  { value: 1, label: "1 hour" },
  { value: 3, label: "3 hours" },
  { value: 6, label: "6 hours" },
  { value: 12, label: "12 hours" },
  { value: 24, label: "1 day" },
  { value: 72, label: "3 days" },
  { value: 168, label: "7 days" },
  { value: 336, label: "14 days" },
];

/**
 * Encrypts the message and sends it to the API.
 */
const encrypt = async () => {
  isLoading.value = true;
  try {
    const encryptedMsg = await encryptMsg(message.value, password.value);
    encryptedMsg.expiration_hours = expirationHours.value;
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
        v-model.number="expirationHours"
        :disabled="isLoading"
      >
        <option
          v-for="option in expirationOptions"
          :key="option.value"
          :value="option.value"
        >
          {{ option.label }}
        </option>
      </select>
    </div>

    <button class="btn btn-primary" @click="encrypt" :disabled="isLoading">
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
</style>
