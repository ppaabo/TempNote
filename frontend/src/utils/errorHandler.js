/**
 * Centralized error types for consistent error handling across the application
 */
export const ErrorTypes = {
  // API/Network errors
  NETWORK_ERROR: "network_error",
  API_ERROR: "api_error",

  // Resource errors
  NOT_FOUND: "not_found",
  RESOURCE_DELETED: "resource_deleted",

  // Cryptography errors
  ENCRYPTION_ERROR: "encryption_error",
  DECRYPTION_ERROR: "decryption_error",
  PASSWORD_ERROR: "password_error",

  // Input validation
  VALIDATION_ERROR: "validation_error",

  // General / Unknown errors
  UNKNOWN_ERROR: "unknown_error",
};

/**
 * Custom application error with type information
 */
export class AppError extends Error {
  constructor(type, message = null, originalError = null) {
    super(message || defaultErrorMessages[type]);
    this.name = "AppError";
    this.type = type;
    this.originalError = originalError;

    // Capture stack trace
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, AppError);
    }
  }
}

/**
 * Maps error types to notification types for display
 */
const errorTypeToNotificationType = {
  [ErrorTypes.NETWORK_ERROR]: "error",
  [ErrorTypes.API_ERROR]: "error",
  [ErrorTypes.NOT_FOUND]: "warning",
  [ErrorTypes.RESOURCE_DELETED]: "info",
  [ErrorTypes.ENCRYPTION_ERROR]: "error",
  [ErrorTypes.DECRYPTION_ERROR]: "error",
  [ErrorTypes.PASSWORD_ERROR]: "warning",
  [ErrorTypes.VALIDATION_ERROR]: "warning",
  [ErrorTypes.UNKNOWN_ERROR]: "error",
};

/**
 * Maps error types to user-friendly messages
 */
const defaultErrorMessages = {
  [ErrorTypes.NETWORK_ERROR]:
    "Network connection issue. Please check your internet connection.",
  [ErrorTypes.API_ERROR]: "Server error occurred. Please try again later.",
  [ErrorTypes.NOT_FOUND]: "The requested resource was not found.",
  [ErrorTypes.RESOURCE_DELETED]:
    "This resource has been deleted or has expired.",
  [ErrorTypes.ENCRYPTION_ERROR]: "Failed to encrypt data.",
  [ErrorTypes.DECRYPTION_ERROR]: "Failed to decrypt data.",
  [ErrorTypes.PASSWORD_ERROR]: "Incorrect password provided.",
  [ErrorTypes.VALIDATION_ERROR]: "Please check your input and try again.",
  [ErrorTypes.UNKNOWN_ERROR]: "An unexpected error occurred.",
};

/**
 * Centralized error handler. Uses notification store to display error notifications
 *
 * @param {Error|AppError} error - The error object
 * @param {Object} notificationStore - The notification store instance
 * @param {string} context - Optional context information about where the error occurred
 * @param {boolean} showNotification - Whether to show a notification for this error
 */
export const handleError = (
  error,
  notificationStore,
  context = "",
  showNotification = true
) => {
  const errorType =
    error instanceof AppError ? error.type : ErrorTypes.UNKNOWN_ERROR;
  const originalError = error instanceof AppError ? error.originalError : error;

  // Log error with context for debugging
  if (context) {
    console.error(`Error in ${context}:`, error);
  } else {
    console.error(error);
  }

  // Show notification if requested
  if (showNotification && notificationStore) {
    const message = error.message || defaultErrorMessages[errorType];
    const type = errorTypeToNotificationType[errorType] || "error";

    notificationStore.add({
      message,
      type,
      timeout: type === "error" ? 8000 : 5000,
    });
  }

  return error;
};
