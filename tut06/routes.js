const express = require('express');
const { login } = require('./auth');
const { authenticateToken, authorizeRoles } = require('./middleware');

const router = express.Router();

router.post('/login', login);

router.get('/secure/user', authenticateToken, (req, res) => {
    res.json({ message: "Welcome, authenticated user!" });
});

router.get('/secure/admin', authenticateToken, authorizeRoles('admin'), (req, res) => {
    res.json({ message: "Welcome, Admin!" });
});

module.exports = router;
