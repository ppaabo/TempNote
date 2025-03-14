export function useCrypto() {
  const generateKey = async () => {
    return crypto.subtle.generateKey(
      {
        name: "AES-GCM",
        length: 256,
      },
      true,
      ["encrypt", "decrypt"]
    );
  };

  const encode = (data) => {
    const encoder = new TextEncoder();

    return encoder.encode(data);
  };

  const generateIv = () => {
    return window.crypto.getRandomValues(new Uint8Array(12));
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

  const encryptMsg = async (message, password) => {
    const encoded = encode(message);
    const iv = generateIv();
    const salt = crypto.getRandomValues(new Uint8Array(16));

    let key;
    if (password) {
      key = await deriveKey(password, salt);
    } else {
      key = await generateKey();
    }

    const cipher = await crypto.subtle.encrypt(
      { name: "AES-GCM", iv },
      key,
      encoded
    );
    return {
      ciphertext: btoa(String.fromCharCode(...new Uint8Array(cipher))),
      iv: btoa(String.fromCharCode(...iv)),
      salt: password ? btoa(String.fromCharCode(...salt)) : null, // Store salt if using a password
    };
  };

  return { encryptMsg };
}
