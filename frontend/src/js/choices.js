import "choices.js/public/assets/styles/choices.css";
import { each } from "./utils.js";

each("#agency-search", async el => {
  let { default: Choices } = await import("choices.js");

  new Choices(el, {
    itemSelectText: "",
    fuseOptions: {
      shouldSort: true,
      tokenize: true,
      matchAllTokens: true,
      includeScore: true
    }
  });
  el.addEventListener("change", event => {
    event.target.closest("form").submit();
  });
});
