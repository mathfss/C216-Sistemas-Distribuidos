import { expect, test } from "@playwright/test";

test.describe("Gerenciador de Itens E2E", () => {
  test("carrega a interface inicial com estado vazio", async ({ page }) => {
    await page.goto("/");
    await expect(
      page.getByRole("heading", { name: "Gerenciador de Itens" }),
    ).toBeVisible();
    await expect(page.getByText("Nenhum item cadastrado.")).toBeVisible();
  });

  test("exibe mensagem de erro quando nome for vazio", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Adicionar" }).click();
    await expect(page.getByRole("alert")).toHaveText("O nome é obrigatório.");
  });

  test("cadastra um item e o exibe na listagem", async ({ page }) => {
    await page.goto("/");

    await page.getByLabel("Nome").fill("Notebook");
    await page.getByLabel("Descrição").fill("14 polegadas");
    await page.getByRole("button", { name: "Adicionar" }).click();

    await expect(page.getByRole("listitem")).toContainText("Notebook");
    await expect(page.getByRole("listitem")).toContainText("14 polegadas");
    await expect(page.getByText("Nenhum item cadastrado.")).toBeHidden();
  });
});
