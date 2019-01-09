import { each } from "./utils.js";

import "codemirror/lib/codemirror.css";

each("[name=sql],.sql[disabled]", async el => {
  let [{ default: CodeMirror }] = await Promise.all([
    import("codemirror/lib/codemirror.js"),
    import("codemirror/mode/sql/sql.js")
  ]);

  var editor = CodeMirror.fromTextArea(el, {
    lineNumbers: true,
    mode: "text/x-sql",
    lineWrapping: true,
    readOnly: el.disabled
  });
  editor.setOption("extraKeys", {
    "Shift-Enter": () => {
      el.closest("form").submit();
    },
    Tab: false
  });
});
