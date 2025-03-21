<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
const url = ref("");

const props = defineProps({
  id: String,
});

onMounted(() => {
  if (props.id) {
    url.value = `http://localhost:5173/read/${props.id}`;
  }
});

const copyToClipboard = () => {
  try {
    navigator.clipboard.writeText(url.value);
    const notif = document.getElementById("notification");
    notif.className = "show";

    setTimeout(() => {
      notif.className = notif.className.replace("show", "");
    }, 3000);
  } catch (error) {
    console.error("Failed to copy: ", error);
  }
};

const writeNew = () => {
  router.push({ name: "write" });
};
</script>

<template>
  <div class="saved-container">
    <p>
      Your message has been created! <br />
      Copy the URL from below and send it to the recipient
    </p>
    <input class="text-input" v-model="url" readonly />
    <button class="button" @click="copyToClipboard">Copy URL</button>
    <button class="button" @click="writeNew">Write a new message</button>
  </div>
  <div id="notification">URL copied to clipboard</div>
</template>

<style scoped>
.saved-container {
  display: flex;
  flex-direction: column;
}

input {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}

button {
  padding: 12px 20px;
  margin: 8px 0;
  cursor: pointer;
}

#notification {
  visibility: hidden;
  min-width: 250px;
  margin-left: -125px;
  background-color: #3f5eab;
  color: #fff;
  text-align: center;
  border-radius: 2px;
  padding: 16px;
  position: fixed;
  z-index: 1;
  left: 50%;
  bottom: 25%;
  font-size: 17px;
}

#notification.show {
  visibility: visible;
  -webkit-animation: fadein 0.5s, fadeout 0.5s 2.5s;
  animation: fadein 0.5s, fadeout 0.5s 2.5s;
}

@-webkit-keyframes fadein {
  from {
    bottom: 0;
    opacity: 0;
  }
  to {
    bottom: 25%;
    opacity: 1;
  }
}

@keyframes fadein {
  from {
    bottom: 0;
    opacity: 0;
  }
  to {
    bottom: 25%;
    opacity: 1;
  }
}

@-webkit-keyframes fadeout {
  from {
    bottom: 25%;
    opacity: 1;
  }
  to {
    bottom: 0;
    opacity: 0;
  }
}

@keyframes fadeout {
  from {
    bottom: 25%;
    opacity: 1;
  }
  to {
    bottom: 0;
    opacity: 0;
  }
}
</style>
