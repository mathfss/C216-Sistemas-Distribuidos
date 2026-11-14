import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "../../src/App";

function jsonResponse(data, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => data,
  };
}

describe("App Integration", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("exibe mensagem de carregamento antes de receber os dados", () => {
    vi.stubGlobal("fetch", vi.fn().mockReturnValue(new Promise(() => {})));
    render(<App />);

    expect(screen.getByText("Carregando itens...")).toBeInTheDocument();
  });

  it("renderiza estado de lista vazia após retorno da API com array vazio", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse([])));
    render(<App />);

    await waitFor(() => {
      expect(screen.queryByText("Carregando itens...")).not.toBeInTheDocument();
    });

    expect(screen.getByText("Nenhum item cadastrado.")).toBeInTheDocument();
  });

  it("renderiza lista de itens obtidos da API com sucesso", async () => {
    const mockItems = [
      { id: 1, name: "Servidor Node A", description: "Cluster local" },
      { id: 2, name: "Load Balancer", description: "Proxy NGINX" },
    ];
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(mockItems)));
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Servidor Node A")).toBeInTheDocument();
    });

    expect(screen.getByText("Load Balancer")).toBeInTheDocument();
    expect(
      screen.queryByText("Nenhum item cadastrado."),
    ).not.toBeInTheDocument();
  });

  it("exibe mensagem de erro quando a API estiver inacessível no carregamento inicial", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new Error("Network request failed")),
    );
    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(
        "Não foi possível conectar à API.",
      );
    });

    expect(screen.queryByText("Carregando itens...")).not.toBeInTheDocument();
  });

  it("cadastra um novo item via POST e atualiza a listagem", async () => {
    const user = userEvent.setup();
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(jsonResponse([]))
      .mockResolvedValueOnce(
        jsonResponse({
          id: 10,
          name: "Notebook Dell",
          description: "16GB RAM",
        }),
      );

    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Nenhum item cadastrado.")).toBeInTheDocument();
    });

    const nameInput = screen.getByLabelText("Nome");
    const descInput = screen.getByLabelText("Descrição");

    await user.type(nameInput, "Notebook Dell");
    await user.type(descInput, "16GB RAM");
    await user.click(screen.getByRole("button", { name: "Adicionar" }));

    await waitFor(() => {
      expect(screen.getByText("Notebook Dell")).toBeInTheDocument();
    });

    expect(screen.getByText("16GB RAM")).toBeInTheDocument();
    expect(
      screen.queryByText("Nenhum item cadastrado."),
    ).not.toBeInTheDocument();
    expect(nameInput).toHaveValue("");
    expect(descInput).toHaveValue("");

    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock).toHaveBeenLastCalledWith(
      expect.stringContaining("/items/"),
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: "Notebook Dell",
          description: "16GB RAM",
        }),
      }),
    );
  });

  it("exibe erro 409 quando o backend recusa item com nome duplicado e mantém os campos", async () => {
    const user = userEvent.setup();
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(jsonResponse([]))
      .mockResolvedValueOnce(
        jsonResponse({ detail: "Já existe um item com esse nome" }, 409),
      );

    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Nenhum item cadastrado.")).toBeInTheDocument();
    });

    const nameInput = screen.getByLabelText("Nome");
    const descInput = screen.getByLabelText("Descrição");

    await user.type(nameInput, "Notebook Dell");
    await user.type(descInput, "16GB RAM");
    await user.click(screen.getByRole("button", { name: "Adicionar" }));

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(
        "Já existe um item com esse nome",
      );
    });

    // Campos devem continuar preenchidos para correcao
    expect(nameInput).toHaveValue("Notebook Dell");
    expect(descInput).toHaveValue("16GB RAM");
  });

  it("não chama a API quando houver erro de validação local no formulário", async () => {
    const user = userEvent.setup();
    const fetchMock = vi.fn().mockResolvedValueOnce(jsonResponse([]));
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Nenhum item cadastrado.")).toBeInTheDocument();
    });

    await user.click(screen.getByRole("button", { name: "Adicionar" }));

    expect(screen.getByRole("alert")).toHaveTextContent(
      "O nome é obrigatório.",
    );
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});
