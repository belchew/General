const express = require('express');
const router = express.Router();
const User = require('../models/User');
const { authenticateToken, requireAdmin } = require('../middleware/authMiddleware');

// Всички потребители (само admin)
router.get('/', authenticateToken, requireAdmin, async (req, res) => {
    try {
        const users = await User.find({}, '-passwordHash');
        res.json(users);
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Грешка на сървъра" });
    }
});

// Промяна на роля
router.put('/:userId/role', authenticateToken, requireAdmin, async (req, res) => {
    try {
        const { role } = req.body;
        const { userId } = req.params;
        if (!['user','admin'].includes(role)) {
            return res.status(400).json({ message: "Невалидна роля" });
        }
        const user = await User.findByIdAndUpdate(userId, { role }, { new: true, select: '-passwordHash' });
        res.json(user);
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Грешка на сървъра" });
    }
});

// Изтриване на потребител
router.delete('/:userId', authenticateToken, requireAdmin, async (req, res) => {
    try {
        const { userId } = req.params;
        await User.findByIdAndDelete(userId);
        res.json({ message: "Потребителят е изтрит" });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Грешка на сървъра" });
    }
});

module.exports = router;
