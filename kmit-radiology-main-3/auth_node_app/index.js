"use strict";
const express = require("express");
const bodyParser = require("body-parser");
const sqlite3 = require("sqlite3").verbose();
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const SECRET_KEY = "secretkey23456";
const cookieParser = require("cookie-parser");
const hashers = require("node-django-hashers");

const database = new sqlite3.Database("../db.sqlite3");

const app = express();
app.use(cookieParser());
const router = express.Router();

router.use(bodyParser.urlencoded({ extended: false }));
router.use(bodyParser.json());

// const createUsersTable = () => {
//     const sqlQuery =
//         " CREATE TABLE IF NOT EXISTS users (  id integer PRIMARY KEY, name text, email text UNIQUE, password text)";
//     return database.run(sqlQuery);
// };

const findUserByName = (name, cb) => {
    return database.get(
        `SELECT * FROM auth_user WHERE username = ?`,
        [name],
        (err, row) => {
            cb(err, row);
        }
    );
};

const findUserByEmail = (email, cb) => {
    return database.get(
        `SELECT * FROM auth_user WHERE email = ?`,
        [email],
        (err, row) => {
            cb(err, row);
        }
    );
};

const createUser = (user, cb) => {
    return database.run(
        "INSERT INTO auth_user (username, email, password, is_superuser, first_name, last_name, is_staff, is_active, date_joined) VALUES (?, ?, ?, false, '','',false,1, DATE('now'));",
        user,
        (err) => {
            cb(err);
        }
    );
};
// createUsersTable();

router.post("/register", async (req, res) => {
    const hash_algorithm = hashers.getHasher("pbkdf2_sha256");
    const name = req.body.name;
    const email = req.body.email;
    const age = req.body.age;
    const pd = req.body.password;
    let password;
    const pp = await hash_algorithm.encode(pd).then((data) => {
        return data;
    });
    password = pp;

    createUser([name, email, password], (err) => {
        if (err) return res.status(500).send(err);
        findUserByEmail(email, (err, user) => {
            if (err) return res.status(500).send(err);
            const expiresIn = 24 * 60 * 60;
            const accessToken = jwt.sign({ id: user.id }, SECRET_KEY, {
                expiresIn: expiresIn,
            });
            res.cookie("nToken", accessToken, {
                maxAge: 900000,
                httpOnly: true,
            });
            res.send("OK");
        });
    });
});

router.post("/login", (req, res) => {
    const name = req.body.name;
    const password = req.body.password;
    const hash_algorithm = hashers.getHasher("pbkdf2_sha256");
    findUserByName(name, (err, user) => {
        if (err) return res.status(500).send("Server error!");
        if (!user) return res.status(404).send("User not found!");

        const result = hash_algorithm
            .verify(password, user.password)
            .then(console.log);
        if (!result) return res.status(401).send("Password not valid!");

        const expiresIn = 15;
        const accessToken = jwt.sign({ id: user.id }, SECRET_KEY, {
            expiresIn: expiresIn,
        });
        res.cookie("nToken", accessToken, { maxAge: 900000, httpOnly: true });
        res.send("OK");
    });
});

// LOGOUT
router.get("/logout", (req, res) => {
    res.clearCookie("nToken");
    res.send("OK");
    console.log("Logged out");
});

router.get("/", (req, res) => {
    // const username = req.body.name;
    // findUserByName(username,  (err, user) => {
    //     console.log(user);
    //     res.status(200).send("This is an authentication server");
    // })
    // res.status(200).send("This is an authentication server");
    res.status(200).send("This is an authentication server");
});

app.use(router);
const port = 1234;
const server = app.listen(port, () => {
    console.log("Server listening at " + port);
});
