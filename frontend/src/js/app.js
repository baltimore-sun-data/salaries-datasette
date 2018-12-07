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

window.addEventListener("load", function() {
  on("click", ".icon-twitter.js-click", e => {
    var tweet = e.target.getAttribute("data-share-text");
    var url = window.location.href;

    var twitterURL =
      "https://twitter.com/intent/tweet?text=" +
      encodeURIComponent(tweet) +
      "&url=" +
      encodeURIComponent(url) +
      "&tw_p=tweetbutton";
    window.open(
      twitterURL,
      "mywin",
      "left=200,top=200,width=500,height=300,toolbar=1,resizable=0"
    );
    return false;
  });
  on("click", ".icon-facebook.js-click", () => {
    // FaceBook has deprecated all the options in the pop-up,
    // so it all needs to be controlled by the meta tags on the page.
    // See https://developers.facebook.com/docs/sharing/reference/feed-dialog
    var url = window.location.href;
    var facebookURL =
      "https://www.facebook.com/dialog/feed?display=popup&app_id=310302989040998&link=" +
      encodeURIComponent(url) +
      "&redirect_uri=https://www.facebook.com";
    window.open(
      facebookURL,
      "mywin",
      "left=200,top=200,width=500,height=300,toolbar=1,resizable=0"
    );
    return false;
  });

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
});
