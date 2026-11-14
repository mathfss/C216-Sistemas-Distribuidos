import { expect, test } from "@playwright/test";

function uniqueName(prefix = "Item") {
  return `${prefix} ${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

test.describe("Gerenciador de Itens E2E Full-stack", () => {
  test("carrega a interface e lista itens ou mensagem inicial", async ({
    page,
  }) => {
    await page.goto("/");
    await expect(
      page.getByRole("heading", { name: "Gerenciador de Itens" }),
    ).toBeVisible();
    await expect(page.getByLabel("Nome")).toBeVisible();
  });

  test("exibe mensagem de erro quando o nome for vazio", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Adicionar" }).click();
    await expect(page.getByRole("alert")).toHaveText("O nome é obrigatório.");
  });

  test("cadastra um item e ele persiste após recarregar a página", async ({
    page,
  }) => {
    const name = uniqueName("Notebook Dell");
    await page.goto("/");

    await page.getByLabel("Nome").fill(name);
    await page.getByLabel("Descrição").fill("16GB RAM SSD 512GB");
    await page.getByRole("button", { name: "Adicionar" }).click();

    const item = page.getByRole("listitem").filter({ hasText: name });
    await expect(item).toBeVisible();
    await expect(item).toContainText("16GB RAM SSD 512GB");

    // Recarrega a pagina: os dados devem vir do banco de dados (PostgreSQL via API)
    await page.reload();
    await expect(item).toBeVisible();
    await expect(item).toContainText("16GB RAM SSD 512GB");
  });

  test("exibe erro ao tentar cadastrar item com nome duplicado", async ({
    page,
  }) => {
    const name = uniqueName("Servidor Web");
    await page.goto("/");

    // Primeiro cadastro com sucesso
    await page.getByLabel("Nome").fill(name);
    await page.getByLabel("Descrição").fill("Primeiro cadastro");
    await page.getByRole("button", { name: "Adicionar" }).click();

    const item = page.getByRole("listitem").filter({ hasText: name });
    await expect(item).toBeVisible();

    // Tenta cadastrar novamente com o mesmo nome
    await page.getByLabel("Nome").fill(name);
    await page.getByLabel("Descrição").fill("Tentativa repetida");
    await page.getByRole("button", { name: "Adicionar" }).click();

    // Deve exibir o erro 409 vindo da API
    await expect(page.getByRole("alert")).toHaveText(
      "Já existe um item com esse nome",
    );
    // Campos devem continuar preenchidos
    await expect(page.getByLabel("Nome")).toHaveValue(name);
  });
});
