import { useState } from "react";
import { validateItem } from "../validation";

export function ItemForm({ onAdd }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitError("");
    const result = validateItem({ name, description });
    setErrors(result.errors);
    if (Object.keys(result.errors).length > 0) return;

    setIsSubmitting(true);
    try {
      await onAdd(result.values);
      setName("");
      setDescription("");
      setErrors({});
    } catch (error) {
      setSubmitError(error.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      noValidate
      className="space-y-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
    >
      {submitError && (
        <p role="alert" className="text-sm font-medium text-red-700">
          {submitError}
        </p>
      )}
      <div className="space-y-1">
        <label htmlFor="item-name" className="block text-sm font-medium">
          Nome
        </label>
        <input
          id="item-name"
          value={name}
          onChange={(event) => {
            setName(event.target.value);
            setSubmitError("");
          }}
          disabled={isSubmitting}
          aria-invalid={errors.name ? "true" : "false"}
          aria-describedby={errors.name ? "item-name-error" : undefined}
          className="w-full rounded border border-slate-300 p-2 disabled:bg-slate-100"
        />
        {errors.name && (
          <p id="item-name-error" role="alert" className="text-sm text-red-700">
            {errors.name}
          </p>
        )}
      </div>
      <div className="space-y-1">
        <label htmlFor="item-description" className="block text-sm font-medium">
          Descrição
        </label>
        <textarea
          id="item-description"
          value={description}
          onChange={(event) => {
            setDescription(event.target.value);
            setSubmitError("");
          }}
          disabled={isSubmitting}
          rows={3}
          className="w-full rounded border border-slate-300 p-2 disabled:bg-slate-100"
        />
      </div>
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 disabled:opacity-50 sm:w-auto"
      >
        {isSubmitting ? "Salvando..." : "Adicionar"}
      </button>
    </form>
  );
}
