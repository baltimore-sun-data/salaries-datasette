const each = (qs, callback) => {
  var els = typeof qs === "string" ? document.querySelectorAll(qs) : qs;
  var i;
  for (i = 0; i < els.length; i++) {
    callback(els[i], i);
  }
};

const on = (event, qs, callback) => {
  each(qs, el => {
    el.addEventListener(event, callback);
  });
};

export { each, on };
