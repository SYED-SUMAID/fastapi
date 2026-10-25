const API = {
  list: "/products",
  create: "/product",
  item: (id) => `/product/${id}`
};

const rows = document.getElementById("productRows");
const searchInput = document.getElementById("searchInput");
const modalBackdrop = document.getElementById("modalBackdrop");
const form = document.getElementById("productForm");
const formError = document.getElementById("formError");
const submitBtn = document.getElementById("submitBtn");
let products = [];
let editingId = null;
let toastTimer;

const money = (value) => new Intl.NumberFormat("en-IN", {
  style: "currency", currency: "INR", maximumFractionDigits: 0
}).format(Number(value || 0));

function showToast(message, isError = false) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.toggle("error", isError);
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 3200);
}

function updateStats(list) {
  document.getElementById("totalProducts").textContent = list.length;
  document.getElementById("totalUnits").textContent = list.reduce((sum, p) => sum + Number(p.quantity || 0), 0).toLocaleString("en-IN");
  document.getElementById("inventoryValue").textContent = money(list.reduce((sum, p) => sum + Number(p.price || 0) * Number(p.quantity || 0), 0));
  document.getElementById("lowStock").textContent = list.filter(p => Number(p.quantity) <= 5).length;
}

function stockInfo(quantity) {
  if (Number(quantity) <= 0) return { label: "Out of stock", cls: "stock-out" };
  if (Number(quantity) <= 5) return { label: "Low stock", cls: "stock-low" };
  return { label: "In stock", cls: "stock-ok" };
}

function renderProducts() {
  const query = searchInput.value.trim().toLowerCase();
  const filtered = products.filter(p =>
    String(p.name || "").toLowerCase().includes(query) ||
    String(p.description || "").toLowerCase().includes(query)
  );
  document.getElementById("resultCount").textContent =
    `${filtered.length} product${filtered.length === 1 ? "" : "s"} shown · ${products.length} total`;
  if (!filtered.length) {
    rows.innerHTML = `<tr><td colspan="7" class="empty-state">${query ? "No products match your search." : "Your inventory is empty. Add your first product to get started."}</td></tr>`;
    return;
  }
  rows.innerHTML = filtered.map(p => {
    const stock = stockInfo(p.quantity);
    const id = Number(p.product_id);
    return `<tr>
      <td class="id-cell">#${id}</td>
      <td class="product-name">${escapeHtml(p.name)}</td>
      <td class="product-description">${escapeHtml(p.description)}</td>
      <td class="price-cell">${money(p.price)}</td>
      <td>${Number(p.quantity).toLocaleString("en-IN")}</td>
      <td><span class="stock-badge ${stock.cls}">${stock.label}</span></td>
      <td><div class="row-actions">
        <button class="action-btn edit" data-action="edit" data-id="${id}" title="Edit product" aria-label="Edit ${escapeHtml(p.name)}">✎</button>
        <button class="action-btn delete" data-action="delete" data-id="${id}" title="Delete product" aria-label="Delete ${escapeHtml(p.name)}">⌫</button>
      </div></td>
    </tr>`;
  }).join("");
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[ch]));
}

async function loadProducts() {
  rows.innerHTML = `<tr><td colspan="7" class="empty-state">Loading inventory from FastAPI…</td></tr>`;
  try {
    const response = await fetch(API.list);
    if (!response.ok) throw new Error(`Server returned ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data)) throw new Error("Expected a list of products from GET /products");
    products = data;
    updateStats(products);
    renderProducts();
  } catch (error) {
    rows.innerHTML = `<tr><td colspan="7" class="empty-state">Could not load products. Check that FastAPI is running and GET /products works. (${escapeHtml(error.message)})</td></tr>`;
    document.getElementById("resultCount").textContent = "Connection error";
    showToast("Could not connect to the product API.", true);
  }
}

function openModal(product = null) {
  editingId = product ? Number(product.product_id) : null;
  form.reset();
  formError.textContent = "";
  document.getElementById("modalEyebrow").textContent = product ? "EDIT ENTRY" : "NEW ENTRY";
  document.getElementById("modalTitle").textContent = product ? "Edit product" : "Add a product";
  submitBtn.innerHTML = product ? "Save changes <span>↗</span>" : "Save product <span>↗</span>";
  if (product) {
    form.elements.name.value = product.name;
    form.elements.description.value = product.description;
    form.elements.price.value = product.price;
    form.elements.quantity.value = product.quantity;
  }
  modalBackdrop.hidden = false;
  document.body.style.overflow = "hidden";
  setTimeout(() => form.elements.name.focus(), 40);
}

function closeModal() {
  modalBackdrop.hidden = true;
  document.body.style.overflow = "";
  editingId = null;
}

async function submitProduct(event) {
  event.preventDefault();
  formError.textContent = "";
  const data = {
    name: form.elements.name.value.trim(),
    description: form.elements.description.value.trim(),
    price: Number(form.elements.price.value),
    quantity: Number(form.elements.quantity.value)
  };
  if (!data.name || !data.description) {
    formError.textContent = "Name and description are required.";
    return;
  }
  if (!Number.isInteger(data.price) || data.price <= 0) {
    formError.textContent = "Price must be a positive whole number.";
    return;
  }
  if (!Number.isInteger(data.quantity) || data.quantity < 0) {
    formError.textContent = "Quantity must be zero or a positive whole number.";
    return;
  }
  submitBtn.disabled = true;
  submitBtn.textContent = editingId ? "Saving…" : "Adding…";
  try {
    const response = await fetch(editingId ? API.item(editingId) : API.create, {
      method: editingId ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!response.ok) {
      let detail = `Request failed (${response.status})`;
      try {
        const body = await response.json();
        detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail || body);
      } catch (_) {}
      throw new Error(detail);
    }
    closeModal();
    await loadProducts();
    showToast(editingId ? "Product updated successfully." : "Product added successfully.");
  } catch (error) {
    formError.textContent = error.message || "Could not save product.";
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = editingId ? "Save changes <span>↗</span>" : "Save product <span>↗</span>";
  }
}

async function deleteProduct(id) {
  const product = products.find(p => Number(p.product_id) === id);
  if (!product) return;
  if (!window.confirm(`Delete "${product.name}"? This cannot be undone.`)) return;
  try {
    const response = await fetch(API.item(id), { method: "DELETE" });
    if (!response.ok) {
      let detail = `Request failed (${response.status})`;
      try { const body = await response.json(); detail = body.detail || detail; } catch (_) {}
      throw new Error(detail);
    }
    await loadProducts();
    showToast("Product deleted successfully.");
  } catch (error) {
    showToast(error.message || "Could not delete product.", true);
  }
}

document.getElementById("addProductTop").addEventListener("click", () => openModal());
document.getElementById("navAdd").addEventListener("click", () => openModal());
document.getElementById("closeModal").addEventListener("click", closeModal);
document.getElementById("cancelModal").addEventListener("click", closeModal);
document.getElementById("refreshBtn").addEventListener("click", loadProducts);
searchInput.addEventListener("input", renderProducts);
form.addEventListener("submit", submitProduct);
modalBackdrop.addEventListener("click", event => { if (event.target === modalBackdrop) closeModal(); });
document.addEventListener("keydown", event => { if (event.key === "Escape" && !modalBackdrop.hidden) closeModal(); });
rows.addEventListener("click", event => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const id = Number(button.dataset.id);
  if (button.dataset.action === "edit") {
    const product = products.find(p => Number(p.product_id) === id);
    if (product) openModal(product);
  }
  if (button.dataset.action === "delete") deleteProduct(id);
});

loadProducts();
