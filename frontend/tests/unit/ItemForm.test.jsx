import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { ItemForm } from "../../src/components/ItemForm";

describe("ItemForm", () => {
  it("mostra erro e não chama onAdd com nome vazio", async () => {
    const user = userEvent.setup();
    const onAdd = vi.fn();
    render(<ItemForm onAdd={onAdd} />);

    await user.click(screen.getByRole("button", { name: "Adicionar" }));

    expect(screen.getByRole("alert")).toHaveTextContent(
      "O nome é obrigatório.",
    );
    expect(onAdd).not.toHaveBeenCalled();
  });

  it("chama onAdd com dados válidos e limpa os campos", async () => {
    const user = userEvent.setup();
    const onAdd = vi.fn();
    render(<ItemForm onAdd={onAdd} />);

    const nameInput = screen.getByLabelText("Nome");
    const descInput = screen.getByLabelText("Descrição");

    await user.type(nameInput, "Monitor");
    await user.type(descInput, "27 polegadas");
    await user.click(screen.getByRole("button", { name: "Adicionar" }));

    expect(onAdd).toHaveBeenCalledWith({
      name: "Monitor",
      description: "27 polegadas",
    });
    expect(nameInput).toHaveValue("");
    expect(descInput).toHaveValue("");
  });
});
