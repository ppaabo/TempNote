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
      throw new Error(`Response status: ${response.status}`);
    }
    const data = response.json();
    return data;
  } catch (error) {
    console.error(error.message);
    return null;
  }
};

export const fetchMessage = async (id) => {
  try {
    const response = await fetch(`/api/messages/${id}`);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    const data = await response.json();
    const { ciphertext, iv, salt } = data;
    return { ciphertext, iv, salt };
  } catch (error) {
    console.error(error.message);
    return null;
  }
};
