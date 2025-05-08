import { AppError, ErrorTypes } from "../utils/errorHandler";

/**
 * Converts an ArrayBuffer to a Base64 string
 * @param {ArrayBuffer} buffer - The buffer to encode
 * @returns {string} Base64 encoded string
 */
const pack = (buffer) => {
  return window.btoa(String.fromCharCode(...new Uint8Array(buffer)));
};

/**
 * Converts a Base64 string back to an ArrayBuffer
 * @param {string} packed - Base64 encoded string
 * @returns {ArrayBuffer} The decoded buffer
 */
const unpack = (packed) => {
  const string = window.atob(packed);
  const buffer = new ArrayBuffer(string.length);
  const bufferView = new Uint8Array(buffer);

  for (let i = 0; i < string.length; i++) {
    bufferView[i] = string.charCodeAt(i);
  }

  return buffer;
};

/**
 * Encodes a string to a Uint8Array
 * @param {string} data - String to encode
 * @returns {Uint8Array} Encoded data
 */
const encode = (data) => {
  const encoder = new TextEncoder();
  return encoder.encode(data);
};

/**
 * Decodes a Uint8Array to a string
 * @param {Uint8Array} data - Data to decode
 * @returns {string} Decoded string
 */
const decode = (data) => {
  const decoder = new TextDecoder();
  return decoder.decode(data);
};

/**
 * Derives a key from a given password and salt using PBKDF2.
 * @async
 * @function deriveKey
 * @param {string} password - The password to derive the key from.
 * @param {Uint8Array} salt - A cryptographically secure random value used to derive the key.
 * @returns {Promise<CryptoKey>} A promise that resolves to a derived AES-GCM key.
 */
const deriveKey = async (password, salt) => {
  const encodedPassword = encode(password);
  const keyMaterial = await window.crypto.subtle.importKey(
    "raw",
    encodedPassword,
    { name: "PBKDF2" },
    false,
    ["deriveKey"]
  );
  // OWASP recommendation: 600,000 Iterations for PBKDF2 (800 000 used)
  return await window.crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt: salt,
      iterations: 800000,
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
    // 12-byte IV recommended for AES-GCM
    const iv = window.crypto.getRandomValues(new Uint8Array(12));
    // 16-byte salt recommended for PBKDF2
    const salt = window.crypto.getRandomValues(new Uint8Array(16));
    const key = await deriveKey(password, salt);
    const cipher = await window.crypto.subtle.encrypt(
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
 * Decrypts an AES-GC<WM encrypted message using a password-derived key.
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

    const decrypted = await window.crypto.subtle.decrypt(
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
