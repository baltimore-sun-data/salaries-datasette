var ManifestPlugin = require("webpack-manifest-plugin");

module.exports = {
  baseUrl:
    process.env.NODE_ENV === "production"
      ? "/static/"
      : "http://localhost:9002/static/",
  outputDir: "dist",
  chainWebpack: config => {
    config.plugins.delete("html");
    config.plugins.delete("preload");
    config.plugins.delete("prefetch");
    config.optimization.splitChunks(false);
  },
  devServer: {
    port: "9002",
    allowedHosts: ["*"],
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "no-cache"
    }
  },
  configureWebpack: {
    plugins: [new ManifestPlugin()]
  }
};
