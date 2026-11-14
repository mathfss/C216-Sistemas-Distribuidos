export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const ITEMS_URL = `${API_URL}/items/`;

async function request(url, options, defaultErrorMessage) {
  let response;
  try {
    response = await fetch(url, options);
  } catch (_error) {
    throw new Error("Não foi possível conectar à API.");
  }

  if (!response.ok) {
    let message = defaultErrorMessage;
    try {
      const data = await response.json();
      if (data && typeof data.detail === "string") {
        message = data.detail;
      } else if (data && Array.isArray(data.detail) && data.detail.length > 0) {
        message = data.detail[0].msg || defaultErrorMessage;
      }
    } catch (_parseError) {
      // Mantem mensagem padrao caso nao consiga fazer o parse
    }
    throw new Error(message);
  }

  return response.json();
}

export function listItems() {
  return request(ITEMS_URL, undefined, "Erro ao carregar os itens.");
}

export function createItem({ name, description }) {
  return request(
    ITEMS_URL,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description: description || null }),
    },
    "Erro ao cadastrar o item.",
  );
}
