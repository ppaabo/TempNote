import { AppError, ErrorTypes } from "../utils/errorHandler";

export const sendMessage = async (message) => {
  try {
    const response = await fetch("/api/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(message),
    });
    if (!response.ok) {
      const status = response.status;
      throw new AppError(
        ErrorTypes.API_ERROR,
        `Failed to send message: Server responded with status ${status}`,
        new Error(`Response status: ${status}`)
      );
    }
    return await response.json();
  } catch (error) {
    if (error instanceof AppError) {
      throw error;
    }

    if (error.name === "TypeError" || error.name === "NetworkError") {
      throw new AppError(ErrorTypes.NETWORK_ERROR, null, error);
    }

    throw new AppError(
      ErrorTypes.UNKNOWN_ERROR,
      "An unexpected error occurred while sending the message",
      error
    );
  }
};

export const fetchMessage = async (id) => {
  try {
    const response = await fetch(`/api/messages/${id}`);

    if (response.status === 404) {
      throw new AppError(
        ErrorTypes.NOT_FOUND,
        "Message not found or already read",
        new Error(`Message with ID ${id} not found`)
      );
    }

    if (!response.ok) {
      throw new AppError(
        ErrorTypes.API_ERROR,
        `Failed to retrieve message: Server responded with status ${response.status}`,
        new Error(`Response status: ${response.status}`)
      );
    }
    const data = await response.json();
    const { ciphertext, iv, salt } = data;
    return { ciphertext, iv, salt };
  } catch (error) {
    if (error instanceof AppError) {
      throw error;
    }

    if (error.name === "TypeError" || error.name === "NetworkError") {
      throw new AppError(ErrorTypes.NETWORK_ERROR, null, error);
    }

    throw new AppError(
      ErrorTypes.UNKNOWN_ERROR,
      "An unexpected error occurred while retrieving the message",
      error
    );
  }
};

export const consumeMessage = async (id) => {
  try {
    const response = await fetch(`/api/messages/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      throw new AppError(
        ErrorTypes.API_ERROR,
        `Failed to delete message: Server responded with status ${response.status}`,
        new Error(`Response status: ${response.status}`)
      );
    }
    return await response.json();
  } catch (error) {
    if (error instanceof AppError) {
      throw error;
    }

    if (error.name === "TypeError" || error.name === "NetworkError") {
      throw new AppError(ErrorTypes.NETWORK_ERROR, null, error);
    }

    throw new AppError(
      ErrorTypes.UNKNOWN_ERROR,
      "An unexpected error occured while deleting the message",
      error
    );
  }
};
