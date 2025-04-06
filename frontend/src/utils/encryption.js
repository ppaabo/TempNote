import { AppError, ErrorTypes } from "../utils/errorHandler";

const pack = (buffer) => {
  return window.btoa(String.fromCharCode(...new Uint8Array(buffer)));
};

const unpack = (packed) => {
  const string = window.atob(packed);
  const buffer = new ArrayBuffer(string.length);
  const bufferView = new Uint8Array(buffer);

  for (let i = 0; i < string.length; i++) {
    bufferView[i] = string.charCodeAt(i);
  }

  return buffer;
};

const encode = (data) => {
  const encoder = new TextEncoder();
  return encoder.encode(data);
};

const decode = (data) => {
  const decoder = new TextDecoder();
  return decoder.decode(data);
};

const deriveKey = async (password, salt) => {
  const encodedPassword = encode(password);
  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    encodedPassword,
    { name: "PBKDF2" },
    false,
    ["deriveKey"]
  );

  return await crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt: salt,
      iterations: 100000,
      hash: "SHA-256",
    },
    keyMaterial,
    { name: "AES-GCM", length: 256 },
    true,
    ["encrypt", "decrypt"]
  );
};
/**
 * Encrypts a given message using AES-GCM encryption with a password-derived key.
 *
 * @async
 * @function encryptMsg
 * @param {string} message - The plaintext message to encrypt.
 * @param {string} password - The password used to derive the encryption key.
 * @returns {Promise<Object>} An object containing the encrypted message, initialization vector (iv), and salt:
 * - `ciphertext` {string}: The Base64-encoded encrypted message.
 * - `iv` {string}: The Base64-encoded initialization vector used for encryption.
 * - `salt` {string}: The Base64-encoded salt used for key derivation.
 * @throws {AppError} Throws a validation error if the message or password is empty.
 * @throws {AppError} Throws an encryption error if the encryption process fails.
 */
export const encryptMsg = async (message, password) => {
  if (!message.trim()) {
    throw new AppError(
      ErrorTypes.VALIDATION_ERROR,
      "Cannot encrypt empty message"
    );
  }
  if (!password.trim()) {
    throw new AppError(
      ErrorTypes.VALIDATION_ERROR,
      "Password is required for encryption"
    );
  }
  try {
    const encoded = encode(message);
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const key = await deriveKey(password, salt);
    const cipher = await crypto.subtle.encrypt(
      { name: "AES-GCM", iv },
      key,
      encoded
    );
    return {
      ciphertext: pack(cipher),
      iv: pack(iv),
      salt: pack(salt),
    };
  } catch (error) {
    throw new AppError(
      ErrorTypes.ENCRYPTION_ERROR,
      "Failed to encrypt message",
      error
    );
  }
};
/**
 * Decrypts an AES-GCM encrypted message using a password-derived key.
 *
 * @async
 * @function decryptMsg
 * @param {string} ciphertext - The Base64-encoded encrypted message to decrypt.
 * @param {string} iv - The Base64-encoded initialization vector used during encryption.
 * @param {string} salt - The Base64-encoded salt used for key derivation.
 * @param {string} password - The password used to derive the decryption key.
 * @returns {Promise<string>} The decrypted plaintext message.
 * @throws {AppError} Throws a validation error if any required parameter is missing.
 * @throws {AppError} Throws a password error if the provided password is incorrect.
 * @throws {AppError} Throws a decryption error if the decryption process fails.
 */
export const decryptMsg = async (ciphertext, iv, salt, password) => {
  if (!ciphertext || !iv) {
    throw new AppError(ErrorTypes.VALIDATION_ERROR, "Missing encrypted data");
  }

  if (!password) {
    throw new AppError(
      ErrorTypes.VALIDATION_ERROR,
      "Password is required for decryption"
    );
  }

  if (!salt) {
    throw new AppError(
      ErrorTypes.VALIDATION_ERROR,
      "Missing salt value required for decryption"
    );
  }

  try {
    const ivBuffer = new Uint8Array(unpack(iv));
    const cipherBuffer = new Uint8Array(unpack(ciphertext));
    const saltBuffer = new Uint8Array(unpack(salt));
    const key = await deriveKey(password, saltBuffer);

    const decrypted = await crypto.subtle.decrypt(
      { name: "AES-GCM", iv: ivBuffer },
      key,
      cipherBuffer
    );
    return decode(decrypted);
  } catch (error) {
    // OperationError = wrong password typically
    if (error.name === "OperationError") {
      throw new AppError(
        ErrorTypes.PASSWORD_ERROR,
        "Incorrect password provided",
        error
      );
    }

    throw new AppError(
      ErrorTypes.DECRYPTION_ERROR,
      "Failed to decrypt message",
      error
    );
  }
};
