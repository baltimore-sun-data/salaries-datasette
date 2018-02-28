// Convenience extension to NodeList:
NodeList.prototype.addEventListener = function(event, func) {
  this.forEach(function(content, item) {
    content.addEventListener(event, func);
  });
};

window.addEventListener("load", function() {
  document.body.classList.add("js-active");

  document
    .querySelectorAll(".icon-twitter.js-click")
    .addEventListener("click", function(e) {
      var tweet = e.target.getAttribute("data-share-text");
      var url = window.location.href; // Interactive URL

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

  document
    .querySelectorAll(".icon-facebook.js-click")
    .addEventListener("click", function(e) {
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
  document
    .querySelectorAll(".dbresults.js-click tbody")
    .addEventListener("click", function(e) {
      if (e.target.closest("table").classList.contains("hide-columns")) {
        window.location = e.target.closest("tr").querySelector("a").href;
      }
    });

  // Toggle extra columns
  document
    .querySelectorAll(".dbresults.js-click thead")
    .addEventListener("click", function(e) {
      e.target.closest("table").classList.toggle("hide-columns");
    });
});
