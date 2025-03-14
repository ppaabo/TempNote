<script setup>
// For testing decryption of messages
import { ref } from "vue";
import { useCrypto } from "../composables/useCrypto.js";

const { decryptMsg } = useCrypto();

const ciphertext = ref("");
const password = ref("");
const iv = ref("");
const salt = ref("");
const decrypted = ref(null);

const decrypt = async () => {
  decrypted.value = await decryptMsg(
    ciphertext.value,
    iv.value,
    salt.value,
    password.value
  );
};
</script>

<template>
  <div class="reader-container">
    <input class="text-input" v-model="ciphertext" placeholder="Enter cipher" />
    <input class="text-input" v-model="iv" placeholder="Enter iv" />
    <input class="text-input" v-model="salt" placeholder="Enter salt" />
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
