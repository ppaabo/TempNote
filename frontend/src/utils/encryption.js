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

// const generateIv = () => {
//   return crypto.getRandomValues(new Uint8Array(12));
// };

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

export const encryptMsg = async (message, password) => {
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
};

export const decryptMsg = async (ciphertext, iv, salt, password) => {
  const ivBuffer = new Uint8Array(unpack(iv));
  const cipherBuffer = new Uint8Array(unpack(ciphertext));
  const saltBuffer = salt ? new Uint8Array(unpack(salt)) : null;

  try {
    if (!password || !saltBuffer) {
      throw new Error("Salt & password are required for decryption.");
    }
    const key = await deriveKey(password, saltBuffer);
    const decrypted = await crypto.subtle.decrypt(
      { name: "AES-GCM", iv: ivBuffer },
      key,
      cipherBuffer
    );
    return decode(decrypted);
  } catch (error) {
    console.error("Decryption failed:", error);
    return null;
  }
};
