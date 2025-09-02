const express = require("express");
const fs = require("fs");
const path = require("path");
const bodyParser = require("body-parser");

const app = express();
const PORT = process.env.PORT || 3000;

// middleware
app.use(bodyParser.urlencoded({ extended: true }));

// file path
const filePath = path.join(__dirname, "ind.html");

// login middleware
const USER = "admin";
const PASS = "_genesis_pritam_";

app.use("/admin", (req, res, next) => {
  const auth = req.headers.authorization;
  if (!auth) {
    res.setHeader("WWW-Authenticate", 'Basic realm="Admin Panel"');
    return res.status(401).send("Auth required");
  }

  const base64 = auth.split(" ")[1];
  const [user, pass] = Buffer.from(base64, "base64").toString().split(":");

  if (user === USER && pass === PASS) return next();
  res.status(403).send("Forbidden");
});

// admin panel UI
app.get("/admin", (req, res) => {
  const content = fs.readFileSync(filePath, "utf8");
  res.send(`
    <form method="POST" action="/admin/save">
      <textarea name="code" style="width:100%;height:500px;">${content}</textarea>
      <br><button type="submit">Save</button>
    </form>
  `);
});

// save changes
app.post("/admin/save", (req, res) => {
  const newCode = req.body.code;
  fs.writeFileSync(filePath, newCode, "utf8");
  res.send("Saved! <a href='/ind.html'>View Site</a>");
});

app.use(express.static(__dirname));

app.listen(PORT, () => console.log(`Server running on ${PORT}`));
