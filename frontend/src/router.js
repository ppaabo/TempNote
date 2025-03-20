import { createWebHistory, createRouter } from "vue-router";

import MessageComposer from "./components/MessageComposer.vue";
import MessageReader from "./components/MessageReader.vue";

const routes = [
  { path: "/", name: "write", component: MessageComposer },
  { path: "/read", name: "read", component: MessageReader },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
