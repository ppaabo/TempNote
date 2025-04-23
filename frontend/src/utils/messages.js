import { AppError, ErrorTypes } from "../utils/errorHandler";
import { validate as uuidValidate } from "uuid";
export const sendMessage = async (message) => {
  try {
    const response = await fetch("/api/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(message),
    });
    const jsonResponse = await response.json();
    if (!response.ok) {
      const status = response.status;
      throw new AppError(
        ErrorTypes.API_ERROR,
        `Failed to send message: Server responded with status ${status}`,
        new Error(`Response status: ${status}`)
      );
    }
    return jsonResponse.data;
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
    if (!uuidValidate(id)) {
      throw new AppError(
        ErrorTypes.VALIDATION_ERROR,
        `The message link appears to be invalid`,
        new Error(`Invalid UUID format: ${id}`)
      );
    }
    const response = await fetch(`/api/messages/${id}`);
    const jsonResponse = await response.json();

    if (response.status === 400) {
      throw new AppError(
        ErrorTypes.VALIDATION_ERROR,
        `The message ID appears to be invalid`,
        new Error(`Invalid UUID format: ${id}`)
      );
    }

    if (response.status === 404) {
      throw new AppError(
        ErrorTypes.NOT_FOUND,
        "This message is unavailable or has already been read",
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
    const data = jsonResponse.data;
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
    if (!uuidValidate(id)) {
      throw new AppError(
        ErrorTypes.VALIDATION_ERROR,
        `The message ID appears to be invalid`,
        new Error(`Invalid UUID format: ${id}`)
      );
    }
    const response = await fetch(`/api/messages/${id}`, {
      method: "DELETE",
    });
    const jsonResponse = await response.json();
    if (!response.ok) {
      throw new AppError(
        ErrorTypes.API_ERROR,
        `Failed to delete message: Server responded with status ${response.status}`,
        new Error(`Response status: ${response.status}`)
      );
    }
    return jsonResponse.data;
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
