const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const pool = require('./db');

async function login(req, res) {
    const { username, password } = req.body;
    const [users] = await pool.query("SELECT * FROM users WHERE username = ?", [username]);

    if (users.length === 0) {
        return res.status(401).json({ message: "Invalid username or password" });
    }

    const user = users[0];

    const passwordValid = await bcrypt.compare(password, user.password);
    if (!passwordValid) {
        return res.status(401).json({ message: "Invalid username or password" });
    }

    const token = jwt.sign(
        { userId: user.id, role: user.role },
        process.env.JWT_SECRET,
        { expiresIn: process.env.TOKEN_EXPIRY }
    );

    res.json({ token });
}

module.exports = { login };
