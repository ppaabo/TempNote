import { ref, provide, inject } from "vue";

const NOTIFICATION_KEY = Symbol("notification");
export const createNotificationStore = () => {
  const notifications = ref([]);

  /**
   * Adds a new notification to the store.
   *
   * @param {Object} notification - The notification to add.
   * @param {string} [notification.message=""] - The message to display.
   * @param {string} [notification.type="info"] - The type of notification ("info", "success", "error", "warning").
   * @param {number} [notification.timeout=5000] - Duration in milliseconds before the notification is dismissed.
   * @returns {string} The unique ID of the created notification.
   */
  const addNotification = (notification) => {
    // Generate unique ID for the notification
    const id =
      Date.now().toString() + Math.random().toString(36).substring(2, 9);

    notifications.value.push({
      id,
      message: notification.message || "",
      type: notification.type || "info",
      timeout: notification.timeout !== undefined ? notification.timeout : 5000,
    });

    return id;
  };

  /**
   * Removes a notification from the store.
   *
   * @param {string} id - The ID of the notification to remove.
   */
  const removeNotification = (id) => {
    const index = notifications.value.findIndex((n) => n.id === id);
    if (index !== -1) {
      notifications.value.splice(index, 1);
    }
  };

  /**
   * Clears all notifications from the store.
   */
  const clearNotifications = () => {
    notifications.value = [];
  };

  const store = {
    notifications,
    add: addNotification,
    remove: removeNotification,
    clear: clearNotifications,
  };

  provide(NOTIFICATION_KEY, store);

  return store;
};

export const useNotificationStore = () => {
  const store = inject(NOTIFICATION_KEY);
  if (!store) {
    throw new Error(
      "Notification store not found. Ensure createNotificationStore is called in App.vue"
    );
  }
  return store;
};
