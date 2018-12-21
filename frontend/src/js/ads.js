import { each } from "./utils.js";

window.gptadslots = [];
window.googletag = window.googletag || {};
window.googletag.cmd = window.googletag.cmd || [];

var adUnit = "/4011/trb.baltimoresun/";

each("[data-slot-sizes]", (el, n) => {
  // Create inner div
  var divId = "ad-unit-" + n.toString();
  var slot = document.createElement("div");
  slot.id = divId;
  slot.classList.add("slot");
  el.appendChild(slot);

  // Create ad mappings
  var sizes = JSON.parse(el.getAttribute("data-slot-sizes"));
  var viewports = JSON.parse(el.getAttribute("data-slot-viewports"));
  var adSlot = el.getAttribute("data-slot-name") || "news";
  var adTarget = adUnit + adSlot;

  window.googletag.cmd.push(function() {
    var mapping = window.googletag.sizeMapping();
    sizes.forEach((size, i) => {
      mapping.addSize(viewports[i], size);
    });
    mapping = mapping.build();

    // Push ad call
    var slot = window.googletag
      .defineSlot(adTarget, mapping, divId)
      .defineSizeMapping(mapping)
      .setTargeting("pos", ["1"])
      .setCollapseEmptyDiv(true)
      .addService(window.googletag.pubads());
    window.gptadslots.push(slot);
    window.googletag.pubads().setTargeting("ptype", ["s"]);
    window.googletag.enableServices();
    window.googletag.display(divId);

    // If we're supposed to refresh this periodically, do that
    var refreshInterval = el.getAttribute("data-refresh");
    if (refreshInterval) {
      window.adIntervalTimer = window.setInterval(() => {
        window.googletag.cmd.push(function() {
          window.googletag.pubads().refresh([slot]);
        });
      }, refreshInterval);
    }
  });
});
