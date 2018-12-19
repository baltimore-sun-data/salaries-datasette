import "choices.js/public/assets/styles/choices.css";
import Choices from "choices.js";
import { each } from "./utils.js";

each("#agency-search", el => {
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
