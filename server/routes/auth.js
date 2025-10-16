const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

// Регистрация
router.post('/register', async (req, res) => {
    try {
        const { email, password } = req.body;
        const existing = await User.findOne({ email });
        if (existing) {
            return res.status(400).json({ message: "Имейл вече е регистриран" });
        }
        const salt = await bcrypt.genSalt(10);
        const hash = await bcrypt.hash(password, salt);
        const user = new User({ email, passwordHash: hash });
        await user.save();
        res.json({ message: "Регистрация успешна" });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Грешка на сървъра" });
    }
});

// Логин
router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).json({ message: "Невалиден имейл или парола" });
        }
        const isMatch = await bcrypt.compare(password, user.passwordHash);
        if (!isMatch) {
            return res.status(400).json({ message: "Невалиден имейл или парола" });
        }
        const payload = { id: user._id, role: user.role };
        const token = jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '8h' });
        res.json({ token, role: user.role });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Грешка на сървъра" });
    }
});

module.exports = router;
