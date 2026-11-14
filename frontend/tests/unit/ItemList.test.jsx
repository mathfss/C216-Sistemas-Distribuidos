import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ItemList } from "../../src/components/ItemList";

describe("ItemList", () => {
  it("exibe mensagem quando não há itens cadastrados", () => {
    render(<ItemList items={[]} />);
    expect(screen.getByText("Nenhum item cadastrado.")).toBeInTheDocument();
  });

  it("renderiza a lista de itens cadastrados", () => {
    const items = [
      { id: "1", name: "Servidor Node A", description: "Cluster local" },
      { id: "2", name: "Roteador", description: "" },
    ];
    render(<ItemList items={items} />);

    expect(screen.getByText("Servidor Node A")).toBeInTheDocument();
    expect(screen.getByText("Cluster local")).toBeInTheDocument();
    expect(screen.getByText("Roteador")).toBeInTheDocument();
    expect(
      screen.queryByText("Nenhum item cadastrado."),
    ).not.toBeInTheDocument();
  });
});
