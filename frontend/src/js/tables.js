import { on } from "./utils.js";

// Make rows clickable
on("click", ".dbresults.js-click tbody", e => {
  if (e.target.closest("table").classList.contains("hide-columns")) {
    window.location = e.target.closest("tr").querySelector("a").href;
  }
});

// Toggle extra columns
on("click", ".view-cols.js-click button", e => {
  e.target
    .closest(".table-wrapper")
    .querySelector("table")
    .classList.toggle("hide-columns");
});
