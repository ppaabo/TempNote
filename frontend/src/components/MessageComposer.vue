<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { sendMessage } from "../utils/messages";
import { encryptMsg } from "../utils/encryption";

const router = useRouter();
const message = ref("");
const password = ref("");
const encrypt = async () => {
  const encryptedMsg = await encryptMsg(message.value, password.value);
  const response = await sendMessage(encryptedMsg);
  if (response) {
    router.push({ name: "save", params: { id: response.msg_id } });
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
