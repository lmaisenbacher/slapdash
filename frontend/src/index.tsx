import * as React from "react";
import ReactDOM from "react-dom";
import App from "./app";

import version from "../../slapdash/version.json";

let api = document.location.href;
if (process.env.NODE_ENV === "development") {
  api = "http://localhost:8000";
  console.log("development");
  console.log(version);
  console.log(`${version.major}.${version.minor}.${version.patch}`);
}

ReactDOM.render(<App api={api} />, document.getElementById("root"));
