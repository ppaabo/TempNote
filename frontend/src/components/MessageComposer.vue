<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { sendMessage } from "../utils/messages";
import { encryptMsg } from "../utils/encryption";

const router = useRouter();
const message = ref("");
const password = ref("");
const expirationDays = ref(3);

const encrypt = async () => {
  const encryptedMsg = await encryptMsg(message.value, password.value);
  encryptedMsg.expiration_days = expirationDays.value;
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
    <select v-model.number="expirationDays">
      <option v-for="day in [3, 5, 7, 14]" :key="day" :value="day">
        {{ day }} days
      </option>
    </select>
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
select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}
</style>
