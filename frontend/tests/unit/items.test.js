import { afterEach, describe, expect, it, vi } from "vitest";
import { API_URL, createItem, listItems } from "../../src/services/items";

function jsonResponse(data, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => data,
  };
}

describe("items service", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  describe("listItems", () => {
    it("chama GET /items/ e retorna a lista em caso de sucesso", async () => {
      const mockData = [{ id: 1, name: "Item 1" }];
      vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(mockData)));

      const result = await listItems();
      expect(result).toEqual(mockData);
      expect(fetch).toHaveBeenCalledWith(`${API_URL}/items/`, undefined);
    });

    it("lança erro amigável se a API estiver fora do ar", async () => {
      vi.stubGlobal(
        "fetch",
        vi.fn().mockRejectedValue(new Error("Connection refused")),
      );

      await expect(listItems()).rejects.toThrow(
        "Não foi possível conectar à API.",
      );
    });

    it("lança erro padrão se o status não for ok e não houver detail", async () => {
      vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({}, 500)));

      await expect(listItems()).rejects.toThrow("Erro ao carregar os itens.");
    });
  });

  describe("createItem", () => {
    it("envia POST com headers e payload JSON", async () => {
      const payload = { name: "Notebook", description: "14 polegadas" };
      const createdItem = { id: 5, ...payload };
      vi.stubGlobal(
        "fetch",
        vi.fn().mockResolvedValue(jsonResponse(createdItem, 201)),
      );

      const result = await createItem(payload);
      expect(result).toEqual(createdItem);
      expect(fetch).toHaveBeenCalledWith(`${API_URL}/items/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    });

    it("converte description vazia em null", async () => {
      const payload = { name: "Sem desc", description: "" };
      vi.stubGlobal(
        "fetch",
        vi
          .fn()
          .mockResolvedValue(
            jsonResponse({ id: 6, name: "Sem desc", description: null }, 201),
          ),
      );

      await createItem(payload);
      expect(fetch).toHaveBeenCalledWith(`${API_URL}/items/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: "Sem desc", description: null }),
      });
    });

    it("repassa mensagem detail do backend em caso de 409", async () => {
      vi.stubGlobal(
        "fetch",
        vi
          .fn()
          .mockResolvedValue(
            jsonResponse({ detail: "Já existe um item com esse nome" }, 409),
          ),
      );

      await expect(
        createItem({ name: "Duplicado", description: "Desc" }),
      ).rejects.toThrow("Já existe um item com esse nome");
    });
  });
});
