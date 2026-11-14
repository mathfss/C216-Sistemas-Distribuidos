import { describe, expect, it } from "vitest";
import { NAME_MAX_LENGTH, validateItem } from "../../src/validation";

describe("validateItem", () => {
  it("rejeita nome vazio ou só com espaços", () => {
    const { errors } = validateItem({ name: "   ", description: "" });
    expect(errors.name).toBe("O nome é obrigatório.");
  });

  it("rejeita nome que excede o limite máximo de caracteres", () => {
    const longName = "a".repeat(NAME_MAX_LENGTH + 1);
    const { errors } = validateItem({ name: longName, description: "" });
    expect(errors.name).toBe(
      `O nome deve ter no máximo ${NAME_MAX_LENGTH} caracteres.`,
    );
  });

  it("aceita item válido e normaliza os dados com trim", () => {
    const { errors, values } = validateItem({
      name: "  Item de Teste  ",
      description: "  Descrição detalhada  ",
    });

    expect(Object.keys(errors)).toHaveLength(0);
    expect(values.name).toBe("Item de Teste");
    expect(values.description).toBe("Descrição detalhada");
  });

  it("permite item sem descrição", () => {
    const { errors, values } = validateItem({
      name: "Item Sem Descrição",
      description: "",
    });

    expect(Object.keys(errors)).toHaveLength(0);
    expect(values.name).toBe("Item Sem Descrição");
    expect(values.description).toBe("");
  });
});
